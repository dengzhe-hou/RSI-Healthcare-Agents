"""Render the RSI-HA operational coding guide as a one-page, source-linked PDF."""
from pathlib import Path
import subprocess
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

RES = Path(__file__).resolve().parents[1]
for family, name in [('Arial', 'Arial'), ('Arial:style=Bold', 'ArialBold')]:
    path = subprocess.check_output(['fc-match','-f','%{file}',family], text=True).strip()
    pdfmetrics.registerFont(TTFont(name, path))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='ArialBold', italic='Arial', boldItalic='ArialBold')
styles={
 'title':ParagraphStyle('title',fontName='ArialBold',fontSize=17,leading=20,spaceAfter=5),
 'sub':ParagraphStyle('sub',fontName='Arial',fontSize=9,leading=12,textColor=colors.HexColor('#333333'),spaceAfter=9),
 'head':ParagraphStyle('head',fontName='ArialBold',fontSize=10,leading=12,spaceBefore=8,spaceAfter=4),
 'body':ParagraphStyle('body',fontName='Arial',fontSize=9,leading=11.5,spaceAfter=5),
 'cell':ParagraphStyle('cell',fontName='Arial',fontSize=8.4,leading=10.5,spaceAfter=0),
 'small':ParagraphStyle('small',fontName='Arial',fontSize=7.7,leading=9.6,spaceAfter=3),
}
def p(text, kind='body'):
    return Paragraph(text,styles[kind])

story=[p('RSI-HA evidence coding guide','title'),
       p('Operational rules for healthcare agent studies | Version 0.3.0 | Search cutoff 4 November 2026','sub'),
       p('<b>LLM-assisted extraction.</b> Verification status is documented in REVIEW_STATUS.md. Apply this guide to the examined source version. It operationalizes existing RSI concepts for this review and does not certify clinical readiness.','body'),
       p('1. Identify the changing object and its role','head'),
       p('Record what changes, what stays fixed, the feedback and retained artifact, and when updating, selection, freezing and testing occur. Ask whether the changed object executes the current task or produces later updates. Keep original section/table/page locators.'),
       p('2. Assign the highest level supported by the examined report','head')]
rows=[['Level','What the evidence shows']]
definitions=[
 ('0','Only current-case or session state changes. Static experience retrieval alone does not show newly learned cross-case memory.'),
 ('1','Memory, skills, tools, configuration or learner weights persist across different cases, under a fixed update procedure.'),
 ('2 explicit','A changed component explicitly constructs, selects or evaluates later training data, interactions, trajectories or recipes. The procedure admitting its changes stays fixed.'),
 ('2 implicit','The changing component has a documented update-producing or update-assessing role as well as a task role, but its update-related contribution is not isolated.'),
 ('3','The update-proposing, selection or evaluation procedure itself is revised, and its effect on subsequent learning is tested.'),
]
rows.extend([[a,b] for a,b in definitions])
t=Table([[p(x,'cell') for x in row] for row in rows],colWidths=[57,478],hAlign='LEFT')
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('FONTNAME',(0,0),(-1,0),'ArialBold'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eeeeee')),('LINEBELOW',(0,0),(-1,0),0.6,colors.black),('LINEBELOW',(0,1),(-1,-1),0.3,colors.HexColor('#bbbbbb')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
story += [t,Spacer(1,5),p('Merely executing tasks whose outputs are later mined is insufficient for Level 2. A Level 2 assignment does not itself establish causal benefit. A Level 3 claim requires testing later learning against the fixed procedure, with independent evaluation and data/compute matching reported.','small'),
 p('3. Keep mechanism, benefit and clinical evaluation separate','head'),
 p('Record publication status; controls for the changed component; and evaluation in simulation, offline benchmarks, retrospective records, external retrospective cohorts or prospective care. Code the study evaluation design separately from whether a patient service is operating. "Not reported" is a reporting gap, not proof of absence.'),
 p('4. Check the boundary examples as coded in this review','head')]
example_rows=[
 ('ClinicalAgents | L0','Static experience memory and changing within-case search do not establish new cross-case learning.','https://arxiv.org/html/2603.26182v2#S3.SS3.SSS2'),
 ('Agent Hospital | L1','Cases and principles accumulate while the reflection and validation procedure stays fixed.','https://arxiv.org/html/2405.02957v3#Sx3'),
 ('ECG-RSI | L2 explicit','Changed synthesis operators and skills create later training data. Frozen-component controls exist, with unequal generation-search costs.','https://arxiv.org/html/2610.17718v1#S5.T10'),
 ('SEMPA | L2 implicit','The changing Critic affects later update selection; its evolving evaluator contribution is not isolated.','https://aclanthology.org/2026.findings-emnlp.994.pdf#page=4'),
]
for name,meaning,url in example_rows:
    story.append(p('<b>'+escape(name)+'</b> '+escape(meaning)+' <link href="'+escape(url)+'" color="#174e7d">Source</link>.','small'))
story += [p('No mapped healthcare study reaches Level 3 or reports prospective clinical evaluation. These are the review\'s source-version-specific judgments; consult the full extraction and its limitations.','small'),
 p('Use the source-linked extraction and preserve attribution','head'),
 p('Start from the blank extraction template and field codebook. The four examples and 85-study map retain original source locators. Levels, causal benefit, clinical setting and publication status are separate fields; no aggregate quality score is assigned.','small'),
 p('Conceptual sources: Liu et al. (2026), <link href="https://doi.org/10.20944/preprints202608.0051.v1" color="#174e7d">component versus improver</link>; Han et al. (2026), <link href="https://arxiv.org/abs/2610.38266v1" color="#174e7d">L0-L3 roles</link>; Pu et al. (2026), <link href="https://arxiv.org/abs/2610.35193v1" color="#174e7d">functional distinction</link>. Cite those sources for their concepts and the RSI-HA manuscript for this healthcare map and operationalization.','small'),
 p('Use the companion evaluation-design templates for controls, phase separation and experiment records.','small'),
 p('<link href="https://dengzhe-hou.github.io/RSI-Healthcare-Agents/" color="#174e7d">dengzhe-hou.github.io/RSI-Healthcare-Agents</link>','small')]

def footer(canvas,doc):
    canvas.setFont('Arial',7.5)
    canvas.drawString(30,20,'Fixed snapshot 2026-11-04 | LLM-assisted extraction | Review status in REVIEW_STATUS.md')
    canvas.drawRightString(A4[0]-30,20,str(doc.page))

doc=SimpleDocTemplate(str(RES/'EVIDENCE_CODING_GUIDE.pdf'),pagesize=A4,rightMargin=30,leftMargin=30,topMargin=28,bottomMargin=33,title='RSI-HA evidence coding guide',author='Dengzhe Hou et al.')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
import fitz
with fitz.open(RES/'EVIDENCE_CODING_GUIDE.pdf') as check:
    assert len(check)==1, f'Expected one-page guide, got {len(check)} pages'
print(RES/'EVIDENCE_CODING_GUIDE.pdf')
