import test from 'node:test';
import assert from 'node:assert/strict';
import {createWorkspace,workspaceAction,visibleRecords,restoreWorkspace,tourWorkspace,answerFor} from '../src/workspace-state.js';
const first=s=>s.records[0];
const apply=(s,a)=>workspaceAction(s,{...a,time:'10:30'});
test('review requires an opinion; missing evidence cannot be confirmed; double submit is idempotent',()=>{
 let s=createWorkspace();assert.equal(apply(s,{type:'review'}),s);
 s=apply(s,{type:'draft'});s=apply(s,{type:'review'});assert.equal(first(s).reviewed,true);assert.equal(first(s).followUp.owner,'transport');
 assert.equal(apply(s,{type:'review'}),s);
 s=apply(s,{type:'select',id:s.records[1].id});s=apply(s,{type:'edit',field:'reviewDraft',value:'材料缺失'});assert.equal(apply(s,{type:'review'}),s);
});
test('review, owner, due time, discussion, and history survive serialization and do not affect another record',()=>{
 let s=createWorkspace(),other=structuredClone(s.records[1]);
 for(const action of [{type:'draft'},{type:'edit',field:'reviewDraft',value:'已人工核对，要求反馈差异原因。'},{type:'edit',field:'taskOwner',value:'finance'},{type:'edit',field:'taskDue',value:'17:30'},{type:'review'},{type:'task-status',status:'progress'},{type:'comment',text:'请补充处理结果。'},{type:'task-status',status:'done'}])s=apply(s,action);
 assert.deepEqual(s.records[1],other);assert.equal(first(s).followUp.owner,'finance');assert.equal(first(s).followUp.due,'17:30');assert.equal(first(s).followUp.status,'done');assert.equal(first(s).followUp.comments[0].text,'请补充处理结果。');assert.equal(first(s).note,'已人工核对，要求反馈差异原因。');assert.equal(first(s).activity.at(-1).time,'10:30');assert.deepEqual(restoreWorkspace(JSON.stringify(s)),s);
});
test('search, status filters, and assignee filters intersect with updated review state',()=>{
 let s=createWorkspace();assert.equal(visibleRecords(s,'','review').length,4);assert.equal(visibleRecords(s,'','missing').length,2);assert.equal(visibleRecords(s,'T-260906-024').length,1);assert.equal(visibleRecords(s,'not-found').length,0);assert.equal(visibleRecords(s,'杭州','missing','transport').length,1);
 s=apply(apply(s,{type:'draft'}),{type:'review'});assert.equal(visibleRecords(s,'','review').length,3);assert.equal(visibleRecords(s,'','complete').length,7);
});
test('task cannot complete without a recorded response; comments cannot post before task creation',()=>{
 let s=createWorkspace();assert.equal(apply(s,{type:'comment',text:'结果'}),s);s=apply(s,{type:'create-task'});assert.equal(apply(s,{type:'task-status',status:'done'}),s);assert.equal(apply(s,{type:'comment',text:'  '}),s);
});
test('AI responses stay with their original record even after selection changes',()=>{
 let s=createWorkspace(),id=first(s).id;s=apply(s,{type:'ai-request',id,text:'生成复核意见'});s=apply(s,{type:'select',id:s.records[1].id});s=apply(s,{type:'ai-response',id,...answerFor(first(s),'生成复核意见')});assert.ok(first(s).reviewDraft);assert.equal(s.records[1].reviewDraft,'');assert.equal(s.records[1].thread.length,2);assert.equal(first(s).thread.length,4);
});
test('tour snapshots use the same validation transitions and cannot mutate a manual session',()=>{
 let s=createWorkspace();s=apply(s,{type:'edit',field:'reviewDraft',value:'我的意见'});const before=JSON.stringify(s),tour=tourWorkspace(32000);assert.equal(first(tour).reviewed,true);assert.equal(first(tour).followUp.comments.length,1);assert.equal(JSON.stringify(s),before);assert.equal(first(tourWorkspace(9000)).reviewed,false);assert.equal(tourWorkspace(9000).view,'sources');assert.equal(first(tourWorkspace(1000)).thread.length,0);
});
test('invalid old storage fails closed',()=>{assert.equal(restoreWorkspace('bad json'),null);assert.equal(restoreWorkspace('{"version":1}'),null);});
