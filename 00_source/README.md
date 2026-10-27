# 00_source — raw provenance (do not edit)

Everything in this folder was pulled verbatim from the shared ChatGPT conversation
**"AI Video System Research"** (model `gpt-6-pro`, conversation id `6acf03ec-b480-83ee-a000-3701059934d9`)
on 14 October 2026. Nothing here is edited; the numbered sections `01_…` to `10_…` are built from it.

Share link: https://chatgpt.com/share/6acf03ec-b480-83ee-a000-3701059934d9

## Important: the share page hides half the conversation

The rendered share page shows only three prompt/response pairs. The underlying conversation has **six**.
The page data (React Router context) contained all 610 nodes; the linear path was exported in full.

| # | User prompt (file in `chatgpt_transcript/messages/`) | Assistant response | Deliverable pack |
|---|---|---|---|
| 1 | `01_USER_prompt_video_engine_research_v1.md` | `02_ASSISTANT_video_engine_architecture_and_plan_v1.md` (48K chars) | `ExamLeaf_Video_Engine_Planning_Pack.zip`, `ExamLeaf_Cost_and_Skills.xlsx` |
| 2 | `03_USER_prompt_learning_psychology.md` | `04_ASSISTANT_learning_psychology_blueprint.md` (58K) | none |
| 3 | `05_USER_prompt_business_model.md` | `06_ASSISTANT_business_model_launch_financial_plan.md` (51K) | `ExamLeaf_Business_Launch_Toolkit.zip`, `ExamLeaf_Business_Model.xlsx` |
| 4 | `07_USER_prompt_super_teacher.md` | `08_ASSISTANT_super_teacher_framework.md` (48K) | `ExamLeaf_Super_Teacher_Starter_Pack.zip` + 2 md |
| 5 | `09_USER_prompt_video_engine_skills_and_implementation_v2.md` | `10_ASSISTANT_video_engine_implementation_v2.md` (44K) | `ExamLeaf_Video_Engine_Implementation.zip`, `ExamLeaf_Video_Engine_Cost_Model.xlsx`, 3 md/csv, 4 mp4, 2 jpg |
| 6 | `11_USER_prompt_narration_system.md` | `12_ASSISTANT_narration_system.md` (45K) | `ExamLeaf_Narration_System.zip`, `ExamLeaf_Narration_Cost_Model.xlsx`, 3 md |

Short "progress note" assistant messages (`*a_`, `*b_`, `*c_`) are kept too.

## Folder map

| Path | What it is |
|---|---|
| `chatgpt_transcript/full_linear_transcript.md` | All user + assistant text messages on the linear path, in order, verbatim (341K chars) |
| `chatgpt_transcript/messages/*.md` | The same transcript split one-file-per-message; ChatGPT's internal `citeturn…` tokens stripped |
| `chatgpt_transcript/raw_conversation_linear.json` | The 610-node linear path exported from the page data (includes tool/code/reasoning nodes, trimmed) |
| `chatgpt_transcript/cited_source_links.md` | Every external URL the responses cited, grouped |
| `downloads/` | The 23 files exactly as served by ChatGPT's `file_from_message` endpoint, in their original `/mnt/data/` layout |
| `downloads/_download_manifest.json` | The path → signed-URL list used for the download (URLs expired within ~30 min) |
| `extracted/<pack>/` | The five zips unpacked, one folder per zip (462 files) |
| `extracted_file_inventory.txt` | Size + path of every extracted file |
| `spreadsheets_as_csv/` | Every sheet of the four `.xlsx` workbooks as `<workbook>__<sheet>__values.csv` and `__formulas.csv` (35 sheets, 68 files) |

## Downloaded files (23/23, 6.1 MB)

```
ExamLeaf_Video_Engine/ExamLeaf_Cost_and_Skills.xlsx                     22,240
ExamLeaf_Video_Engine_Planning_Pack.zip                                 28,607
ExamLeaf_Business_Plan/ExamLeaf_Business_Model.xlsx                    104,052
ExamLeaf_Business_Launch_Toolkit.zip                                   114,407
ExamLeaf_Super_Teacher_Starter_Pack.zip                                 73,396
ExamLeaf_Super_Teacher/Super_Teacher_Guide.md                           14,714
ExamLeaf_Super_Teacher/examples/Complete_Sample_Script.md               14,406
ExamLeaf_Video_Engine_Implementation.zip                             3,976,407
ExamLeaf_Video_Engine_Cost_Model.xlsx                                   31,774
ExamLeaf_Engine_Implementation/README.md                                 5,907
ExamLeaf_Engine_Implementation/research/Public_Skills_Directory.md      15,701
ExamLeaf_Engine_Implementation/research/custom_skills.csv               18,147
ExamLeaf_Engine_Implementation/outputs/physics_rc_16x9.mp4             347,653
ExamLeaf_Engine_Implementation/outputs/chemistry_balance_16x9.mp4      212,515
ExamLeaf_Engine_Implementation/outputs/mathematics_chain_16x9.mp4      225,773
ExamLeaf_Engine_Implementation/outputs/biology_genetics_16x9.mp4       203,333
ExamLeaf_Engine_Implementation/outputs/technical_previews_contact_sheet.jpg 105,919
ExamLeaf_Engine_Implementation/outputs/vertical_review.jpg              63,830
ExamLeaf_Narration_System.zip                                          532,127
ExamLeaf_Narration_Cost_Model.xlsx                                      29,574
ExamLeaf_Narration_System/docs/Voice_Identity_Guide.md                   5,435
ExamLeaf_Narration_System/research/Public_Narration_Directory.md        12,437
ExamLeaf_Narration_System/examples/Before_After.md                       2,391
```

## Known gap

The user's own uploaded attachment on prompt 3, `Pasted text(1).txt` (14,505 bytes, their original
business-model brief), is a user upload and is **not** served by the share endpoint (404/403 on every
candidate route). Only the fragment ChatGPT quoted survives, in the business-model response.

## How the files were retrieved

1. Page text and the `__reactRouterContext` object were read from the share page in the built-in browser.
2. Each `sandbox:/mnt/data/...` link was resolved with
   `GET https://chatgpt.com/backend-anon/share/<conversation_id>/file_from_message/<message_id>?file_path=<urlencoded path>`
   which returns `{"download_url": "<signed Azure blob URL>"}`.
3. The signed URLs were fetched with `curl` into `downloads/`.
