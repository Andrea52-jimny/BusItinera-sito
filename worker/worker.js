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

// ── Richieste demo: helper anti-abuso ────────────────────────────────────────
function clip(s, n) { return String(s == null ? '' : s).slice(0, n).trim(); }

// ── Richieste demo: validazione dei campi ────────────────────────────────────
// Lettere (anche accentate), apostrofo e trattino: niente cifre né simboli.
const LETTERE = "A-Za-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u024F";
const RE_NOME = new RegExp("^[" + LETTERE + "'\\-]+( [" + LETTERE + "'\\-]+)+$");

// Persona di riferimento: almeno due parole, solo lettere (+ ' e -).
function referenteValido(s) {
  const v = String(s || '').replace(/\s+/g, ' ').trim();
  if (v.length < 4 || v.length > 120) return false;
  if (!RE_NOME.test(v)) return false;
  const parti = v.split(' ');
  return parti.length >= 2 && parti.every(p => p.replace(/['\-]/g, '').length >= 2);
}

// Email: una sola chiocciola e almeno un punto nel dominio.
function emailValida(s) {
  const v = String(s || '').trim();
  if (!v || v.length > 160 || /\s/.test(v)) return false;
  const parti = v.split('@');
  if (parti.length !== 2) return false;              // esattamente una chiocciola
  const [locale, dominio] = parti;
  if (!/^[A-Za-z0-9._%+\-]+$/.test(locale)) return false;
  if (!/^[A-Za-z0-9.\-]+$/.test(dominio)) return false;
  if (dominio.indexOf('.') < 0) return false;        // almeno un punto
  if (/^[.\-]|[.\-]$|\.\./.test(dominio)) return false;
  return /\.[A-Za-z]{2,}$/.test(dominio);
}

// Telefono: solo cifre (con prefisso + e separatori di lettura), da 6 a 15 cifre.
function telefonoValido(s) {
  const v = String(s || '').trim();
  if (!v || v.length > 60) return false;
  if (!/^\+?[0-9 ./()\-]+$/.test(v)) return false;   // nessuna lettera, nessun simbolo estraneo
  const cifre = v.replace(/\D/g, '');
  return cifre.length >= 6 && cifre.length <= 15;
}

// Sito: almeno un punto, niente caratteri speciali (schema e / finale ammessi).
function sitoValido(s) {
  let v = String(s || '').trim();
  if (!v) return true;                               // campo facoltativo
  if (v.length > 160) return false;
  v = v.replace(/^https?:\/\//i, '').replace(/\/+$/, '');
  if (!/^[A-Za-z0-9.\-]+$/.test(v)) return false;
  if (v.indexOf('.') < 0) return false;
  if (/^[.\-]|[.\-]$|\.\./.test(v)) return false;
  return /\.[A-Za-z]{2,}$/.test(v);
}

// Rate limit per IP: max 5 richieste demo all'ora (contatore in KV con TTL).
async function demoRateOk(env, ip) {
  try {
    const key = 'rl:' + await sha256hex('demo|' + (ip || 'noip'));
    const cur = parseInt(await env.SUBS.get(key) || '0', 10) || 0;
    if (cur >= 5) return false;
    await env.SUBS.put(key, String(cur + 1), { expirationTtl: 3600 });
    return true;
  } catch (e) { return true; } // errore KV: non blocchiamo l'utente onesto
}

// Verifica Turnstile. Se TURNSTILE_SECRET non è impostato, il controllo è
// disattivato (ritorna true) così il form funziona anche prima di creare le chiavi.
async function turnstileOk(env, token, ip) {
  if (!env.TURNSTILE_SECRET) return true;
  if (!token) return false;
  try {
    const form = new URLSearchParams();
    form.append('secret', env.TURNSTILE_SECRET);
    form.append('response', token);
    if (ip) form.append('remoteip', ip);
    const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
    const d = await r.json();
    return !!(d && d.success);
  } catch (e) { return false; }
}

async function vapidJWT(endpoint, env) {
  const aud = new URL(endpoint).origin;
  const header = bytesToB64url(enc.encode(JSON.stringify({ typ: 'JWT', alg: 'ES256' })));
  const payload = bytesToB64url(enc.encode(JSON.stringify({
    aud, exp: Math.floor(Date.now() / 1000) + 12 * 3600,
    sub: env.VAPID_SUBJECT || 'mailto:busitinera@gmail.com'
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

      // ── Richieste demo ──────────────────────────────────────────────────
      // POST /api/demo  (pubblico): form del sito → coda in KV (prefisso demo:).
      if (path === '/api/demo' && req.method === 'POST') {
        const b = await req.json().catch(() => ({}));
        // Honeypot: se il campo trappola è pieno è un bot → fingi successo e scarta.
        if (b && b.hp) return json({ ok: true }, 200, env, req);
        const azienda = clip(b && b.azienda, 120), referente = clip(b && b.referente, 120);
        const email = clip(b && b.email, 160), telefono = clip(b && b.telefono, 60);
        const sito = clip(b && b.sito, 160), note = clip(b && b.note, 1000);
        if (!azienda || !referente || (!email && !telefono)) {
          return json({ error: 'invalid', message: 'Azienda, referente e almeno un contatto sono obbligatori.' }, 400, env, req);
        }
        if (!referenteValido(referente)) {
          return json({ error: 'referente', message: 'Indica nome e cognome della persona di riferimento, senza numeri né simboli.' }, 400, env, req);
        }
        if (email && !emailValida(email)) {
          return json({ error: 'email', message: "L'email non è valida: serve una sola chiocciola e un dominio con almeno un punto (es. info@azienda.it)." }, 400, env, req);
        }
        if (telefono && !telefonoValido(telefono)) {
          return json({ error: 'telefono', message: 'Il telefono deve contenere solo numeri (da 6 a 15 cifre), eventualmente con il prefisso internazionale.' }, 400, env, req);
        }
        if (sito && !sitoValido(sito)) {
          return json({ error: 'sito', message: 'Il sito non è valido: usa un indirizzo con almeno un punto e senza caratteri speciali (es. www.azienda.it).' }, 400, env, req);
        }
        const ip = req.headers.get('CF-Connecting-IP') || '';
        if (!(await turnstileOk(env, b && b.ts, ip))) {
          return json({ error: 'captcha', message: 'Verifica anti-bot non superata. Riprova.' }, 400, env, req);
        }
        if (!(await demoRateOk(env, ip))) {
          return json({ error: 'rate', message: "Troppe richieste da questo indirizzo. Riprova tra un'ora." }, 429, env, req);
        }
        const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
        await env.SUBS.put('demo:' + id, JSON.stringify({
          id, azienda, referente, email, telefono, sito, note,
          ts_created: new Date().toISOString(), ip
        }));
        return json({ ok: true }, 200, env, req);
      }

      // GET /api/demo  (Bearer SEND_SECRET): elenco richieste in coda (per la console).
      if (path === '/api/demo' && req.method === 'GET') {
        const auth = req.headers.get('Authorization') || '';
        if (!env.SEND_SECRET || auth !== 'Bearer ' + env.SEND_SECRET) return json({ error: 'unauthorized' }, 401, env, req);
        const out = []; let cursor;
        do {
          const list = await env.SUBS.list({ prefix: 'demo:', cursor });
          cursor = list.list_complete ? null : list.cursor;
          for (const k of list.keys) { const raw = await env.SUBS.get(k.name); if (raw) { try { out.push(JSON.parse(raw)); } catch (e) {} } }
        } while (cursor);
        out.sort((a, b) => (a.ts_created < b.ts_created ? 1 : -1)); // più recenti prima
        return json({ ok: true, requests: out }, 200, env, req);
      }

      // POST /api/demo/resolve  (Bearer SEND_SECRET): rimuove una richiesta dalla coda.
      if (path === '/api/demo/resolve' && req.method === 'POST') {
        const auth = req.headers.get('Authorization') || '';
        if (!env.SEND_SECRET || auth !== 'Bearer ' + env.SEND_SECRET) return json({ error: 'unauthorized' }, 401, env, req);
        const b = await req.json().catch(() => ({}));
        const id = clip(b && b.id, 64);
        if (!id) return json({ error: 'invalid' }, 400, env, req);
        await env.SUBS.delete('demo:' + id);
        return json({ ok: true }, 200, env, req);
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
