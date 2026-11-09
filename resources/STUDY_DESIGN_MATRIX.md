# Reading the 85-study design matrix

`snapshots/2026-11-04/study_design_matrix.csv/.json/.html` joins existing source-grounded extraction fields with the author-approved mechanism levels and clinical evaluation categories. No classification or study selection changes.

`mechanism_group` is the existing organizational group from the compact evidence table; it is not an evidence score. `evidence_level` and `clinical_evaluation_category` come directly from the manuscript evidence-profile table. The classification-join audit retains the source commit and display-name/key match for every row.

`control_description`, `independent_test_description`, `update_timing`, `selection_and_release`, `fixed_components` and `source_locators` preserve the existing extraction. Their prose is retained rather than forcing varied controls or ambiguous tests into a new yes/no quality judgment. `matched_generator_control_in_review` means that the review identified a matched generator control in ECG-RSI or ReVision3D. `not_identified` for another row does not mean that the paper has no component ablation or no useful evaluation.

The85-row matrix includes the contextual comparators already in the review. It must not be reinterpreted as85 demonstrated RSI systems. Publication status, mechanism evidence, causal benefit and clinical validation remain separate. Original source reports and cited conceptual definitions retain their attribution.

`author_check` and `author_comment` are intentionally blank in every row. `author_review_85.csv` presents the same classifications, controls, testing descriptions and locators in a form the author can check. The earlier fixed 70-record sample-check plan was withdrawn without being performed. The blank fields do not record completed author verification. Review status is documented in REVIEW_STATUS.md.

## Imaging and radiology-report studies (Table S4)

This editable table preserves the 25-study imaging view moved from the manuscript on 9 November 2026. Its modality, task, reference-standard descriptions and evidence levels are unchanged. The complete S3 table is also available in the companion GitHub resources. Publication status, mechanism evidence and clinical evaluation remain separate judgments. Full source versions, boundaries and locators are in the evidence map.

<!-- RSI_HA_IMAGING_TABLE_BEGIN -->
| Key | Study | Modality and task | Data and reference standard | Level | Source URL |
| --- | --- | --- | --- | --- | --- |
| shen2026evomedagent | Evo-MedAgent | Chest radiograph question answering | ChestAgentBench answers, revealed after each case | 1 | https://arxiv.org/html/2604.14475v1 |
| feng2026medexpmem | MedExpMem | CT, MRI, radiography and ultrasound differential diagnosis | Eurorad teaching-file diagnoses; temporal split | 1 | https://arxiv.org/html/2605.22872v1 |
| wu2026medrsi | MedRSI | Imaging diagnosis and tool construction | Public benchmark labels and private retrospective cohorts | 2, implicit | https://arxiv.org/html/2609.24838v1 |
| chen2026medforge | MedForge-RSI | Medical-image forgery detection | Verified forgery labels; separate final test set | 1 | https://arxiv.org/abs/2609.36549v1 |
| coevolving2025 | TissueLab | Imaging and omics analysis with expert interaction | Clinician annotations and accept/reject feedback | 1 | https://arxiv.org/abs/2509.20279 |
| fan2026macro | MACRO | Multiple medical imaging analysis tasks | Public dataset labels | 2, implicit | https://arxiv.org/abs/2603.05860 |
| lee2026revision3d | ReVision3D | CT liver and kidney lesion localization | Reference segmentation masks (LiTS, KiTS23) | 2, explicit | https://arxiv.org/abs/2609.32984v2 |
| xu2026oaims | OAIMS | Interactive segmentation under modality and pathology shift | Reference masks; correction clicks simulated from labels | 1 | https://arxiv.org/abs/2503.06717v4 |
| tzanis2026reclaim | ReclAIm | MRI, CT and radiograph classifier maintenance | Dataset labels; monitoring cohort reused for reassessment | 1 | https://arxiv.org/pdf/2510.17004v2 |
| hu2026templar | TEMPLAR | PET/CT and CT reporting templates | Report corpora; expert and LLM-judged ratings | 1 | https://arxiv.org/abs/2610.05247v1 |
| zhuang2025doctor | Learning to Be A Doctor | Dermatology image diagnosis with workflow search | Skin Concepts and augmented Skin Conditions labels | 1 | https://arxiv.org/html/2504.11301v2 |
| sayeedi2026r4 | R4Agent | Chest radiograph detection and reporting | Public chest X-ray datasets; memory written from self-critique | 1 | https://arxiv.org/html/2601.08192v2 |
| zhu2026ultrasoundagents | Ultrasound-Agents | Breast ultrasound malignancy and BI-RADS assessment | Public datasets; attribute, box and BI-RADS labels | 2, implicit | https://arxiv.org/html/2603.10852v1 |
| chen2026theraagent | TheraAgent | PSMA PET/CT-based radioligand therapy outcome prediction | Single-centre cohort; documented PSA response and survival | 1 | https://arxiv.org/html/2603.13676v1 |
| chen2026skingptx | SkinGPT-X | Dermatology image diagnosis | Public clinical and dermoscopic datasets; expert labels | 1 | https://arxiv.org/html/2603.26122v1 |
| meng2026topoagent | TopoAgent | Topological descriptors for 2D image classification across 11 modalities | Public benchmark labels; reflection on feature statistics | 1 | https://arxiv.org/html/2606.29763v1 |
| qu2026sageagent | SAGEAgent | Glioma survival prediction with staged radiology acquisition | TCGA-LGG, TCGA-GBM and BraTS outcomes | 1 | https://arxiv.org/html/2607.09521v1 |
| wang2026mira | MIRA | Medical image question answering | Public VQA benchmark answers | 2, implicit | https://arxiv.org/pdf/2608.10827v1 |
| liu2026bat | BaT | Medical-imaging AI development and radiology viewer tasks | Synthetic sandboxes scored by a rubric verifier | 2, explicit | https://arxiv.org/html/2608.16211v1 |
| shao2026case | CASE | Longitudinal multi-sequence MRI diagnosis questions | UK Biobank MRI; ICD-10-derived multiple-choice labels | 2, implicit | https://arxiv.org/html/2609.39566v3 |
| feng2026gatedopenclaw | Gated OpenClaw | Fundus-image diagnosis with adapter and guidance updates | Private fundus images; report-simulated feedback; test cases reused | 1 | https://ijocsit.org/pdf/2026/10.62051-ijcsit.v8n4.01.pdf |
| li2026emai | EMAI | Chest-radiology report summarization | MIMIC-CXR and Open-I report texts; reference impressions and clinician ratings | 1 | https://www.sciencedirect.com/science/article/abs/pii/S016926072500495X |
| li2026decisionrules | Evolved decision rules | Multi-image medical video question answering | MedFrameQA answers; video-grouped evolution, selection and test partitions | 1 | https://arxiv.org/abs/2607.27564v1 |
| fan2026medenv | MedEnv | Simulated diagnosis with optional chest radiograph review | Virtual EHR environment; author-reported held-out cases and reward ablations | 2, implicit | https://papers.miccai.org/miccai-2026/paper/5084_paper.pdf |
| chen2027mdtace | MDTace | Multidisciplinary medical text and image QA | MedQA, PubMedQA, VQA-RAD and SLAKE; training-derived Playbook only | 1 | https://link.springer.com/chapter/10.1007/978-981-92-3403-5_6 |
<!-- RSI_HA_IMAGING_TABLE_END -->
