import {initialRecords, owners, recordFiles, recordCategory} from './q2q-records.js';
import {analysisFor} from './q2q-analysis.js';

export const STORAGE_KEY = 'forflow-workspace-v2';
const ownerName = id => owners.find(o => o.id === id)?.name || '业务复核人';
export const timeNow = () => new Intl.DateTimeFormat('zh-CN', {hour:'2-digit', minute:'2-digit', hour12:false}).format(new Date());
export function createWorkspace() {
  return {version:2, selected:initialRecords[0].id, view:'overview', source:'receipt', records:initialRecords.map(r => ({...r,
    reviewDraft:r.note, taskOwner:analysisFor(r).owner, taskDue:'16:00', commentDraft:'', composer:'',
    thread:[{role:'user', text:'核对这笔运输单据，把需要处理的差异整理出来。'}, {role:'assistant', text:analysisFor(r).finding, artifact:true}],
    activity:[{title:'业务材料已关联', detail:`${recordFiles(r).length} 份材料 · 运输单号 ${r.id}`, time:'09:12'}, {title:'跨单据核验完成', detail:analysisFor(r).title+' · 规则 '+r.rule, time:'09:14'}],
  }))};
}
export function restoreWorkspace(raw) {
  try {
    const data=JSON.parse(raw);
    if(data?.version!==2 || !Array.isArray(data.records) || data.records.length!==initialRecords.length || !data.records.some(r=>r.id===data.selected)) return null;
    if(!data.records.every(r=>initialRecords.some(i=>i.id===r.id) && Array.isArray(r.thread) && Array.isArray(r.activity) && typeof r.reviewDraft==='string')) return null;
    return data;
  } catch {return null;}
}
export function visibleRecords(state, query='', category='all', owner='all') {
  return state.records.filter(r=>(category==='all'||recordCategory(r)===category)&&(owner==='all'||r.owner===owner)&&
    `${r.id} ${r.from} ${r.to} ${ownerName(r.owner)} ${analysisFor(r).title}`.toLowerCase().includes(query.trim().toLowerCase()));
}
export function workspaceAction(state, action) {
  if(action.type==='select') {
    if(!state.records.some(r=>r.id===action.id)) return state;
    return {...state, selected:action.id, view:'overview', source:'waybill'};
  }
  if(action.type==='view') return {...state,view:action.view,source:action.source||state.source};
  const id=action.id||state.selected;
  const current=state.records.find(r=>r.id===id);
  if(!current) return state;
  let record={...current};
  const a=analysisFor(record), time=action.time||timeNow();
  const log=(title,detail)=>{record.activity=[...record.activity,{title,detail,time}];};
  const task=()=>({title:a.task,owner:record.taskOwner,due:record.taskDue,status:'open',comments:[]});
  switch(action.type) {
    case 'edit': {
      if(!['reviewDraft','taskOwner','taskDue','commentDraft','composer'].includes(action.field)) return state;
      if(action.field==='taskOwner'&&!owners.some(o=>o.id===action.value)) return state;
      record[action.field]=action.value; break;
    }
    case 'owner':
      if(!owners.some(o=>o.id===action.owner)||record.owner===action.owner)return state;
      record.owner=action.owner;log('复核负责人已变更',ownerName(action.owner));break;
    case 'ai-request':
      if(!action.text?.trim())return state;
      record.thread=[...record.thread,{role:'user',text:action.text.trim()}];record.composer='';break;
    case 'ai-response':
      record.thread=[...record.thread,{role:'assistant',text:action.text,artifact:!!action.artifact}];
      if(action.draft&&!record.reviewed){record.reviewDraft=a.draft;log('AI 生成复核意见','意见已填入，等待业务复核人确认。');}
      break;
    case 'draft':
      if(record.reviewed||record.originalKind==='missing')return state;
      record.reviewDraft=a.draft;log('AI 生成复核意见','意见已填入，等待业务复核人确认。');break;
    case 'review':
      if(record.reviewed || record.originalKind==='missing' || !record.reviewDraft.trim()) return state;
      record.reviewed=true;record.note=record.reviewDraft.trim();record.reviewedBy='review';
      log('人工复核已确认',record.note);
      if(record.originalKind!=='complete'&&!record.followUp){record.followUp=task();log('跟进任务已创建',`${a.task} · ${ownerName(record.taskOwner)} · ${record.taskDue} 前反馈`);}
      break;
    case 'reopen':
      if(!record.reviewed)return state;
      record.reviewed=false;log('重新打开复核', '保留原有意见与历史记录。');break;
    case 'create-task':
      if(record.followUp)return state;
      record.followUp=task();record.requested=record.originalKind==='missing';
      log(record.requested?'补证任务已创建':'跟进任务已创建',`${a.task} · ${ownerName(record.taskOwner)}`);break;
    case 'task-owner':
      if(!record.followUp||!owners.some(o=>o.id===action.owner)||record.followUp.owner===action.owner)return state;
      record.followUp={...record.followUp,owner:action.owner};log('跟进负责人已变更',ownerName(action.owner));break;
    case 'task-due':
      if(!record.followUp||!action.due||action.due===record.followUp.due)return state;
      record.followUp={...record.followUp,due:action.due};log('反馈时间已更新',`${action.due} 前反馈`);break;
    case 'task-status':
      if(!record.followUp||!['open','progress','done'].includes(action.status)||record.followUp.status===action.status)return state;
      if(action.status==='done'&&!record.followUp.comments.length)return state;
      record.followUp={...record.followUp,status:action.status};
      log('跟进状态已更新',{open:'待处理',progress:'处理中',done:'已完成'}[action.status]);break;
    case 'comment': {
      const text=(action.text??record.commentDraft).trim();
      if(!record.followUp||!text)return state;
      record.followUp={...record.followUp,comments:[...record.followUp.comments,{text,owner:'review',time}]};record.commentDraft='';
      log('补充协作回复',text);break;
    }
    default:return state;
  }
  return {...state,records:state.records.map(r=>r.id===id?record:r)};
}

// The guided sequence and direct manipulation share the exact same transitions.
export const TOUR_DURATION=32000;
export const TOUR_PROMPT='核对这笔运输单据，把差异交给负责人跟进。';
export function tourWorkspace(time) {
  let s=createWorkspace();
  const apply=a=>{s=workspaceAction(s,{...a,time:'09:16'});};
  if(time<2800)s={...s,records:s.records.map((r,i)=>i===0?{...r,thread:[]}:r)};
  else if(time<5500)s={...s,records:s.records.map((r,i)=>i===0?{...r,thread:[{role:'user',text:TOUR_PROMPT}]}:r)};
  if(time<2800) apply({type:'edit',field:'composer',value:TOUR_PROMPT.slice(0,Math.floor(time/2200*TOUR_PROMPT.length))});
  if(time>=9000 && time<14500) apply({type:'view',view:'sources',source:'receipt'});
  if(time>=14500 && time<18500) apply({type:'edit',field:'reviewDraft',value:analysisFor(s.records[0]).draft.slice(0,Math.floor((time-14500)/2800*analysisFor(s.records[0]).draft.length))});
  if(time>=18500)apply({type:'draft'});
  if(time>=21500)apply({type:'review'});
  if(time>=23500)apply({type:'view',view:'team'});
  if(time>=25500)apply({type:'task-status',status:'progress'});
  if(time>=27000 && time<30000)apply({type:'edit',field:'commentDraft',value:'请核对仓库入库记录，补充差异原因和处理结果。'.slice(0,Math.floor((time-27000)/2300*26))});
  if(time>=30000)apply({type:'comment',text:'请核对仓库入库记录，补充差异原因和处理结果。'});
  return s;
}

export function answerFor(record, prompt) {
  const a=analysisFor(record);
  if(/意见|草稿|建议/.test(prompt)) return {text:record.reviewed?'这条记录已复核。可以重新打开复核后修改意见。':record.originalKind==='missing'?'当前缺少签收回执，请先建立补证任务。补齐材料前不能确认签收结论。':'复核意见已填入右侧。你可以修改内容、指定负责人，然后确认交接。',draft:!record.reviewed&&record.originalKind!=='missing',view:'overview'};
  if(/原文|来源|材料|依据|凭证/.test(prompt))return {text:`这条记录关联了 ${recordFiles(record).length} 份材料，已在右侧打开来源。${a.caution}`,view:'sources'};
  if(/协作|跟进|负责人|分派|任务/.test(prompt))return {text:record.followUp?`跟进任务「${record.followUp.title}」由${ownerName(record.followUp.owner)}负责，${record.followUp.due} 前反馈。可以在右侧更新进度、补充处理结果。`:a.action+' 请在右侧确认负责人和反馈时间。',view:'team'};
  if(/数量|差异|核对|核验|检查|总结|摘要|费用|主体|签收/.test(prompt))return {text:a.finding+' '+a.caution,artifact:true,view:'overview'};
  return {text:'请指定这条运单的核验内容，例如“核对数量差异”“查看来源材料”或“生成复核意见”。'};
}
