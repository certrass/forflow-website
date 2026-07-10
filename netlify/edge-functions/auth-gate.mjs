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
  for (let index = 0; index < length; index += 1) mismatch |= (a.charCodeAt(index) || 0) ^ (b.charCodeAt(index) || 0);
  return mismatch === 0;
};

const isProtectedDocument = (pathname) => {
  if (pathname === '/landing' || pathname === '/landing.html') return false;
  if (pathname.startsWith('/.netlify/') || pathname.startsWith('/q/')) return false;
  const finalSegment = pathname.split('/').pop() || '';
  const hasExtension = /\.[a-z0-9]+$/i.test(finalSegment);
  return pathname === '/' || pathname.endsWith('.html') || !hasExtension;
};

export default async (request, context) => {
  const url = new URL(request.url);
  if (!isProtectedDocument(url.pathname)) return context.next();

  const expected = Netlify.env.get('SITE_GATE_PASSWORD');
  const provided = context.cookies.get('ff_gate');
  if (expected && provided) {
    const token = await sha256(`forflow-gate:${expected}`);
    if (secureEqual(provided, token)) return context.next();
  }

  const login = new URL('/landing.html', url.origin);
  login.searchParams.set('next', `${url.pathname}${url.search}`);
  return Response.redirect(login, 302);
};
