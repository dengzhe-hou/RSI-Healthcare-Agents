# RSI-HA evidence coding guide

Version 0.3.0. Search cutoff 4 November 2026. This guide operationalizes the review's existing criteria; it does not introduce a new RSI definition or certify clinical readiness. Verification status is documented in REVIEW_STATUS.md.

## Use the examined report as the unit

Record the source version and locate the object that changes, the feedback it receives, what persists to later different cases, and which generator, selector or evaluator stays fixed. Separate update generation/selection from the later test. A system name or its use of the word "recursive" does not determine its classification.

## Assign the highest evidenced level

| Level | Object/role | Decision rule |
|---|---|---|
| 0 | Current-case or session state | No newly learned artifact is shown to persist to later, different cases. Static experience retrieval alone does not establish learning. |
| 1 | Persistent components; fixed updater | Memory, skills, tools, configuration or learner weights change under an unchanged update procedure. |
| 2-explicit | Changed generator for later learning | A changed component is explicitly used to construct, select or evaluate later training data, interactions, trajectories or recipes; its change-admission procedure stays fixed. |
| 2-implicit | Dual role; update-producing role not isolated | The changed component has a documented role in producing or assessing later updates as well as task execution, but that role is not isolated. |
| 3 | Revised improver; later learning tested | The update-proposing, selection or evaluation procedure itself is revised, and its effect on subsequent learning is tested. |

Merely executing a task whose outputs are later mined does not establish Level 2. For2-implicit, an update-producing or update-assessing role must be documented. A Level 2 assignment is separate from whether its changing component causes a measured gain. A claim to Level 3 requires testing the revised improver's contribution to subsequent learning, with data/compute matching and independent later evaluation reported.

## Keep the other judgments separate

Record publication/acceptance status; whether the changed component has a causal control; and whether evaluation uses simulated, offline, retrospective, external retrospective or prospective clinical data. Record service deployment separately from evaluation design. An operating service evaluated through past dialogues remains retrospective in this map. No mapped study meets Level 3 or reports prospective clinical evaluation.

## Use the coded examples

| Study key | Level in the review | Rationale |
|---|---|---|
| clinicalagents2026 | 0 | Static experience retrieval and changing within-case working state do not show new cross-case learning. |
| medhospital2024 | 1 | Cases and principles accumulate under a fixed reflection and validation design. |
| wang2026ecgrsi | 2-explicit | Synthesis operators and skills generate later training data. Frozen-operator/skill controls exist, but generation-search costs are unequal; this does not establish Level 3. |
| jiang2026sempa | 2-implicit | The changing Critic affects later update selection; its evolving evaluator contribution is not isolated. |

Source URLs and exact original locators are provided in `examples/coded_examples.json` and the full evidence map. Preserve the experimental boundaries when citing an example.

## Reuse and attribution

The component-versus-improver distinction follows Liu et al. (2026), DOI 10.20944/preprints202608.0051.v1. Level roles parallel Han et al. (2026), arXiv 2610.38266v1, and the functional distinction in Pu et al. (2026), arXiv 2610.35193v1. Cite those conceptual sources when adopting their definitions; cite the RSI-HA manuscript when using this healthcare extraction, operationalization or study map. The complete references are in `conceptual_sources.bib`.

Start from `extraction_template.csv` and use the fields described in CODEBOOK.md. Keep the source version and locators when adding or correcting an entry. "Not reported" is not "absent". Do not infer an aggregate quality score from this guide.

For designing a study rather than classifying a report, use EVALUATION_DESIGN_TEMPLATE.md and templates/experiment_plan.csv. The linked records preserve phase boundaries and the scope of matched controls.
