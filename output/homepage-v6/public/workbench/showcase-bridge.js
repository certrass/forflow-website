// Presentation controls call the same public actions used by the original workbench.
(()=>{
 const W=window.ForflowWorkbench,R=window.FFRuntime,L=window.FFLifecycle;
 const tour=new URLSearchParams(location.search).has('tour');
 const actions=[
  {at:2000,action:'lc:node:context',target:'[data-action="lc:node:context"]'},
  {at:5700,action:'lc:node:approval',target:'[data-action="lc:node:approval"]'},
  {at:8500,action:'lc:q2q:open',target:'[data-action="nav:knowledge"]'},
  {at:11000,action:'lc:q2q:prepare',target:'[data-action="lc:q2q:prepare"]'},
  {at:15500,action:'lc:q2q:review',target:'[data-action="lc:q2q:review"]'},
  {at:19500,check:true,target:'[data-q2q-field="scopeAccepted"]'},
  {at:21500,action:'lc:q2q:save-review',target:'[data-action="lc:q2q:save-review"]'},
  {at:26000,action:'lc:evaluate',target:'[data-action="lc:evaluate"]'},
  {at:32500,action:'lc:register',target:'[data-action="lc:register"]'},
  {at:37000,action:'lc:confirm-register',target:'[data-action="lc:confirm-register"]'},
  {at:41500,action:'lc:tab:assetTab:Evidence',target:'[data-action="lc:tab:assetTab:Evidence"]'},
 ];
 let index=-1,manual=false,revision=0,lastPointer=null;
 const post=data=>{if(window.parent!==window)parent.postMessage({scope:'forflow-source-workbench',...data},location.origin)};
 function summary(){return {page:W.state.page,tab:W.state.knowledgeTab,role:R.role,asset:L.state.releases[0]?.version||null,error:W.state.error||null}}
 function reset(){R.reset();L.reset();W.reset();W.action('role:admin');index=0;revision++;}
 function rect(selector){const el=document.querySelector(selector);if(!el)return null;const a=el.getBoundingClientRect();return {x:a.left+a.width/2,y:a.top+a.height/2,width:a.width,height:a.height};}
 function seek(time){
  if(!tour)return;
  const wasManual=manual;manual=false;const count=actions.filter(a=>a.at<=time).length;
  if(wasManual||index<0||count<index)reset();
  while(index<count){const e=actions[index];lastPointer=rect(e.target)||lastPointer;if(e.check){const box=document.querySelector(e.target);if(box&&!box.checked)box.click();}else W.action(e.action);index++;if(W.state.error){post({type:'error',message:W.state.error});return;}}
  const next=actions[index];const pointer=next?rect(next.target)||lastPointer:lastPointer;
  post({type:'frame',time,pointer,revision,...summary()});
 }
 function takeover(event){
  if(!event.isTrusted||manual||!event.target.closest('button,a,input,textarea,select,[data-action],[data-select-asset],[data-select-supplier],[role="button"]'))return;
  if(event.type==='keydown'&&['Tab','Escape','PageUp','PageDown'].includes(event.key))return;
  manual=true;post({type:'takeover',...summary()});
 }
 // Wait for an actual activation; pointerdown also starts ordinary touch scrolling.
 document.getElementById('app').addEventListener('click',takeover,true);
 document.getElementById('app').addEventListener('keydown',takeover,true);
 // A focused inner frame still lets the outer enlarged viewer close with Escape.
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!document.querySelector('[role="dialog"]'))post({type:'escape'});});
 addEventListener('message',e=>{if(e.origin!==location.origin||e.source!==parent||e.data?.scope!=='forflow-source-workbench')return;
  if(e.data.type==='seek'&&Number.isFinite(e.data.time))seek(Math.max(0,Math.min(46000,e.data.time)));
  if(e.data.type==='hello')post({type:'ready',...summary()});
 });
 if(tour)reset();post({type:'ready',...summary()});
})();
