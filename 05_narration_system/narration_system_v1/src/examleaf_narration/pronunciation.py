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

_SYMBOL_TOKENS=frozenset("+−=^<>-")
_JOINERS=frozenset("‌‍")  # ZWNJ/ZWJ: shaping controls inside Indic words; transparent for comparison

def _is_word_char(ch):
    # Letters, numbers AND combining marks. Python's \w excludes category M*, so Devanagari/Bengali vowel
    # signs, virama, nukta and anusvara used to split one word into several fragments ("विद्युत्" -> 4 pieces).
    return unicodedata.category(ch)[0] in "LMN"

def normalized_words(text):
    """Surface comparator: NFC + casefold, words = runs of letters/marks/digits (inner apostrophes kept,
    ZWJ/ZWNJ skipped), maths symbols as single tokens. Script-aware, not a linguistic tokenizer; native
    review is still required for pronunciation and meaning."""
    text=unicodedata.normalize("NFC",text).casefold()
    out=[];buf=[];n=len(text)
    for i,ch in enumerate(text):
        nxt=text[i+1] if i+1<n else ""
        if _is_word_char(ch):
            buf.append(ch)
        elif buf and ch in _JOINERS and _is_word_char(nxt):
            continue
        elif buf and ch in "'’" and _is_word_char(nxt):
            buf.append(ch)
        else:
            if buf: out.append("".join(buf));buf=[]
            if ch in _SYMBOL_TOKENS: out.append(ch)
    if buf: out.append("".join(buf))
    return out

def critical_counts(text,phrases):
    words=normalized_words(text);out={}
    for phrase in phrases:
        p=normalized_words(phrase)
        out[phrase]=sum(words[i:i+len(p)]==p for i in range(len(words)-len(p)+1))
    return out
