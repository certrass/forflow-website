import React, {useEffect, useState} from 'react';
import {ArrowUpRight, Check, Copy, EnvelopeSimple} from '@phosphor-icons/react';
import {bookingUrl, contactEmail} from './contact-config.js';

export function ContactSection() {
  const [copyState, setCopyState] = useState('');
  useEffect(() => {
    if (!copyState) return;
    const timer = setTimeout(() => setCopyState(''), 2600);
    return () => clearTimeout(timer);
  }, [copyState]);
  async function copyEmail() {
    try { await navigator.clipboard.writeText(contactEmail); setCopyState('邮箱已复制'); }
    catch { setCopyState('请复制下方邮箱地址'); }
  }
  return <section className="contact-section v6-container" id="contact">
    <div className="contact-intro"><span className="overline">联系我们</span><h2>聊聊你的业务场景。</h2><p>带上一个问题，一起看产品、接入方式和验证重点。</p></div>
    <div className="contact-card"><a className="v6-button dark" href={bookingUrl} target="_blank" rel="noreferrer">预约产品演示<ArrowUpRight size={16}/></a><p className="contact-form-hint">提交需求后，我们会联系你确认时间。</p><div className="contact-email"><EnvelopeSimple size={17}/><a href={`mailto:${contactEmail}`}>{contactEmail}</a><button onClick={copyEmail} aria-label="复制联系邮箱" title={copyState || '复制邮箱'}>{copyState === '邮箱已复制' ? <Check size={15}/> : <Copy size={15}/>}</button></div><span className="contact-copy-status" role="status">{copyState}</span></div>

  </section>;
}
