const encoder = new TextEncoder();

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

  const expected = Netlify.env.get('SITE_GATE_PASSWORD');
  if (!expected) return json({ message: '访问码服务尚未配置。' }, 503);

  let code = '';
  try {
    ({ code = '' } = await request.json());
  } catch (_) {
    return json({ message: '请求格式不正确。' }, 400);
  }

  if (!secureEqual(code.trim(), expected)) return json({ message: '访问码不正确，请确认后重试。' }, 401);

  const token = await sha256(`forflow-gate:${expected}`);
  return json({ ok: true }, 200, {
    'Set-Cookie': `ff_gate=${token}; Path=/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax`,
  });
};
