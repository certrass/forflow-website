import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import eventsHandler from '../netlify/functions/events.mjs';
import assessmentsHandler from '../netlify/functions/assessments.mjs';
import leadsHandler from '../netlify/functions/leads.mjs';

const sessionId = '11111111-1111-4111-8111-111111111111';
const assessmentId = '22222222-2222-4222-8222-222222222222';
const submissionId = '33333333-3333-4333-8333-333333333333';
const leadId = '44444444-4444-4444-8444-444444444444';
const calls = [];

globalThis.Netlify = {
  env: {
    get(name) {
      return {
        SUPABASE_URL: 'https://db.example.test',
        SUPABASE_SECRET_KEY: 'sb_secret_test-only',
      }[name] || '';
    },
  },
};

globalThis.fetch = async (url, options = {}) => {
  const call = { url: String(url), options, body: options.body ? JSON.parse(options.body) : null };
  calls.push(call);
  assert.equal(options.headers.apikey, 'sb_secret_test-only', 'Supabase secret key must use the apikey header');
  assert.equal(options.headers.Authorization, undefined, 'sb_secret keys must not use Authorization Bearer');
  if (call.url.includes('/leads?')) {
    return Response.json([{ lead_id: leadId }], { status: 201 });
  }
  if (call.url.includes('/assessments?assessment_id=eq.')) {
    return Response.json([{ result_summary: { challenge: '运营流程', goal: '缩短时间', start: '2 周验证', deployment: '混合部署' } }]);
  }
  return new Response(null, { status: 204 });
};

const post = (path, body, headers = {}) => new Request(`https://forflow.ai${path}`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', ...headers },
  body: JSON.stringify(body),
});

let response = await eventsHandler(post('/api/events', {
  event_name: 'email_captured', session_id: sessionId,
}), { requestId: 'invalid-event' });
assert.equal(response.status, 400, 'unknown product events must be rejected');
assert.equal(calls.length, 0, 'rejected events must not reach storage');

response = await eventsHandler(post('/api/events', {
  event_name: 'page_view',
  session_id: sessionId,
  route: '/index.html?email=secret@example.com',
  properties: { email: 'secret@example.com', service_key: 'audit' },
}), { requestId: 'event-ok' });
assert.equal(response.status, 202);
const eventCall = calls.at(-1);
assert.equal(eventCall.body.route, '/index.html', 'event route must drop its query string');
assert.deepEqual(eventCall.body.properties, { service_key: 'audit' }, 'event properties must use the allowlist');
assert.equal(JSON.stringify(eventCall.body).includes('secret@example.com'), false, 'event rows must not contain email');

response = await eventsHandler(post('/api/events', {
  event_name: 'page_view', session_id: sessionId,
}, { Origin: 'https://evil.example' }), { requestId: 'cross-origin' });
assert.equal(response.status, 403, 'cross-origin writes must be rejected');

response = await assessmentsHandler(post('/api/assessments', {
  assessment_id: assessmentId,
  session_id: sessionId,
  challenge: ['operations'],
  goal: ['speed'],
  constraint: ['human'],
  readiness: 'process',
  deployment: 'hybrid',
  timeline: '30d',
  teamSize: 'medium',
  industry: '制造业',
  email: 'must-not-be-stored@example.com',
}), { requestId: 'assessment-ok' });
assert.equal(response.status, 201);
const assessmentCalls = calls.slice(-2);
assert.equal(assessmentCalls[0].url.includes('/assessments?'), true);
assert.equal(assessmentCalls[1].url.includes('/assessment_answers?'), true);
assert.equal(JSON.stringify(assessmentCalls).includes('must-not-be-stored@example.com'), false, 'assessment tables must not contain email');

response = await leadsHandler(post('/api/leads', {
  submission_id: submissionId,
  assessment_id: assessmentId,
  source_type: 'assessment_report',
  email: 'buyer@example.com',
  company: '示例公司',
  consent: true,
}), { requestId: 'lead-ok' });
assert.equal(response.status, 201);
const result = await response.json();
assert.equal(result.notification, 'not_configured');
const leadCall = calls.find((call) => call.url.includes('/leads?'));
assert.equal(leadCall.body.email, 'buyer@example.com', 'email belongs in leads');
assert.equal(leadCall.url.includes('on_conflict=submission_id'), true, 'lead submission must be idempotent');

const sourceFiles = await Promise.all([
  readFile(new URL('../script.js', import.meta.url), 'utf8'),
  readFile(new URL('../netlify/functions/events.mjs', import.meta.url), 'utf8'),
  readFile(new URL('../supabase/migrations/20260711053849_website_data_foundation.sql', import.meta.url), 'utf8'),
]);
assert.equal(sourceFiles[0].includes('SUPABASE_SECRET_KEY'), false, 'client code must not contain a Supabase secret variable');
for (const eventName of ['page_view','service_view','case_view','navigator_start','navigator_step_complete','navigator_complete','result_sort','result_service_click','contact_start','contact_submit']) {
  assert.equal(sourceFiles[1].includes(`'${eventName}'`), true, `event allowlist missing ${eventName}`);
  assert.equal(sourceFiles[2].includes(`'${eventName}'`), true, `database constraint missing ${eventName}`);
}
for (const table of ['website_events', 'assessments', 'assessment_answers', 'leads', 'consent_records']) {
  assert.equal(sourceFiles[2].includes(`alter table public.${table} enable row level security`), true, `${table} must enable RLS`);
  assert.equal(sourceFiles[2].includes(`revoke all on table public.${table} from anon, authenticated`), true, `${table} must deny browser roles`);
}

console.log('OK: website data foundation validation, isolation, idempotency, and secret handling passed.');
