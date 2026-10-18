import React from 'react';
import {ArrowRight, Check, FileText, GitBranch, ShieldCheck, WarningCircle} from '@phosphor-icons/react';
import {ShowcaseViewport} from './ShowcaseViewport.jsx';
import {governanceModules} from './governance-content.js';
import './q2q-asset-canvas.css';

export const assetChapters = [['核对依据', 0], ['记录纠正', 6000], ['形成资产', 12000], ['再次验证', 18000]];
const source = governanceModules[0].samples[0];
const narratives = [
  ['这次判断，依据是什么？', '引用了文件，还要核对结论。', '把回答和原文放在一起，找出真正需要修订的地方。'],
  ['专家改过一次，下次还会错吗？', '把纠正理由留下来。', '保存有效条款、适用范围和预期行为，让经验能被检查。'],
  ['一次纠正，可以留下什么？', '一条规则，一组验收样本。', '规则说明怎么做；样本帮助检查下一次是否做对。'],
  ['换一个模型，这条经验还能用吗？', '用同一组条件，再验一次。', '切换候选回答，观察边界样本；制度变化后先复核适用性。'],
];
const details = [{label:'业务依据',target:'.q2q-asset-input'}, {label:'资产与验证',target:'.q2q-asset-output'}];

function SourceCard({onOpen}) {
  return <div className="q2q-source-card"><span className="q2q-field-label"><FileText size={14}/>原文依据</span><h4>{source.source}</h4><p>{source.location}</p><blockquote>{source.excerpt}</blockquote><button className="q2q-text-action" onClick={onOpen}>查看完整核验记录<ArrowRight size={14}/></button></div>;
}

function RuleCard({outdated = false}) {
  return <div className="q2q-rule-card"><span className="q2q-field-label"><GitBranch size={14}/>{outdated?'旧规则 · 等待复核':'业务规则'}</span><h4>采购审批条件</h4><dl><div><dt>触发条件</dt><dd>金额 ≥ 50 万元</dd></div><div><dt>预期处理</dt><dd>提交集团审核</dd></div><div><dt>适用范围</dt><dd>本制度适用的采购事项</dd></div><div><dt>缺失金额</dt><dd>补充材料后再判断</dd></div></dl><span className="q2q-rule-source">依据：采购管理办法 · 第十二条</span></div>;
}

export function Q2QAssetCanvas({step, threshold, changed, onThreshold, onChanged, pause, openWorkspace}) {
  const narrative = narratives[step];
  // Authored boundary examples illustrate one rule; no model or customer result is inferred.
  const samples = [
    {input:'49 万元', expected:'未触发本条款', result:'未触发本条款', pass:true},
    {input:'50 万元', expected:'提交集团审核', result:threshold===50?'提交集团审核':'未触发本条款', pass:threshold===50},
    {input:'金额缺失', expected:'补充材料', result:'补充材料', pass:true},
  ];
  return <div className="evaluation-showcase q2q-asset-showcase">
    <ShowcaseViewport label="Q2Q · 从业务判断到企业资产" width={1080} focusTarget={details[step>1?1:0].target} focusVersion={step} detailSections={details} onExpand={pause}>
      <div className="q2q-asset-canvas" data-asset-step={step}>
        <header className="evaluation-appbar"><span><ShieldCheck size={16}/><strong>Q2Q</strong><i/>采购审批</span><span>依据 · 规则 · 评测</span></header>
        <div className="q2q-asset-intro"><span>{narrative[0]}</span><h3>{narrative[1]}</h3><p>{narrative[2]}</p></div>
        <div className="q2q-asset-body" key={step}>
          <div className="q2q-asset-input">
            {step===0?<><span className="q2q-field-label">待核对回答</span><div className="q2q-answer">金额低于 <mark>100 万元</mark>，<br/>可由部门自行审批。</div><div className="q2q-judgment"><WarningCircle size={17}/><div><strong>与原文矛盾</strong><p>回答把审批阈值从 50 万元改成了 100 万元。</p></div></div></>:step===1?<><span className="q2q-field-label">业务专家修订</span><div className="q2q-correction"><del>低于 100 万元，部门自行审批。</del><ins>达到 50 万元，提交集团审核。</ins></div><div className="q2q-expert-note"><span>修订理由</span><p>按现行第十二条处理。没有金额时，先补充材料，不推定可以放行。</p></div><button className="q2q-text-action" onClick={openWorkspace}>回看条款与修订<ArrowRight size={14}/></button></>:<RuleCard outdated={step===3&&changed}/>}
          </div>
          <div className="q2q-asset-connector" aria-hidden="true"><ArrowRight size={19}/></div>
          <div className="q2q-asset-output">
            {step===0?<SourceCard onOpen={openWorkspace}/>:step===1?<RuleCard/>:step===2?<><span className="q2q-field-label"><ShieldCheck size={14}/>场景评测样本</span><h4>把容易出错的边界留下。</h4><div className="q2q-sample-list">{samples.map(item=><div key={item.input}><span>{item.input}</span><ArrowRight size={13}/><strong>{item.expected}</strong></div>)}</div><button className="q2q-text-action" onClick={openWorkspace}>查看来源与处理记录<ArrowRight size={14}/></button></>:<>
              <div className="q2q-replay-controls"><label htmlFor="q2q-answer-threshold">候选回答采用的阈值</label><select id="q2q-answer-threshold" value={threshold} onChange={event=>onThreshold(Number(event.target.value))}><option value={100}>100 万元</option><option value={50}>50 万元</option></select></div>
              <div className="q2q-replay-summary" aria-live="polite"><strong>{changed?'适用性待复核':`${samples.filter(item=>item.pass).length} / 3 项符合预期`}</strong><span>{changed?'制度已更新，旧结论不沿用。':'只检查当前审批条件。'}</span></div>
              <table className="q2q-replay-table" aria-label="当前三个边界样本的逐项对照"><thead><tr><th>输入</th><th>候选处理</th><th>核对</th></tr></thead><tbody>{samples.map(item=><tr key={item.input}><td>{item.input}</td><td>{item.result}</td><td>{changed?<span className="q2q-result-pending">待复核</span>:item.pass?<span className="q2q-result-pass"><Check size={12}/>一致</span>:<span className="q2q-result-pending"><WarningCircle size={12}/>漏项</span>}</td></tr>)}</tbody></table>
              <label className="q2q-policy-change"><input type="checkbox" checked={changed} onChange={event=>onChanged(event.target.checked)}/>试试制度发生变化</label>
            </>}
          </div>
        </div>
        <footer className="q2q-asset-footer"><span><GitBranch size={13}/>{['发现一项需要修订的判断','保留专家判断的条件和理由','经验形成可检查、可复用的对象','更换模型，用企业自己的样本验收'][step]}</span><span>{step===3?'变更后重新验证':'采购审批 · 同一条业务记录'}</span></footer>
      </div>
    </ShowcaseViewport>
  </div>;
}
