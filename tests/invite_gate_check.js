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
assert(!landing.includes('FLOW2026') && !script.includes('FLOW2026'), 'legacy invite code must not remain in public source');
assert(!client.includes('forflow2026'), 'access code must not be embedded in the browser client');
assert(login.includes("Netlify.env.get('SITE_GATE_PASSWORD')"), 'server login should read the access code from Netlify environment');
assert(login.includes('HttpOnly') && login.includes('SameSite=Lax'), 'successful gate login should issue a protected cookie');
assert(edge.includes("Netlify.env.get('SITE_GATE_PASSWORD')") && edge.includes("context.cookies.get('ff_gate')"), 'edge gate should verify the protected cookie');
assert(edge.includes("pathname === '/'") && edge.includes("pathname === '/landing'"), 'edge gate should protect documents but leave the gate page reachable');
assert(config.includes('function = "auth-gate"'), 'Netlify config should register the edge gate');

console.log('OK: server-side access-code login, protected cookie, and edge document gate are wired.');
