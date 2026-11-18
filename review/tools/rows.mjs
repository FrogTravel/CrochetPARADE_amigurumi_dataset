// usage: node rows.mjs dsl_patterns.json out.json   (parses every pattern, emits per-row structure)
import {createParser} from './parser.mjs';
import fs from 'node:fs';
const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const only=process.argv[4];
const out={};
for(const [key,v] of Object.entries(data)){
  if(only&&key!==only)continue;
  const msgs=[];const p=createParser({log(){},warn(...a){msgs.push('W '+a.join(' '))},error(...a){msgs.push('E '+a.join(' '))}},m=>msgs.push('A '+m));
  const rec={confidence:v.confidence,msgs};out[key]=rec;
  let st;
  try{st=p.final(v.dsl);}catch(e){rec.error=String(e.message||e).slice(0,600);continue;}
  const idRow=new Map();const rows=[];
  for(const s of st){
    const r=s.nrow;rows[r]??={n:r,types:{},ids:[],chIds:[],targets:[],labels:[],seq:[],st:[]};
    const R=rows[r];R.types[s.type]=(R.types[s.type]||0)+1;
    for(const id of s.id){idRow.set(id,r);R.ids.push(id);if(s.type==='ch')R.chIds.push(id);}
    for(const t of s.id_attach)R.targets.push(t);
    if(s.label?.length)R.labels.push(...s.label);
    R.seq.push(s.type);const ex=!!(s.attach_ref!=null||Object.values(s.at_expr||{}).some(x=>x));R.st.push([s.type,s.id,s.id_attach,ex?1:0]);
  }
  rec.rows=rows.filter(Boolean).map(R=>{
    const tr={};for(const t of R.targets){const q=idRow.has(t)?idRow.get(t):'?';tr[q]=(tr[q]||0)+1;}
    return {n:R.n,types:R.types,made:R.ids.length,ch:R.chIds.length,first:R.ids[0],last:R.ids[R.ids.length-1],targets:R.targets,targetRows:tr,labels:R.labels,st:R.st};
  });
}
fs.writeFileSync(process.argv[3],JSON.stringify(out));
const ks=Object.keys(out);console.log('patterns',ks.length,'errors',ks.filter(k=>out[k].error).length,'withMsgs',ks.filter(k=>out[k].msgs.length).length);
