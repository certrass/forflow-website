import React,{useEffect,useRef,useState} from 'react';
import {ArrowRight,ArrowUpRight,Check,CheckCircle,FileText,FlowArrow,Database,GitBranch,MagnifyingGlass,ShieldCheck,Sparkle,Stack,LinkSimple,Plus,Minus} from '@phosphor-icons/react';
import {ShowcaseViewport} from './ShowcaseViewport.jsx';
import {DetailTabs,ReviewHistory} from './ProductDetailUI.jsx';
import {BusinessBoard} from './BusinessBoard.jsx';
import {PersonAvatar,Collaborators,ReviewMark} from './HumanDetails.jsx';
import {ScenePlayback,useScenePlayback} from './ScenePlayback.jsx';
import {ProductPlaybackGuide} from './ProductPlaybackGuide.jsx';

const scenes=[
 {name:'业务协同',steps:['发现履行异常','关联业务依据','复核与交接'],durations:[3600,5400,6500]},
 {name:'文档处理',steps:['读入合同原文','提取业务字段','对照原文复核'],durations:[3000,5300,6600]},
 {name:'工程知识',steps:['查看原始图纸','展开设备关系','整理检修事项'],durations:[3200,4600,6200]},
];
export function ProductDemo({index,onEvidence}){
 const root=useRef(null),scene=scenes[index],player=useScenePlayback(root,scene.durations);
 const focus=()=>root.current?.querySelector('.showcase-controls')?.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
 return <div className={`product-presentation presentation-${index}`} ref={root} onClickCapture={player.takeOver} onKeyDownCapture={player.takeOver} data-step={player.step} data-playing={player.playing} data-time={Math.floor(player.time)}>
  <ShowcaseViewport label={scene.name} width={1108} focusTarget={index===1&&player.step===2?'.film-fields':undefined} focusVersion={player.run}>
   {index===0?<BusinessBoard player={player} onEvidence={onEvidence}/>:index===1?<DocumentDemo player={player} onEvidence={onEvidence}/>:<KnowledgeDemo player={player} onEvidence={onEvidence}/>}
   <ProductPlaybackGuide root={root} index={index} player={player}/>
  </ShowcaseViewport>
  <ScenePlayback player={player} steps={scene.steps} label={`${scene.name}演示进度`} onNavigate={focus}/>
 </div>;
}
function DemoTopbar({icon:Icon,title,children}){
 return <div className="demo-topbar"><span><Icon size={16}/><strong>{title}</strong></span>{children}</div>;
}
const contractFields=[
 {name:'合同参与方',value:'采购方 / 供应商',source:'第一条',text:'甲方与供应商就本次采购与交付建立合作关系。'},
 {name:'合同期限',value:'2026.09 — 2027.08',source:'第二条',text:'合作期限自 2026 年 9 月起至 2027 年 8 月止。'},
 {name:'付款条件',value:'验收后 30 日内付款',source:'第三条',text:'货物验收完成后 30 日内，按合同约定支付款项。'},
 {name:'交付要求',value:'按采购订单约定',source:'第四条',text:'交付品类、数量及时间，以双方确认的采购订单为准。'},
 {name:'异常处理',value:'双方书面确认',source:'第五条',text:'异常情形由双方核对，并以书面形式确认补充安排。'},
];
function DocumentDemo({player,onEvidence}){
 const [selected,setSelected]=useState(2),[count,setCount]=useState(0),[confirmed,setConfirmed]=useState([]),[panel,setPanel]=useState('fields'),[notice,setNotice]=useState('');
 const active=contractFields[selected];
 useEffect(()=>{
  if(player.step===0){setCount(0);setConfirmed([]);setSelected(2);setPanel('fields');setNotice('');return;}
  if(player.step===2){setCount(5);return;}
  setCount(0);

 },[player.step,player.run]);
 const extractedCount=player.step===1?Math.min(5,Math.floor(player.elapsed/620)):null;
 useEffect(()=>{if(extractedCount!==null)setCount(extractedCount)},[extractedCount]);
 useEffect(()=>{if(player.playing&&player.step===2){setSelected(2);setPanel('fields')}},[player.playing,player.step]);
 const autoConfirmed=player.step===2&&player.elapsed>=3600;
 useEffect(()=>{if(autoConfirmed){setConfirmed(v=>v.includes(2)?v:[...v,2]);setNotice('')}},[autoConfirmed,player.run]);
 const choose=index=>{setSelected(index);setPanel('fields');player.seek(2)};
 const done=confirmed.includes(selected);
 const nextPending=Array.from({length:contractFields.length},(_,i)=>(selected+i+1)%contractFields.length).find(i=>!confirmed.includes(i));
 const confirm=()=>{setConfirmed(v=>v.includes(selected)?v:[...v,selected]);setNotice(`「${active.name}」已确认，${contractFields.length-confirmed.length-1} 项待复核。`)};
 const undo=()=>{setConfirmed(v=>v.filter(i=>i!==selected));setNotice(`已撤销「${active.name}」的确认。`)};
 const moveField=event=>{if(!['ArrowDown','ArrowUp','Home','End'].includes(event.key))return;event.preventDefault();const buttons=[...event.currentTarget.querySelectorAll('button')];const current=buttons.indexOf(event.target.closest('button'));const next=event.key==='Home'?0:event.key==='End'?count-1:(current+(event.key==='ArrowDown'?1:-1)+count)%count;choose(next);buttons[next]?.focus()};
 return <div className="document-film" data-extracted={count}>
  <DemoTopbar icon={FileText} title="文档工作空间"><span className="demo-breadcrumb"><FileText size={13}/>供应商合作协议.pdf <span className="detail-status">{confirmed.length===5?'已完成复核':'待逐项复核'}</span><Collaborators members={['procurement']} label="采购复核"/></span></DemoTopbar>
  <div className="document-film-body">
   <div className="film-source"><div className="film-panel-title"><FileText size={14}/>原始文档<span>PDF <i/> 第 1 页 / 共 1 页</span></div>
    <div className={`film-paper ${player.step===1?'is-reading':''}`}>
     <h3>供应商合作协议</h3>
     <div className="paper-clauses">{contractFields.map((field,i)=><button key={field.name} onClick={()=>choose(i)} className={(player.step===2&&i===selected)||(player.step===1&&i===count-1)?'active':''}><span className="clause-number">{String(i+1).padStart(2,'0')}</span><span><strong>{field.source} · {field.name}</strong><span>{field.text}</span></span>{player.step===2&&i===selected&&<ReviewMark done={confirmed.includes(i)}/>}</button>)}</div>
     <div className="paper-end"><span>供应商合作协议</span><span>1</span></div><div className="document-scan" style={{animation:'none',transform:`translateY(${50+490*Math.min(1,player.elapsed/3400)}px)`,opacity:player.step===1&&player.elapsed>150&&player.elapsed<3400?1:0}}/>
    </div>
   </div>
   <aside className="film-fields"><div className="film-panel-title"><Sparkle size={15}/>合同复核<span>{confirmed.length} / 5 已确认</span></div><DetailTabs value={panel} onChange={setPanel} items={[['fields','提取字段',count],['history','复核记录',confirmed.length]]} label="合同复核视图"/>{panel==='history'?<ReviewHistory items={confirmed.map(i=>({id:i,title:contractFields[i].name+'已确认',description:contractFields[i].source+' · '+contractFields[i].value,person:'procurement',actor:'采购团队确认'}))} onSelect={choose} onStart={()=>choose(confirmed.length?confirmed[0]:2)}/>:<>
    <div className="fields-lead"><span className="field-blueprint"><Stack size={14}/>采购合同字段</span><h3>{player.step===0?'提取合同字段':player.step===1?'正在提取字段':'对照原文复核'}</h3><p>{player.step===0?'按预设字段提取关键条款，并保留对应的原文位置。':player.step===1?'正在提取合同参与方、期限、付款条件等信息。':confirmed.length===5?'5 项已全部确认，可在复核记录中逐项回看。':`选择字段核对原文，还有 ${5-confirmed.length} 项待复核。`}</p></div>
    <div className="extracted-fields" onKeyDown={moveField} aria-label="提取字段，支持上下方向键切换">{contractFields.map((field,i)=><button key={field.name} disabled={i>=count} aria-pressed={selected===i&&player.step===2} title={i<count?`查看${field.source}原文${confirmed.includes(i)?' · 已确认':''}`:'等待提取'} className={`${i<count?'revealed':''} ${player.step===2&&selected===i?'active':''}`} onClick={()=>choose(i)}><span className="extracted-index">{String(i+1).padStart(2,'0')}</span><span><small>{field.name}</small>{i<count?<strong key={`${player.run}-${count>i}`}>{field.value}</strong>:<i className="field-placeholder"/>}</span>{i<count?<span className="field-origin">{confirmed.includes(i)?<CheckCircle size={15}/>:<LinkSimple size={14}/>}<small>{field.source}</small></span>:<span className="waiting-mark"/>}</button>)}</div>
    <div className="field-action" key={player.step===2?selected:player.step}>
     {player.step<2?<><div className="extract-summary"><span className="extract-orbit"><Sparkle size={15}/></span><span>{count===5?'5 个字段已保留原文出处':player.step===0?'提取后可逐项核对原文':'正在对照字段定义读取原文'}</span></div><button className="demo-primary" onClick={()=>player.step===0?player.startAt(1):player.seek(2)}>{player.step===0?'提取合同字段':'对照原文'}<ArrowRight size={14}/></button></>:<><div className="source-quote"><span><FileText size={12}/>第 1 页 · {active.source}<span className="source-match">已定位原文</span></span><p>{active.text}</p></div>{done?<div className="field-confirmed-actions"><div><span className="confirmed-by-person"><PersonAvatar person="procurement" size={22} checked/>已确认「{active.name}」</span><button onClick={undo}>撤销确认</button></div><button className="demo-primary" onClick={()=>nextPending!==undefined?choose(nextPending):setPanel('history')}>{nextPending!==undefined?'核对下一项':'查看完整复核记录'}<ArrowRight size={14}/></button></div>:<button className="demo-primary" onClick={confirm}>确认「{active.name}」<ArrowRight size={14}/></button>}</>}
    </div>
   </>}</aside>
  </div>
  <div className="demo-foot"><span role="status" aria-live="polite"><LinkSimple size={13}/>{notice|| (confirmed.length?`${confirmed.length} 个字段已确认，来源与复核记录一起保留`:'原文、字段与复核结果保持对应')}</span><button onClick={onEvidence}>查看文档处理案例<ArrowUpRight size={13}/></button></div>
 </div>;
}

const equipment=[
 {id:'inlet',name:'入口管线',type:'上游连接',x:54,y:127,icon:GitBranch},
 {id:'isolation',name:'隔离阀组',type:'控制与隔离',x:54,y:329,icon:GitBranch},
 {id:'pump',name:'泵组',type:'当前设备',x:282,y:225,icon:Database},
 {id:'outlet',name:'出口管线',type:'下游连接',x:510,y:89,icon:GitBranch},
 {id:'valve',name:'调节阀组',type:'控制与隔离',x:510,y:253,icon:GitBranch},
 {id:'downstream',name:'下游设备',type:'关联设备',x:510,y:417,icon:Database},
];
function KnowledgeDemo({player,onEvidence}){
 const [picked,setPicked]=useState('pump'),[direction,setDirection]=useState('down'),[manualView,setManualView]=useState(null),[zoom,setZoom]=useState(100),[preparedIds,setPreparedIds]=useState([]),[hovered,setHovered]=useState(null);
 useEffect(()=>{setManualView(null);setPreparedIds([]);setPicked(player.step===2?'valve':'pump');setDirection('down')},[player.step,player.run]);
 const autoPrepared=player.step===2&&player.elapsed>=3300;
 useEffect(()=>{if(autoPrepared)setPreparedIds(ids=>ids.includes('valve')?ids:[...ids,'valve'])},[autoPrepared,player.run]);
 const focusId=hovered||picked;
 const graph=manualView?manualView==='graph':player.step>0;
 const selected=equipment.find(e=>e.id===picked);
 const related=direction==='up'?equipment.slice(0,2):equipment.slice(3);
 const prepared=preparedIds.includes(picked);
 const select=id=>setPicked(id);
 return <div className="knowledge-film">
  <DemoTopbar icon={Database} title="工程知识"><span className="demo-breadcrumb"><FileText size={13}/>P&ID 工程图纸 <span className="detail-status">已关联来源</span><Collaborators members={['engineering']} label="工程复核"/></span></DemoTopbar>
  <div className="knowledge-film-body">
   <div className="knowledge-stage"><div className="knowledge-view-tabs"><div><button aria-pressed={!graph} className={!graph?'active':''} onClick={()=>setManualView('drawing')}><FileText size={13}/>原始图纸</button><button aria-pressed={graph} className={graph?'active':''} onClick={()=>setManualView('graph')}><GitBranch size={13}/>设备关系</button></div>{graph?<span className="map-status"><span/>6 个对象 · 5 条连接</span>:<div><button disabled={zoom<=80} title="缩小图纸" aria-label="缩小图纸" onClick={()=>setZoom(v=>Math.max(80,v-20))}><Minus size={13}/></button><button className="zoom-reset" onClick={()=>setZoom(100)} aria-label="重置图纸缩放" title="恢复为 100%">{zoom}%</button><button disabled={zoom>=180} title="放大图纸" aria-label="放大图纸" onClick={()=>setZoom(v=>Math.min(180,v+20))}><Plus size={13}/></button></div>}</div>
    {graph?<div className="relationship-map" key="graph" data-connection-focus={focusId}><div className="map-caption"><GitBranch size={14}/>以泵组为中心 · 当前查看{selected.name}</div><svg className={`relationship-lines direction-${direction}`} viewBox="0 0 764 585" aria-hidden="true"><defs><marker id="relation-arrow" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="currentColor"/></marker></defs>{['M234 174H260Q274 174 274 188V258Q274 272 282 272','M234 376H260Q274 376 274 362V286Q274 272 282 272','M462 272H478Q492 272 492 258V150Q492 136 510 136','M462 272H480Q493 272 493 286Q493 300 510 300','M462 272H478Q492 272 492 286V450Q492 464 510 464'].map((d,i)=><path key={d} d={d} className={`${i<2?'up':'down'} ${focusId==='pump'||focusId===['inlet','isolation','outlet','valve','downstream'][i]?'is-focused':'is-muted'}`} markerEnd="url(#relation-arrow)"/>)}</svg>{equipment.map(({id,name,type,x,y,icon:Icon},i)=><button key={id} className={`equipment-node ${id==='pump'?'central':''} ${picked===id?'selected':''} ${related.some(e=>e.id===id)?'in-direction':''}`} aria-pressed={picked===id} onMouseEnter={()=>setHovered(id)} onMouseLeave={()=>setHovered(null)} onFocus={()=>setHovered(id)} onBlur={()=>setHovered(null)} onClick={()=>select(id)} style={{left:x,top:y,animationDelay:`${i*85}ms`}}><span className="equipment-node-icon"><Icon size={19}/></span><span><strong>{name}</strong><small>{type}</small></span>{picked===id&&<span className="node-selected-dot"/>}</button>)}<div className="map-legend"><span><i/>设备连接</span><span><i/>当前查看的连接</span></div></div>:<div className="source-drawing" key="drawing"><img src="/assets/pid.png" style={{transform:`scale(${zoom/100})`}} alt="团队过往 P&ID 项目的原始工程图纸"/><div className="drawing-open-card"><FileText size={20}/><div><strong>P&ID 工程图纸</strong><span>设备、管线与仪表关系</span></div><button onClick={()=>setManualView('graph')}>展开设备关系<ArrowRight size={14}/></button></div></div>}
   </div>
   <aside className="knowledge-inspector"><div className="film-panel-title"><Database size={14}/>设备档案<span><LinkSimple size={12}/>已关联</span></div><div className="equipment-detail-title"><span className="equipment-large-icon"><selected.icon size={24}/></span><div><span>{selected.type}</span><h3>{selected.name}</h3></div></div><div className="equipment-detail-meta"><button onClick={()=>setManualView('drawing')}><span>来源</span><FileText size={12}/>P&ID 工程图纸<ArrowUpRight size={12}/></button><span>上下文<GitBranch size={12}/>设备与连接关系</span></div><div className="relation-context">泵组的关联对象</div><div className="relation-direction" role="tablist" aria-label="设备连接方向"><button role="tab" aria-selected={direction==='up'} onClick={()=>{setDirection('up');setManualView('graph')}}>上游连接<span>2</span></button><button role="tab" aria-selected={direction==='down'} onClick={()=>{setDirection('down');setManualView('graph')}}>下游连接<span>3</span></button></div><div className="relation-results">{related.map(item=><button key={item.id} className={picked===item.id?'selected':''} onClick={()=>{select(item.id);setManualView('graph')}}><GitBranch size={14}/><span>{item.name}</span><ArrowUpRight size={12}/></button>)}</div><div className="maintenance-prepare"><span className="prepare-label"><ShieldCheck size={14}/>检修准备{preparedIds.length>0&&<span className="prepare-count">{preparedIds.length} 个设备</span>}</span>{prepared?<div className="prepared-work" role="status"><strong><CheckCircle size={16}/>已加入检修准备</strong><div className="engineering-review-owner"><PersonAvatar person="engineering" size={25}/><span>{selected.name} · 待工程师复核</span></div><p>核对图纸版本与现场一致性</p><p>确认上下游设备与隔离范围</p><p>补充维护记录，进入工单准备</p><button className="prepare-undo" onClick={()=>setPreparedIds(ids=>ids.filter(id=>id!==picked))}>撤销加入</button></div>:<><p>将当前设备加入检修准备，并列出需要工程师核对的事项。</p><button className="demo-primary" onClick={()=>setPreparedIds(ids=>[...new Set([...ids,picked])])}>将{selected.name}加入准备<ArrowRight size={14}/></button></>}</div></aside>
  </div>
  <div className="demo-foot"><span><GitBranch size={13}/>{preparedIds.length?`${preparedIds.length} 个设备已加入准备，切换设备可继续核对`:'点击设备查看档案，点击来源回到图纸'}</span><button onClick={onEvidence}>查看工程案例<ArrowUpRight size={13}/></button></div>
 </div>;
}
