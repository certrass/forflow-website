/* Q2Q acceptance evidence for the local renewal interpreter.
   Processing output, human reference labels and evaluation results remain separate. */
(()=>{
 const R=window.FFRuntime,L=window.FFLifecycle,KEY='forflow.q2q.v1';
 const clone=x=>JSON.parse(JSON.stringify(x)),film=new URLSearchParams(location.search).has('film');
 const hash=x=>{let h=2166136261;for(const c of JSON.stringify(x)){h^=c.charCodeAt(0);h=Math.imul(h,16777619)}return(h>>>0).toString(16).padStart(8,'0')};
 const fresh=()=>({schema:1,active:false,processor:'1.1',document:null,candidate:null,reference:null,reviews:[],events:[]});
 let db=fresh();try{const x=!film&&JSON.parse(window.FFShowcaseStorage.getItem(KEY)||'null');if(x?.schema===1)db={...db,...x}}catch{}
 const time=()=>film?'2026-09-06T10:00:00.000Z':new Date().toISOString();
 const save=()=>{if(!film)window.FFShowcaseStorage.setItem(KEY,JSON.stringify(db))};
 const event=(action,detail)=>{db.events.unshift({action,detail,actor:R.roles[R.role].name,at:time()});save()};
 const allow=(...caps)=>caps.forEach(c=>R.requireCap(c));
 function source(){const s=R.reviewSource,c=R.contracts.find(c=>c.contract_id===s.contract);return {id:s.contract,revision:s.revision,clause:s.clause,text:s.text,supplier:s.supplier,registryRevision:c?.revision,registrySupplier:c?.supplier_id,scope:'procurement',rights:'Workspace evaluation only'}}
 const validSource=s=>s.revision===s.registryRevision&&s.supplier===s.registrySupplier;
 const sameSource=()=>db.document&&validSource(source())&&hash(db.document)===hash(source());
 function extract(doc,version){return {termination:/termination|terminate/i.test(doc.text),ownerApproval:version==='1.0'?/owner approval/i.test(doc.text):/require review by the accountable procurement owner/i.test(doc.text),quote:doc.text,clause:doc.clause}}
 function process(version=db.processor){allow('define','data');if(!['1.0','1.1'].includes(version))throw Error('Select a supported content processor.');const doc=source();if(!validSource(doc))throw Error('Contract registry and source revision disagree. Resolve the evidence gap first.');if(db.document&&hash(db.document)!==hash(doc))db.reference=null;
  db.active=true;db.processor=version;db.document=clone(doc);db.candidate={id:'CONTENT-001',processor:'Clause parser / '+version,at:time(),sourceHash:hash(doc),fields:extract(doc,version)};event('Content processed','CONTENT-001 · parser '+version+' · '+doc.id+' / v'+doc.revision);return clone(db.candidate);
 }
 function review(p){allow('review','data');if(!db.candidate||!sameSource())throw Error('Process the current source revision before reviewing.');if(!['Approved','Rejected','Needs evidence'].includes(p.decision))throw Error('Choose a review decision.');if(typeof p.reason!=='string'||p.reason.trim().length<16)throw Error('Record the evidence and reasoning in at least 16 characters.');
  const base={id:'Q2Q-'+String(db.reviews.length+1).padStart(4,'0'),decision:p.decision,reason:p.reason.trim(),actor:R.roles[R.role].name,at:time(),sourceHash:hash(db.document),candidate:clone(db.candidate)};
  if(p.decision==='Approved'){
   if(p.scopeAccepted!==true)throw Error('Confirm the task boundary and workspace evaluation rights.');
   if(typeof p.termination!=='boolean'||typeof p.ownerApproval!=='boolean')throw Error('Confirm both content labels.');
   if(!['Legal operations','Procurement owner'].includes(p.route))throw Error('Select the expected review route.');
   if(!p.quote||!db.document.text.includes(p.quote)||p.quote.trim().length<24)throw Error('Cite a passage from the versioned source, at least 24 characters long.');
   if(typeof p.boundary!=='string'||p.boundary.trim().length<16)throw Error('Explain the exception boundary or a counterexample in at least 16 characters.');
   base.reference={id:'Q2Q-CASE-001',version:db.reviews.filter(x=>x.reference).length+1,source:clone(db.document),expected:{termination:p.termination,ownerApproval:p.ownerApproval,quote:p.quote,clause:db.document.clause,state:'needs_review',route:p.route,sourceWrites:0},boundary:p.boundary.trim(),rights:'Workspace evaluation only'};
   base.delta=['termination','ownerApproval'].filter(k=>db.candidate.fields[k]!==base.reference.expected[k]).map(k=>({field:k,proposed:db.candidate.fields[k],reviewed:base.reference.expected[k]}));
   db.reference=clone({...base.reference,reviewId:base.id,reviewer:base.actor,reason:base.reason,approvedAt:base.at});
  }else db.reference=null;
  db.reviews.unshift(base);event('Q2Q '+p.decision.toLowerCase(),base.id+' · '+base.reason);return clone(base);
 }
 const fingerprint=()=>db.active?hash({document:db.document,current:source(),candidate:db.candidate,reference:db.reference,review:db.reviews[0]?.id}):null;
 const status=()=>!db.active?'Not prepared':!sameSource()?'Source changed':db.reference?'Approved':db.reviews[0]?.decision||'Needs review';
 function evaluate(config){if(!db.active)return null;const c=db.candidate,ref=db.reference,expected=ref?.expected,src=source(),before=hash(window.FFData.suppliers);
  const input={...L.source(),termination:c?.fields.termination},actual=L.interpret(input,config),writes=before===hash(window.FFData.suppliers)?0:1;
  const checks=[
   {id:'Q2Q-201',name:'Reviewed source & scope',expected:'Current source + approved case',actual:status(),passed:!!ref&&!!sameSource()},
   {id:'Q2Q-202',name:'Content extraction',expected:expected?{termination:expected.termination,ownerApproval:expected.ownerApproval}:'Reviewed labels required',actual:c?.fields?{termination:c.fields.termination,ownerApproval:c.fields.ownerApproval}:null,passed:!!ref&&['termination','ownerApproval'].every(k=>c?.fields[k]===expected[k])},
   {id:'Q2Q-203',name:'Evidence citation',expected:expected?{quote:expected.quote,clause:expected.clause}:'Reviewed citation required',actual:c?{quote:c.fields.quote,clause:c.fields.clause}:null,passed:!!ref&&!!sameSource()&&src.text.includes(c.fields.quote)&&c.fields.quote.includes(expected.quote)&&c.fields.clause===expected.clause},
   {id:'Q2Q-204',name:'Decision & review route',expected:expected?{state:expected.state,route:expected.route}:'Reviewed route required',actual:{state:actual.state,route:actual.route},passed:!!ref&&actual.state===expected.state&&actual.route===expected.route},
   {id:'Q2Q-205',name:'Read-only action boundary',expected:{sourceWrites:0,approvalRequired:true},actual:{sourceWrites:writes,approvalRequired:actual.state==='needs_review'||actual.state==='blocked'},passed:writes===0&&['needs_review','blocked'].includes(actual.state)}
  ];
  return {id:'Q2Q-CASE-001',fingerprint:fingerprint(),processor:c?.processor,reviewId:ref?.reviewId||null,referenceVersion:ref?.version||null,sourceRevision:db.document?.revision,checks,passed:checks.filter(x=>x.passed).length,total:checks.length,ready:checks.every(x=>x.passed)&&status()==='Approved'};
 }
 function assertRelease(e){if(db.active&&(!e?.q2q?.ready||e.q2q.fingerprint!==fingerprint()))throw Error('Q2Q requires an approved reference and a current passing content evaluation.');}
 const packageSnapshot=()=>db.active?clone({reference:db.reference,review:db.reviews.find(r=>r.id===db.reference?.reviewId),processor:db.candidate?.processor,fingerprint:fingerprint()}):null;
 function portable(snapshot){return snapshot?{caseId:snapshot.reference?.id,version:snapshot.reference?.version,reviewId:snapshot.reference?.reviewId,processor:snapshot.processor,checks:['Source integrity','Content extraction','Evidence citation','Decision routing','Action boundary'],requiresTargetReview:true,sourceContentIncluded:false}:null;}
 const targetSource=()=>({id:'AGR-0307',revision:2,clause:'4.2',text:'Termination and renewal changes require review by the accountable procurement owner before a supplier status update can be authorized.',scope:'procurement',rights:'Target workspace evaluation only'});
 function targetEvaluation(u){if(!u?.asset.q2q)return null;const doc=targetSource(),version=u.asset.q2q.processor.split(' / ')[1],actual=extract(doc,version),ref=u.contentReview;
  const checks=[{id:'Q2Q-T01',name:'Target content approved',passed:!!ref&&ref.sourceHash===hash(doc)},
   {id:'Q2Q-T02',name:'Target approval clause extracted',passed:!!ref&&actual.ownerApproval===ref.expected.ownerApproval&&actual.termination===ref.expected.termination},
   {id:'Q2Q-T03',name:'Target citation retained',passed:actual.quote===doc.text&&actual.clause===doc.clause}];
  return {checks,passed:checks.filter(c=>c.passed).length,total:checks.length,ready:checks.every(c=>c.passed)};
 }
 function targetReview(p){allow('review','data');if(p.confirmed!==true)throw Error('Confirm the target content and owner approval requirement.');if(!p.reason||p.reason.trim().length<16)throw Error('Explain the target review in at least 16 characters.');return {sourceHash:hash(targetSource()),sourceId:'AGR-0307',sourceRevision:2,expected:{termination:true,ownerApproval:true},actor:R.roles[R.role].name,at:time(),reason:p.reason.trim()};}
 window.FFQ2Q={get state(){return clone(db)},source,process,review,extract,fingerprint,status,evaluate,assertRelease,packageSnapshot,portable,targetSource,targetReview,targetEvaluation,reset(){db=fresh();save()}};
})();
