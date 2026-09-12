import {
  POLICY_VERSION,
  assertSameOriginJson,
  cleanText,
  env,
  escapeHtml,
  isUuid,
  json,
  selectRows,
  supabaseRequest,
  upsertRows,
} from './_shared/site-data.mjs';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const SOURCE_TYPES = new Set(['contact', 'assessment_report']);

async function sendEmail({ to, subject, html, replyTo }) {
  const key = env('RESEND_API_KEY');
  const from = env('LEADS_FROM_EMAIL');
  if (!key || !from) return { configured: false, sent: false };
  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from, to: [to], subject, html, reply_to: replyTo || undefined }),
  });
  if (!response.ok) throw new Error(`Email ${response.status}: ${(await response.text()).slice(0, 300)}`);
  return { configured: true, sent: true };
}

const reportHtml = (summary) => `
  <div style="font-family:Arial,'PingFang SC',sans-serif;line-height:1.7;color:#111;max-width:640px;margin:auto">
    <p style="color:#246b39;font-weight:700;letter-spacing:.08em">FORFLOW AI 场景诊断</p>
    <h1 style="font-size:28px">你的第一版场景建议</h1>
    <p>这份结果用于团队讨论。正式试点仍需结合真实流程、样本、权限和验收标准确认。</p>
    <table style="width:100%;border-collapse:collapse;margin:24px 0">
      <tr><td style="padding:12px;border-bottom:1px solid #ddd;color:#666">业务重点</td><td style="padding:12px;border-bottom:1px solid #ddd"><b>${escapeHtml(summary.challenge)}</b></td></tr>
      <tr><td style="padding:12px;border-bottom:1px solid #ddd;color:#666">优先目标</td><td style="padding:12px;border-bottom:1px solid #ddd"><b>${escapeHtml(summary.goal)}</b></td></tr>
      <tr><td style="padding:12px;border-bottom:1px solid #ddd;color:#666">建议起步</td><td style="padding:12px;border-bottom:1px solid #ddd"><b>${escapeHtml(summary.start)}</b></td></tr>
      <tr><td style="padding:12px;border-bottom:1px solid #ddd;color:#666">部署边界</td><td style="padding:12px;border-bottom:1px solid #ddd"><b>${escapeHtml(summary.deployment)}</b></td></tr>
    </table>
    <p>下一步可以准备一条当前流程、少量真实样本、负责人和希望改善的指标。</p>
    <p><a href="https://forflow.ai/contact.html" style="color:#0d7b35">联系 ForFlow →</a></p>
  </div>`;

const internalHtml = (lead, summary) => `
  <div style="font-family:Arial,'PingFang SC',sans-serif;line-height:1.6;color:#111">
    <h2>ForFlow 官网新线索</h2>
    <p><b>来源：</b>${escapeHtml(lead.source_type)}</p>
    <p><b>邮箱：</b>${escapeHtml(lead.email)}</p>
    <p><b>联系人：</b>${escapeHtml(lead.name || '未填写')}</p>
    <p><b>公司：</b>${escapeHtml(lead.company || '未填写')}</p>
    <p><b>感兴趣的服务：</b>${escapeHtml(lead.service_interest || '未填写')}</p>
    <p><b>希望沟通时间：</b>${escapeHtml(lead.preferred_time || '未填写')}</p>
    <p><b>问题：</b>${escapeHtml(lead.problem || '未填写')}</p>
    ${summary ? `<p><b>诊断摘要：</b>${escapeHtml(summary.challenge)} / ${escapeHtml(summary.goal)} / ${escapeHtml(summary.start)}</p>` : ''}
  </div>`;

export default async (request, context) => {
  const rejected = assertSameOriginJson(request, 24_576);
  if (rejected) return rejected;

  let payload;
  try { payload = await request.json(); }
  catch (_) { return json({ ok: false, error: 'Invalid JSON.' }, 400); }

  if (payload.website) return json({ ok: true }, 202);
  if (!isUuid(payload.submission_id)) return json({ ok: false, error: '提交编号无效，请刷新页面后重试。' }, 400);
  const sourceType = SOURCE_TYPES.has(payload.source_type) ? payload.source_type : 'contact';
  const email = cleanText(payload.email, 254).toLowerCase();
  if (!EMAIL_RE.test(email)) return json({ ok: false, error: '请输入有效的工作邮箱。' }, 400);
  if (payload.assessment_id && !isUuid(payload.assessment_id)) return json({ ok: false, error: '诊断编号无效。' }, 400);
  if (sourceType === 'assessment_report' && !isUuid(payload.assessment_id)) return json({ ok: false, error: '没有找到本次诊断，请重新完成诊断后再发送。' }, 400);
  if (payload.consent !== true) return json({ ok: false, error: '请确认隐私说明后再提交。' }, 400);

  const now = new Date().toISOString();
  const lead = {
    submission_id: payload.submission_id,
    assessment_id: payload.assessment_id || null,
    source_type: sourceType,
    email,
    name: cleanText(payload.name, 100),
    company: cleanText(payload.company, 160),
    problem: cleanText(payload.problem, 2_000),
    service_interest: cleanText(payload.service_interest, 120),
    preferred_time: cleanText(payload.preferred_time, 160),
    source: cleanText(payload.source, 100),
    medium: cleanText(payload.medium, 100),
    campaign: cleanText(payload.campaign, 120),
    consent_at: now,
  };

  try {
    const inserted = await upsertRows('leads', lead, 'submission_id', true);
    const leadId = inserted?.[0]?.lead_id;
    if (!leadId) throw new Error('Lead insert did not return an id.');
    const purposes = [{ lead_id: leadId, purpose: 'contact_follow_up', policy_version: POLICY_VERSION, consented_at: now }];
    if (sourceType === 'assessment_report') purposes.push({ lead_id: leadId, purpose: 'assessment_report', policy_version: POLICY_VERSION, consented_at: now });
    await upsertRows('consent_records', purposes, 'lead_id,purpose,policy_version');

    let summary = null;
    if (lead.assessment_id) {
      const rows = await selectRows(`assessments?assessment_id=eq.${encodeURIComponent(lead.assessment_id)}&select=result_summary&limit=1`);
      summary = rows?.[0]?.result_summary || null;
    }

    const jobs = [sendEmail({
      to: 'hello@forflow.ai',
      subject: `ForFlow 官网新线索｜${lead.company || lead.email}`,
      html: internalHtml(lead, summary),
      replyTo: lead.email,
    })];
    if (sourceType === 'assessment_report' && summary) {
      jobs.push(sendEmail({ to: lead.email, subject: '你的 ForFlow AI 场景诊断结果', html: reportHtml(summary) }));
    }
    const emailConfigured = Boolean(env('RESEND_API_KEY') && env('LEADS_FROM_EMAIL'));
    const results = await Promise.allSettled(jobs);
    const sent = results.some((item) => item.status === 'fulfilled' && item.value.sent);
    if (sent) {
      const updates = { notification_sent_at: now };
      if (sourceType === 'assessment_report' && summary && results[1]?.status === 'fulfilled' && results[1].value.sent) updates.report_sent_at = now;
      await upsertLeadStatus(leadId, updates);
    }
    results.filter((item) => item.status === 'rejected').forEach((item) => console.error('lead email failed', context?.requestId || '', item.reason?.message || item.reason));

    return json({ ok: true, lead_id: leadId, notification: emailConfigured ? (sent ? 'sent' : 'failed') : 'not_configured' }, 201);
  } catch (error) {
    console.error('lead ingest failed', context?.requestId || '', error?.message || error);
    return json({ ok: false, error: '提交暂时不可用，请稍后重试或邮件联系 hello@forflow.ai。' }, 503);
  }
};

async function upsertLeadStatus(leadId, updates) {
  return supabaseRequest(`leads?lead_id=eq.${encodeURIComponent(leadId)}`, {
    method: 'PATCH',
    body: { ...updates, updated_at: new Date().toISOString() },
    prefer: 'return=minimal',
  });
}

export const config = {
  path: '/api/leads',
  rateLimit: { windowLimit: 5, windowSize: 60, aggregateBy: ['ip', 'domain'] },
};
