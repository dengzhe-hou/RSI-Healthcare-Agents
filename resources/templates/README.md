# Fillable experiment records

Choose CSV for flat tables or JSON for structured processing. The fields have the same names in both formats. The blank files contain one empty record; replace it with your actual plan/records. `field_lists.json` lists all columns. This is a reporting format, not an evaluator or automated RSI classifier.

Use `experiment_plan` before a run. Link `run_log`, `update_log`, `cost_log` and `metric_results` by design/run IDs. Keep each task's native metric name and unit. Report the uncertainty method the study actually uses. Separate update selection from independent final testing and separate total search cost from accepted-data or learner-training cost.

The filled source-summary examples are explicitly labelled `reported_summary`; they must not be imported as measured runs. Missing source data is represented by an empty value with an explicit status/reason. Author-review columns in the 85-study matrix are intentionally empty until the author records a decision.

## Field notes

### record_kind

Use actual_run, reported_summary or unexecuted_plan. Never mix a literature reconstruction with locally measured execution.

### design_id

Stable identifier linking a plan and its runs. It is a local record label, not a published benchmark identifier.

### run_id

Stable identifier for one condition/repetition or an explicitly labelled source-summary record.

### question

persistent_memory, changed_generator_or_recipe, or revised_improver; the three comparisons answer different causal questions.

### target_claim

The precise claim this comparison is meant to support, without assuming its result.

### changed_object

Name the memory, generator, recipe, proposer, selector or evaluator that changes; do not substitute the system name.

### matching_requirements

List the quantities and configurations to match, plus intended deviations; preserve study-author choices.

### feedback_and_label_access

What labels/outcomes are available before each update, with the point of access.

### test_freeze_point

The final selection/update action before an independent test, or the exact between-case protocol if writeback remains allowed.

### native_metrics_and_units

Study-author-selected task metrics and original units. The template does not choose or aggregate metrics.

### uncertainty_and_repeats

Report the actually planned or conducted repetitions and uncertainty procedure; missing information is not a single-run assumption.

### execution_state

For actual runs record queued, running, completed, failed or cancelled, separately from whether scientific outputs were accepted.

### candidate_count_status

reported or measured; distinguish a count derived by subtraction from a directly reported count.

### measurement_status

Explain whether each cost is measured, reported, not extracted or unavailable. Blank or unknown costs are not zero.

### value_status

measured, reported, not_extracted, not_reported_in_examined_source or not_applicable. Use a numeric zero only for an actual zero.

### used_for_selection

Record whether this outcome/test contributed to candidate selection. Report mixed roles explicitly.

### source_locator

Original URL with the section/table/page or, for actual runs, the local log/artifact that supports the field.

### author_decision_status

Who approved a new plan or checked a reported case. Preserve pending author review.

## Follow a plan with exactly the same columns

`examples/experiment_plan_filled.csv/.json` fills every plan column for the four source-grounded cases. This is a reported-design reconstruction, not an execution plan approved for new experiments. Explicit not-re-extracted statements preserve unknown checkpoint IDs, seeds and other configuration details rather than inventing them. Run and update histories are not fabricated from aggregate paper results.
