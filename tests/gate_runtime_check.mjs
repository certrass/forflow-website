import assert from 'node:assert/strict';

const testPassword = 'test-only-never-deploy-7mK9!';
globalThis.Netlify = { env: { get: (name) => name === 'SITE_GATE_PASSWORD' ? testPassword : undefined } };

const { default: login } = await import('../netlify/functions/gate-login.mjs');
const { default: gate } = await import('../netlify/edge-functions/auth-gate.mjs');

const wrong = await login(new Request('https://forflow.ai/.netlify/functions/gate-login', {
  method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ code: 'wrong' }),
}));
assert.equal(wrong.status, 401);

const correct = await login(new Request('https://forflow.ai/.netlify/functions/gate-login', {
  method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ code: testPassword }),
}));
assert.equal(correct.status, 200);
const cookie = correct.headers.get('set-cookie');
assert.match(cookie, /__Host-ff_gate=[a-f0-9]{64}/);
assert.match(cookie, /HttpOnly/);
assert.match(cookie, /Secure/);
const token = cookie.match(/__Host-ff_gate=([a-f0-9]{64})/)[1];

const next = () => new Response('allowed', { status: 200 });
const blocked = await gate(new Request('https://forflow.ai/contact.html'), { cookies: { get: () => undefined }, next });
assert.equal(blocked.status, 302);
assert.match(blocked.headers.get('location'), /landing\.html\?next=%2Fcontact\.html/);
assert.equal(blocked.headers.get('x-content-type-options'), 'nosniff');

const blockedAsset = await gate(new Request('https://forflow.ai/search-index.json'), { cookies: { get: () => undefined }, next });
assert.equal(blockedAsset.status, 302);
assert.match(blockedAsset.headers.get('location'), /landing\.html\?next=%2Fsearch-index\.json/);

const blockedInternalRoute = await gate(new Request('https://forflow.ai/.netlify/unknown-internal-path'), { cookies: { get: () => undefined }, next });
assert.equal(blockedInternalRoute.status, 302);

const publicQrRoute = await gate(new Request('https://forflow.ai/q/demo'), { cookies: { get: () => undefined }, next });
assert.equal(publicQrRoute.status, 200);

const allowed = await gate(new Request('https://forflow.ai/contact'), { cookies: { get: () => token }, next });
assert.equal(allowed.status, 200);
assert.equal(await allowed.text(), 'allowed');
assert.equal(allowed.headers.get('cache-control'), 'private, no-store, max-age=0');
assert.equal(allowed.headers.get('x-robots-tag'), 'noindex, nofollow, noarchive');

const publicStyle = await gate(new Request('https://forflow.ai/styles.css'), { cookies: { get: () => undefined }, next });
assert.equal(publicStyle.status, 200);

const landing = await gate(new Request('https://forflow.ai/landing.html'), { cookies: { get: () => undefined }, next });
assert.equal(landing.status, 200);

const reset = await gate(new Request('https://forflow.ai/landing.html?reset=1'), { cookies: { get: () => token }, next });
assert.equal(reset.status, 302);
assert.equal(reset.headers.get('location'), '/landing.html');
assert.match(reset.headers.get('set-cookie'), /__Host-ff_gate=;/);
assert.match(reset.headers.get('set-cookie'), /Max-Age=0/);
assert.match(reset.headers.get('cache-control'), /(?:^|,\s*)no-store(?:,|$)/);

console.log('OK: wrong code is rejected, correct code sets a secure cookie, edge access is enforced, and reset clears access.');
