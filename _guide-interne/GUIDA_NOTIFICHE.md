# Notifiche "novità" del sito — guida all'attivazione

Sistema di notifiche push per avvisare i visitatori quando pubblichi una novità.
Stessa logica dell'app: pulsante campanella nella navbar, **operativo su Android/desktop**,
con **tutorial "Aggiungi a Home" su iOS** (dove le push richiedono l'app installata).

- **Client** (già nel sito): `sw.js`, `bus-notify.js`, `manifest.json`, icone. Il pulsante
  si inietta da solo nella navbar di ogni pagina.
- **Server**: un **Cloudflare Worker** (`worker/`) che salva le iscrizioni in **KV** e invia
  le push (VAPID + cifratura aes128gcm). Nessuna dipendenza esterna.

Le chiavi **VAPID** sono già generate:
- Pubblica (nel client e in `wrangler.toml`): `BC7tA5De-0L2nmqO0jKF4OnofzYP4_bw0S153PICUVCLquORRQbbQNh-ib9_W8LDI---l_labMBpw3vC1KdvjiM`
- Privata (SEGRETA, va messa come secret del Worker): `MY4lbK-oy-SdwUh72h6p_vlRb-kxOFs6TBjVcorpj-g`

> Se preferisci rigenerarle, sostituisci sia la pubblica (in `bus-notify.js` e `wrangler.toml`) sia la privata (secret).

## 1. Prerequisiti
```bash
npm install -g wrangler
wrangler login
```

## 2. Crea il KV e incolla l'id
```bash
cd worker
wrangler kv namespace create SUBS
# copia l'id restituito dentro worker/wrangler.toml → [[kv_namespaces]] id = "..."
```

## 3. Imposta i secret
```bash
wrangler secret put VAPID_PRIVATE
# incolla:  MY4lbK-oy-SdwUh72h6p_vlRb-kxOFs6TBjVcorpj-g

wrangler secret put SEND_SECRET
# scegli una password lunga a piacere: ti servirà per INVIARE le notifiche
```
In `worker/wrangler.toml` controlla anche `ALLOWED_ORIGIN` (il dominio del sito, es. `https://busitinera.it`).

## 4. Pubblica il Worker
```bash
wrangler deploy
```
Annota l'URL del Worker, es. `https://busitinera-push.<tuo-account>.workers.dev`.

## 5. Collega il sito al Worker
Apri `bus-notify.js` e metti l'URL del Worker in cima:
```js
var WORKER_BASE = 'https://busitinera-push.<tuo-account>.workers.dev';
```
(in alternativa aggiungi `<meta name="bi-push" content="https://…">` nell'`<head>` delle pagine).
Poi fai il commit e push del sito (Cloudflare Pages ripubblica da solo).

## 6. Prova
- **Android/desktop**: apri il sito, clicca la 🔔 in alto → **Attiva le notifiche** → Consenti.
- **iPhone/iPad**: la campanella mostra il tutorial: **Condividi → Aggiungi a Home**, poi riapri
  BusItinera dalla Home e attiva.

## 7. Inviare una notifica quando pubblichi una novità
```bash
curl -X POST https://busitinera-push.<tuo-account>.workers.dev/api/send \
  -H "Authorization: Bearer IL_TUO_SEND_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"title":"BusItinera","body":"È disponibile la versione 1.14 🎉","url":"https://busitinera.it/novita.html"}'
```
Risposta: `{ "ok": true, "sent": N, "gone": M, "failed": K }`
(`gone` = iscrizioni scadute, rimosse automaticamente).

## Note
- Le iscrizioni scadute (404/410) vengono cancellate da sole all'invio.
- Il Worker **non** sta nel percorso del sito: se lo spegni, il sito continua a funzionare
  (semplicemente non si inviano/ricevono notifiche).
- Rotte del Worker: `GET /api/vapidPublicKey`, `POST /api/subscribe`, `POST /api/unsubscribe`,
  `POST /api/send` (protetta da `SEND_SECRET`).
