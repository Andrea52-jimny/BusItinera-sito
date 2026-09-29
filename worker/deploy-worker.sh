#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# BusItinera — deploy del Worker notifiche (Opzione A: Worker separato).
# Lancialo DENTRO la cartella worker/:   bash deploy-worker.sh
# Fa: login (se serve) → crea il KV e inserisce l'id in wrangler.toml →
#     imposta i secret VAPID_PRIVATE e SEND_SECRET → deploy.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")"

WR="npx --yes wrangler"
VAPID_PRIVATE="MY4lbK-oy-SdwUh72h6p_vlRb-kxOFs6TBjVcorpj-g"   # generata per questo progetto

echo "▶ 1/5  Verifica login Cloudflare…"
if ! $WR whoami >/dev/null 2>&1; then
  echo "   Non risulti loggato: apro il login (si aprirà il browser)."
  $WR login
fi

echo "▶ 2/5  Creo il KV namespace 'SUBS' (se non esiste già)…"
KV_OUT="$($WR kv namespace create SUBS 2>&1 || true)"
echo "$KV_OUT"
KV_ID="$(printf '%s\n' "$KV_OUT" | grep -oE 'id *= *"?[a-f0-9]{32}"?' | grep -oE '[a-f0-9]{32}' | head -1 || true)"

if [ -n "${KV_ID:-}" ]; then
  # Inserisce l'id nel wrangler.toml (sostituisce il placeholder o un id precedente)
  if grep -q 'INCOLLA_QUI_L_ID_DEL_KV_NAMESPACE' wrangler.toml; then
    sed -i.bak "s/INCOLLA_QUI_L_ID_DEL_KV_NAMESPACE/$KV_ID/" wrangler.toml && rm -f wrangler.toml.bak
  else
    sed -i.bak -E "s/(id *= *\").*(\")/\1$KV_ID\2/" wrangler.toml && rm -f wrangler.toml.bak
  fi
  echo "   ✓ KV id inserito in wrangler.toml: $KV_ID"
else
  echo "   ⚠ Non sono riuscito a leggere l'id del KV automaticamente."
  echo "     Se il namespace esiste già, recuperalo con:  $WR kv namespace list"
  echo "     e incollalo a mano in wrangler.toml alla riga  id = \"…\"  poi rilancia."
  read -rp "     Incolla qui l'id del KV (32 caratteri) e premi Invio: " KV_ID
  sed -i.bak -E "s/(id *= *\").*(\")/\1$KV_ID\2/" wrangler.toml && rm -f wrangler.toml.bak
fi

echo "▶ 3/5  Imposto il secret VAPID_PRIVATE…"
printf '%s' "$VAPID_PRIVATE" | $WR secret put VAPID_PRIVATE

echo "▶ 4/5  Genero e imposto SEND_SECRET (password per inviare le notifiche)…"
SEND_SECRET="$(openssl rand -base64 24 | tr -d '\n' | tr '+/' '-_')"
printf '%s' "$SEND_SECRET" | $WR secret put SEND_SECRET
echo ""
echo "   ┌───────────────────────────────────────────────────────────────┐"
echo "   │  SALVA QUESTO SEND_SECRET (ti serve per inviare le notifiche): │"
echo "   │  $SEND_SECRET"
echo "   └───────────────────────────────────────────────────────────────┘"
echo ""

echo "▶ 5/5  Deploy del Worker…"
$WR deploy

echo ""
echo "✅ Fatto. Prendi l'URL del Worker qui sopra (es. https://busitinera-push.<account>.workers.dev)"
echo "   e incollalo in  ../bus-notify.js  alla riga:  var WORKER_BASE = '...'"
echo ""
echo "   Per inviare una novità:"
echo "     curl -X POST <URL_WORKER>/api/send \\"
echo "       -H \"Authorization: Bearer $SEND_SECRET\" \\"
echo "       -H \"Content-Type: application/json\" \\"
echo "       -d '{\"title\":\"BusItinera\",\"body\":\"Nuova versione disponibile!\",\"url\":\"https://busitinera.it/novita.html\"}'"
