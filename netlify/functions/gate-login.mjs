const encoder = new TextEncoder();
const COOKIE_NAME = '__Host-ff_gate';
const MAX_BODY_BYTES = 1024;
const COMPROMISED_PASSWORD_HASH = '2e23e9d8401eebbfb610a424c7e4d5cf24118192d3836c74d41f536c8d456168';

const sha256 = async (value) => {
  const bytes = await crypto.subtle.digest('SHA-256', encoder.encode(value));
  return [...new Uint8Array(bytes)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
};

const secureEqual = (left, right) => {
  const a = String(left || '');
  const b = String(right || '');
  let mismatch = a.length ^ b.length;
  const length = Math.max(a.length, b.length);
  for (let index = 0; index < length; index += 1) {
    mismatch |= (a.charCodeAt(index) || 0) ^ (b.charCodeAt(index) || 0);
  }
  return mismatch === 0;
};

const json = (body, status, headers = {}) => Response.json(body, {
  status,
  headers: { 'Cache-Control': 'no-store', ...headers },
});

export default async (request) => {
  if (request.method !== 'POST') return json({ message: 'Method not allowed.' }, 405, { Allow: 'POST' });

  const requestUrl = new URL(request.url);
  const origin = request.headers.get('origin');
  if (origin && origin !== requestUrl.origin) return json({ message: '请求来源不被允许。' }, 403);

  const contentType = request.headers.get('content-type') || '';
  if (!contentType.toLowerCase().includes('application/json')) return json({ message: '请求格式不正确。' }, 415);

  const contentLength = Number(request.headers.get('content-length') || 0);
  if (Number.isFinite(contentLength) && contentLength > MAX_BODY_BYTES) return json({ message: '请求内容过大。' }, 413);

  const expected = Netlify.env.get('SITE_GATE_PASSWORD');
  if (!expected) return json({ message: '访问码服务尚未配置。' }, 503);
  if (secureEqual(await sha256(expected), COMPROMISED_PASSWORD_HASH)) {
    return json({ message: '访问码已停用，请联系 ForFlow 团队获取新码。' }, 503);
  }

  let code = '';
  try {
    ({ code = '' } = await request.json());
  } catch (_) {
    return json({ message: '请求格式不正确。' }, 400);
  }

  if (typeof code !== 'string' || code.length > 256) return json({ message: '请求格式不正确。' }, 400);
  if (!secureEqual(code.trim(), expected)) return json({ message: '访问码不正确，请确认后重试。' }, 401);

  const token = await sha256(`forflow-gate:${expected}`);
  return json({ ok: true }, 200, {
    'Set-Cookie': `${COOKIE_NAME}=${token}; Path=/; Max-Age=86400; HttpOnly; Secure; SameSite=Lax`,
  });
};

export const config = {
  path: '/api/gate-login',
  rateLimit: {
    windowLimit: 5,
    windowSize: 60,
    aggregateBy: ['ip', 'domain'],
  },
};
