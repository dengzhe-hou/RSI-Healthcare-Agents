"""Build the site map from the released, unchanged evidence snapshot."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]
SNAP=ROOT/'resources/snapshots/2026-11-04'
GROUPS=[
 {'key':'memory','label':'Memory and experience','color':'#009e73'},
 {'key':'skills','label':'Skills and workflows','color':'#0072b2'},
 {'key':'generators','label':'Parameters and generators','color':'#d55e00'},
 {'key':'comparators','label':'Contextual comparators','color':'#62686d'},
]
LEVELS={'0':'Level 0','1':'Level 1','2-implicit':'Level 2 (implicit)','2-explicit':'Level 2 (explicit)'}
SETTINGS={'simulated':'Simulation','offline_benchmark':'Offline benchmark','retrospective':'Retrospective','external_retrospective':'External retrospective'}
evidence=json.loads((SNAP/'evidence_map.json').read_text())
design=json.loads((SNAP/'study_design_matrix.json').read_text())
by_key={p['key']:p for p in evidence}
assert len(evidence)==len(design)==85
assert set(by_key)=={p['key'] for p in design}
bibtext=(ROOT/'resources/references_mapped.bib').read_text()
bibs={}
for entry in re.split(r'(?m)(?=^@)',bibtext):
 m=re.match(r'@\w+\{([^,]+),',entry)
 if m:bibs[m[1]]=entry.strip()
assert set(by_key)<=set(bibs)
studies=[]
for row in design:
 p={**by_key[row['key']],**row}
 p['group_label']=p['mechanism_group_label']
 p['bibtex']=bibs[p['key']]
 p['search_text']=' '.join(str(v) for k,v in p.items() if k not in ['bibtex','source_locators','locators']).lower()
 assert p['mechanism_group'] in {g['key'] for g in GROUPS}
 assert p['evidence_level'] in LEVELS and p['clinical_evaluation_category'] in SETTINGS
 studies.append(p)
studies.sort(key=lambda p:(p['year'],p['name'].lower()))
out={'cutoff':'2026-11-04','resource_version':'0.3.2','groups':GROUPS,'levels':LEVELS,'settings':SETTINGS,'studies':studies}
(ROOT/'map').mkdir(exist_ok=True)
(ROOT/'map/data.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
lines=['# Study index','', 'The fixed 4 November 2026 snapshot contains 85 study records. Open the [interactive map](https://dengzhe-hou.github.io/rsi-healthcare-agents/map/) for full evidence fields and source locators.','', '| Study | Year | Mechanism | Evidence level | Evaluation |','| --- | --- | --- | --- | --- |']
for p in studies:
 name=p['name'].replace('|','/')
 lines.append(f"| [{name}]({p['source_url']}) | {p['year']} | {next(g['label'] for g in GROUPS if g['key']==p['mechanism_group'])} | {LEVELS[p['evidence_level']]} | {SETTINGS[p['clinical_evaluation_category']]} |")
(ROOT/'PAPERS.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'studies':len(studies),'groups':{g['key']:sum(p['mechanism_group']==g['key'] for p in studies) for g in GROUPS}}))
