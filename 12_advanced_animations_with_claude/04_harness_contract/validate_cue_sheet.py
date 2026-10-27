#!/usr/bin/env python3
"""validate_cue_sheet.py - validate an ExamLeaf cue sheet (stdlib only, no jsonschema).

Two layers:
  1. Structure: a small JSON Schema draft-07 subset interpreter driven by
     cue_sheet.schema.json (the schema file is the single source of truth).
  2. Semantics (what draft-07 cannot say): monotonic times, non-overlapping words,
     cues/sfx/beats inside the duration, reveal-lead rule, path safety, hashes.

Usage:
  validate_cue_sheet.py SHEET.json [--schema PATH] [--production] [--tol 1e-6] [--json]
  validate_cue_sheet.py --selftest

Exit codes (contract.md section 12): 0 valid, 1 invalid (or selftest failed), 2 usage/IO error.
Report: contract.md, README.md. Rules: research report section 5.5 and [V4-MP] sync rule.
"""
import argparse
import copy
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SCHEMA = os.path.join(HERE, "cue_sheet.schema.json")
EXAMPLE = os.path.join(HERE, "cue_sheet.example.json")

# Keywords the mini interpreter implements, and annotation keywords it may ignore.
IMPLEMENTED = {"type", "const", "enum", "pattern", "minimum", "maximum", "exclusiveMinimum",
               "exclusiveMaximum", "minLength", "maxLength", "items", "minItems", "maxItems",
               "uniqueItems", "required", "properties", "additionalProperties", "$ref"}
ANNOTATION = {"$schema", "$id", "title", "description", "definitions", "default", "examples"}

REVEAL_LEAD_S = 0.05      # [V4-MP]: reveal on, or about 0.05 s before, the word
REVEAL_EARLY_WARN_S = 0.10
PRODUCTION_BAD_SOURCES = {"synthetic_even_spacing", "example"}


# --------------------------------------------------------------------------- structure
def _is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _type_ok(inst, t):
    if t == "object":
        return isinstance(inst, dict)
    if t == "array":
        return isinstance(inst, list)
    if t == "string":
        return isinstance(inst, str)
    if t == "number":
        return _is_num(inst)
    if t == "integer":
        return _is_num(inst) and float(inst).is_integer()
    if t == "boolean":
        return isinstance(inst, bool)
    if t == "null":
        return inst is None
    return False


def unsupported_keywords(schema, found=None):
    """Return the set of schema keywords the interpreter does not understand."""
    found = set() if found is None else found
    if isinstance(schema, dict):
        for k, v in schema.items():
            if k in ("properties", "definitions"):
                for sub in v.values():
                    unsupported_keywords(sub, found)
            elif k == "items":
                unsupported_keywords(v, found)
            elif k == "additionalProperties":
                if isinstance(v, dict):
                    unsupported_keywords(v, found)
            elif k not in IMPLEMENTED and k not in ANNOTATION:
                found.add(k)
    return found


def check_schema(inst, schema, root, path, errs):
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            errs.append("%s: unsupported $ref %r" % (path, ref))
            return
        node = root
        for part in ref[2:].split("/"):
            node = node[part]
        check_schema(inst, node, root, path, errs)
        return
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(inst, t) for t in types):
            errs.append("%s: type error: expected %s, got %s" % (path, "/".join(types), type(inst).__name__))
            return
    if "const" in schema and inst != schema["const"]:
        errs.append("%s: must equal %r" % (path, schema["const"]))
    if "enum" in schema and inst not in schema["enum"]:
        errs.append("%s: %r not in enum %s" % (path, inst, schema["enum"]))
    if isinstance(inst, str):
        if "minLength" in schema and len(inst) < schema["minLength"]:
            errs.append("%s: string shorter than %d" % (path, schema["minLength"]))
        if "maxLength" in schema and len(inst) > schema["maxLength"]:
            errs.append("%s: string longer than %d" % (path, schema["maxLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], inst):
            errs.append("%s: does not match pattern %s" % (path, schema["pattern"]))
    if _is_num(inst):
        if "minimum" in schema and inst < schema["minimum"]:
            errs.append("%s: %r below minimum %r" % (path, inst, schema["minimum"]))
        if "maximum" in schema and inst > schema["maximum"]:
            errs.append("%s: %r above maximum %r" % (path, inst, schema["maximum"]))
        if "exclusiveMinimum" in schema and inst <= schema["exclusiveMinimum"]:
            errs.append("%s: %r not above %r" % (path, inst, schema["exclusiveMinimum"]))
        if "exclusiveMaximum" in schema and inst >= schema["exclusiveMaximum"]:
            errs.append("%s: %r not below %r" % (path, inst, schema["exclusiveMaximum"]))
    if isinstance(inst, list):
        if "minItems" in schema and len(inst) < schema["minItems"]:
            errs.append("%s: fewer than %d items" % (path, schema["minItems"]))
        if "maxItems" in schema and len(inst) > schema["maxItems"]:
            errs.append("%s: more than %d items" % (path, schema["maxItems"]))
        if schema.get("uniqueItems") and len({json.dumps(i, sort_keys=True) for i in inst}) != len(inst):
            errs.append("%s: items not unique" % path)
        if "items" in schema:
            for i, item in enumerate(inst):
                check_schema(item, schema["items"], root, "%s[%d]" % (path, i), errs)
    if isinstance(inst, dict):
        for r in schema.get("required", []):
            if r not in inst:
                errs.append("%s: required property %r missing" % (path, r))
        props = schema.get("properties", {})
        for k, v in inst.items():
            if k in props:
                check_schema(v, props[k], root, "%s.%s" % (path, k), errs)
            elif schema.get("additionalProperties") is False:
                errs.append("%s: additional property %r not allowed" % (path, k))
            elif isinstance(schema.get("additionalProperties"), dict):
                check_schema(v, schema["additionalProperties"], root, "%s.%s" % (path, k), errs)


# --------------------------------------------------------------------------- semantics
def semantic_checks(s, errs, warns, production, tol):
    dur = s["duration"]
    fps = s["fps"]
    words = s.get("words", [])
    cues = s.get("cues", [])
    beats = s.get("beats", [])
    sfx = s.get("sfx", [])

    frames = dur * fps
    if abs(frames - round(frames)) > 1e-6:
        warns.append("$.duration*fps = %r is not an integer; renderer will use round() = %d frames" % (frames, round(frames)))

    # words: t1>t0, inside duration, monotonic, non-overlapping
    for i, w in enumerate(words):
        p = "$.words[%d]" % i
        if w["t1"] <= w["t0"]:
            errs.append("%s: t1 (%r) must be greater than t0 (%r)" % (p, w["t1"], w["t0"]))
        if w["t1"] > dur + tol:
            errs.append("%s: t1 (%r) beyond duration (%r)" % (p, w["t1"], dur))
        if i:
            prev = words[i - 1]
            if w["t0"] < prev["t0"] - tol:
                errs.append("%s: non-monotonic t0 (%r after %r)" % (p, w["t0"], prev["t0"]))
            elif w["t0"] < prev["t1"] - tol:
                errs.append("%s: overlaps previous word (t0 %r < previous t1 %r)" % (p, w["t0"], prev["t1"]))
        if not unicodedata.is_normalized("NFC", w["w"]):
            warns.append("%s: word %r is not NFC-normalised (fixture text diff may fail)" % (p, w["w"]))
        if re.search(r"\s", w["w"]):
            warns.append("%s: word %r contains whitespace; use one token per word" % (p, w["w"]))
    if not words:
        warns.append("$.words is empty (music-only scene?)")

    # repeated surface forms and occurrence numbering
    groups = {}
    for i, w in enumerate(words):
        groups.setdefault(w["w"], []).append(i)
    for form, idxs in groups.items():
        if len(idxs) < 2:
            continue
        occs = [words[i].get("occurrence") for i in idxs]
        if all(o is None for o in occs):
            continue  # occurrence is optional; cues can use word_index instead
        if occs != list(range(1, len(idxs) + 1)):
            errs.append("$.words: occurrence numbers for %r must be 1..%d in order, got %s" % (form, len(idxs), occs))

    # beats strictly increasing and inside duration
    for i, b in enumerate(beats):
        if b > dur + tol:
            errs.append("$.beats[%d]: %r beyond duration (%r)" % (i, b, dur))
        if i and b <= beats[i - 1]:
            errs.append("$.beats[%d]: beats must be strictly increasing (%r after %r)" % (i, b, beats[i - 1]))

    # cues: inside duration, sorted, unique (id, occurrence), until/word_index rules
    seen = set()
    for i, c in enumerate(cues):
        p = "$.cues[%d]" % i
        if c["at"] > dur + tol:
            errs.append("%s: at (%r) beyond duration (%r)" % (p, c["at"], dur))
        if i and c["at"] < cues[i - 1]["at"] - tol:
            errs.append("%s: cues must be sorted by at (%r after %r)" % (p, c["at"], cues[i - 1]["at"]))
        key = (c["id"], c.get("occurrence", 1))
        if key in seen:
            errs.append("%s: duplicate cue id %r (occurrence %r); use occurrence for repeats" % (p, c["id"], key[1]))
        seen.add(key)
        if "until" in c:
            if c["kind"] != "hold":
                errs.append("%s: 'until' is only valid for kind 'hold'" % p)
            elif c["until"] < c["at"]:
                errs.append("%s: until (%r) before at (%r)" % (p, c["until"], c["at"]))
            elif c["until"] > dur + tol:
                errs.append("%s: until (%r) beyond duration (%r)" % (p, c["until"], dur))
        if c["kind"] == "hold" and "until" not in c:
            warns.append("%s: hold cue without 'until'" % p)
        if c["kind"] in ("reveal", "emphasis") and "element_id" not in c:
            warns.append("%s: %s cue without element_id" % (p, c["kind"]))
        if "word_index" in c:
            wi = c["word_index"]
            if wi >= len(words):
                errs.append("%s: word_index %d out of range (%d words)" % (p, wi, len(words)))
            elif c["kind"] in ("reveal", "emphasis"):
                lead = words[wi]["t0"] - c["at"]
                if lead < -tol:
                    errs.append("%s: late %s: at %r is after word t0 %r (rule: on or %.2f s before)" % (p, c["kind"], c["at"], words[wi]["t0"], REVEAL_LEAD_S))
                elif lead > REVEAL_EARLY_WARN_S + tol:
                    warns.append("%s: %s is %.3f s before its word (rule: about %.2f s)" % (p, c["kind"], lead, REVEAL_LEAD_S))

    # sfx
    for i, x in enumerate(sfx):
        p = "$.sfx[%d]" % i
        if x["at"] > dur + tol:
            errs.append("%s: at (%r) beyond duration (%r)" % (p, x["at"], dur))
        if i and x["at"] < sfx[i - 1]["at"] - tol:
            warns.append("%s: sfx not sorted by at" % p)
        parts = x["file"].replace("\\", "/").split("/")
        if ".." in parts or x["file"].startswith("/"):
            errs.append("%s: path traversal or absolute path in file %r" % (p, x["file"]))

    # provenance
    for k in ("narration_audio_sha256", "script_sha256"):
        if s.get(k) is None:
            (errs if production else warns).append("$.%s is null%s" % (k, " (production requires a hash)" if production else ""))
    if production and s.get("alignment_source") in PRODUCTION_BAD_SOURCES | {None}:
        errs.append("$.alignment_source %r is not valid for production" % s.get("alignment_source"))


def validate(sheet, schema, production=False, tol=1e-6):
    errs, warns = [], []
    check_schema(sheet, schema, schema, "$", errs)
    if not errs:  # semantic checks assume a structurally valid sheet
        semantic_checks(sheet, errs, warns, production, tol)
    return errs, warns


# --------------------------------------------------------------------------- selftest
def selftest():
    fails = []

    def ok(name, cond, detail=""):
        print("  %s %s%s" % ("PASS" if cond else "FAIL", name, (" - " + detail) if detail and not cond else ""))
        if not cond:
            fails.append(name)

    print("validate_cue_sheet.py --selftest")
    try:
        schema = json.load(open(DEFAULT_SCHEMA, encoding="utf-8"))
        example = json.load(open(EXAMPLE, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("  FAIL cannot load schema/example next to the script: %s" % e)
        return 1
    ok("schema uses only implemented keywords", not unsupported_keywords(schema), str(unsupported_keywords(schema)))
    e, w = validate(example, schema)
    ok("example sheet is valid", not e, "; ".join(e))
    ok("example sheet has no warnings", not w, "; ".join(w))
    e, w = validate(example, schema, production=True)
    ok("example sheet rejected by --production (example alignment source)", any("production" in x for x in e))

    def mut(name, fn, needle, production=False):
        s = copy.deepcopy(example)
        fn(s)
        e, _ = validate(s, schema, production=production)
        ok("rejects: " + name, any(needle in x for x in e), "errors=%s" % e)

    mut("unknown property", lambda s: s.update(bogus=1), "additional property")
    mut("missing duration", lambda s: s.pop("duration"), "required property 'duration'")
    mut("fps as string", lambda s: s.update(fps="30"), "type error")
    mut("short hash", lambda s: s.update(script_sha256="abc"), "pattern")
    mut("word overlap", lambda s: s["words"][2].update(t0=1.0), "overlaps")
    mut("word non-monotonic", lambda s: s["words"].__setitem__(slice(3, 5), [s["words"][4], s["words"][3]]), "non-monotonic")
    mut("word t1<=t0", lambda s: s["words"][0].update(t1=0.3), "must be greater than t0")
    mut("word beyond duration", lambda s: s["words"][-1].update(t1=9.0), "beyond duration")
    mut("cue beyond duration", lambda s: s["cues"][1].update(at=9.0), "beyond duration")
    mut("cues unsorted", lambda s: s["cues"].__setitem__(slice(0, 2), [s["cues"][1], s["cues"][0]]), "sorted")
    mut("duplicate cue id", lambda s: s["cues"][1].update(id="headline_in"), "duplicate cue id")
    mut("late reveal", lambda s: s["cues"][0].update(at=0.7), "late reveal")
    mut("word_index out of range", lambda s: s["cues"][0].update(word_index=99), "out of range")
    mut("until on non-hold", lambda s: s["cues"][0].update(until=2.0), "only valid for kind 'hold'")
    mut("beats not increasing", lambda s: s["beats"].__setitem__(2, 0.1), "strictly increasing")
    mut("sfx traversal", lambda s: s["sfx"][0].update(file="sfx/../x.wav"), "traversal")
    mut("sfx positive gain", lambda s: s["sfx"][0].update(gain_db=3), "above maximum")
    mut("bad occurrence numbering", lambda s: s["words"][14].update(occurrence=1), "occurrence numbers")
    mut("null audio hash in production", lambda s: s.update(narration_audio_sha256=None, alignment_source="forced_alignment"), "production requires a hash", production=True)
    # late-reveal rule boundary: exactly on the word is allowed
    s = copy.deepcopy(example)
    s["cues"][0]["at"] = s["words"][1]["t0"]
    e, _ = validate(s, schema)
    ok("accepts reveal exactly on word t0", not e, str(e))
    s = copy.deepcopy(example)
    s["narration_audio_sha256"] = None
    e, w = validate(s, schema)
    ok("null audio hash is a warning outside production", not e and any("null" in x for x in w))
    print("selftest: %s (%d failed)" % ("OK" if not fails else "FAILED", len(fails)))
    return 1 if fails else 0


# --------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate an ExamLeaf cue sheet (stdlib only).")
    ap.add_argument("sheet", nargs="?", help="cue sheet JSON file")
    ap.add_argument("--schema", default=DEFAULT_SCHEMA, help="schema path (default: next to this script)")
    ap.add_argument("--production", action="store_true", help="require non-null hashes and a real alignment source")
    ap.add_argument("--tol", type=float, default=1e-6, help="time tolerance in seconds (default 1e-6)")
    ap.add_argument("--json", action="store_true", help="print a JSON report")
    ap.add_argument("--selftest", action="store_true", help="run built-in tests and exit")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.sheet:
        ap.print_usage(sys.stderr)
        return 2
    try:
        schema = json.load(open(a.schema, encoding="utf-8"))
        sheet = json.load(open(a.sheet, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    bad_kw = unsupported_keywords(schema)
    if bad_kw:
        print("error: schema uses keywords this validator does not implement: %s" % sorted(bad_kw), file=sys.stderr)
        return 2
    errs, warns = validate(sheet, schema, a.production, a.tol)
    if a.json:
        print(json.dumps({"file": a.sheet, "valid": not errs, "errors": errs, "warnings": warns}, ensure_ascii=False, indent=2))
    else:
        for x in errs:
            print("ERROR   " + x)
        for x in warns:
            print("WARNING " + x)
        print("%s: %s (%d errors, %d warnings)" % (a.sheet, "VALID" if not errs else "INVALID", len(errs), len(warns)))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
