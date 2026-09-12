const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const read = (file) => fs.readFileSync(path.join(ROOT, file), 'utf8');
const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const landing = read('landing.html');
const client = read('gate-client.js');
const login = read('netlify/functions/gate-login.mjs');
const edge = read('netlify/edge-functions/auth-gate.mjs');
const script = read('script.js');
const config = read('netlify.toml');

assert(landing.includes('data-gate'), 'landing page should mount the access-code gate');
assert(/data-gate-code/.test(landing) && /type="password"/.test(landing), 'landing page should collect the access code as a password');
assert(landing.includes('gate-client.js'), 'landing page should load the gate client');
assert(/<form[^>]+action="\/api\/gate-login"[^>]+method="post"/.test(landing), 'landing form should fail closed with POST when JavaScript is unavailable');
assert(client.includes("fetch('/api/gate-login'"), 'gate client should use the rate-limited login path');
assert(!/const\s+(?:ACCESS|INVITE|GATE)_?(?:CODE|PASSWORD)\s*=/.test(`${landing}\n${client}\n${script}`), 'access code must not be embedded in browser source');
assert(login.includes("Netlify.env.get('SITE_GATE_PASSWORD')"), 'server login should read the access code from Netlify environment');
assert(login.includes('HttpOnly') && login.includes('SameSite=Lax'), 'successful gate login should issue a protected cookie');
assert(edge.includes("Netlify.env.get('SITE_GATE_PASSWORD')") && edge.includes("context.cookies.get(COOKIE_NAME)"), 'edge gate should verify the protected cookie');
assert(edge.includes('PUBLIC_PATHS') && edge.includes('isProtectedResource'), 'edge gate should protect all non-public resources, not only HTML documents');
assert(edge.includes("url.searchParams.get('reset') === '1'") && edge.includes('Max-Age=0'), 'edge gate should clear access through landing.html?reset=1');
assert(edge.includes('Content-Security-Policy') && edge.includes('X-Content-Type-Options'), 'edge gate should add browser security headers');
assert(login.includes("path: '/api/gate-login'") && login.includes('rateLimit'), 'server login should define a per-path rate limit');
assert(login.includes('__Host-ff_gate') && login.includes('Max-Age=86400'), 'server login should issue a host-only one-day cookie');
assert(login.includes('COMPROMISED_PASSWORD_HASH'), 'server login should fail closed for the leaked legacy password');
assert(config.includes('function = "auth-gate"'), 'Netlify config should register the edge gate');

console.log('OK: server-side access-code login, protected cookie, and edge document gate are wired.');
