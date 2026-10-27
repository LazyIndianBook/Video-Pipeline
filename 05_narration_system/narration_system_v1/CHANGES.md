# Local changes to the delivered narration starter

The folder was delivered by the ChatGPT research session (13 Oct 2026). Changes made afterwards are listed here; the pristine copy is in `../../00_source/extracted/ExamLeaf_Narration_System/`.

## 2026-10-15 — Fix Indic tokenization in `normalized_words` (`src/examleaf_narration/pronunciation.py`)

**Bug.** `normalized_words` tokenized with `[^\W_]+`. Python's `\w` excludes combining marks (Unicode category M), so Devanagari and Bengali–Assamese vowel signs, virama, nukta and anusvara split one word into fragments: `'विद्युत् धारा।'` → `['व','द','य','त','ध','र']`, `'নियम'`-style words likewise. Every consumer routes through this function: `validate_alignment` (alignment-vs-transcript equality), `cue_time` (one normalized token per aligned word; it raised "Cue alignment requires one normalized token per word" on most Hindi words), `critical_counts`/`transcript_check` (critical-phrase and word-error-rate checks), and `scripts/build_examples.py` (fixture word lists).

**Fix.** Replaced the regex with a category-based scanner: a word is a run of letters, marks and numbers (`unicodedata.category(ch)[0] in "LMN"`); inner apostrophes are kept; ZWJ/ZWNJ (U+200C/U+200D) are transparent (skipped, not split) for comparison; maths symbols `+ − = ^ < > -` remain single tokens; underscore still separates. NFC + casefold unchanged. The function remains a surface comparator, not a linguistic tokenizer; native review is still required for pronunciation and meaning.

**Verification.** `PYTHONPATH=src pytest -q`: 58 passed (55 original + 3 new: `test_indic_words_stay_whole`, `test_cue_time_anchors_hindi_words`, `test_transcript_check_hindi_critical_phrase`); 2 failures are pre-existing and environmental (`test_silent_loudness_rejected`, `test_two_pass_master_real_signal_file` shell out to `ffmpeg`, which is not installed on this machine; they failed identically before the change). All six English example segments in `examples/teacher.json` and `examples/textbook.json` produce identical token streams before and after. `outputs/tests.txt` still records the delivered "57 passed" run and was not regenerated.

**Out of scope.** `cue_time` still requires exactly one normalized token per aligned word; an aligner that emits sub-word pieces for Indic text must be merged upstream. Hindi/Assamese lexicon entries remain absent (see `configs/pronunciation.json`).
