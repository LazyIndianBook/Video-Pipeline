#!/usr/bin/env python3
"""determinism_hash_check.py - compare two directories of rendered frames by SHA-256 (stdlib only).

The double-render determinism test (contract.md section 11): render the same scene twice in
separate processes, then run this on the two frame directories. Hash raw frames (PNG), not the
encoded MP4: encoders may embed metadata that differs between runs.

Usage:
  determinism_hash_check.py DIR_A DIR_B [--glob '*.png'] [--json] [--write-manifest FILE]
  determinism_hash_check.py --selftest

Frames are matched by file name (natural sort, so frame_2.png < frame_10.png).
Exit codes (contract.md section 12): 0 identical, 1 different or missing/extra frames
(or selftest failed), 2 usage/IO error.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile


def natural_key(name):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def hash_dir(d, pattern):
    import fnmatch
    names = [n for n in os.listdir(d) if fnmatch.fnmatch(n, pattern) and os.path.isfile(os.path.join(d, n))]
    names.sort(key=natural_key)
    return {n: sha256_file(os.path.join(d, n)) for n in names}, names


def compare(dir_a, dir_b, pattern="*.png"):
    ha, order_a = hash_dir(dir_a, pattern)
    hb, order_b = hash_dir(dir_b, pattern)
    union = sorted(set(ha) | set(hb), key=natural_key)
    only_a = [n for n in union if n in ha and n not in hb]
    only_b = [n for n in union if n in hb and n not in ha]
    differing = [n for n in union if n in ha and n in hb and ha[n] != hb[n]]
    first = None
    for i, n in enumerate(union):
        if n in only_a or n in only_b or n in differing:
            first = {"index": i, "name": n,
                     "sha256_a": ha.get(n), "sha256_b": hb.get(n),
                     "reason": "missing in B" if n in only_a else "missing in A" if n in only_b else "content differs"}
            break
    return {
        "identical": not (only_a or only_b or differing) and bool(union),
        "frames_a": len(ha), "frames_b": len(hb), "frames_compared": len(set(ha) & set(hb)),
        "differing_count": len(differing), "only_in_a": only_a, "only_in_b": only_b,
        "first_difference": first, "pattern": pattern,
        "differing_names_head": differing[:10],
    }, ha


def selftest():
    fails = []

    def ok(name, cond):
        print("  %s %s" % ("PASS" if cond else "FAIL", name))
        if not cond:
            fails.append(name)

    print("determinism_hash_check.py --selftest")
    with tempfile.TemporaryDirectory() as root:
        def mk(sub, files):
            d = os.path.join(root, sub)
            os.makedirs(d)
            for n, data in files.items():
                with open(os.path.join(d, n), "wb") as f:
                    f.write(data)
            return d

        base = {"frame_%04d.png" % i: ("frame-%d" % i).encode() * 50 for i in range(12)}
        a = mk("a", base)
        b = mk("b", dict(base))
        r, _ = compare(a, b)
        ok("identical directories: identical=True, 12 compared", r["identical"] and r["frames_compared"] == 12 and r["first_difference"] is None)

        two = dict(base)
        two["frame_0003.png"] = b"changed"
        two["frame_0009.png"] = b"also changed"
        c = mk("c", two)
        r, _ = compare(a, c)
        ok("two differing frames: count=2", not r["identical"] and r["differing_count"] == 2)
        ok("first differing frame is frame_0003.png (index 3)", r["first_difference"]["name"] == "frame_0003.png" and r["first_difference"]["index"] == 3)

        missing = dict(base)
        del missing["frame_0005.png"]
        missing["frame_0100.png"] = b"extra"
        d = mk("d", missing)
        r, _ = compare(a, d)
        ok("missing and extra frames detected", r["only_in_a"] == ["frame_0005.png"] and r["only_in_b"] == ["frame_0100.png"] and not r["identical"])

        # natural sort: frame_2 must come before frame_10
        e1 = mk("e1", {"f_2.png": b"1", "f_10.png": b"1"})
        e2 = mk("e2", {"f_2.png": b"1", "f_10.png": b"2"})
        r, _ = compare(e1, e2)
        ok("natural ordering (f_2 before f_10) and diff found at f_10", r["first_difference"]["name"] == "f_10.png" and r["first_difference"]["index"] == 1)

        empty1, empty2 = mk("z1", {}), mk("z2", {})
        r, _ = compare(empty1, empty2)
        ok("two empty directories are NOT reported identical", not r["identical"])

        # non-frame files are ignored by the glob
        f1 = mk("g1", {"frame_0001.png": b"x", "notes.txt": b"1"})
        f2 = mk("g2", {"frame_0001.png": b"x", "notes.txt": b"2"})
        r, _ = compare(f1, f2)
        ok("files outside --glob are ignored", r["identical"])
    print("selftest: %s (%d failed)" % ("OK" if not fails else "FAILED", len(fails)))
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compare two frame directories by SHA-256.")
    ap.add_argument("dir_a", nargs="?")
    ap.add_argument("dir_b", nargs="?")
    ap.add_argument("--glob", default="*.png", help="frame file pattern (default *.png)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    ap.add_argument("--write-manifest", metavar="FILE", help="write {name: sha256} for DIR_A to FILE")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.dir_a and a.dir_b):
        ap.print_usage(sys.stderr)
        return 2
    for d in (a.dir_a, a.dir_b):
        if not os.path.isdir(d):
            print("error: not a directory: %s" % d, file=sys.stderr)
            return 2
    r, ha = compare(a.dir_a, a.dir_b, a.glob)
    if a.write_manifest:
        with open(a.write_manifest, "w", encoding="utf-8") as f:
            json.dump(ha, f, indent=1, sort_keys=True)
    if a.json:
        print(json.dumps(r, indent=2))
    else:
        print("frames: A=%d B=%d compared=%d  differing=%d  only-in-A=%d  only-in-B=%d" % (
            r["frames_a"], r["frames_b"], r["frames_compared"], r["differing_count"], len(r["only_in_a"]), len(r["only_in_b"])))
        fd = r["first_difference"]
        if fd:
            print("first difference: index %d  %s  (%s)" % (fd["index"], fd["name"], fd["reason"]))
        if r["frames_a"] == 0 and r["frames_b"] == 0:
            print("no frames matched %r in either directory" % a.glob)
        print("RESULT: %s" % ("IDENTICAL" if r["identical"] else "DIFFERENT"))
    return 0 if r["identical"] else 1


if __name__ == "__main__":
    sys.exit(main())
