# docs-src — sorgenti dei PDF pubblici

Qui vivono i sorgenti dei due PDF scaricabili da `download.html`. I PDF in
`../public/docs/` sono **generati**: non si modificano a mano, si rigenerano da qui.

## Rigenerare

```bash
cd docs-src
pip install --break-system-packages weasyprint   # solo la prima volta
python3 build.py
```

Scrive `../public/docs/BusItinera_Documentazione_Funzionalita.pdf` e
`../public/docs/BusItinera_Attestato_Funzionale_e_Sicurezza.pdf`.

## Cosa sta dove

| File | Contiene |
|---|---|
| `build.py` | Assemblaggio, copertina, indice. Qui stanno `VERSIONE_DOC` e `DATA_DOC` della documentazione. |
| `content_doc1.py` | **Testo** della Documentazione delle Funzionalità (indice + corpo). |
| `content_doc2.py` | **Testo** dell'Attestato di Collaudo, più `DATA_COLLAUDO` e `VERSIONE_COLLAUDATA`. |
| `legal.py` | Avviso di copyright, appendice condivisa dai due documenti. |
| `common.css` | Impaginazione: A4, copertina, footer, tabelle, callout. Non serve toccarlo per un aggiornamento di testo. |
| `fonts/` | DM Sans Regular/Medium/Bold, istanze statiche del font variabile di Google Fonts (OFL). |

Il logo di copertina è `../public/logo-chiaro.png`: la variante per fondo chiaro.
Il `logo.png` del sito ha "Itinera" e il payoff in bianco (è disegnato per fondo
scuro) e sul riquadro bianco della copertina sparirebbe, lasciando solo "Bus".

## Aggiornare un documento

1. Modifica il testo nel `content_doc*.py`.
2. Se cambia la release descritta, aggiorna `VERSIONE_DOC` / `DATA_DOC` in `build.py`.
3. `python3 build.py`, apri i PDF, committa sorgenti e PDF insieme.

**L'attestato è un'eccezione.** È il verbale di una verifica realmente
svolta: `DATA_COLLAUDO` e `VERSIONE_COLLAUDATA` si spostano solo dopo aver
rieseguito davvero il collaudo sul codice di quella versione. Allinearne la
data "perché è uscita una release" significa attestare qualcosa che non è
stato controllato.

## Elementi disponibili nel testo

`<div class="note">` (nota azzurra), `.tip` (verde), `.warn` (arancio),
`.new` (blu, per le novità), `<span class="badge">NUOVO</span>`,
`<table>` e `<table class="k">` (prima colonna chiave), `.verdict` (esito in
evidenza, usato nell'attestato).

Le voci dell'indice sono coppie `(ancora, testo)`; l'ancora deve
corrispondere a un `id=` nel corpo, altrimenti quella riga resta senza
numero di pagina.
