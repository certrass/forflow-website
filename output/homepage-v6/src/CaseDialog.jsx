import React, {useEffect, useRef} from 'react';
import {ArrowRight, ArrowUpRight, Check, FileText, X} from '@phosphor-icons/react';
import {bookingUrl} from './contact-config.js';

// Publicly disclosed methods and attribution from the existing case pages.
// Business outcomes below describe the workflow output, not a measured ROI claim.
const details = {
  bpillar: {
    audience: '汽车工程 · 质量与研发团队',
    summary: '把材料、工艺、失效机理和工程变更连起来，让经验可以继续使用。',
    problem: 'B 柱的工程判断分散在 DFMEA 表格、试验记录、供应商邮件和资深工程师经验中。设计或工艺改变后，团队难以完整找回当时的判断依据。',
    steps: [
      ['整理工程对象', '从一个零部件出发，关联需求、功能、结构、材料、工艺与历史失效记录。'],
      ['追踪关系与来源', '保留风险判断对应的设计版本、试验依据和适用条件，支持工程师追查原因。'],
      ['随变更重新复核', '发生 ECO 或供应商工艺变更时，沿关联关系查找受影响的判断，交由工程团队复核。'],
    ],
    outcome: '可追溯的工程知识链，以及变更后需要重新验证的风险与依据。',
    responsibility: '工程师确认关联关系与适用条件，结合企业自己的设计、试验和质量数据作出最终判断。',
    context: '源于团队成员在原组织积累的汽车工程与智能体实践，聚焦 B 柱 DFMEA 的知识建模与变更追溯。',
    source: 'case-automotive-dfmea-ontology-agent.html',
  },
  supply: {
    audience: '供应链运营 · 履约团队',
    summary: '订单出了异常，团队需要的下一步，是查清原因并推动处理。',
    problem: '履行明细、订单状态和信用控制记录分散在不同系统。业务人员看到告警后，仍要找人查数、核对规则，再协调后续处理。',
    steps: [
      ['定位问题', '从一笔订单或一组履行异常出发，明确要查的业务对象。'],
      ['关联证据', '按业务定义查询相关记录，对照订单状态和信用控制条件。'],
      ['推进处理', '整理原因、待核对事项和行动建议，由业务负责人确认并承接。'],
    ],
    outcome: '一份带有查询依据、处理条件和责任人的异常分析，可继续用于业务交接。',
    responsibility: '业务负责人确认归因与处理条件，再决定是否推进后续动作。',
    context: '基于团队成员在原组织参与的全球鞋服零售供应链项目，客户信息作匿名处理。',
    source: 'case-supply-chain-agentic-decision.html',
  },
  docs: {
    audience: '采购运营 · 合同管理',
    summary: '让合同信息进入业务流程，同时保留每个字段的原文依据。',
    problem: '供应商合同没有统一模板。只得到一段摘要，仍然需要人工重新录入参与方、期限、义务和终止条件。',
    steps: [
      ['定义字段', '按采购或法务流程确定需要哪些条款，以及日期、对象和列表等字段类型。'],
      ['提取并复核', '按字段蓝图提取内容，将缺失、低置信度及关键条款交给负责人对照原文。'],
      ['交付结构化结果', '保留确认值与来源，按下游系统要求整理为结构化字段。'],
    ],
    outcome: '可复核的合同字段，以及后续同类文档可以沿用的提取与校验标准。',
    responsibility: '采购或法务人员复核关键义务、期限和终止条件，确认后再进入业务系统。',
    context: '基于文档自动化工程方法，将供应商合同条款整理为可复核的业务字段。',
    source: 'case-financial-bda-document-automation.html',
  },
  knowledge: {
    audience: '工程团队 · 设备运维',
    summary: '围绕一台设备，找到上下游连接和相关资料。',
    problem: 'P&ID 中的设备、阀门和管线关系锁在图纸里。查找影响范围、准备检修时，工程师需要反复翻图，并依赖熟悉现场的同事。',
    steps: [
      ['读取图纸', '提取 PDF 中已有的文字和线条，识别设备、仪表与管线符号。'],
      ['重建设备关系', '关联对象与连接，保留页码和版本，由工程师确认关键符号及跨页关系。'],
      ['支持查询与准备', '按设备查询上下游，结合维护资料整理待核对事项与检修准备清单。'],
    ],
    outcome: '有图纸依据的设备关系，以及工程师可以继续核对的维护准备材料。',
    responsibility: '工程师确认图纸版本、设备关系与现场条件，再作出检修和操作判断。',
    context: '基于团队成员加入 ForFlow 前的 P&ID 智能化实践。',
    source: 'case-manufacturing-pid-intelligence.html',
  },
};

export function CaseDialog({item, onClose, onNext}) {
  const ref = useRef(null);
  const content = details[item.id];
  useEffect(() => {
    const dialog = ref.current;
    const previous = document.activeElement;
    dialog.showModal();
    const overflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { dialog.close(); document.body.style.overflow = overflow; previous?.focus({preventScroll:true}); };
  }, []);
  useEffect(() => { ref.current.querySelector('.case-dialog-body')?.scrollTo(0, 0); }, [item.id]);
  return <dialog ref={ref} className="case-dialog" aria-labelledby="case-dialog-title" onCancel={onClose} onClick={e => {if(e.target === e.currentTarget)onClose();}}>
    <div className="case-dialog-shell">
      <header className="case-dialog-top"><span>{item.name}<i/>案例详解</span><button aria-label="关闭案例" onClick={onClose}><X size={20}/></button></header>
      <div className="case-dialog-body" key={item.id}>
        <div className="case-dialog-intro"><span className="case-audience">{content.audience}</span><h2 id="case-dialog-title">{item.title}</h2><p>{content.summary}</p></div>
        <section className="case-problem"><span>业务问题</span><p>{content.problem}</p></section>
        <section className="case-process"><h3>工作是怎样推进的</h3>{content.steps.map(([title, text], i) => <div key={title}><span>0{i+1}</span><div><h4>{title}</h4><p>{text}</p></div></div>)}</section>
        <section className="case-deliverable"><Check size={20}/><div><h3>团队拿到什么</h3><p>{content.outcome}</p><small>{content.responsibility}</small></div></section>
        <section className="case-provenance"><h3>{item.tag}</h3><p>{content.context}</p><div>{item.sources.map(s => <span key={s}><FileText size={13}/>{s}</span>)}</div></section>
      </div>
      <footer className="case-dialog-footer"><a className="v6-button dark" href={bookingUrl} target="_blank" rel="noreferrer">聊聊类似需求<ArrowUpRight size={14}/></a><button onClick={onNext}>下一个案例<ArrowRight size={15}/></button></footer>
    </div>
  </dialog>;
}
