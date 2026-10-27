# CMP results for the six separately downloaded files

Added by the organiser (not part of the ChatGPT download). The six files in this folder are copies of
`00_source/downloads/ExamLeaf_Engine_Implementation/outputs/` (four 16:9 MP4s, `technical_previews_contact_sheet.jpg`, `vertical_review.jpg`).

Each was compared with `cmp -s` against (i) the same path inside `00_source/downloads/ExamLeaf_Video_Engine_Implementation.zip` (read with `unzip -p`), (ii) the extracted copy under `00_source/extracted/`, and (iii) `../<same filename>`.

| File | Bytes | MD5 | vs zip | vs extracted | vs `../` |
|---|---:|---|---|---|---|
| physics_rc_16x9.mp4 | 347653 | 7b2fd6f7a11dceec8a454273d537608b | IDENTICAL | IDENTICAL | IDENTICAL |
| chemistry_balance_16x9.mp4 | 212515 | 1924fa1ea73e9bdc10df7190164e3130 | IDENTICAL | IDENTICAL | IDENTICAL |
| mathematics_chain_16x9.mp4 | 225773 | 34989e90f8d6ba0f6e952a66da1a5ab8 | IDENTICAL | IDENTICAL | IDENTICAL |
| biology_genetics_16x9.mp4 | 203333 | 8fef84fa05b649b4fd64d6db1ba0b632 | IDENTICAL | IDENTICAL | IDENTICAL |
| technical_previews_contact_sheet.jpg | 105919 | 85506b4559c0d7e44f7aac7870e2c755 | IDENTICAL | IDENTICAL | IDENTICAL |
| vertical_review.jpg | 63830 | fd4a0eca1b3fadeb5e5607803c7ca6c9 | IDENTICAL | IDENTICAL | IDENTICAL |

Conclusion: the download contains nothing the zip does not. Full measured properties are in `../../PREVIEW_BENCHMARKS.md` (section 4).
