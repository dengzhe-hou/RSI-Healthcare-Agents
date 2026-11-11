const examples=[
 {file:'medexpmem',name:'MedExpMem',kind:'Memory and experience',key:'feng2026medexpmem',copy:'Diagnostic errors become pairwise experience notes. An anatomical index helps later cases retrieve and filter relevant notes.',source:'https://arxiv.org/html/2605.22872v1#S2.F1'},
 {file:'macro',name:'MACRO',kind:'Skills and tools',key:'fan2026macro',copy:'Recurring fragments of verified tool trajectories become composite tools. The new action is retained alongside the primitive tool library.',source:'https://arxiv.org/html/2603.05860v1#S3.F2'},
 {file:'tissuelab',name:'TissueLab',kind:'Visual classifier updating',key:'coevolving2025',copy:'Experts review predictions and retain cell annotations as supervision. The classifier is updated and analysis is rerun for further review. The annotation interface depicts a different field of view from the prediction examples.',source:'https://arxiv.org/html/2509.20279v1'},
 {file:'diagagent',name:'DiagAgent',kind:'Diagnostic policy learning',key:'qiu2025diaggym',copy:'Diagnostic rollouts interact with a simulated environment. Diagnosis match, examination overlap and the turn limit provide rewards for policy updating.',source:'https://arxiv.org/html/2510.24654v2#S5.F7'},
 {file:'ecgrsi',name:'ECG-RSI',kind:'Training-generator refinement',key:'wang2026ecgrsi',copy:'A data factory edits waveforms, synthesizes questions and checks the results. Construction failures guide repairs to operators, prompts and skills.',source:'https://arxiv.org/html/2610.17718v1'},
 {file:'revision3d',name:'ReVision3D',kind:'Reading-pipeline revision',key:'lee2026revision3d',copy:'CT replay supports attribution of missed lesions. Revisions target acquisition, perception, training recipes or inference under a fixed development objective. The routing rule was formulated retrospectively.',source:'https://arxiv.org/html/2609.32984v2#S1.F1'}
];
document.querySelectorAll('[data-panel]').forEach(button=>button.addEventListener('click',()=>{
 const p=examples[Number(button.dataset.panel)];
 document.querySelectorAll('[data-panel]').forEach(b=>b.setAttribute('aria-selected',String(b===button)));
 document.querySelector('#mechanism-image').src='assets/panels/'+p.file+'.svg';
 document.querySelector('#mechanism-image').alt=p.name+' mechanism illustration';
 document.querySelector('#mechanism-zoom').href='assets/panels/'+p.file+'.svg';
 document.querySelector('#mechanism-name').textContent=p.name;document.querySelector('#mechanism-kind').textContent=p.kind;
 document.querySelector('#mechanism-copy').textContent=p.copy;document.querySelector('#mechanism-source').href=p.source;
 document.querySelector('#mechanism-map').href='map/#'+p.key;
}));
document.querySelector('#copy-citation').addEventListener('click',async e=>{
 const button=e.currentTarget;await navigator.clipboard.writeText(document.querySelector('#citation-text').textContent);button.textContent='Copied';
});
fetch('map/data.json').then(r=>{if(!r.ok)throw Error('Map data unavailable');return r.json()}).then(data=>{
 const svg=document.querySelector('#map-preview'),NS='http://www.w3.org/2000/svg';
 const groups=[['memory','Memory and experience','#009e73'],['skills','Skills and workflows','#0072b2'],['generators','Parameters and generators','#d55e00'],['comparators','Contextual comparators','#62686d']];
 groups.forEach(([key,label,color],j)=>{
  const x=35+(j%2)*550,y=35+Math.floor(j/2)*190,ps=data.studies.filter(p=>p.mechanism_group===key);
  const t=document.createElementNS(NS,'text');t.setAttribute('x',x);t.setAttribute('y',y);t.setAttribute('fill',color);t.setAttribute('font-size','17');t.setAttribute('font-weight','bold');t.textContent=label+'  '+ps.length;svg.append(t);
  ps.forEach((p,i)=>{const c=document.createElementNS(NS,'circle');c.setAttribute('cx',x+10+(i%10)*47);c.setAttribute('cy',y+35+Math.floor(i/10)*33);c.setAttribute('r','5');c.setAttribute('fill',color);const title=document.createElementNS(NS,'title');title.textContent=p.name;c.append(title);svg.append(c)});
 });
}).catch(()=>{document.querySelector('#map-preview').setAttribute('aria-label','Open the source-linked evidence map')});
