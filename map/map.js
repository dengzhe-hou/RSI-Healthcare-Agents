const $=s=>document.querySelector(s),NS='http://www.w3.org/2000/svg';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const state={data:null,selected:null,view:{x:0,y:0,w:1600,h:1000},mode:'map'};
function element(tag,attrs,text){const e=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);if(text)e.textContent=text;return e}
function matches(p){const q=$('#search').value.trim().toLowerCase();return (!$('#group').value||p.mechanism_group===$('#group').value)&&(!$('#level').value||p.evidence_level===$('#level').value)&&(!$('#setting').value||p.clinical_evaluation_category===$('#setting').value)&&(!$('#year').value||String(p.year)===$('#year').value)&&(!q||p.search_text.includes(q))}
function view(){const v=state.view;$('#map').setAttribute('viewBox',[v.x,v.y,v.w,v.h].join(' '))}
function fit(){state.view={x:0,y:0,w:1600,h:1000};view()}
function zoom(f,cx,cy){const v=state.view,r=$('#map').getBoundingClientRect(),fx=(cx??r.width/2)/r.width,fy=(cy??r.height/2)/r.height;const w=Math.max(380,Math.min(2400,v.w/f)),h=w/1.6;state.view={x:v.x+fx*(v.w-w),y:v.y+fy*(v.h-h),w,h};view()}
function visibleStudies(){return state.data.studies.filter(matches)}
function render(){
 const data=state.data,shown=visibleStudies(),svg=$('#map');svg.replaceChildren();$('#count').textContent=shown.length+' of '+data.studies.length+' studies';$('#empty').hidden=shown.length>0;
 data.groups.forEach((group,j)=>{
  const gx=20+(j%2)*800,gy=20+Math.floor(j/2)*490,all=data.studies.filter(p=>p.mechanism_group===group.key),n=all.filter(matches).length;
  svg.append(element('rect',{x:gx,y:gy,width:760,height:450,rx:15,fill:'#fff',stroke:'#d9e2db'}));
  svg.append(element('text',{x:gx+25,y:gy+36,fill:group.color,class:'cluster-title'},group.label));
  svg.append(element('text',{x:gx+25,y:gy+59,class:'cluster-sub'},n+' shown · '+all.length+' mapped'));
  all.forEach((p,i)=>{p.x=gx+43+(i%6)*120;p.y=gy+95+Math.floor(i/6)*48;if(!matches(p))return;
   const node=element('g',{class:'node'+(state.selected?.key===p.key?' selected':''),tabindex:0,role:'button','aria-label':p.name,'data-study':p.key});
   node.append(element('circle',{cx:p.x,cy:p.y,r:7,fill:group.color}));node.append(element('text',{x:p.x,y:p.y+20,'text-anchor':'middle'},p.name.length>18?p.name.slice(0,17)+'…':p.name));node.append(element('title',{},p.name+' · '+p.year));
   node.addEventListener('click',()=>select(p));node.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(p)}});svg.append(node);
  });
 });
 $('#paper-index').innerHTML=shown.map(p=>`<button class="paper-row" data-key="${esc(p.key)}"><strong>${esc(p.name)} <span>(${esc(p.year)})</span></strong><span>${esc(p.title)}</span><br><span>${esc(p.group_label)} · ${esc(data.levels[p.evidence_level])} · ${esc(data.settings[p.clinical_evaluation_category])}</span></button>`).join('')||'<p>No studies match. Clear a filter to see more.</p>';
 $('#paper-index').querySelectorAll('[data-key]').forEach(b=>b.addEventListener('click',()=>select(data.studies.find(p=>p.key===b.dataset.key))));
 view();
}
function select(p){
 state.selected=p;const data=state.data,group=data.groups.find(g=>g.key===p.mechanism_group),panel=$('#detail');
 const section=(heading,text)=>text?`<h3>${heading}</h3><p>${esc(text)}</p>`:'';
 panel.innerHTML=`<div class="detail-top"><span class="group-label" style="color:${group.color}">${esc(group.label)}</span><button class="close" aria-label="Close study details">×</button></div><h2>${esc(p.name)}</h2><p class="paper-title">${esc(p.title)}</p><p class="authors">${esc(p.authors.join(', '))} · ${esc(p.year)}</p><p class="status">${esc(p.publication_status)}${p.version?' · Examined '+esc(p.version):''}</p><div class="tags"><span>${esc(data.levels[p.evidence_level])}</span><span>${esc(data.settings[p.clinical_evaluation_category])}</span></div><a class="source-button" href="${esc(p.source_url)}" target="_blank" rel="noopener">Read the source ↗</a>${section('What changes',p.update_target)}${section('What stays fixed',p.fixed_components)}${section('Retained experience',p.retained_artifact)}${section('Feedback',p.feedback)}${section('Update timing',p.update_timing)}${section('Controls',p.control_description)}${section('Independent evaluation',p.independent_test_description)}${section('Evidence boundary',p.evidence_boundary)}<h3>Original source locators</h3><ul class="locators">${p.source_locators.map(l=>`<li><a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.location||l.url)} ↗</a></li>`).join('')}</ul><div class="record-actions"><button id="copy-link">Copy study link</button><button id="copy-bib">Copy BibTeX</button><button id="save-record">Download record</button></div>`;
 panel.hidden=false;panel.scrollTop=0;history.replaceState(null,'','#'+p.key);
 panel.querySelector('.close').addEventListener('click',close);
 $('#copy-link').addEventListener('click',async e=>{const button=e.currentTarget;await navigator.clipboard.writeText(location.href);button.textContent='Copied'});
 $('#copy-bib').addEventListener('click',async e=>{const button=e.currentTarget;await navigator.clipboard.writeText(p.bibtex);button.textContent='Copied'});
 $('#save-record').addEventListener('click',()=>{const record={...p};delete record.search_text;delete record.x;delete record.y;const url=URL.createObjectURL(new Blob([JSON.stringify(record,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=p.key+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});
 render();
}
function close(){state.selected=null;$('#detail').hidden=true;history.replaceState(null,'',location.pathname);render()}
function mode(value){state.mode=value;$('#map-stage').hidden=value!=='map';$('#paper-index').hidden=value!=='list';$('#view-map').setAttribute('aria-pressed',String(value==='map'));$('#view-list').setAttribute('aria-pressed',String(value==='list'))}
$('#filters').addEventListener('submit',e=>e.preventDefault());
['search','group','level','setting','year'].forEach(id=>$('#'+id).addEventListener(id==='search'?'input':'change',()=>{if(state.data)render()}));
$('#reset-filters').addEventListener('click',()=>{$('#filters').reset();fit();render()});
$('#view-map').addEventListener('click',()=>mode('map'));$('#view-list').addEventListener('click',()=>mode('list'));
$('#zoom-in').addEventListener('click',()=>zoom(1.4));$('#zoom-out').addEventListener('click',()=>zoom(1/1.4));$('#zoom-fit').addEventListener('click',fit);
$('#map').addEventListener('wheel',e=>{e.preventDefault();const r=e.currentTarget.getBoundingClientRect();zoom(Math.exp(-e.deltaY*.0015),e.clientX-r.left,e.clientY-r.top)},{passive:false});
let drag=null;$('#map').addEventListener('pointerdown',e=>{if(e.target.closest('.node')||e.button>0)return;drag={x:e.clientX,y:e.clientY,v:{...state.view}};e.currentTarget.setPointerCapture(e.pointerId)});
$('#map').addEventListener('pointermove',e=>{if(!drag)return;const r=e.currentTarget.getBoundingClientRect();state.view={...drag.v,x:drag.v.x-(e.clientX-drag.x)*drag.v.w/r.width,y:drag.v.y-(e.clientY-drag.y)*drag.v.h/r.height};view()});
$('#map').addEventListener('pointerup',()=>drag=null);$('#map').addEventListener('pointercancel',()=>drag=null);
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&state.selected)close()});
window.addEventListener('hashchange',()=>{
 if(!state.data)return;
 const p=state.data.studies.find(p=>p.key===decodeURIComponent(location.hash.slice(1)));
 if(p)select(p);else close();
});
fetch('data.json').then(r=>{if(!r.ok)throw Error('Evidence data unavailable');return r.json()}).then(data=>{
 state.data=data;
 const option=(select,value,label)=>{const o=document.createElement('option');o.value=value;o.textContent=label;select.append(o)};
 data.groups.forEach(g=>option($('#group'),g.key,g.label));Object.entries(data.levels).forEach(([k,v])=>option($('#level'),k,v));Object.entries(data.settings).forEach(([k,v])=>option($('#setting'),k,v));
 [...new Set(data.studies.map(p=>p.year))].sort().forEach(y=>option($('#year'),String(y),String(y)));
 render();if(matchMedia('(max-width:760px)').matches)mode('list');
 if(location.hash){const p=data.studies.find(p=>p.key===decodeURIComponent(location.hash.slice(1)));if(p)select(p)}
}).catch(e=>{$('#count').textContent='The evidence map could not load. Reload or open the downloadable records.';console.error(e)});
