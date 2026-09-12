import React from 'react';
import {ArrowRight, Check, FileText, LinkSimple} from '@phosphor-icons/react';
import {Person} from './ShowcaseFilmUI.jsx';

export function WorkspaceReport({record, ready, reviewing, confirmed, onSource}) {
  return <article className={`canvas-report story-result ${ready ? 'is-ready' : ''}`} aria-label="运输单据核验报告">
    <div className="canvas-report-kicker"><span>运输履约</span><span>{record.id}</span></div>
    <h3>运输单据核验报告</h3>
    <p className="canvas-report-summary">{ready ? '运单与签收回执存在数量差异，收货地点与运输单号一致。差异保留原文依据，等待负责人核实。' : '正在读取关联单据，对齐数量、收货地点与运输单号。'}</p>
    <section className="canvas-quantity-chart" aria-label={ready ? '数量对照：发运 240 箱，签收 238 箱' : '数量对照，正在核验'}>
      <div className="canvas-report-section"><h4>数量对照</h4><span>{ready ? '2 箱待核实' : '核对中'}</span></div>
      <div className="canvas-bar"><span>运输运单</span><div className="canvas-bar-track"><i style={{width:'100%'}}/></div><strong>{record.shipped}<small>箱</small></strong></div>
      <button className="canvas-bar canvas-received" onClick={onSource} aria-label="核对签收数量 238 箱"><span>签收回执</span><div className="canvas-bar-track"><i style={{width:ready ? `${record.received/record.shipped*100}%` : '0%'}}/></div><strong>{ready ? record.received : '—'}<small>箱</small></strong><LinkSimple size={12}/></button>
      <div className="canvas-chart-axis"><span>0</span><span>240 箱</span></div>
    </section>
    <table className="canvas-field-table"><thead><tr><th>关联字段</th><th>运输运单</th><th>签收回执</th></tr></thead><tbody><tr><td>收货地点</td><td>{record.to}仓</td><td>{record.to}仓<Check size={12}/></td></tr><tr><td>运输单号</td><td>{record.id}</td><td>一致<Check size={12}/></td></tr></tbody></table>
    <div className={`canvas-review-note ${reviewing ? 'is-reviewing' : ''}`}><div><Person small/><strong>{confirmed ? '复核意见已交接' : '复核意见'}</strong>{reviewing && <span>业务复核人</span>}</div><p>{ready ? '请运输负责人核对仓库记录，确认 2 箱差异的原因。' : '核验结果生成后，可在这里确认复核意见。'}</p></div>
    <footer className="canvas-report-footer"><span><FileText size={13}/>2 份关联材料</span><button onClick={onSource}>查看原文<LinkSimple size={13}/></button></footer>
  </article>;
}

export function ReportThumbnail({onClick, ready}) {
  return <button className="canvas-artifact-link" onClick={onClick}>
    <span className="canvas-document-thumb" aria-hidden="true"><i/><i/><b/><b/><i/><i/></span>
    <span><strong>运输单据核验报告</strong><small>{ready ? '2 份材料 · 1 项差异' : '正在整理核验结果'}</small><em>在画布中查看<ArrowRight size={12}/></em></span>
  </button>;
}
