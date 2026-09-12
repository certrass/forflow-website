/* Local, deterministic workflow interpreter. No network, model inference or source writes. */
(()=>{
 const R=window.FFRuntime,D=window.FFData,KEY='forflow.lifecycle.v1',film=new URLSearchParams(location.search).has('film');
 const clone=x=>JSON.parse(JSON.stringify(x));
 const defaults={name:'Supplier renewal',owner:'Procurement operations',requireOwner:true,requireEvidence:true,routeExceptions:!film,riskLimit:70};
 const fresh=()=>({schema:1,config:clone(defaults),revision:1,runs:[],feedback:[],evaluations:[],releases:[],reuse:null,events:[]});
 let db=fresh();try{const saved=!film&&JSON.parse(window.FFShowcaseStorage.getItem(KEY)||'null');if(saved?.schema===1)db={...db,...saved}}catch{}
 let storageAvailable=true;const save=()=>{if(film)return;try{window.FFShowcaseStorage.setItem(KEY,JSON.stringify(db));storageAvailable=true}catch{storageAvailable=false}};
 const stamp=()=>film?'2026-09-06T10:00:00.000Z':new Date().toISOString();
 const allow=(...caps)=>{if(!caps.every(c=>R.can(c)))throw Error('This action requires '+caps.join(' and ')+' access. Switch to an authorized workspace role.');};
 const hash=x=>{let h=2166136261;for(const c of JSON.stringify(x)){h^=c.charCodeAt(0);h=Math.imul(h,16777619)}return (h>>>0).toString(16).padStart(8,'0')};
 const event=(action,resource,detail)=>{db.events.unshift({id:'EVT-'+String(db.events.length+1).padStart(4,'0'),action,resource,detail,actor:R.roles[R.role].name,at:stamp()});save()};
 const source=()=>{const s=D.suppliers.find(s=>s.id==='SUP-018'),c=R.contracts.find(c=>c.contract_id==='CTR-1042');return {supplierId:s.id,name:s.name,ownerTeam:s.owner,region:s.region,renewalStatus:s.status,contract:c.contract_id,revision:c.revision,requestId:'REQ-0261',termination:/termination|terminate/i.test(R.reviewSource.text),riskScore:32,evidence:!!c,expired:false,scope:'procurement'};};
 function interpret(input,c){
  if(input.scope!=='procurement')return {state:'blocked',route:'None',reason:'Object is outside the permitted procurement scope.'};
  if(c.requireEvidence&&(!input.evidence||!input.revision))return {state:'blocked',route:'Evidence review',reason:'A versioned contract is required before a renewal recommendation.'};
  if(c.requireOwner&&!input.ownerTeam)return {state:'blocked',route:'Ownership review',reason:'The supplier has no accountable business owner.'};
  if(input.expired)return {state:'blocked',route:'Contract review',reason:'The contract is expired; renewal requires a new agreement.'};
  if(input.riskScore>=c.riskLimit)return {state:'needs_review',route:'Risk committee',reason:'The risk score meets the configured escalation threshold.'};
  if(input.termination)return c.routeExceptions?{state:'needs_review',route:'Legal operations',reason:'Termination terms require a legal review before an owner can approve.'}:{state:'blocked',route:'Unassigned',reason:'Termination exception has no configured review route.'};
  return {state:'needs_review',route:'Procurement owner',reason:'Evidence is complete. A business owner must approve the proposed renewal.'};
 }
 const cases=(a=source())=>{return [
 ['TC-001','Termination clause',a,'needs_review','Legal operations'],
 ['TC-002','Standard renewal',{...a,termination:false},'needs_review','Procurement owner'],
 ['TC-003','Missing owner',{...a,ownerTeam:null},'blocked','Ownership review'],
 ['TC-004','Missing contract',{...a,evidence:false},'blocked','Evidence review'],
 ['TC-005','Unversioned evidence',{...a,revision:null},'blocked','Evidence review'],
 ['TC-006','Outside object scope',{...a,scope:'service'},'blocked','None'],
 ['TC-007','Elevated risk',{...a,riskScore:85},'needs_review','Risk committee'],
 ['TC-008','Expired contract',{...a,expired:true},'blocked','Contract review']
 ].map(([id,name,input,state,route])=>({id,name,input,expected:{state,route}}))};
 const fingerprint=()=>hash({engine:'renewal-1.0',config:db.config,source:source(),cases:cases().map(c=>({id:c.id,input:c.input,expected:c.expected})),feedback:db.feedback.map(f=>({id:f.id,run:f.run,note:f.note})),...(window.FFQ2Q?.fingerprint()?{q2q:window.FFQ2Q.fingerprint()}:{})});
 function execute(){allow('operate');const input=source(),config=clone(db.config),result=interpret(input,config);const id='FLOW-'+String(249+db.runs.length).padStart(4,'0');
  const run={id,at:stamp(),actor:R.roles[R.role].name,input,config,revision:db.revision,fingerprint:fingerprint(),result,sourceWrites:0,trace:[
   {name:'Receive renewal request',status:'Completed',input:{supplierId:input.supplierId,requestId:input.requestId,riskScore:input.riskScore},output:{objectType:'Supplier',objectVersion:'2.1'}},
   {name:'Resolve business context',status:'Completed',input:{source:'supplier_master',key:input.supplierId},output:{name:input.name,ownerTeam:input.ownerTeam,contract:input.contract,revision:input.revision}},
   {name:'Evaluate renewal rules',status:'Completed',input:{termination:input.termination,riskScore:input.riskScore,riskLimit:config.riskLimit},output:{state:result.state,route:result.route}},
   {name:'Request business approval',status:result.state==='blocked'?'Blocked':'Awaiting review',input:{ownerTeam:input.ownerTeam},output:{reason:result.reason,sourceWrites:0}}
  ]};db.runs.unshift(run);event('Workflow executed',id,result.reason);return clone(run);
 }
 function configure(p){allow('define');const keys=['name','owner','requireOwner','requireEvidence','routeExceptions','riskLimit'];const n={...db.config};for(const k of keys)if(Object.hasOwn(p,k))n[k]=p[k];
  if(typeof n.name!=='string'||n.name.trim().length<3)throw Error('Enter a workflow name with at least 3 characters.');
  if(!['Procurement operations','Legal operations','Platform team'].includes(n.owner))throw Error('Select an accountable team.');
  for(const k of ['requireOwner','requireEvidence','routeExceptions'])if(typeof n[k]!=='boolean')throw Error('Invalid rule configuration.');
  n.riskLimit=Number(n.riskLimit);if(!Number.isFinite(n.riskLimit)||n.riskLimit<1||n.riskLimit>100)throw Error('Risk threshold must be between 1 and 100.');
  if(JSON.stringify(n)!==JSON.stringify(db.config)){db.config=n;db.revision++;event('Workflow updated','WF-RENEWAL','Draft revision '+db.revision);}return clone(db.config);
 }
 function captureFeedback(runId,note){allow('operate');const run=db.runs.find(r=>r.id===runId);if(!run)throw Error('Select an existing run.');if(note.trim().length<16)throw Error('Explain the observed issue in at least 16 characters.');const old=db.feedback.find(f=>f.run===runId);if(old)throw Error('This run is already linked to '+old.id+'.');
  const f={id:'FB-'+String(db.feedback.length+1).padStart(4,'0'),run:run.id,note:note.trim(),source:clone(run.input),observed:clone(run.result),actor:R.roles[R.role].name,at:stamp(),status:'Open'};db.feedback.unshift(f);event('Feedback captured',f.id,run.id);return clone(f);
 }
 function evaluate(){allow('evaluate');const results=cases().map(c=>{const actual=interpret(c.input,db.config);return {...c,actual,passed:actual.state===c.expected.state&&actual.route===c.expected.route}});const ev={id:'EVAL-'+String(1001+db.evaluations.length),at:stamp(),actor:R.roles[R.role].name,fingerprint:fingerprint(),revision:db.revision,q2q:window.FFQ2Q?.evaluate(db.config)||null,results,passed:results.filter(r=>r.passed).length,total:results.length};db.evaluations.unshift(ev);event('Regression evaluated',ev.id,ev.passed+'/'+ev.total+' workflow checks'+(ev.q2q?' · Q2Q '+ev.q2q.passed+'/'+ev.q2q.total:'')+' passed');return clone(ev);}
 const evaluation=()=>db.evaluations[0]?{...clone(db.evaluations[0]),stale:db.evaluations[0].fingerprint!==fingerprint()}:null;
 function release(note){allow('maintain','review');const ev=evaluation();window.FFQ2Q?.assertRelease(ev);if(!db.feedback.length&&!window.FFQ2Q?.state.reference)throw Error('Review source content or link a runtime observation before registering this asset.');if(!ev||ev.stale||ev.passed!==ev.total)throw Error('Run all regression checks on the current revision before registering.');if(note.trim().length<16)throw Error('Record a release rationale in at least 16 characters.');if(db.releases.some(r=>r.fingerprint===ev.fingerprint))throw Error('This evaluated revision is already registered.');
  const a={id:'AI-RENEWAL',version:'1.'+db.releases.length+'.0',name:db.config.name+' · controlled review',config:clone(db.config),fingerprint:ev.fingerprint,evaluation:clone(ev),q2q:window.FFQ2Q?.packageSnapshot()||null,feedback:clone(db.feedback),owner:db.config.owner,reviewer:R.roles[R.role].name,note:note.trim(),at:stamp(),rights:{workflow:'Workspace reuse permitted',data:'Source records stay in their project',export:'Definition, rules and evaluation fixtures'},dependencies:[{name:'Supplier',version:'2.1',kind:'Object schema'},{name:'Contract',version:R.getAsset('Contract').version,kind:'Object schema'},{name:'Renewal interpreter',version:'1.0',kind:'Rule engine'}]};db.releases.unshift(a);db.feedback.forEach(f=>f.status='Included in '+a.version);event('AI asset registered',a.id+'@'+a.version,note);return clone(a);
 }
 const mappingDefaults={supplierId:'vendor_key',ownerTeam:'accountable_team',revision:'agreement_revision'};
 const targetFields=['vendor_key','accountable_team','agreement_revision','vendor_name','review_status'];
 const targetCases=()=>cases({supplierId:'VND-041',name:'Nordvale Service Parts',ownerTeam:'Aftermarket procurement',region:'Europe',renewalStatus:'Pending review',contract:'AGR-0307',revision:2,requestId:'REQ-SERVICE-004',termination:true,riskScore:38,evidence:true,expired:false,scope:'procurement'});
 const targetRows=()=>targetCases().map(c=>({caseId:c.id,vendor_key:c.input.supplierId,accountable_team:c.input.ownerTeam,agreement_revision:c.input.revision,vendor_name:c.input.name,review_status:c.input.renewalStatus,context:clone(c.input)}));
 const reuseFingerprint=()=>db.reuse?hash({asset:db.reuse.asset.fingerprint,mapping:db.reuse.mapping,scopeAccepted:db.reuse.scopeAccepted,rows:targetRows(),...(db.reuse.asset.q2q?{contentReview:db.reuse.contentReview||null}:{})}):null;
 function createReuse(version){allow('define');const asset=db.releases.find(a=>a.version===version);if(!asset)throw Error('Select a registered version.');if(db.reuse?.asset.version===version)return clone(db.reuse);if(db.reuse)throw Error('The target project already has an installation. Its pinned version cannot be silently replaced.');db.reuse={id:'REUSE-001',project:'Service parts procurement',asset:clone(asset),mapping:{supplierId:'vendor_key',ownerTeam:'',revision:'agreement_revision'},scopeAccepted:false,status:'Draft',evaluations:[],at:stamp()};event('Reuse draft created','REUSE-001',asset.id+'@'+version);return clone(db.reuse);}
 function configureReuse(mapping,scopeAccepted){allow('define');if(!db.reuse)throw Error('Create a reuse draft first.');if(db.reuse.status==='Active')throw Error('The activated installation is read-only.');for(const k of Object.keys(mappingDefaults))if(mapping[k]&&!targetFields.includes(mapping[k]))throw Error('Unknown target source field.');db.reuse.mapping=clone(mapping);db.reuse.scopeAccepted=!!scopeAccepted;event('Target mapping updated','REUSE-001','Compatibility checks must be rerun.');}
 function evaluateReuse(){allow('evaluate');const u=db.reuse;if(!u)throw Error('Create a reuse draft first.');const results=targetRows().map((row,i)=>{const input={...row.context,supplierId:row[u.mapping.supplierId],ownerTeam:row[u.mapping.ownerTeam],revision:row[u.mapping.revision]};const actual=interpret(input,u.asset.config),expected=cases()[i].expected;const binding=Object.entries(mappingDefaults).every(([k,v])=>u.mapping[k]===v);return {id:'MIG-'+String(i+1).padStart(3,'0'),name:cases()[i].name,passed:binding&&u.scopeAccepted&&actual.state===expected.state&&actual.route===expected.route,actual,expected,mappingValid:binding,scopeAccepted:u.scopeAccepted}});const e={q2q:window.FFQ2Q?.targetEvaluation(u)||null,id:'VERIFY-'+String(u.evaluations.length+1).padStart(3,'0'),fingerprint:reuseFingerprint(),passed:results.filter(r=>r.passed).length,total:results.length,results,at:stamp()};u.evaluations.unshift(e);event('Target evaluated',u.id,e.passed+'/'+e.total+' checks passed');return clone(e);}
 const reuseEvaluation=()=>{const e=db.reuse?.evaluations[0];return e?{...clone(e),stale:e.fingerprint!==reuseFingerprint()}:null;};
 function activate(){allow('maintain','review');const e=reuseEvaluation(),u=db.reuse;if(u?.asset.q2q&&(!e?.q2q?.ready||e.stale))throw Error('Review and verify the target project content before activation.');if(!e||e.stale||e.passed!==e.total)throw Error('Current target mappings, scope and all checks must pass before activation.');if(u.status==='Active')throw Error('This installation is already active.');u.status='Active';u.activatedAt=stamp();u.activatedBy=R.roles[R.role].name;event('Project installation activated',u.id,u.asset.id+'@'+u.asset.version);return clone(u);}
 function reviewTargetContent(p){allow('review','data');if(!db.reuse?.asset.q2q)throw Error('The installation has no Q2Q content requirement.');if(db.reuse.status==='Active')throw Error('An active installation is read-only.');db.reuse.contentReview=window.FFQ2Q.targetReview(p);event('Target content reviewed',db.reuse.id,'AGR-0307 / v2');return clone(db.reuse.contentReview);}
 function exportPackage(){allow('export');const sourceAsset=db.reuse?.asset||db.releases[0];if(!sourceAsset)throw Error('Register an asset first.');const a=clone(sourceAsset);
 if(a.q2q){a.q2q=window.FFQ2Q.portable(a.q2q);a.evaluation.q2q={...a.evaluation.q2q,checks:a.evaluation.q2q.checks.map(({id,name,passed})=>({id,name,passed}))};}
 a.feedback=a.feedback.map(f=>({id:f.id,run:f.run,status:f.status,at:f.at,sourceBinding:{object:'Supplier',contractRevision:f.source.revision}}));
 a.evaluation.results=a.evaluation.results.map(r=>({...r,input:{...r.input,supplierId:'fixture-supplier',name:'Example supplier',ownerTeam:r.input.ownerTeam?'Example owner':null,contract:'fixture-contract',region:'Example region'}}));
 const target=db.reuse?{id:db.reuse.id,project:db.reuse.project,status:db.reuse.status,sourceAsset:a.id,sourceVersion:a.version,mapping:clone(db.reuse.mapping),scopeAccepted:db.reuse.scopeAccepted,evaluations:clone(db.reuse.evaluations)}:null;
 return {format:'forflow.asset-package/1',asset:a,target,sourceRecordsIncluded:false,fixtures:'Synthetic acceptance examples; source record identities replaced.',executionBoundary:'Local rule interpreter; no model calls or external system writes.'};}

 window.FFLifecycle={get storageAvailable(){return storageAvailable},get state(){return clone(db)},get config(){return clone(db.config)},source,cases,interpret,fingerprint,configure,execute,captureFeedback,evaluate,evaluation,release,createReuse,configureReuse,evaluateReuse,reuseEvaluation,activate,reviewTargetContent,exportPackage,targetFields,targetRows,reset(){db=fresh();window.FFQ2Q?.reset();save()},can:(...caps)=>caps.every(c=>R.can(c))};
})();
