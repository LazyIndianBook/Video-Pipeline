# Subject Validation Profiles v1

Validation scales by subject family, never by commercial value (CE-L8). Each family is a registry entry validated by `schemas/subject_profile.schema.json`. Every subject is listed in exactly one family; the Resolver derives the family from the subject (R3), so a request cannot pair `history` with STEM validators. A family cannot be activated without at least one named reviewer in the reviewer registry (schema: `activation.activated: true` requires `named_reviewer_ids` with at least one entry). Contested claims always need at least two reviewers (schema minimum). Each family also lists the levels at which its subjects may be requested (`levels_allowed`, required; R3 refuses any other level) and the levels at which a contested claim must be taught through Perspectives (`perspectives_required_at_levels`), both in the §11 matrix (added 15 Oct 2026). A profile whose `validation_mode` is claim_ledger or hybrid must list `claim_flagger` and `span_hash`; a fixture-mode profile must list `fixture_exec` (schema).

## 1. Rules common to all families

### 1.1 Claim ledger rules

Applied to every non-fixture claim, including STEM definitions and conventions [Recommendation, CE-28]:

1. **Burden of proof on the author** [N13]. The drafting agent must attach a source and span or the claim does not enter the ledger.
2. **Unsourced is removed by default** [N14]. Schema: `source_refs` minItems 1. Closure: any flagged assertive sentence without a node fails.
3. **Truth is not enough** [N15]. A reliable published source is required; model knowledge is never a source.
4. **Cost of access is not a reason to reject** [N16]. Schema constant `reject_for_cost_of_access: false`; the copy hash lets reviewers re-check spans.
5. **Exceptional and sensitive claims need ≥2 sources** [N17]. Schema-enforced.
6. **No self-published source about living people** [N18]. Schema-enforced on SRC.
7. **No open wikis as sources** [N19]. Schema constant `open_wiki: false`; usable for discovery only.
8. **Corroboration against reliable secondary sources** [N39].

### 1.2 Pipeline of checks

Flagger → span-hash → family validators → qualified reviewer. The citation-need flagger [N41]–[N43] runs on the cheap cascade and **only adds flags**. Citations go missing even under policy [N40], robustness varies with quality class [N44], and human-only checking is uneven [N45] (contested), so no single check suffices. The span-hash check confirms the quoted span exists in the registered copy. Strong models act only as offline judges. Flagger recall and precision against reviewer findings is a KPI per family.

### 1.3 Contested-claim states (CE-29)

- **settled:** normal rules.
- **attributed:** an interpretation stated with its holder ("According to …"); attribution required.
- **contested:** scholarship differs. Each position is attributed and sourced; no verdict. Two qualified reviewers. A Short may show it only with attribution and may not state one side as fact. Where the family requires it, the topic is taught through the Perspectives format: at the levels in the family's `perspectives_required_at_levels`; at other levels a contested claim renders in attributed form only (15 Oct 2026).
- **board_vs_scholarship:** the prescribed textbook differs from current scholarship. The video states "the syllabus states …" (exam-relevant) and the academic lead records whether the attributed scholarly position is included (`board_position_decision`).

Any reviewer can escalate a claim to contested. Escalation freezes dependent artefacts at their current gate.

### 1.4 Time-bound claims (CE-30)

`time_bound: true` requires `as_of_date` and `review_by`. Claim types exam_pattern, legal_rule, rate_or_threshold, current_affairs and clinical are always time-bound (schema). When `review_by` passes, the claim becomes stale and its artefacts are queued. If it is not re-reviewed within the family's grace period [Hypothesis per family], it is revoked and release is blocked (Q-EXPIRY).

### 1.5 Reviewer rubric (all families)

Accuracy (claim-level), attribution, level-appropriateness, misconception coverage [N73], bias and sensitivity, safety, exam alignment, rights. Britannica's editorial roles [N63] (contested as evidence) map onto in-house roles: flagger + reviewer = fact checker; family-qualified reviewer = subject editor; academic lead = supervisory editor; native-language editor = copy editor; founder-engineer = information architect. In a small team one person may hold several roles, ~~but never twice on one artefact (approval service)~~ but never two roles in the same gate on one artefact, and never a gate covering their own work (approval service; corrected 15 Oct 2026, Architecture P3).

### 1.6 Gates per family

Every family passes GV-claims → GA-Graph → GA-Δ → H-SB → A-suite → GF/GS → DISCLOSURE → RELEASE-CHECK. Families add validators and reviewer roles; none removes a gate.

### 1.7 Representation, rights and localisation (15 Oct 2026)

- **Representation (level-3+, CE-121).** In every family, not only humanities and EVS: no community, caste or religion is used as a marker of ability, wealth or wrongdoing. This applies to STEM word-problem contexts, story characters, assessment stems and images as much as to civics content; the sensitivity screen and the rubric's "bias and sensitivity" line check it per artefact. Skew across many individually acceptable artefacts is caught at corpus level by **Q-REPR** (QA_PROFILES_REGISTRY): a quarterly, report-only query over released artefacts per level × family × locale, using the optional `depicted_attributes` tags {given_name_origin_region, gender_presented, setting, disability_presented, language} on WRK contexts, STY characters, ASM stems and MED people (generated or drawn only; never real children). Reference ranges are registry policy set by the academic lead and the sensitivity reviewer. Q-REPR feeds the next quarter's authoring brief and never blocks an artefact.
- **Rights (level-1, CE-112).** The "rights" line of the rubric (§1.5) and the `quote_rights` validator rest on a written rights position per publisher class (NCERT, state boards, CBSE, NTA and other exam bodies, universities), open item **O-23** (owner Counsel), recorded as versioned `rights/<publisher>@x.y.z` policies. An SRC whose `rights_status` is not `consulted_only` carries `rights_basis` {policy_ref, decided_by, decided_on}; Q-RIGHTS fails when it is missing or the policy has expired. The `quotation_within_policy` limits are defined in those policies. Until O-23 closes, a past-paper item uses an adapted stem and shows no official-key marks.
- **Localisation (level-3+, CE-118).** A locale rendering (REN) changes wording only (ARCHITECTURE §8, "a REN changes wording only"). It may not change ANL `mapping` or `non_mapping`, STY beats, WRK numbers or context entities, or ASM keys. A culturally adapted analogy, story or word-problem context is a new ANL, STY or WRK node with `adapted_from` and `locale_scope[]`, validated by its family and reviewed at GA-Graph like any node. `Q-LOC.meaning` (back-translation diff, flagged sentences to a bilingual subject reviewer at GA-Δ) is report-only until the level-4 pilot.

---

## 2. family/stem_fixture

- **Subjects:** mathematics, physics, chemistry, biology, earth_science, computer_science, engineering (UG/PG engineering design included).
- **Validation mode:** hybrid. Numeric claims, worked steps and quantitative relationships are **fixture-validated**: computed by executable fixtures, never generated. The four validated scientific models in 04 are the first fixtures. Definitions, conventions and historical notes use the claim ledger.
- **Validators:** fixture_exec, unit_dimension, sigfig, answer_key_solver, claim_flagger, span_hash, source_policy, executable_sandbox (CS).
- **Executable fixtures (CS):** code shown on screen runs in the render container's sandbox: no network, read-only file system, CPU, memory and time caps (schema constant `no_network_readonly_fs_cpu_mem_time_capped`), with pinned runtimes (`runtime_pins`). The output on screen must equal the captured output. Untrusted code from sources is never executed outside the sandbox.
- **Claim-ledger specifics:** board textbook as primary authority for definitions and conventions at school levels; peer-reviewed or scholarly sources beyond the syllabus.
- **Reviewer qualification:** subject teacher for school levels (existing GA); PG-qualified for UG; specialist for PG.
- **Contested handling:** rare; history-of-science claims follow humanities rules.
- **Risk:** standard. Every on-screen number traces to a fixture output (Q-FIX).
- **Fixture growth:** a new fixture is code + tests + a golden output; one owner per fixture.

## 3. family/quant_social (quantitative social science)

- **Subjects:** economics, accountancy, commerce, business_studies, statistics, management.
- **Validation mode:** hybrid. Numeric recomputation as fixtures (ledger balancing, ratios, index numbers, elasticity calculations) plus a claim ledger for rules and concepts.
- **Validators:** ledger_recompute, fixture_exec, claim_flagger, span_hash, source_policy, statute_edition, expiry_check.
- **Claim-ledger specifics:** accounting standards, tax rules and official statistics cite the registered edition with a date; rate_or_threshold claims are time-bound; official statistics (`official_statistics` reliability class) are the primary authority for data.
- **Reviewer qualification:** qualified commerce or economics teacher; CA/CS or economist for UG/PG and adult_prof.
- **Contested handling:** policy debates use attributed or contested states; normative statements are marked as positions, not facts.
- **Risk:** standard; time-bound claims drive re-QA.
- **Gate note:** an expired rate in a worked accountancy problem blocks release.

## 4. family/humanities_citation

- **Subjects:** history, geography, civics, political_science, sociology, philosophy, iks (Indian Knowledge Systems), value_education.
- **Validation mode:** claim ledger.
- **Validators:** claim_flagger, span_hash, source_policy, date_name_consistency (dates, names and places consistent across all nodes in a scope), map_boundary, sensitivity_screen, rubric_entailment (every ASM rubric criterion cites approved CLMs within the item's objectives; added 15 Oct 2026).
- **Claim-ledger specifics:** every date, name, quantity, quotation and causal claim cites a source. Interpretations are attributed. Board textbook is the primary authority at school levels, with scholarly books and peer-reviewed sources for depth. Geography maps require a boundary review against the registered official policy source (O-8; schema on MED). IKS and value education: historical claims are sourced as history; normative statements are marked `normative_position` ("the curriculum states", not empirical fact) [N35].
- **Reviewer qualification:** discipline-qualified (historian, geographer, political scientist). **Sensitivity reviewer** required for claims tagged sensitive (religion, caste, community, region, contested boundaries, political figures). A reviewer qualified in the specific tradition for IKS.
- **Contested handling:** Perspectives format required for contested topics at l9_10 and above; two reviewers; the board_vs_scholarship decision is recorded.
- **Risk:** standard, with a sensitive risk class per claim (≥2 sources).

## 5. family/languages_literature

- **Subjects:** english, hindi, assamese, sanskrit, urdu, bengali and other languages (one subject ID per language); literature per language.
- **Validation mode:** hybrid. Text record (TXT with edition hash) + claim ledger + linguistic checks.
- **Validators:** grammar_orthography (per locale), quote_rights (quote length within policy; licensed or public-domain edition), lexicon, claim_flagger, span_hash, rubric_entailment (every ASM rubric criterion cites linguistic_rule CLMs or a TXT with edition; added 15 Oct 2026).
- **Claim-ledger specifics:** every quotation cites a registered edition (`edition_source_id`); critical interpretations are attributed; linguistic_rule claims cite a grammar reference or the board textbook.
- **Reviewer qualification:** native-language subject editor (also required for any locale rendering; a rendering changes wording only, and an adapted context is a new node, §1.7, 15 Oct 2026). Pronunciation lexicon review for read-along.
- **Contested handling:** literary interpretations default to attributed; contested readings use Perspectives at l9_10 and above.
- **Language as subject vs medium:** this family validates language and literature *content*. A Hindi-medium physics lesson is stem_fixture plus locale/hi-in.
- **Target locales (15 Oct 2026):** each language subject names its target locale in `subject_locales`: english → locale/en-in, hindi → locale/hi-in, assamese → locale/as-in. A language with no registered locale has none, and R4 refuses it (Architecture §3.4 R9a).
- **Risk:** standard; rights are the main exposure (TXT licence, music in songs). Rights basis per publisher class: O-23 and `rights/` policies (§1.7, 15 Oct 2026).

## 6. family/arts_skills

- **Subjects:** visual_art, music, dance, theatre, physical_education, wellbeing.
- **Validation mode:** claim ledger + demonstration record.
- **Validators:** claim_flagger, span_hash, safety_claim (PE and physical activities), quote_rights (music), procedure_completeness (technique steps).
- **Claim-ledger specifics:** technique and history claims sourced; performance demonstrations credited (MED with performer release). Well-being claims that touch health are routed to health_medicine rules for those claims (sensitive, ≥2 sources).
- **Reviewer qualification:** practitioner-teacher (qualified PE, art or music teacher); safety reviewer for physical activities, mandatory for AC0.
- **Contested handling:** stylistic or aesthetic judgements are attributed.
- **Risk:** standard; physical safety for AC0 (household-safe, grown-up cue).
- **Voice:** demonstration formats are Path A when `demo_kind = real` (R1).

## 7. family/vocational

- **Subjects:** trade subjects per NSQF qualification pack (one subject ID per trade, e.g. electrician, plumbing, it_ites, agriculture, beauty_wellness, retail).
- **Validation mode:** hybrid. Procedure fixtures + claim ledger.
- **Validators:** procedure_completeness (every step present, in order, with tools and checks), safety_claim (mandatory for every procedure), statute_edition (safety standards by edition), claim_flagger, span_hash, expiry_check.
- **Claim-ledger specifics:** the official vocational curriculum and safety standards cited by edition; equipment ratings and codes time-bound where they change.
- **Reviewer qualification:** trade-qualified instructor (practitioner) + safety reviewer.
- **Contested handling:** rare; differing industry practices attributed.
- **Risk:** standard to high depending on the trade (electrical and chemical trades flagged high by the profile version).
- **Gate note:** activation needs NSQF descriptors registered (O-11).

## 8. family/exam_strategy

- **Subjects:** exam_strategy, aptitude, reasoning.
- **Validation mode:** claim ledger tied to official papers.
- **Validators:** pattern_recompute (pattern claims recomputed from the stored paper set: question counts per section, marks distribution, time limits), source_policy, expiry_check, answer_key_solver (aptitude items), claim_flagger, span_hash (the last two added 15 Oct 2026: a claim-ledger profile must list both, schema).
- **Claim-ledger specifics:** pattern claims cite the official notification or paper only (`official_paper_or_key`); all exam_pattern claims are time-bound (schema); predictive claims ("will come") are forbidden unless stated with evidence and attributed as a trend analysis over named papers.
- **Reviewer qualification:** academic lead; subject reviewer for content items.
- **Contested handling:** coaching-industry claims are never sources (self_published or practitioner without evidence).
- **Risk:** standard; staleness is the main exposure, so expiry drives re-QA.
- **Safety note:** AC1 overlays forbid fear, urgency and peer-comparison language; AC0 has no exam strategy format.

## 9. family/health_medicine (high risk)

- **Subjects:** health_education, anatomy_physiology, pharmacology, nursing, medicine, public_health, biology health topics where clinical claims appear.
- **Validation mode:** hybrid. Dosage and calculation fixtures (`dosage_fixture`) + claim ledger.
- **Validators:** dosage_fixture, claim_flagger, span_hash, source_policy, expiry_check, sensitivity_screen.
- **Claim-ledger specifics:** `risk_class: high` forces **≥2 sources for every claim** (schema) and requires disclaimers. Clinical claims are time-bound (schema). Primary authorities are official guidelines and peer-reviewed sources. Every artefact carries a "not medical advice" disclaimer whose wording is pending O-9.
- **Reviewer qualification:** clinician or licensed health professional for UG/PG and any clinical claim; health educator for school health education; sensitivity reviewer for reproductive, mental health and substance topics with level checks.
- **Contested handling:** evolving guidance is attributed with as-of dates; never presented as settled when guidelines differ.
- **Risk:** high; not activated before O-9 and named clinician reviewers.

## 10. family/law (high risk)

- **Subjects:** law, legal_studies (UG/PG and adult_prof); constitutional content at school levels remains civics in humanities_citation unless it states legal rules.
- **Validation mode:** claim ledger with jurisdiction.
- **Validators:** jurisdiction_check, statute_edition, claim_flagger, span_hash, source_policy, expiry_check.
- **Claim-ledger specifics:** `legal_rule` claims require `jurisdiction`, `as_of_date` and `review_by` (schema); statutes and judgments cite the official text by edition; ≥2 sources per claim (high risk). A "not legal advice" disclaimer (O-9).
- **Reviewer qualification:** licensed advocate or law faculty at or above the content level.
- **Contested handling:** conflicting judgments attributed by court and date; Perspectives for unsettled questions.
- **Risk:** high; amendments trigger revocation of affected claims.

---

## 11. Summary matrix

| Family | Mode | Key validators | Reviewer | Risk | Contested default | Levels allowed (15 Oct 2026) | Perspectives required at (15 Oct 2026) |
|---|---|---|---|---|---|---|---|
| stem_fixture | hybrid | fixture_exec, unit_dimension, sigfig, sandbox | subject teacher → specialist | standard | rare | all ten levels | none |
| quant_social | hybrid | ledger_recompute, statute_edition, expiry | commerce/economics → CA/economist | standard | attributed | all ten levels | none |
| humanities_citation | claim ledger | flagger, span_hash, date_name, map_boundary, sensitivity | discipline-qualified + sensitivity | standard (sensitive claims ≥2 sources) | Perspectives at l9_10+ | all ten levels | l9_10, l11_12, ug, pg, adult_prof |
| languages_literature | hybrid | grammar_orthography, quote_rights, lexicon | native-language editor | standard | attributed | all ten levels | l9_10, l11_12, ug, pg, adult_prof |
| arts_skills | ledger + demo | safety_claim, procedure_completeness | practitioner + safety | standard | attributed | all ten levels | none |
| vocational | hybrid | procedure_completeness, safety_claim, statute_edition | trade instructor + safety | standard/high | attributed | all ten levels | none |
| exam_strategy | ledger (official papers) | pattern_recompute, expiry, claim_flagger, span_hash | academic lead | standard | n/a | all ten levels | none |
| health_medicine | hybrid | dosage_fixture, expiry, sensitivity | clinician | high | attributed with dates | all ten levels | none |
| law | ledger + jurisdiction | jurisdiction_check, statute_edition | licensed advocate | high | attributed by court | ug, pg, adult_prof (add l11_12 only if the lead brings CBSE Legal Studies into scope) | ug, pg, adult_prof |
| evs_foundational (added 15 Oct 2026, [Recommendation]) | hybrid | fixture_exec, claim_flagger, span_hash, safety_claim, sensitivity_screen | primary-years teacher + child-development reviewer co-sign | standard (activities and health content flagged) | attributed | l1_2, l3_5 (CE-65) | none |

## 12. Activation order

stem_fixture is active at M1 (current scope). humanities_citation (Class 10 social science) is the first non-STEM family at M4 because its rules exercise the full ledger, contested states and map review. quant_social and languages_literature follow when named reviewers exist. health_medicine and law wait for counsel items O-9 and named licensed reviewers. Each activation is a registry change through GR with a pilot: every rendered claim resolves to an approved claim, and an adversarial test (an injected unsourced claim) is caught by Q-CLOSURE and Q-LEDGER.

## 13. family/evs_foundational (Classes 1–5 Environmental Studies) — added 15 Oct 2026, [Recommendation], CE-65

**Why.** Environmental Studies (EVS, "the world around us") at Classes 1–5 integrates science, social and health content. It belongs to none of the nine families above, so the Resolver (R3: the family is derived from the one profile whose `subjects[]` lists the subject) would refuse every Class 1–5 EVS request. Splitting an integrated strand across `stem_fixture` and `humanities_citation` would break the rule that a subject sits in exactly one family. This section adds one family. It is a design recommendation, not an evidence-backed fact, and it needs a lead decision to activate.

- **Subjects:** evs, environmental_studies, world_around_us. Valid at `level/l1_2` and `level/l3_5` only. From `level/l6_8` the strands separate into their own subjects (science, social science, health education) and resolve to `stem_fixture`, `humanities_citation` or `health_medicine` (health education at school level, under the O-9 rule) as those profiles already provide.
- **Validation mode:** hybrid.
  - **Fixture where quantitative.** Counting, measuring, simple quantities, time and calendar facts, and any number on screen come from an executable fixture, never from generation (`fixture_exec`, Q-FIX).
  - **Citation where factual.** Facts about living things, places, communities, food, water, weather, safety and health are claim-ledger claims with a board textbook (the primary authority at these levels) or another reliable source and a span hash. The common rules in §1.1 apply unchanged, and the unsourced-is-removed default applies.
  - **Child-development reviewer co-sign** on every claim set and every GA-Δ. This is the same role CE-L9 already requires for AC0 content, held here as a family reviewer role so the Resolver can refuse the family when no qualified reviewer is available.
- **Validators:** fixture_exec, claim_flagger, span_hash, source_policy, safety_claim (every household activity), sensitivity_screen (community, caste, religion, family structure, food, body and health topics), expiry_check for time-bound facts (for example seasonal or administrative facts).
- **Claim types:** definition, quantitative, procedure_fact, safety, historical_event, date_fact, biographical, interpretation.
- **Claim-ledger specifics:** child-appropriate wording is a Level Profile concern (`level/l1_2`, `level/l3_5`), never a reason to simplify a claim into a falsehood. A simplification is an SIM node with its approximation stated. Local examples (a river, a festival, a crop) carry a source and a region tag, because EVS content is place-specific.
- **Reviewer qualification:** a primary-years teacher; the child-development reviewer (co-sign); a science or social-science subject reviewer for the matching strand; a health educator for health strands; a safety reviewer for every physical activity. A reviewer in the reviewer registry must hold each role before activation.
- **Contested handling:** attributed. Contested social or environmental topics are not taught as contested at these levels; the profile routes them to a human decision (`board_vs_scholarship` flag) rather than an automatic verdict, and Perspectives is not available at AC0.
- **Risk:** standard, with activities and health content flagged for the safety reviewer. Not high-risk unless a claim crosses into clinical content, which is routed to `health_medicine` and blocked until O-9.
- **Safety class:** inherits `safety/ac0` from the level, so all AC0 rules (no data solicitation, zero-flash, Path A voice, household-safe materials with a "with a grown-up" cue) apply.
- **Gate note:** activation needs the child-development reviewer onboarded with a backup (Roadmap level 5a), O-1 to O-4, O-7 and O-10, the G-COUNSEL record, and a named EVS reviewer. Until then the family is defined but `activation.activated` is `false`.
- **Registry change:** adds `family/evs_foundational` to the subject-profile registry through GR. The `subject_profile.schema.json` `family_id` is a pattern (`^family/[a-z0-9_]+$`), so no schema change is needed for the id. (15 Oct 2026: the schema now requires `levels_allowed`; this family sets `[level/l1_2, level/l3_5]`, so R3 refuses `subject: evs` at any other level.) ~~The subsystem schemas that enumerate families (`script_spec`, `interaction_spec`) gain the value.~~ No schema change is needed (15 Oct 2026: the subsystem schemas take family ids as patterns).
