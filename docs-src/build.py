#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera i due PDF pubblici di BusItinera (cartella ../docs/).

    cd docs-src && python3 build.py

Dipendenze:  pip install --break-system-packages weasyprint
Font:        fonts/DMSans-{Regular,Medium,Bold}.ttf (già nel repo)
Output:      ../docs/BusItinera_Documentazione_Funzionalita.pdf
             ../docs/BusItinera_Attestato_Funzionale_e_Sicurezza.pdf

I contenuti stanno in content_doc1.py / content_doc2.py; la presentazione in
common.css. Per aggiornare un documento si modifica il testo nel file dei
contenuti e si rilancia questo script: l'impaginazione non va toccata.
"""
import html as _h
import os
import sys
from pathlib import Path

from weasyprint import HTML

import content_doc1
import content_doc2
from legal import COPYRIGHT

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "docs"

# ─── Metadati di copertina ──────────────────────────────────────────────────
# VERSIONE: la release del gestionale che i contenuti descrivono.
# La data dell'attestato NON si tocca qui: vive in content_doc2.DATA_COLLAUDO,
# perché è la data di una verifica realmente svolta.
VERSIONE_DOC = "1.16.0"
DATA_DOC = "30 settembre 2026"

PRODOTTO = ("BusItinera — Gestionale viaggi, noleggi e fatturazione "
            "per aziende di trasporto con autista")
AUTORE = "Ceol Andrea"

HEAD = """<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="common.css"></head><body>
"""


def cover(kicker, titolo, sottotitolo, nome_doc, data, versione=None):
    """Copertina a piena pagina."""
    riga_ver = f"  ·  Versione del software: <b>{_h.escape(versione)}</b>" if versione else ""
    return f"""
<div class="cover">
  <img class="logo" src="../logo.png" alt="BusItinera">
  <div class="kicker">{_h.escape(kicker)}</div>
  <h1>{_h.escape(titolo)}</h1>
  <div class="sub">{_h.escape(sottotitolo)}</div>
  <div class="meta">
    <b>Prodotto:</b> {_h.escape(PRODOTTO)}<br>
    <b>Documento:</b> {_h.escape(nome_doc)}  ·  <b>Data:</b> {_h.escape(data)}{riga_ver}<br>
    <b>Autore del software:</b> {_h.escape(AUTORE)}
  </div>
  <div class="band"></div>
</div>
"""


def toc(voci):
    """Indice con numeri di pagina calcolati da WeasyPrint (target-counter)."""
    def riga(anchor, testo):
        cls = ' class="part"' if anchor == "legal" else ""
        return f'<li{cls}><a href="#{anchor}">{_h.escape(testo)}</a></li>'

    righe = "\n".join(riga(a, t) for a, t in voci)
    return f'<nav class="toc"><h2>Indice</h2><ol>{righe}</ol></nav>'


def build(path, title, body):
    doc = HEAD.format(title=_h.escape(title)) + body + COPYRIGHT + "</body></html>"
    HTML(string=doc, base_url=str(HERE) + os.sep).write_pdf(path)
    print(f"  scritto  {path}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    print("Documentazione delle Funzionalità…")
    build(
        OUT / "BusItinera_Documentazione_Funzionalita.pdf",
        "BusItinera — Documentazione delle Funzionalità",
        cover("Documentazione",
              "Documentazione delle Funzionalità",
              "Guida completa alle funzioni del gestionale BusItinera: operatività, "
              "contabilità, fatturazione elettronica e portale autista.",
              "Documentazione delle Funzionalità",
              DATA_DOC, VERSIONE_DOC)
        + toc(content_doc1.TOC) + content_doc1.BODY,
    )

    print("Attestato di Collaudo…")
    build(
        OUT / "BusItinera_Attestato_Funzionale_e_Sicurezza.pdf",
        "BusItinera — Attestato Funzionale e di Sicurezza",
        cover("Attestato",
              "Attestato di Collaudo — Funzionale e di Sicurezza",
              "Esito del collaudo funzionale, della conformità FatturaPA e della "
              "verifica di sicurezza applicativa del software BusItinera.",
              "Attestato di Collaudo",
              content_doc2.DATA_COLLAUDO, content_doc2.VERSIONE_COLLAUDATA)
        + toc(content_doc2.TOC) + content_doc2.BODY,
    )

    print("Fatto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
