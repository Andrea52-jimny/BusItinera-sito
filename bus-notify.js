/*
 * bus-notify.js — Notifiche "novità" per il sito BusItinera.
 * - Inietta un pulsante campanella nella navbar (una riga di <script> per pagina).
 * - Android/desktop: iscrizione Web Push operativa (permesso + subscribe + invio al Worker).
 * - iOS: tutorial esplicativo "Aggiungi a Home" (le push su iOS richiedono l'app installata).
 * Same-origin, nessuna dipendenza esterna.
 *
 * ⚙️ CONFIGURA QUI l'indirizzo del Worker Cloudflare che salva le iscrizioni e invia le push.
 *    Es. "https://busitinera-push.tuo-account.workers.dev"  oppure  "https://busitinera.it"
 *    (se il Worker è servito sullo stesso dominio con route /api/*).
 */
(function () {
  'use strict';

  var WORKER_BASE = 'https://REPLACE-WITH-YOUR-WORKER.workers.dev'; // ← CAMBIA QUESTO
  var meta = document.querySelector('meta[name="bi-push"]');
  if (meta && meta.content) WORKER_BASE = meta.content;
  WORKER_BASE = WORKER_BASE.replace(/\/+$/, '');

  // Chiave pubblica VAPID (è pubblica: può stare nel client).
  var VAPID_PUBLIC = 'BC7tA5De-0L2nmqO0jKF4OnofzYP4_bw0S153PICUVCLquORRQbbQNh-ib9_W8LDI---l_labMBpw3vC1KdvjiM';

  // ── util ────────────────────────────────────────────────────────────────
  function isIOS() {
    var ua = navigator.userAgent || '';
    return /iPad|iPhone|iPod/.test(ua) || (navigator.platform === 'MacIntel' && (navigator.maxTouchPoints || 0) > 1);
  }
  function isStandalone() {
    return (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) || window.navigator.standalone === true;
  }
  function supported() {
    return ('serviceWorker' in navigator) && ('PushManager' in window) && ('Notification' in window);
  }
  function b64ToU8(s) {
    var pad = '='.repeat((4 - (s.length % 4)) % 4);
    var b = (s + pad).replace(/-/g, '+').replace(/_/g, '/');
    var raw = atob(b), a = new Uint8Array(raw.length);
    for (var i = 0; i < raw.length; i++) a[i] = raw.charCodeAt(i);
    return a;
  }

  var swReg = null;
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').then(function (r) { swReg = r; }).catch(function () {});
  }

  // ── stile (iniettato una volta) ──────────────────────────────────────────
  var css = '' +
  '.bi-bell{position:relative;display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border:1px solid var(--line2,#d6deea);background:#fff;border-radius:50%;cursor:pointer;color:#1f2b45;transition:border-color .2s,transform .2s}' +
  '.bi-bell:hover{border-color:#2563eb;transform:translateY(-1px)}' +
  '.bi-bell .bi-dot{position:absolute;top:8px;right:9px;width:8px;height:8px;border-radius:50%;background:#f97316;display:none}' +
  '.bi-bell.on .bi-dot{display:block;background:#059669}' +
  '.bi-pop{position:fixed;z-index:2000;width:320px;max-width:calc(100vw - 24px);background:#fff;border:1px solid #e6ecf3;border-radius:16px;box-shadow:0 24px 60px rgba(16,27,45,.18);padding:18px;font-family:inherit;color:#3b4a5e;display:none}' +
  '.bi-pop.open{display:block}' +
  '.bi-pop h4{font-size:1rem;font-weight:700;color:#0f1b2d;margin:0 0 6px}' +
  '.bi-pop p{font-size:.86rem;line-height:1.5;margin:0 0 12px;color:#6b7a90}' +
  '.bi-pop ol{margin:0 0 12px 18px;padding:0}.bi-pop li{font-size:.85rem;margin:5px 0;color:#3b4a5e}' +
  '.bi-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;width:100%;padding:11px 16px;border:none;border-radius:10px;background:#2563eb;color:#fff;font-weight:600;font-size:.92rem;cursor:pointer;font-family:inherit}' +
  '.bi-btn:hover{background:#1d4ed8}.bi-btn.sec{background:#f5f8fc;color:#0f1b2d;border:1px solid #d6deea}' +
  '.bi-note{font-size:.78rem;color:#8a929b;margin-top:10px}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  // ── pannello ─────────────────────────────────────────────────────────────
  var pop = document.createElement('div'); pop.className = 'bi-pop'; document.body.appendChild(pop);
  function closePop() { pop.classList.remove('open'); }
  document.addEventListener('click', function (e) {
    if (pop.classList.contains('open') && !pop.contains(e.target) && !e.target.closest('.bi-bell')) closePop();
  });

  function placePop(bell) {
    var r = bell.getBoundingClientRect();
    pop.style.top = (r.bottom + 10) + 'px';
    var left = Math.min(r.right - 320, window.innerWidth - 332);
    pop.style.left = Math.max(12, left) + 'px';
  }

  function render(bell) {
    var perm = ('Notification' in window) ? Notification.permission : 'unsupported';
    getSub().then(function (sub) {
      var html;
      if (isIOS() && !isStandalone()) {
        html = '<h4>🔔 Novità su iPhone/iPad</h4>' +
          '<p>Per ricevere le notifiche delle novità, aggiungi prima BusItinera alla schermata Home:</p>' +
          '<ol><li>Tocca <b>Condividi</b> nella barra di Safari</li><li>Scegli <b>“Aggiungi a Home”</b></li><li>Apri BusItinera dalla Home e tocca di nuovo la campanella per attivare</li></ol>' +
          '<button class="bi-btn sec" data-act="close">Ho capito</button>';
      } else if (!supported()) {
        html = '<h4>🔔 Notifiche non disponibili</h4><p>Questo browser non supporta le notifiche push. Prova con Chrome, Edge o Firefox aggiornati.</p><button class="bi-btn sec" data-act="close">Chiudi</button>';
      } else if (sub) {
        html = '<h4>✅ Notifiche attive</h4><p>Riceverai un avviso quando pubblichiamo una novità su BusItinera.</p><button class="bi-btn sec" data-act="off">Disattiva le notifiche</button>';
      } else if (perm === 'denied') {
        html = '<h4>🔕 Notifiche bloccate</h4><p>Hai bloccato le notifiche per questo sito. Riattivale dalle impostazioni del browser (lucchetto accanto all’indirizzo → Notifiche → Consenti), poi ricarica la pagina.</p><button class="bi-btn sec" data-act="close">Chiudi</button>';
      } else {
        html = '<h4>🔔 Resta aggiornato</h4><p>Attiva le notifiche per ricevere un avviso quando arriva una nuova versione o una novità di BusItinera. Niente spam, solo aggiornamenti importanti.</p><button class="bi-btn" data-act="on">Attiva le notifiche</button><div class="bi-note">Puoi disattivarle quando vuoi.</div>';
      }
      pop.innerHTML = html;
    });
  }

  function getSub() {
    if (!supported() || !swReg) return Promise.resolve(null);
    return navigator.serviceWorker.ready.then(function (r) { return r.pushManager.getSubscription(); }).catch(function () { return null; });
  }

  function subscribe() {
    return Notification.requestPermission().then(function (p) {
      if (p !== 'granted') return null;
      return navigator.serviceWorker.ready.then(function (r) {
        return r.pushManager.getSubscription().then(function (ex) {
          return ex || r.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64ToU8(VAPID_PUBLIC) });
        });
      }).then(function (sub) {
        var j = sub.toJSON();
        return fetch(WORKER_BASE + '/api/subscribe', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ endpoint: j.endpoint, keys: j.keys })
        }).then(function () { return sub; });
      });
    });
  }

  function unsubscribe() {
    return navigator.serviceWorker.ready.then(function (r) { return r.pushManager.getSubscription(); }).then(function (sub) {
      if (!sub) return;
      var ep = sub.endpoint;
      return sub.unsubscribe().then(function () {
        return fetch(WORKER_BASE + '/api/unsubscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ endpoint: ep }) }).catch(function () {});
      });
    });
  }

  pop.addEventListener('click', function (e) {
    var b = e.target.closest('[data-act]'); if (!b) return;
    var act = b.dataset.act, bell = document.querySelector('.bi-bell');
    if (act === 'close') return closePop();
    if (act === 'on') { b.textContent = 'Attivazione…'; b.disabled = true; subscribe().then(function (s) { refreshBell(); render(bell); }).catch(function () { render(bell); }); }
    if (act === 'off') { b.textContent = 'Disattivazione…'; b.disabled = true; unsubscribe().then(function () { refreshBell(); render(bell); }); }
  });

  function refreshBell() {
    var bell = document.querySelector('.bi-bell'); if (!bell) return;
    getSub().then(function (s) { bell.classList.toggle('on', !!s); });
  }

  // ── inietta la campanella nella nav ──────────────────────────────────────
  function injectBell() {
    var links = document.querySelector('.nav-links'); if (!links || document.querySelector('.bi-bell')) return;
    var bell = document.createElement('button');
    bell.className = 'bi-bell'; bell.type = 'button'; bell.setAttribute('aria-label', 'Notifiche novità');
    bell.innerHTML = '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg><span class="bi-dot"></span>';
    var cta = links.querySelector('.nav-cta');
    if (cta) links.insertBefore(bell, cta); else links.appendChild(bell);
    bell.addEventListener('click', function (e) {
      e.stopPropagation();
      if (pop.classList.contains('open')) return closePop();
      render(bell); placePop(bell); pop.classList.add('open');
    });
    window.addEventListener('resize', function () { if (pop.classList.contains('open')) placePop(bell); });
    refreshBell();
  }

  if (document.readyState !== 'loading') injectBell();
  else document.addEventListener('DOMContentLoaded', injectBell);
})();
