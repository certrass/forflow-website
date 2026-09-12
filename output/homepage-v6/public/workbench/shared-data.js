(function(root){
  const models=[{id:'reasoning',name:'Reasoning model',color:'#4479bd',rate:17},{id:'fast',name:'Fast model',color:'#72ad90',rate:3},{id:'private',name:'Private endpoint',color:'#a391c8',rate:5},{id:'embedding',name:'Embedding model',color:'#e0af60',rate:1}];
  const workflows=[{id:'supplier',name:'Supplier renewal',owner:'Procurement',color:'#4479bd'},{id:'support',name:'Customer support',owner:'Service operations',color:'#72ad90'},{id:'knowledge',name:'Knowledge review',owner:'Knowledge team',color:'#a391c8'},{id:'contract',name:'Contract analysis',owner:'Legal operations',color:'#e0af60'}];
  const facts=[];let state=62171;function rand(){state=(Math.imul(state,1664525)+1013904223)>>>0;return state/4294967296;}
  for(let day=0;day<14;day++)for(let model=0;model<4;model++)for(let workflow=0;workflow<4;workflow++){
    const requests=Math.round((220+rand()*500)*(1+.3*Math.sin(day*.6+model))*(model===1?1.8:1)*(day>9&&workflow===0?1.35:1));
    const tokens=requests*Math.round(250+rand()*700),costCents=Math.round(tokens*models[model].rate/1000);
    facts.push({day,model,workflow,requests,tokens,costCents});
  }
  function aggregate(field='requests',group='model',byDay=false){const n=byDay?14:4,res=Array.from({length:n},()=>byDay?[0,0,0,0]:0);for(const f of facts){if(byDay)res[f.day][f[group]]+=f[field];else res[f[group]]+=f[field];}return res;}
  const assets=[{id:'supplier',name:'Supplier renewal',type:'Workflow',version:'2.1',owner:'Procurement',status:'Controlled use',objects:6,rules:12,tests:64},{id:'support',name:'Customer support',type:'Workflow',version:'1.4',owner:'Service operations',status:'Controlled use',objects:4,rules:8,tests:48},{id:'knowledge',name:'Knowledge review',type:'Workflow',version:'3.0',owner:'Knowledge team',status:'Review due',objects:5,rules:9,tests:56},{id:'contract',name:'Contract analysis',type:'Workflow',version:'1.8',owner:'Legal operations',status:'Controlled use',objects:7,rules:16,tests:72}];
  const dayLabel=i=>i<13?'Aug '+(19+i):'Sep 01';
  const api={seed:62171,provenance:'Deterministic illustrative data, not customer results or provider pricing.',models,workflows,facts,aggregate,assets,dayLabel,total:field=>facts.reduce((n,r)=>n+r[field],0)};
  if(typeof module!=='undefined')module.exports=api;root.ForFlowData=api;
})(typeof globalThis!=='undefined'?globalThis:this);
