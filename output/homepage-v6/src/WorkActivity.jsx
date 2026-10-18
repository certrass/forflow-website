import React from 'react';
const rows=[
  [['⌕','合同原文已关联'],['✓','待复核条款已定位'],['↗','异常交给业务负责人'],['≋','知识来源保持同步'],['◇','设备关系可追溯'],['⊞','智能体分工协作']],
  [['↻','改动后重新核验'],['✓','保留每次复核记录'],['⌘','沿用已确认的工作流'],['↗','下一步责任清楚'],['≡','输出关联原文依据'],['◎','操作按权限执行']],
  [['▤','合同复核'],['↗','业务跟进'],['⌕','知识查询'],['⊞','多智能体并行'],['≋','系统与资料接入'],['◇','Q2Q 持续评估']]
];
export function WorkActivity(){return <section className="guru-activity" data-guru-motion aria-label="ForFlow 工作过程与结果"><div aria-hidden="true">{rows.map((row,i)=><div className="guru-marquee" key={i}>{[0,1].map(copy=><div className="guru-marquee-group" key={copy}>{row.map(([icon,label])=><span className="guru-work-chip" key={label}><i>{icon}</i>{label}</span>)}</div>)}</div>)}</div><p className="sr-only">关联原文、核对条款、交接负责人；保留复核记录、重用工作流、持续评估。</p><button className="guru-motion-toggle" data-motion-toggle aria-label="暂停工作动态" aria-pressed="false">Ⅱ 暂停动态</button></section>}
