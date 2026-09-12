import {
  assertSameOriginJson,
  cleanText,
  isUuid,
  json,
  safeDate,
  safeStringArray,
  upsertRows,
} from './_shared/site-data.mjs';

const CHALLENGES = new Set(['customer', 'marketing', 'knowledge', 'operations', 'finance', 'hr']);
const GOALS = new Set(['speed', 'cost', 'revenue', 'quality', 'experience', 'risk']);
const CONSTRAINTS = new Set(['sensitive', 'audit', 'integration', 'multilingual', 'budget', 'human']);
const READINESS = new Set(['idea', 'process', 'data', 'pilot']);
const DEPLOYMENTS = new Set(['cloud', 'hybrid', 'private']);
const TIMELINES = new Set(['30d', 'quarter', 'roadmap']);
const TEAM_SIZES = new Set(['small', 'medium', 'large']);
const HR_STAGES = new Set(['recruit', 'onboard', 'service', 'learn', 'performance', 'analytics']);

const oneOf = (value, allowed) => {
  const clean = cleanText(value, 40);
  return allowed.has(clean) ? clean : '';
};

const labels = {
  challenge: {
    customer: '客户触达与服务', marketing: '营销与内容增长', knowledge: '企业知识与决策',
    operations: '运营流程自动化', finance: '经营分析与财务', hr: '人才与组织效率',
  },
  goal: {
    speed: '缩短处理时间', cost: '降低成本', revenue: '增加收入', quality: '提高质量',
    experience: '改善体验', risk: '降低风险',
  },
};

const summaryFor = (row) => ({
  challenge: row.challenges.map((key) => labels.challenge[key] || key).join(' · ') || '待确认',
  goal: row.goals.map((key) => labels.goal[key] || key).join(' · ') || '待确认',
  start: row.timeline === '30d' ? '2 周场景验证' : row.timeline === 'quarter' ? '4–8 周分阶段试点' : '分阶段路线图',
  deployment: row.deployment === 'private' ? '私有化优先' : row.deployment === 'cloud' ? '云端快速起步' : '混合部署优先',
});

export default async (request, context) => {
  const rejected = assertSameOriginJson(request, 16_384);
  if (rejected) return rejected;

  let payload;
  try { payload = await request.json(); }
  catch (_) { return json({ ok: false, error: 'Invalid JSON.' }, 400); }

  if (!isUuid(payload.assessment_id) || !isUuid(payload.session_id)) {
    return json({ ok: false, error: 'Invalid assessment or session.' }, 400);
  }

  const row = {
    assessment_id: payload.assessment_id,
    session_id: payload.session_id,
    status: 'complete',
    challenges: safeStringArray(payload.challenge, CHALLENGES, 2),
    goals: safeStringArray(payload.goal, GOALS, 2),
    constraints: safeStringArray(payload.constraint, CONSTRAINTS, 6),
    readiness: oneOf(payload.readiness, READINESS),
    deployment: oneOf(payload.deployment, DEPLOYMENTS),
    timeline: oneOf(payload.timeline, TIMELINES),
    team_size: oneOf(payload.teamSize, TEAM_SIZES),
    industry: cleanText(payload.industry, 80),
    hr_stage: oneOf(payload.hrStage, HR_STAGES),
    completed_at: safeDate(payload.completed_at) || new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
  row.result_summary = summaryFor(row);

  const answers = [
    ['challenge', row.challenges], ['goal', row.goals], ['constraint', row.constraints],
    ['readiness', row.readiness], ['deployment', row.deployment], ['timeline', row.timeline],
    ['teamSize', row.team_size], ['industry', row.industry], ['hrStage', row.hr_stage],
  ].filter(([, value]) => Array.isArray(value) ? value.length : Boolean(value))
    .map(([field_key, value_json]) => ({ assessment_id: row.assessment_id, field_key, value_json }));

  try {
    await upsertRows('assessments', row, 'assessment_id');
    if (answers.length) await upsertRows('assessment_answers', answers, 'assessment_id,field_key');
    return json({ ok: true, assessment_id: row.assessment_id, summary: row.result_summary }, 201);
  } catch (error) {
    console.error('assessment ingest failed', context?.requestId || '', error?.message || error);
    return json({ ok: false, error: 'Assessment storage is unavailable.' }, 503);
  }
};

export const config = {
  path: '/api/assessments',
  rateLimit: { windowLimit: 30, windowSize: 60, aggregateBy: ['ip', 'domain'] },
};
