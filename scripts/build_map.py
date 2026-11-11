"""Rebuild the paper network and reading collection from the fixed public records.

Pass --manuscript to refresh the saved section/co-discussion index from LaTeX.
Ordinary rebuilds use map/survey_context.json and require only Python's stdlib.
Network edges mean co-citation within a review paragraph, never lineage.
"""
from pathlib import Path
from collections import defaultdict
import argparse, html, itertools, json, math, random, re

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / 'resources/snapshots/2026-11-04'
GROUPS = [
    dict(key='memory', label='Memory and experience', color='#009e73', x=300, y=260),
    dict(key='skills', label='Skills and workflows', color='#0072b2', x=900, y=260),
    dict(key='generators', label='Parameters and generators', color='#d55e00', x=850, y=650),
    dict(key='comparators', label='Contextual comparators', color='#62686d', x=290, y=650),
]
LEVELS = {'0':'Level 0', '1':'Level 1', '2-implicit':'Level 2 (implicit)', '2-explicit':'Level 2 (explicit)'}
SETTINGS = {'simulated':'Simulation', 'offline_benchmark':'Offline benchmark', 'retrospective':'Retrospective', 'external_retrospective':'External retrospective'}
EXAMPLES = ['feng2026medexpmem','fan2026macro','coevolving2025','qiu2025diaggym','wang2026ecgrsi','lee2026revision3d']

def plain(s):
    s = re.sub(r'(?m)(?<!\\)%.*$', '', s)
    for command,symbol in [('\\pm',' ± '),('\\leq',' ≤ '),('\\geq',' ≥ '),('\\times',' × '),('\\,',' ')]:
        s=s.replace(command,symbol)
    s = re.sub(r'\\(?:cite\w*|[Cc]ref|ref|label|nocite)(?:\[[^\]]*\])?\{[^}]*\}', '', s)
    s = re.sub(r'\\(?:textbf|textit|emph|textrm|mathrm|text)\{([^{}]*)\}', r'\1', s)
    s = s.replace('\\%', '%').replace('\\&','&').replace('~',' ').replace('---',' ').replace('--','–')
    s = re.sub(r'\\[A-Za-z]+\*?(?:\[[^\]]*\])?', '', s)
    return re.sub(r'\s+', ' ', s.replace('{','').replace('}','').replace('$','')).strip()

def build_context(path, keys):
    tex = path.read_text()
    tex = tex[tex.index('\\section{Introduction}'):]
    tex = tex.split('\\bibliographystyle')[0]
    tex = re.sub(r'(?m)(?<!\\)%.*$', '', tex)
    tex = re.sub(r'\\begin\{(figure\*?|table\*?|equation\*?|landscape)\}[\s\S]*?\\end\{\1\}', '\n\n', tex)
    tex = re.sub(r'\\nocite\{[^}]+\}', '', tex)
    parts = re.split(r'(\\(?:sub)*section\{[^}]+\})', tex)
    counters = [0,0,0]; sections=[]; paragraphs=[]; edge_sections=defaultdict(set)
    current=None
    for part in parts:
        m = re.fullmatch(r'\\((?:sub)*section)\{([^}]+)\}', part)
        if m:
            depth = {'section':0,'subsection':1,'subsubsection':2}[m[1]]
            counters[depth] += 1
            for i in range(depth+1,3): counters[i]=0
            number = '.'.join(str(x) for x in counters[:depth+1])
            current = dict(number=number, title=plain(m[2]), depth=depth, key='section-'+number.replace('.','-'))
            sections.append(current)
        elif current:
            for raw in re.split(r'\n\s*\n', part):
                cited = list(dict.fromkeys(k.strip() for m in re.finditer(r'\\cite\w*(?:\[[^\]]*\])?\{([^}]+)\}',raw) for k in m[1].split(',') if k.strip() in keys))
                if not cited: continue
                text=plain(raw)
                if not text: continue
                # One short, verbatim excerpt per cited paragraph. Full manuscript is not published here.
                excerpt = text if len(text)<=320 else text[:317].rsplit(' ',1)[0]+'…'
                marked=re.sub(r'\\cite\w*(?:\[[^\]]*\])?\{([^}]+)\}', lambda m:' '.join('@@'+k.strip()+'@@' for k in m[1].split(',')),raw)
                marked=re.sub(r'([.!?])\s*((?:@@[^@]+@@\s*)+)',r' \2\1 ',marked)
                sentences=re.split(r'(?<=[.!?])\s+',plain(marked))
                excerpts={}
                for key in cited:
                    sentence=' '.join(re.sub(r'@@[^@]+@@','',s).strip() for s in sentences if '@@'+key+'@@' in s)
                    sentence=re.sub(r'\s+([.!?,])',r'\1',re.sub(r'\s+',' ',sentence)).strip()
                    excerpts[key]=sentence if len(sentence)<=500 else sentence[:497].rsplit(' ',1)[0]+'…'
                paragraphs.append(dict(id='p'+str(len(paragraphs)+1), section=current['number'], section_title=current['title'], section_key=current['key'], keys=cited, excerpt=excerpt,excerpts=excerpts))
                for a,b in itertools.combinations(sorted(cited),2): edge_sections[(a,b)].add(current['number'])
    return dict(source='Current author-revision manuscript, 12 November 2026', relation='Cited together in a review paragraph', sections=sections, paragraphs=paragraphs,
                edges=[dict(source=a,target=b,sections=sorted(v)) for (a,b),v in sorted(edge_sections.items())])

def positions(studies, edges):
    # Navigation layout. Categories supply anchors; co-discussion gently draws neighbors together.
    nodes={}; anchors={g['key']:(g['x'],g['y']) for g in GROUPS}
    for g in GROUPS:
        items=[p for p in studies if p['mechanism_group']==g['key']]
        rx,ry={'memory':(250,180),'skills':(220,175),'generators':(210,120),'comparators':(165,100)}[g['key']]
        for i,p in enumerate(items):
            r=math.sqrt((i+.7)/len(items)); t=i*2.39996323
            nodes[p['key']]=[g['x']+rx*r*math.cos(t),g['y']+ry*r*math.sin(t)]
    pairs=list(itertools.combinations(studies,2))
    for step in range(650):
        force={p['key']:[0.,0.] for p in studies}
        for p in studies:
            k=p['key'];x,y=nodes[k];a,b=anchors[p['mechanism_group']]
            attraction=.004 if step<550 else 0
            force[k][0]+=(a-x)*attraction;force[k][1]+=(b-y)*attraction
        for e in edges:
            a,b=e['source'],e['target'];dx=nodes[b][0]-nodes[a][0];dy=nodes[b][1]-nodes[a][1]
            if step<550 and math.hypot(dx,dy)>170:
                force[a][0]+=dx*.00012;force[a][1]+=dy*.00012;force[b][0]-=dx*.00012;force[b][1]-=dy*.00012
        for p,q in pairs:
            a,b=p['key'],q['key'];dx=nodes[b][0]-nodes[a][0];dy=nodes[b][1]-nodes[a][1]
            # Collision boxes include the right-aligned label, not just its node.
            wa=min(25,len(p['short_name']))*7.2+24;wb=min(25,len(q['short_name']))*7.2+24
            ca=nodes[a][0]+wa/2;cb=nodes[b][0]+wb/2
            ox=(wa+wb)/2-abs(cb-ca);oy=29-abs(dy)
            if ox>0 and oy>0:
                if ox<oy*2.5:
                    push=(ox+1)*.32;sgn=1 if cb>ca else -1
                    force[a][0]-=push*sgn;force[b][0]+=push*sgn
                else:
                    push=(oy+1)*.34;sgn=1 if dy>0 else -1
                    force[a][1]-=push*sgn;force[b][1]+=push*sgn
            distance=max(.1,math.hypot(dx,dy))
            if distance<58 and step<550:
                push=(58-distance)*.045
                force[a][0]-=dx/distance*push;force[b][0]+=dx/distance*push
                force[a][1]-=dy/distance*push;force[b][1]+=dy/distance*push
        rate=.6 if step<550 else .4
        for k,v in force.items():
            nodes[k][0]=max(85,min(1110,nodes[k][0]+max(-9,min(9,v[0]))*rate))
            nodes[k][1]=max(90,min(790,nodes[k][1]+max(-9,min(9,v[1]))*rate))
    return {k:[round(x,2),round(y,2)] for k,(x,y) in nodes.items()}

def bibfield(entry,name):
    m=re.search(r'\b'+name+r'\s*=\s*\{',entry,re.I)
    if not m:return ''
    depth=1;i=m.end();start=i
    while i<len(entry) and depth:
        if entry[i]=='{':depth+=1
        if entry[i]=='}':depth-=1
        i+=1
    return plain(entry[start:i-1])

def md(s):return str(s).replace('|','/').replace('\n',' ')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--manuscript',type=Path);args=parser.parse_args()
    evidence=json.loads((SNAP/'evidence_map.json').read_text());design=json.loads((SNAP/'study_design_matrix.json').read_text())
    summaries={x['key']:x for x in json.loads((SNAP/'mechanism_summaries.json').read_text())}
    by_key={p['key']:p for p in evidence};assert len(evidence)==len(design)==85
    assert set(by_key)=={p['key'] for p in design}
    bibs={}
    for entry in re.split(r'(?m)(?=^@)',(ROOT/'resources/references_mapped.bib').read_text()):
        m=re.match(r'@\w+\{([^,]+),',entry)
        if m:bibs[m[1]]=entry.strip()
    assert set(by_key)<=set(bibs)
    context_path=ROOT/'map/survey_context.json'
    if args.manuscript:context_path.write_text(json.dumps(build_context(args.manuscript,set(by_key)),ensure_ascii=False,indent=2)+'\n')
    context=json.loads(context_path.read_text())
    studies=[]
    for row in design:
        p={**by_key[row['key']],**row};p['group_label']=p['mechanism_group_label'];p['bibtex']=bibs[p['key']]
        p['summary']=summaries[p['key']];p['short_name']=p['name'].split(' / ')[0]
        p['venue']=bibfield(p['bibtex'],'journal') or bibfield(p['bibtex'],'booktitle') or 'Preprint / report'
        p['survey_passages']=[x['id'] for x in context['paragraphs'] if p['key'] in x['keys']]
        p['sections']=list(dict.fromkeys(x['section'] for x in context['paragraphs'] if p['key'] in x['keys']))
        p['search_text']=' '.join(str(v) for k,v in p.items() if k not in ['bibtex','source_locators','locators']).lower()
        assert p['mechanism_group'] in {g['key'] for g in GROUPS}
        assert p['evidence_level'] in LEVELS and p['clinical_evaluation_category'] in SETTINGS
        studies.append(p)
    studies.sort(key=lambda p:(p['year'],p['name'].lower()))
    layout=positions(studies,context['edges'])
    for p in studies:p['x'],p['y']=layout[p['key']]
    out=dict(cutoff='2026-11-04',resource_version='0.3.2',groups=GROUPS,levels=LEVELS,settings=SETTINGS,studies=studies,edges=context['edges'],sections=context['sections'],passages=context['paragraphs'],examples=EXAMPLES)
    (ROOT/'map/data.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    lines=['# Healthcare agent self-improvement paper collection','',
       '[Homepage](https://dengzhe-hou.github.io/rsi-healthcare-agents/) · [Interactive network](https://dengzhe-hou.github.io/rsi-healthcare-agents/map/) · [Evidence and templates](resources/) · [85 BibTeX entries](resources/references_mapped.bib)','',
       'This reading collection accompanies *A Survey on Recursive Self-Improvement in Healthcare AI Agents*. All 85 records come from the fixed 4 November 2026 snapshot. The groups and evidence codes are unchanged.','',
       '## Contents','']
    for g in GROUPS:lines.append(f"- [{g['label']}](#{g['key']}) ({sum(p['mechanism_group']==g['key'] for p in studies)} studies)")
    lines+=['','## Start here','', 'Six studies illustrated in the survey. The rows identify concrete update objects and evaluation designs, rather than rank methods.','',
       '| Study | Retained change and fixed components | Evaluation | Source and record |','| --- | --- | --- | --- |']
    for key in EXAMPLES:
        p=next(x for x in studies if x['key']==key)
        lines.append(f"| **{md(p['name'])}** | {md(p['summary']['changes_fixed'])} | {md(p['summary']['evaluation'])} | [Paper]({p['source_url']}) · [Evidence](https://dengzhe-hou.github.io/rsi-healthcare-agents/map/#{p['key']}) |")
    for g in GROUPS:
        lines+=['',f'<a id="{g["key"]}"></a>',f'## {g["label"]}','',
            '| Paper | Year / venue in bibliography | What changes | Evaluation |','| --- | --- | --- | --- |']
        for p in sorted((p for p in studies if p['mechanism_group']==g['key']),key=lambda p:(-p['year'],p['name'].lower())):
            lines.append(f"| **[{md(p['name'])}]({p['source_url']})**<br>{md(p['title'])}<br>[Evidence record](https://dengzhe-hou.github.io/rsi-healthcare-agents/map/#{p['key']}) | {p['year']}<br>{md(p['venue'])} | {md(p['summary']['changes_fixed'])} | {md(p['summary']['evaluation'])} |")
    lines+=['','## Reading the records','', 'Each network record includes the update target, retained artifact, fixed components, feedback, controls, independent tests and original source locators. Network edges mean that two mapped studies are cited in the same paragraph of the current review. They do not denote a citation from one primary paper to another.','',
        'Publication and study-evaluation information is reported as recorded at the snapshot, not continuously re-verified. See [review status](resources/REVIEW_STATUS.md), [coding guide](resources/EVIDENCE_CODING_GUIDE.md) and [contribution instructions](CONTRIBUTING.md).']
    (ROOT/'PAPERS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(dict(studies=len(studies),edges=len(context['edges']),passages=len(context['paragraphs']),with_context=sum(bool(p['sections']) for p in studies))))

if __name__=='__main__':main()
