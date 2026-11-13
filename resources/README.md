# RSI-HA evidence resources

Companion resources for **A Survey on Recursive Self-Improvement in Healthcare AI Agents** by Dengzhe Hou, Zihao Wu, Yuwen Zeng, Lingyu Jiang, Fangzhou Lin and Kazunori D Yamada. Fixed search cutoff **4 November 2026**, resource version **0.3.2**.

Screening and extraction were LLM-assisted. Read [review status](REVIEW_STATUS.md) before reuse.

## Start here

- Read the [one-page coding guide](EVIDENCE_CODING_GUIDE.pdf) or its [editable text](EVIDENCE_CODING_GUIDE.md).
- Download the 85-study evidence map as [CSV](snapshots/2026-11-04/evidence_map.csv), [JSON](snapshots/2026-11-04/evidence_map.json) or [searchable HTML](snapshots/2026-11-04/evidence_map.html).
- Read [field descriptions](CODEBOOK.md), [four coded examples](examples/coded_examples.json) and the [blank extraction template](extraction_template.csv).
- Inspect all 10,720 screening records as [CSV](snapshots/2026-11-04/screening_decisions.csv), [JSON](snapshots/2026-11-04/screening_decisions.json) or [searchable HTML](snapshots/2026-11-04/screening_decisions.html).
- Read the complete 85-study mechanism table S3 as [PDF](snapshots/2026-11-04/mechanism_summaries.pdf), or inspect the same study summaries as [CSV](snapshots/2026-11-04/mechanism_summaries.csv) and [JSON](snapshots/2026-11-04/mechanism_summaries.json). Read the [search provenance](snapshots/2026-11-04/SEARCH_METHOD.md).

- Inspect the 25-study imaging view (Table S4) in [editable Markdown](STUDY_DESIGN_MATRIX.md#imaging-and-radiology-report-studies-table-s4), [CSV](snapshots/2026-11-04/imaging_studies.csv), [JSON](snapshots/2026-11-04/imaging_studies.json) or [searchable HTML](snapshots/2026-11-04/imaging_studies.html).

## Read an entry in Python

No external packages are needed to read the data. From the repository root, run:

```bash
python resources/examples/read_evidence.py
```

The example joins CSV and JSON by the stable bibliography key, filters update targets and prints a study's evaluation boundaries and original source locators. This example reads existing judgments; it does not assign evidence levels automatically.

## Cite and interpret the resource

See [CITATION.cff](../CITATION.cff) and [BibTeX](../CITATION.bib). Cite the accompanying manuscript for use of its healthcare synthesis and coding operationalization; identify the resource version when reporting an extraction or reanalysis. Credit the original conceptual and primary sources where their definitions or findings are used.

These are literature-extraction records, not a patient dataset or executable benchmark. Publication status, mechanism level, demonstrated benefit and clinical evaluation remain separate judgments. Read [rights](RIGHTS.md), [fixed-version policy](VERSIONS.md) and [changelog](CHANGELOG.md). No Zenodo DOI or arXiv identifier has been assigned to this revised manuscript/resource at preparation time.

The revised manuscript remains under author revision and is not included in this resource publication. Its earlier version is on [Preprints.org](https://www.preprints.org/manuscript/202605.1547), with a different title and earlier contents.

The evidence resources were made public on 9 November 2026 with author authorization. Manuscript revision continues, and arXiv upload and submission remain paused. No additional open-content license has been selected.

## Design an evaluation and record it

Read the evaluation-design guide in [PDF](EVALUATION_DESIGN_TEMPLATE.pdf) or [editable text](EVALUATION_DESIGN_TEMPLATE.md). Select a question, then fill the [plan](templates/experiment_plan.csv) and linked [CSV/JSON record formats](templates/README.md). Inspect the [four filled design assessments](examples/worked_designs.json) and [source-labelled cost/metric examples](examples/cost_log_reported.csv).

The [85-study design matrix](snapshots/2026-11-04/study_design_matrix.html) aligns mechanism class, controls, independent tests and original locators. Download [CSV](snapshots/2026-11-04/study_design_matrix.csv) or [JSON](snapshots/2026-11-04/study_design_matrix.json), read its [field notes](STUDY_DESIGN_MATRIX.md), or complete the [author review form](author_review_85.csv).

For a direct field-by-field example, compare the blank [plan CSV](templates/experiment_plan.csv) with the [completed plan CSV](examples/experiment_plan_filled.csv) or [JSON](examples/experiment_plan_filled.json). Every column is filled, while unavailable source details are explicitly labelled rather than fabricated.
