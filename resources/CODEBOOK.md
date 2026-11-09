# Evidence extraction codebook

Version 0.3.0, fixed search cutoff 4 November 2026. Read REVIEW_STATUS.md before reuse. Fields retain the source-version-specific judgments of the manuscript.

## key

Stable manuscript bibliography key. Use this to join records across the extraction and mechanism summaries.

## name

System or study label used in the review. Multiple reports of the same study are reconciled before counting.

## title

Title of the examined primary report.

## authors

Authors as recorded in the extraction. JSON uses a list; CSV uses semicolon-separated names.

## year

Bibliographic year. This can differ from first public availability; a2027 imprint first online in2026 remains2027.

## publication_status

Publication or acceptance information for the source version examined. Keep separate from mechanism evidence and clinical setting.

## version

Examined preprint revision, publication version or explicitly recorded documentation snapshot.

## source_url

Public landing page or full-text URL of the examined report. Third-party reports are linked, not redistributed.

## doi

DOI when recorded; an empty value is missing metadata rather than evidence that no DOI exists.

## update_target

The object that changes, such as memory, skills, tools, workflow, learner parameters or a training generator.

## fixed_components

Backbones, prompts, generation rules, selectors, evaluators or other components held fixed in the examined design.

## feedback

Information used to propose or accept an update, with label/reference availability where reported.

## timing

When learning, selection, writeback, freezing and later testing occur across cases or episodes.

## retained_artifact

What survives a completed case and is reused on later, different cases.

## update_generator

The component or procedure proposing subsequent updates.

## selection_and_release

How candidates are selected, validated, accepted and exposed to later tasks.

## independent_evaluation

Reported held-out tests, external data, time separation, clinician assessment and component controls.

## fixed_procedure_control

Whether a matched comparison freezes the changed update-producing component or improvement procedure. Preserve disclosed mismatches.

## improver_change

What, if anything, changes in constructing, selecting or evaluating future updates. This field alone is not a causal-effect or clinical-benefit claim.

## clinical_setting

Setting of the reported study evaluation. An operating service and a prospective test of its adaptation mechanism are different facts.

## evidence_boundary

Constraints on what the examined report supports, including missing controls, source limitations and evaluation boundaries.

## locators

Original sections, tables, appendices or PDF pages supporting the extraction. JSON retains objects with url/location; CSV uses one locator per line.

## Missing information and interpretation

"Not reported" is a reporting gap in the examined version, not proof that a mechanism is absent. Empty DOI/version fields indicate missing metadata. Publication status, mechanism level, causal benefit and clinical validation must be assessed separately. Do not turn these fields into a single quality score or pool performance gains across incompatible tasks. The reviewed levels are defined in EVIDENCE_CODING_GUIDE.md; `mechanism_summaries` groups are organizational headings rather than level labels.

## Screening ledger

`id` is a stable local screening-record identifier. `title`, `date`, `sources`, `arxiv`, `doi` and `openalex_ids` preserve report metadata. `stage`, `outcome` and `reason` retain the screening decision. `source_used` and `source_completeness` document available examination sources when recorded. IDs are local to the screening ledger; use DOI/arXiv/title and source locators to relate them to the 85 study keys. Multiple reports can map to one study.
