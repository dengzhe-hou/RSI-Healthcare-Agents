# Evaluation design templates for healthcare agent improvement

Companion resource version 0.3.0, fixed search cutoff4 November 2026. These are study-design and reporting templates accompanying the structured narrative review. They operationalize existing concepts; they are not a validated reporting standard, executable benchmark or new aggregate metric. Authors select their task, native outcome measures, configuration and resource budget before using a template. No new experiment has been run for this resource.

## Choose the question your experiment answers

| Question | Comparison | What to keep fixed or disclose |
|---|---|---|
| persistent_memory | Paired persistent-memory condition versus memory-disabled/empty condition. A frozen prebuilt-memory arm answers a different question from ongoing writeback. | Task backbone, orchestration, tools, starting policy and base artifacts, feedback access and initial cases. Keep the patient/case sequence paired or record the ordering difference. |
| changed_generator_or_recipe | Changed generator/operator/skill/recipe versus the corresponding frozen version, followed by matched learner training and independent downstream evaluation. | Shared learner start, task model, training protocol, data access, selection rule and downstream evaluator. State whether accepted-data volume, learner compute, generator compute or total search compute is actually matched. |
| revised_improver | Start from the same learner and improvement procedure. Compare keeping that procedure fixed with revising it, then evaluate their subsequent learning on separate later tasks or cycles. | Shared initial agent, update opportunities, data access, task distribution, resource envelope, evaluator and outcome definition. Record any intended difference. |

For each question, complete `templates/experiment_plan.csv` or `.json`. Fill all fields with the planned choices and their provenance. Explicitly record any unmatched element. Do not merge memory contribution, generator contribution and improvement-procedure contribution into one score or treat task accuracy alone as evidence of all three.

## Specify the data and update timeline

Record the model/harness and source versions, update data, candidate-selection data and final-test data separately. Identify every route by which labels, retrieved examples, patient history or feedback can enter later decisions. State whether the memory starts empty, includes a frozen prior bank or grows during the test stream. Mark the last selection/writeback step before an untouched final test. Online learning protocols can allow between-case updates, but must identify what feedback is available before each later case. A test stream used to shape updates is not simultaneously an untouched final test.

Use patient/case-disjoint or temporal separation appropriate to the actual task; record the official benchmark split and any deviation rather than invent a new split silently. A deployed service is not automatically a prospective evaluation of its improvement mechanism. Clinical setting, mechanism evidence, causal benefit and publication status remain separate fields.

## Record the actual scope of matching

List which quantities are matched: learner initialization, accepted-data volume, learner-training compute, candidate-generation/search compute, total resources and evaluation settings. If one is not matched, record what differs. An equal target of accepted samples can require different candidate counts, as in ECG-RSI. A longer-training control can address learner-training compute without measuring all outer-loop search cost. Describe the comparison that was actually conducted.

## Keep four linked records

- `run_log` identifies the condition, repetition, versions, input stream, memory state and artifact/result links for each actual run.
- `update_log` records parent/candidate versions, available feedback, candidate decisions and release timing. Retain rejected and failed proposals.
- `cost_log` separates generation, repair, selection, training and testing. Count all candidates, including rejections; keep calls, tokens, wall time, hardware use and money in their original units.
- `metric_results` records each task-native outcome and its original unit, aggregation and uncertainty method. It neither selects new metrics automatically nor converts them into a composite quality score.

Every template is supplied as CSV and JSON. Stable `design_id` and `run_id` fields join the tables. Empty cells in blank templates are intentional. In filled records, use the documented statuses to distinguish a measured zero, unavailable measurement, a value not extracted from a report and a planned-but-unexecuted item. Do not invent timestamps, seeds or costs to make a reconstruction look complete.

## Read the worked cases before filling a plan

`examples/worked_designs.json/.csv` contains four complete design assessments from three mapped studies: PrivMeSA for paired memory contribution; ECG-RSI for changed synthesis components; ReVision3D for a changed training recipe; and ReVision3D as a negative boundary case for revised-improver evidence. They reconstruct reported designs, not runs executed by this project. The fourth example explains why a changing recipe under a fixed designer does not establish a revised improver. No positive healthcare Level 3 example is fabricated.

`examples/cost_log_reported.csv/.json` and `metric_results_reported.csv/.json` demonstrate the linked record format with ECG-RSI's published Table 10. Recorded candidate counts are16193/36723/22398 at 10,000 accepted questions; unmeasured or unextracted resource fields remain explicitly labelled. These summaries do not constitute executable runs or a new performance comparison.

## Attribution and verification

The component/improver distinction follows Liu et al.; the level roles and functional distinction follow Han et al. and Pu et al., as cited in `conceptual_sources.bib`. Cite those conceptual sources for their ideas and the RSI-HA manuscript when using this healthcare operationalization,85-study coding or templates. Each worked case retains its examined source version and original locators. The source versions and classifications are unchanged. The fixed sample-check plan was withdrawn without being performed. The 85-row author review form remains blank and is not evidence of completed author verification.

The four fully populated `examples/experiment_plan_filled.csv/.json` records use exactly the same columns as the blank experiment plan. Unknown source details have explicit not-re-extracted statements rather than invented IDs, seeds or timings.
