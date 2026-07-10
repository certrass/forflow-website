import assert from 'node:assert/strict';

globalThis.Netlify = { env: { get: (name) => name === 'SITE_GATE_PASSWORD' ? 'forflow2026' : undefined } };

const { default: login } = await import('../netlify/functions/gate-login.mjs');
const { default: gate } = await import('../netlify/edge-functions/auth-gate.mjs');

const wrong = await login(new Request('https://forflow.ai/.netlify/functions/gate-login', {
  method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ code: 'wrong' }),
}));
assert.equal(wrong.status, 401);

const correct = await login(new Request('https://forflow.ai/.netlify/functions/gate-login', {
  method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ code: 'forflow2026' }),
}));
assert.equal(correct.status, 200);
const cookie = correct.headers.get('set-cookie');
assert.match(cookie, /ff_gate=[a-f0-9]{64}/);
assert.match(cookie, /HttpOnly/);
assert.match(cookie, /Secure/);
const token = cookie.match(/ff_gate=([a-f0-9]{64})/)[1];

const next = () => new Response('allowed', { status: 200 });
const blocked = await gate(new Request('https://forflow.ai/contact.html'), { cookies: { get: () => undefined }, next });
assert.equal(blocked.status, 302);
assert.match(blocked.headers.get('location'), /landing\.html\?next=%2Fcontact\.html/);

const allowed = await gate(new Request('https://forflow.ai/contact'), { cookies: { get: () => token }, next });
assert.equal(allowed.status, 200);
assert.equal(await allowed.text(), 'allowed');

const landing = await gate(new Request('https://forflow.ai/landing.html'), { cookies: { get: () => undefined }, next });
assert.equal(landing.status, 200);

console.log('OK: wrong code is rejected, correct code sets a secure cookie, and edge access is enforced.');
