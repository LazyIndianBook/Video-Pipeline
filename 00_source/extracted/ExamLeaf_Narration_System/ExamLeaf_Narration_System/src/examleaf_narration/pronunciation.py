"""Explicit symbolic speech choices; never infer ambiguous mathematics silently."""
import hashlib
import json
import re
import unicodedata
TOKEN=re.compile(r"\{\{([a-z][a-z0-9_]*)\}\}")

def digest(value):
    raw=json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()

def expand(template,lexicon,locale,form="spoken"):
    if form not in {"spoken","display","caption"}: raise ValueError("Unknown pronunciation form")
    def replace(match):
        key=match.group(1)
        if key not in lexicon["entries"]: raise ValueError(f"Unresolved STEM token: {key}")
        entry=lexicon["entries"][key];language=entry.get("locales",{}).get(locale)
        if not language or not language.get("editorially_checked",False):
            raise ValueError(f"No editorially checked {locale} mapping for {key}")
        # Acoustic approval is separate from this explicit editorial mapping.
        return entry["display"] if form=="display" else language.get(form,language["spoken"])
    out=TOKEN.sub(replace,template)
    if "{{" in out or "}}" in out: raise ValueError("Malformed/unresolved speech token")
    return unicodedata.normalize("NFC",out)

def normalized_words(text):
    text=unicodedata.normalize("NFC",text).casefold()
    # Only an English/surface comparator. Native Indic tokenization requires separate review.
    return re.findall(r"[^\W_]+(?:['’][^\W_]+)*|[+−=^<>-]",text,flags=re.UNICODE)

def critical_counts(text,phrases):
    words=normalized_words(text);out={}
    for phrase in phrases:
        p=normalized_words(phrase)
        out[phrase]=sum(words[i:i+len(p)]==p for i in range(len(words)-len(p)+1))
    return out
