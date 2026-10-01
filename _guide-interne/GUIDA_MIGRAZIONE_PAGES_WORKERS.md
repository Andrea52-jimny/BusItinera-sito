# Migrazione del sito da Cloudflare Pages a Workers

Stato attuale: il sito è un progetto **Cloudflare Pages** (`busitinera-sito`), deploy automatico
sul push a `main` del repo GitHub, dominio **busitinera.it**.

Con i **Workers Static Assets** un singolo Worker può servire il sito statico **e** far girare
il codice delle notifiche (le rotte `/api/*`): una sola pubblicazione, un solo dominio.

> Non è obbligatorio migrare: puoi tenere il sito su Pages e il Worker delle notifiche separato
> (funziona già così). Migra se vuoi **un unico deployment** e le `/api/*` sullo stesso dominio.

---

## Opzione A — Restare su Pages (nessuna migrazione)
Il sito resta su Pages; le notifiche girano sul Worker `busitinera-push` (vedi `GUIDA_NOTIFICHE.md`).
`WORKER_BASE` nel client punta all'URL `*.workers.dev` del Worker. Fine. È la via più rapida.

## Opzione B — Unificare tutto su Workers (consigliata a regime)

### 1. Aggiungi il file di ingresso del Worker (serve gli asset + le /api)
Crea in **root del repo** il file `server.js`:
```js
import push from './worker/worker.js';   // riusa la logica notifiche già pronta e testata
export default {
  async fetch(req, env, ctx) {
    const p = new URL(req.url).pathname;
    if (p.startsWith('/api/')) return push.fetch(req, env, ctx); // notifiche
    return env.ASSETS.fetch(req);                                 // sito statico
  }
};
```

### 2. Sostituisci `wrangler.toml` (root) con la configurazione Workers
```toml
name = "busitinera"
main = "server.js"
compatibility_date = "2024-09-25"

# Serve i file statici del sito (la cartella corrente) e li espone come env.ASSETS
[assets]
directory = "."
binding = "ASSETS"
html_handling = "auto-trailing-slash"   # /funzionalita → funzionalita.html
not_found_handling = "404-page"          # opzionale: crea un 404.html se vuoi

# KV delle iscrizioni push (stesso namespace del Worker separato, o creane uno nuovo)
[[kv_namespaces]]
binding = "SUBS"
id = "INCOLLA_QUI_L_ID_DEL_KV_NAMESPACE"

[vars]
VAPID_PUBLIC = "BC7tA5De-0L2nmqO0jKF4OnofzYP4_bw0S153PICUVCLquORRQbbQNh-ib9_W8LDI---l_labMBpw3vC1KdvjiM"
VAPID_SUBJECT = "mailto:busitinera@gmail.com"
ALLOWED_ORIGIN = "https://busitinera.it"
```
> La riga `pages_build_output_dir` del vecchio `wrangler.toml` va rimossa (era specifica di Pages).
> Escludi dagli asset ciò che non è pubblico (es. i `.md` di guida) spostandoli fuori dalla root
> o in una cartella non servita.

### 3. Secret (come per il Worker separato)
```bash
wrangler secret put VAPID_PRIVATE   # MY4lbK-oy-SdwUh72h6p_vlRb-kxOFs6TBjVcorpj-g
wrangler secret put SEND_SECRET     # la tua password d'invio
```

### 4. Poiché ora è same-origin, semplifica il client
In `bus-notify.js` puoi puntare al **dominio stesso**:
```js
var WORKER_BASE = '';   // stringa vuota = stesso dominio: le /api/* sono servite dal Worker
```
(le chiamate diventano `"/api/subscribe"`, ecc. — niente più CORS).

### 5. Pubblica il Worker
```bash
wrangler deploy
```
Verrà creato/aggiornato il Worker `busitinera` con un URL `*.workers.dev`.

### 6. Sposta il dominio busitinera.it sul Worker
Nel dashboard Cloudflare:
1. **Workers & Pages → busitinera (Worker) → Settings → Domains & Routes → Add → Custom domain** → `busitinera.it` (e `www` se lo usi).
2. Attendi il provisioning del certificato.
3. Nel progetto **Pages** `busitinera-sito`: rimuovi il custom domain `busitinera.it` (resta il `*.pages.dev`), poi puoi **mettere in pausa o eliminare** il progetto Pages una volta verificato che il Worker serve tutto.

### 7. Ripristina il deploy automatico da GitHub (come faceva Pages)
Due strade:
- **Workers Builds (consigliata):** Workers & Pages → il Worker → **Settings → Builds → Connect** al repo GitHub `Andrea52-jimny/BusItinera-sito`, branch `main`, deploy command `npx wrangler deploy`. Da lì ogni push ripubblica.
- **GitHub Actions:** aggiungi un workflow che esegue `wrangler deploy` con `CLOUDFLARE_API_TOKEN` nei secret del repo.

### 8. Verifica
- `https://busitinera.it/` e le pagine si aprono correttamente;
- `https://busitinera.it/api/vapidPublicKey` risponde con la chiave;
- la campanella iscrive e l'invio (`/api/send`) recapita.

---

## Note e accorgimenti
- **Routing degli asset:** con Pages `/funzionalita` serviva `funzionalita.html`. Su Workers Static
  Assets lo stesso comportamento si ottiene con `html_handling = "auto-trailing-slash"` (o `"drop-trailing-slash"`).
  I link interni del sito usano già `*.html`, quindi funzionano in ogni caso.
- **File non pubblici:** i `.md` di guida e la cartella `worker/` non dovrebbero essere serviti come
  asset pubblici. Con `[assets] directory="."` verrebbero esposti: meglio spostare le guide fuori dal
  repo del sito o in una sottocartella esclusa, e tenere `worker/worker.js` importato ma non servito
  (gli asset servono file statici; un `.js` importato dal `main` non è un problema, ma evita di linkarlo).
- **KV condiviso:** se avevi già iscrizioni sul Worker separato e vuoi conservarle, usa lo **stesso**
  `id` di KV namespace nella nuova config.
- **Rollback:** finché non elimini il progetto Pages, puoi tornare indietro rimettendo il dominio su Pages.

## In breve
| | Pages (oggi) | Workers (unificato) |
|---|---|---|
| Sito statico | ✅ | ✅ (Static Assets) |
| Notifiche /api/* | Worker separato | stesso Worker |
| Domini | busitinera.it su Pages | busitinera.it sul Worker |
| Deploy da GitHub | integrato | Workers Builds / Action |
| CORS notifiche | sì (cross-origin) | no (same-origin) |
