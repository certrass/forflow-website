import {
  assertSameOriginJson,
  cleanText,
  insertRows,
  isUuid,
  json,
  safeDate,
} from './_shared/site-data.mjs';

const EVENT_NAMES = new Set([
  'page_view',
  'service_view',
  'case_view',
  'navigator_start',
  'navigator_step_complete',
  'navigator_complete',
  'result_sort',
  'result_service_click',
  'contact_start',
  'contact_submit',
]);
const PROPERTY_KEYS = new Set([
  'step',
  'sort_mode',
  'service_key',
  'case_key',
  'source_type',
  'result_count',
  'challenge_count',
  'goal_count',
]);

const cleanProperties = (value) => {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return {};
  const output = {};
  for (const [key, raw] of Object.entries(value)) {
    if (!PROPERTY_KEYS.has(key)) continue;
    if (typeof raw === 'number' && Number.isFinite(raw)) output[key] = raw;
    else if (typeof raw === 'boolean') output[key] = raw;
    else output[key] = cleanText(raw, 80);
  }
  return output;
};

const routeOnly = (value) => {
  try {
    const url = new URL(String(value || ''), 'https://forflow.ai');
    return cleanText(url.pathname, 180) || '/';
  } catch (_) {
    return '/';
  }
};

export default async (request, context) => {
  const rejected = assertSameOriginJson(request, 8_192);
  if (rejected) return rejected;

  let payload;
  try { payload = await request.json(); }
  catch (_) { return json({ ok: false, error: 'Invalid JSON.' }, 400); }

  const eventName = cleanText(payload.event_name, 60);
  if (!EVENT_NAMES.has(eventName)) return json({ ok: false, error: 'Unknown event.' }, 400);
  if (!isUuid(payload.session_id)) return json({ ok: false, error: 'Invalid session.' }, 400);
  if (payload.assessment_id && !isUuid(payload.assessment_id)) return json({ ok: false, error: 'Invalid assessment.' }, 400);

  const row = {
    session_id: payload.session_id,
    assessment_id: payload.assessment_id || null,
    event_name: eventName,
    page_key: cleanText(payload.page_key, 100),
    route: routeOnly(payload.route),
    referrer_host: cleanText(payload.referrer_host, 160),
    source: cleanText(payload.source, 100),
    medium: cleanText(payload.medium, 100),
    campaign: cleanText(payload.campaign, 120),
    properties: cleanProperties(payload.properties),
    occurred_at: safeDate(payload.occurred_at),
    netlify_request_id: cleanText(context?.requestId, 120),
  };

  try {
    await insertRows('website_events', row);
    return json({ ok: true }, 202);
  } catch (error) {
    console.error('website event ingest failed', error?.message || error);
    return json({ ok: false, error: 'Event storage is unavailable.' }, 503);
  }
};

export const config = {
  path: '/api/events',
  rateLimit: { windowLimit: 120, windowSize: 60, aggregateBy: ['ip', 'domain'] },
};
