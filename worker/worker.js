/*
 * BusItinera — Worker notifiche "novità" (Cloudflare Workers + KV)
 *
 * Rotte:
 *   GET  /api/vapidPublicKey                          → { key }
 *   POST /api/subscribe    { endpoint, keys:{p256dh,auth} }   → salva in KV
 *   POST /api/unsubscribe  { endpoint }                        → rimuove da KV
 *   POST /api/send   (Authorization: Bearer <SEND_SECRET>)
 *        { title, body, url? }                                 → invia a tutti gli iscritti
 *
 * Binding richiesti (vedi wrangler.toml):
 *   KV namespace:  SUBS
 *   Variabili:     VAPID_PUBLIC, VAPID_SUBJECT, ALLOWED_ORIGIN
 *   Secret:        VAPID_PRIVATE, SEND_SECRET
 *
 * Web Push implementato con WebCrypto (nessuna dipendenza): VAPID JWT (ES256)
 * e cifratura del payload aes128gcm secondo RFC 8291 / RFC 8188.
 */

const enc = new TextEncoder();

function b64urlToBytes(s) {
  s = s.replace(/-/g, '+').replace(/_/g, '/');
  const pad = '='.repeat((4 - (s.length % 4)) % 4);
  const raw = atob(s + pad);
  const a = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i++) a[i] = raw.charCodeAt(i);
  return a;
}
function bytesToB64url(buf) {
  const a = new Uint8Array(buf);
  let s = '';
  for (let i = 0; i < a.length; i++) s += String.fromCharCode(a[i]);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function concat(...arrs) {
  let len = 0; arrs.forEach(a => len += a.length);
  const out = new Uint8Array(len); let o = 0;
  arrs.forEach(a => { out.set(a, o); o += a.length; });
  return out;
}
async function hkdf(salt, ikm, info, len) {
  const key = await crypto.subtle.importKey('raw', ikm, 'HKDF', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits({ name: 'HKDF', hash: 'SHA-256', salt, info }, key, len * 8);
  return new Uint8Array(bits);
}
async function sha256hex(str) {
  const h = await crypto.subtle.digest('SHA-256', enc.encode(str));
  return [...new Uint8Array(h)].map(b => b.toString(16).padStart(2, '0')).join('');
}

async function vapidJWT(endpoint, env) {
  const aud = new URL(endpoint).origin;
  const header = bytesToB64url(enc.encode(JSON.stringify({ typ: 'JWT', alg: 'ES256' })));
  const payload = bytesToB64url(enc.encode(JSON.stringify({
    aud, exp: Math.floor(Date.now() / 1000) + 12 * 3600,
    sub: env.VAPID_SUBJECT || 'mailto:ceolandrea006@gmail.com'
  })));
  const signingInput = header + '.' + payload;
  const pub = b64urlToBytes(env.VAPID_PUBLIC); // 0x04 || x(32) || y(32)
  const jwk = {
    kty: 'EC', crv: 'P-256',
    x: bytesToB64url(pub.slice(1, 33)),
    y: bytesToB64url(pub.slice(33, 65)),
    d: env.VAPID_PRIVATE, ext: true, key_ops: ['sign']
  };
  const key = await crypto.subtle.importKey('jwk', jwk, { name: 'ECDSA', namedCurve: 'P-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign({ name: 'ECDSA', hash: 'SHA-256' }, key, enc.encode(signingInput));
  return signingInput + '.' + bytesToB64url(sig);
}

async function encryptPayload(payloadBytes, p256dhB64, authB64) {
  const uaPub = b64urlToBytes(p256dhB64);   // 65 bytes
  const auth = b64urlToBytes(authB64);       // 16 bytes
  const asKeys = await crypto.subtle.generateKey({ name: 'ECDH', namedCurve: 'P-256' }, true, ['deriveBits']);
  const asPubRaw = new Uint8Array(await crypto.subtle.exportKey('raw', asKeys.publicKey)); // 65 bytes
  const uaKey = await crypto.subtle.importKey('raw', uaPub, { name: 'ECDH', namedCurve: 'P-256' }, false, []);
  const ecdh = new Uint8Array(await crypto.subtle.deriveBits({ name: 'ECDH', public: uaKey }, asKeys.privateKey, 256)); // 32
  // RFC 8291 §3.4
  const keyInfo = concat(enc.encode('WebPush: info\0'), uaPub, asPubRaw);
  const ikm = await hkdf(auth, ecdh, keyInfo, 32);
  // RFC 8188 aes128gcm
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const cek = await hkdf(salt, ikm, enc.encode('Content-Encoding: aes128gcm\0'), 16);
  const nonce = await hkdf(salt, ikm, enc.encode('Content-Encoding: nonce\0'), 12);
  const aesKey = await crypto.subtle.importKey('raw', cek, { name: 'AES-GCM' }, false, ['encrypt']);
  const plain = concat(payloadBytes, new Uint8Array([2])); // record unico, delimitatore 0x02
  const ct = new Uint8Array(await crypto.subtle.encrypt({ name: 'AES-GCM', iv: nonce, tagLength: 128 }, aesKey, plain));
  const rs = new Uint8Array([0, 0, 0x10, 0]); // record size 4096
  const header = concat(salt, rs, new Uint8Array([asPubRaw.length]), asPubRaw);
  return concat(header, ct);
}

async function sendOne(sub, message, env) {
  const jwt = await vapidJWT(sub.endpoint, env);
  const body = await encryptPayload(enc.encode(JSON.stringify(message)), sub.keys.p256dh, sub.keys.auth);
  return fetch(sub.endpoint, {
    method: 'POST',
    headers: {
      'Content-Encoding': 'aes128gcm',
      'Content-Type': 'application/octet-stream',
      'TTL': '2419200',
      'Authorization': 'vapid t=' + jwt + ', k=' + env.VAPID_PUBLIC
    },
    body
  });
}

// ── HTTP helpers ────────────────────────────────────────────────────────────
function cors(env, req) {
  const origin = env.ALLOWED_ORIGIN || '*';
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400'
  };
}
function json(data, status, env, req) {
  return new Response(JSON.stringify(data), { status: status || 200, headers: Object.assign({ 'Content-Type': 'application/json' }, cors(env, req)) });
}

export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url);
    const path = url.pathname;
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(env, req) });

    try {
      if (path === '/api/vapidPublicKey' && req.method === 'GET') {
        return json({ key: env.VAPID_PUBLIC }, 200, env, req);
      }

      if (path === '/api/subscribe' && req.method === 'POST') {
        const b = await req.json();
        if (!b || !b.endpoint || !b.keys || !b.keys.p256dh || !b.keys.auth) return json({ error: 'invalid' }, 400, env, req);
        const id = await sha256hex(b.endpoint);
        await env.SUBS.put('sub:' + id, JSON.stringify({ endpoint: b.endpoint, keys: b.keys, ts: Date.now() }));
        return json({ ok: true }, 200, env, req);
      }

      if (path === '/api/unsubscribe' && req.method === 'POST') {
        const b = await req.json();
        if (!b || !b.endpoint) return json({ error: 'invalid' }, 400, env, req);
        await env.SUBS.delete('sub:' + await sha256hex(b.endpoint));
        return json({ ok: true }, 200, env, req);
      }

      if (path === '/api/send' && req.method === 'POST') {
        const auth = req.headers.get('Authorization') || '';
        if (!env.SEND_SECRET || auth !== 'Bearer ' + env.SEND_SECRET) return json({ error: 'unauthorized' }, 401, env, req);
        const b = await req.json();
        const message = {
          title: (b && b.title) || 'BusItinera',
          body: (b && b.body) || '',
          url: (b && b.url) || '/novita.html',
          tag: (b && b.tag) || 'busitinera-novita'
        };
        let sent = 0, gone = 0, failed = 0;
        let cursor;
        do {
          const list = await env.SUBS.list({ prefix: 'sub:', cursor });
          cursor = list.list_complete ? null : list.cursor;
          for (const k of list.keys) {
            const raw = await env.SUBS.get(k.name);
            if (!raw) continue;
            const sub = JSON.parse(raw);
            try {
              const r = await sendOne(sub, message, env);
              if (r.status === 404 || r.status === 410) { await env.SUBS.delete(k.name); gone++; }
              else if (r.status >= 200 && r.status < 300) sent++;
              else failed++;
            } catch (e) { failed++; }
          }
        } while (cursor);
        return json({ ok: true, sent, gone, failed }, 200, env, req);
      }

      if (path === '/' || path === '') {
        return new Response('BusItinera push worker attivo.', { status: 200, headers: { 'Content-Type': 'text/plain' } });
      }
      return json({ error: 'not_found' }, 404, env, req);
    } catch (e) {
      return json({ error: 'server_error', detail: String(e && e.message || e) }, 500, env, req);
    }
  }
};
