import React from 'react';
import brands from './brand-assets.json';

export function ReferenceLogoWall() {
  // The user requested Guru's original logos as temporary layout references.
  // A normal/production build never renders this wall.
  if (import.meta.env.VITE_REFERENCE_LOGOS !== 'true') return null;
  return <section className="reference-logo-wall" data-reference-only aria-label="客户与合作方 logo 排版参考">
    <p>客户与合作方 <span>· 版式参考</span></p>
    <div>{brands.reference_logos.map((logo, i) => <img key={logo.src} src={logo.src} alt={logo.alt} width={logo.width} height={logo.height} title={`Guru 参考标识 ${i + 1} · 待替换`}/>)}</div>
  </section>;
}

export function AgentEcosystem() {
  return <section className="one-ecosystem" aria-label="ForFlow One 智能体生态">
    <p>选择你熟悉的智能体，在 ForFlow One 中一起工作。</p>
    <div className="one-agent-logos">{brands.ecosystem.map(logo => <span key={logo.id}><img src={logo.src} alt="" width="24" height="24"/><b>{logo.name}</b></span>)}</div>
  </section>;
}

export function OneProductBenefits() {
  return <div className="one-product-benefits">
    <div><span>01</span><h3>让任务并行推进</h3><p>选择合适的智能体，在同一工作区处理各自任务。</p></div>
    <div><span>02</span><h3>让结果经得起审阅</h3><p>把任务要求、材料和产出放在一起，核对关键判断。</p></div>
    <div><span>03</span><h3>让下一步接得上</h3><p>保留工作上下文、文件与处理记录，继续跟进。</p></div>
  </div>;
}
