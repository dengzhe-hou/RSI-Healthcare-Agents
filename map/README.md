# Connected paper map

The network and paper index use the 85 unchanged records in `resources/snapshots/2026-11-04/`. Mechanism groups, evidence levels and clinical-evaluation categories are taken directly from that release. Each point has the same size. Color and shape identify the recorded mechanism group.

## Discussion links and survey sections

`survey_context.json` stores section headings, cited bibliography keys and short excerpts from the author-revision manuscript of 12 November 2026. An edge is present exactly when both mapped keys occur in the same prose paragraph. This is a co-discussion index of this survey, not a citation network between the primary papers. Figures, tables, equations and bibliography entries are excluded. All 85 records have at least one indexed discussion location.

The detail panel shows sentences containing the selected paper's citation. Excerpts can be truncated and do not replace the primary source. The current full manuscript PDF is not published here.

## Layout and rebuild

Run `python scripts/build_map.py` from the repository root. The builder uses the fixed public records, source bibliography and saved survey context to regenerate `map/data.json` and `PAPERS.md`. It uses only the Python standard library.

The deterministic layout starts at the four existing category anchors. Discussion links gently attract related papers, and label collision separation makes space for reading. Positions and distances are navigation choices, not measures of evidence quality or scientific similarity.

For maintainers with the author manuscript, `python scripts/build_map.py --manuscript /absolute/path/to/main.tex` refreshes the saved section and co-discussion index. Review the resulting excerpts and preserve the fixed evidence fields. Refreshing survey context does not refresh study eligibility, classification or publication status.

## Interaction

- Search, mechanism, section, clinical-evaluation, level and year filters work in both views.
- Select a paper to reveal its neighbors and read the overview, survey context or full evidence.
- Drag, wheel or pinch to navigate. Fit restores the filtered network.
- Each paper has a shareable hash link, copied BibTeX and downloadable JSON record.
- The paper index opens by default on narrow screens. The network remains available.
- Keyboard users can select study nodes with Enter or Space and close details with Escape.

The six-panel illustrations and existing figures retain their [source notes](../assets/FIGURE_CREDITS.md). No new scientific classifications are introduced by this interface.
