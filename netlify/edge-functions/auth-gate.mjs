const encoder = new TextEncoder();
const COOKIE_NAME = '__Host-ff_gate';
const PUBLIC_PATHS = new Set([
  '/landing',
  '/landing.html',
  '/gate-client.js',
  '/styles.css',
  '/robots.txt',
  '/api/gate-login',
  '/assets/forflow-mark.png',
  '/assets/forflow-lockup-transparent.png',
  '/assets/invite/forflow-private-preview.jpg',
]);
const HTML_CSP = [
  "default-src 'self'",
  "base-uri 'self'",
  "connect-src 'self' https://cloudflareinsights.com",
  "font-src 'self' data:",
  "form-action 'self'",
  "frame-ancestors 'none'",
  "frame-src 'self'",
  "img-src 'self' data:",
  "media-src 'self'",
  "object-src 'none'",
  "script-src 'self' https://static.cloudflareinsights.com",
  "style-src 'self' 'unsafe-inline'",
  'upgrade-insecure-requests',
].join('; ');

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

const isProtectedResource = (pathname) => {
  if (PUBLIC_PATHS.has(pathname)) return false;
  if (pathname === '/.netlify/functions/gate-login') return false;
  if (pathname === '/.netlify/functions/q' || pathname.startsWith('/.netlify/functions/q/')) return false;
  if (pathname.startsWith('/q/')) return false;
  return true;
};

const appendVary = (headers, value) => {
  const current = headers.get('Vary');
  const values = new Set((current || '').split(',').map((item) => item.trim()).filter(Boolean));
  values.add(value);
  headers.set('Vary', [...values].join(', '));
};

const harden = (response, pathname, { privateContent = false } = {}) => {
  const headers = new Headers(response.headers);
  const contentType = headers.get('content-type') || '';
  const isHtml = contentType.includes('text/html') || pathname === '/' || pathname === '/landing' || pathname.endsWith('.html');
  const isPdf = contentType.includes('application/pdf') || pathname.endsWith('.pdf');

  headers.set('Strict-Transport-Security', 'max-age=31536000');
  headers.set('X-Content-Type-Options', 'nosniff');
  headers.set('Referrer-Policy', 'no-referrer');
  headers.set('X-Robots-Tag', 'noindex, nofollow, noarchive');
  headers.set('X-Permitted-Cross-Domain-Policies', 'none');
  headers.set('Cross-Origin-Resource-Policy', 'same-origin');

  if (isHtml) {
    headers.set('Content-Security-Policy', HTML_CSP);
    headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=(), payment=(), usb=()');
    headers.set('Cross-Origin-Opener-Policy', 'same-origin');
    headers.set('X-Frame-Options', 'DENY');
  } else if (isPdf) {
    headers.set('Content-Security-Policy', "default-src 'none'; frame-ancestors 'self'");
    headers.set('X-Frame-Options', 'SAMEORIGIN');
  }

  if (privateContent || pathname === '/landing' || pathname === '/landing.html' || pathname === '/api/gate-login') {
    headers.set('Cache-Control', 'private, no-store, max-age=0');
    appendVary(headers, 'Cookie');
  }

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
};

export default async (request, context) => {
  const url = new URL(request.url);
  const isLanding = url.pathname === '/landing' || url.pathname === '/landing.html';

  if (isLanding && url.searchParams.get('reset') === '1') {
    return harden(new Response(null, {
      status: 302,
      headers: {
        Location: '/landing.html',
        'Set-Cookie': `${COOKIE_NAME}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`,
      },
    }), url.pathname, { privateContent: true });
  }

  if (!isProtectedResource(url.pathname)) {
    const response = await context.next();
    return harden(response, url.pathname, { privateContent: isLanding || url.pathname === '/api/gate-login' });
  }

  const expected = Netlify.env.get('SITE_GATE_PASSWORD');
  const provided = context.cookies.get(COOKIE_NAME);
  if (expected && provided) {
    const token = await sha256(`forflow-gate:${expected}`);
    if (secureEqual(provided, token)) {
      const response = await context.next();
      return harden(response, url.pathname, { privateContent: true });
    }
  }

  const login = new URL('/landing.html', url.origin);
  login.searchParams.set('next', `${url.pathname}${url.search}`);
  return harden(Response.redirect(login, 302), url.pathname, { privateContent: true });
};
