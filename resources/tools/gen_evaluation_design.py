"""Render the source-grounded four-page RSI-HA design and record guide."""
from pathlib import Path
from xml.sax.saxutils import escape
import json,subprocess
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
import fitz

RES=Path(__file__).resolve().parents[1]
for family,name in [('Arial','Arial'),('Arial:style=Bold','ArialBold')]:
 pdfmetrics.registerFont(TTFont(name,subprocess.check_output(['fc-match','-f','%{file}',family],text=True).strip()))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold',italic='Arial',boldItalic='ArialBold')
styles={
 'title':ParagraphStyle('title',fontName='ArialBold',fontSize=18,leading=22,spaceAfter=7),
 'sub':ParagraphStyle('sub',fontName='Arial',fontSize=9,leading=12,spaceAfter=12,textColor=colors.HexColor('#333333')),
 'head':ParagraphStyle('head',fontName='ArialBold',fontSize=11,leading=14,spaceBefore=10,spaceAfter=5),
 'body':ParagraphStyle('body',fontName='Arial',fontSize=10,leading=13.3,spaceAfter=7),
 'small':ParagraphStyle('small',fontName='Arial',fontSize=8.5,leading=11.3,spaceAfter=5),
 'cell':ParagraphStyle('cell',fontName='Arial',fontSize=9,leading=12,spaceAfter=0),
}
def p(text,kind='body'):return Paragraph(text,styles[kind])
def clean(text):return escape(str(text))
def table(rows,widths):
 t=Table([[p(clean(x),'cell') for x in row] for row in rows],colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eeeeee')),('LINEBELOW',(0,0),(-1,0),0.65,colors.black),('LINEBELOW',(0,1),(-1,-1),0.3,colors.HexColor('#bbbbbb')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 return t

controls=json.loads((RES/'templates/control_designs.json').read_text())
cases=json.loads((RES/'examples/worked_designs.json').read_text())
story=[p('Evaluating improvement in healthcare agents','title'),p('Design and reporting templates accompanying RSI-HA | Resource version 0.3.0 | Search cutoff 4 November 2026','sub'),p('Choose the question before choosing the control','head'),p('Memory contribution, generator contribution and a better improvement procedure are different questions. These templates preserve the review\'s existing concepts and task-native outcomes. They do not define a new score or a validated reporting standard. Verification status of the underlying extraction is documented in REVIEW_STATUS.md.','small')]
titles=['1. Does persistent memory help?','2. Does a changed generator or recipe help?','3. Does revising the improver improve later learning?']
for title,row in zip(titles,controls):
 story += [p(title,'head'),p('<b>Comparison.</b> '+clean(row['comparison'])),p('<b>Keep fixed or disclose.</b> '+clean(row['keep_fixed']),'small'),p('<b>Timing and independent tests.</b> '+clean(row['separation']),'small')]
story += [p('Complete the plan before execution','head'),p('Fill templates/experiment_plan.csv or .json. State the target claim, changed object, starting agent, treatment/control, task protocol, update/selection/test data, freeze point, feedback access, matching scope, native metrics, uncertainty procedure, cost boundary and version references. Configuration and metric choices remain with the study author.','small'),PageBreak()]

story += [p('Record the actual comparison','title'),p('Keep the plan, update history, resources and outcomes linked by stable design/run identifiers.','sub'),p('Separate three uses of data','head'),p('Updating changes the agent or its improvement components. Selection accepts a candidate or checkpoint. Testing estimates performance after those choices. Record when labels and outcomes become available, when memory is written, and the last decision before an untouched test. An online adaptation stream can allow between-case writeback, but should not be called an untouched final test.'),p('Make matching explicit','head'),p('List the quantities that are actually matched: initial learner/harness, data access, accepted-data volume, learner-training compute, generator/search compute, evaluation and total resources. Preserve mismatches rather than calling all of them "equal compute".','body'),table([
 ['File','What one record represents'],
 ['experiment_plan','One planned question, treatment/control design, data timeline, scope of matching and intended outcomes.'],
 ['run_log','One condition and repetition, its versions, input order, memory state, execution status and artifact/result links.'],
 ['update_log','One update candidate, its parent/new version, available feedback, selector/evaluator and acceptance/rejection decision.'],
 ['cost_log','One phase or source-summary condition, including failed/rejected candidates and original resource units.'],
 ['metric_results','One task-native outcome, its value/status, test role, aggregation and reported uncertainty.'],
 ],[100,435]),p('Worked cost example from ECG-RSI Table 10','head'),table([
 ['Condition','Candidates','Accepted','Rejected, derived'],
 ['Full method','16,193','10,000','6,193'],
 ['Frozen operators','36,723','10,000','26,723'],
 ['Frozen skills','22,398','10,000','12,398'],
 ],[190,115,115,115]),p('Accepted volume is equal; candidate-generation counts are unequal. Rejected counts are subtraction, not additional measurements. The example does not fill unavailable token, runtime or monetary costs with zero. Cost and outcome example rows are labelled reported_summary, not actual_run.','small'),p('Use missing-value statuses explicitly','head'),p('Distinguish measured/reported values, not_extracted, not_reported_in_examined_source, not_applicable and planned-but-unexecuted records. A missing value is not zero; a value absent from this extraction is not proof it was absent from the source paper. Preserve actual seeds, trials and failures without inventing them.','small'),PageBreak()]

labels=[('treatment','Treatment'),('control','Control'),('held_fixed','Held fixed'),('sequence_and_separation','Sequence and separation'),('matching_scope','Scope of matching'),('outcome_and_cost','Native outcomes and cost'),('supported_interpretation','What this comparison supports'),('boundary','Boundary')]
def case_block(row,title):
 out=[p(title,'head')]
 for key,label in labels:out.append(p('<b>'+label+'.</b> '+clean(row[key]),'small'))
 out.append(p('<link href="'+clean(row['source_url'])+'" color="#174e7d">Original source</link>, '+clean(row['source_version'])+'; '+clean(row['source_sections'])+'. Source locators are retained in worked_designs.json.','small'))
 return out
story += [p('Worked assessments from reported studies','title'),p('These are completed reconstructions of published/preprint designs. This project did not execute their experiments.','sub')]
story += case_block(cases[0],'A. PrivMeSA: persistent memory under a fixed procedure')
story += case_block(cases[1],'B. ECG-RSI: changing synthesis components')
story += [PageBreak(),p('Recipe change and the improver boundary','title'),p('Do not turn a selected-artifact improvement into evidence that the process of making future updates improved.','sub')]
story += case_block(cases[2],'C. ReVision3D: training-recipe comparison')
story += case_block(cases[3],'D. ReVision3D: a negative revised-improver assessment')
story += [p('Use the 85-study matrix and preserve attribution','head'),p('The matrix joins the approved review\'s levels, clinical settings, control descriptions, independent-test descriptions and original source locators without reclassification. Its author-check columns are blank. It includes existing contextual comparators and is not a list of 85 demonstrated RSI systems.','small'),p('Conceptual sources: Liu et al. (2026), <link href="https://doi.org/10.20944/preprints202608.0051.v1" color="#174e7d">component versus improver</link>; Han et al. (2026), <link href="https://arxiv.org/abs/2610.38266v1" color="#174e7d">level roles</link>; Pu et al. (2026), <link href="https://arxiv.org/abs/2610.35193v1" color="#174e7d">functional distinction</link>. Credit the primary studies for their methods/results and RSI-HA for this healthcare operationalization and resource.','small')]

def footer(c,d):
 c.setFont('Arial',7.5);c.drawString(30,20,'RSI-HA | Design templates | Version 0.3.0 | Review status in REVIEW_STATUS.md');c.drawRightString(A4[0]-30,20,str(d.page))
doc=SimpleDocTemplate(str(RES/'EVALUATION_DESIGN_TEMPLATE.pdf'),pagesize=A4,leftMargin=30,rightMargin=30,topMargin=30,bottomMargin=35,title='RSI-HA evaluation design templates',author='Dengzhe Hou et al.')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
with fitz.open(RES/'EVALUATION_DESIGN_TEMPLATE.pdf') as check:
 assert len(check)==4, f'Expected four designed pages, got {len(check)}'
print(RES/'EVALUATION_DESIGN_TEMPLATE.pdf')
