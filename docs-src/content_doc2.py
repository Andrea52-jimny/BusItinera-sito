# -*- coding: utf-8 -*-
"""PDF 2 — Attestato di Collaudo (funzionale e di sicurezza).

ATTENZIONE: il contenuto di questo documento e' il verbale di una verifica
realmente svolta. Non va aggiornato "per allineamento" quando esce una nuova
versione: la data in DATA_COLLAUDO e l'esito vanno cambiati solo dopo che la
verifica e' stata effettivamente rieseguita sul codice di quella versione.

Stato: collaudo del 10 ottobre 2026, eseguito sul codice allora in linea
(v1.22.0). Comprende una riverifica delle aree introdotte dalla 1.15 alla 1.22
(scadenze e promemoria automatici, home mobile, accesso con passkey,
fatturazione elettronica 2.0) e una nuova validazione degli XML FatturaPA
contro lo schema ufficiale v1.2. Un primo collaudo era stato svolto il
29 settembre 2026 sul codice 1.14.
"""

DATA_COLLAUDO = "10 ottobre 2026"
VERSIONE_COLLAUDATA = "1.22.0"

TOC = [
    ("s1", "1. Oggetto, ambito e metodo"),
    ("s2", "2. Attestato di collaudo funzionale"),
    ("s3", "3. Conformità FatturaPA (validazione XSD)"),
    ("s4", "4. Attestato di sicurezza applicativa"),
    ("s5", "5. Interventi di irrobustimento"),
    ("s6", "6. Dichiarazione conclusiva e avvertenze"),
    ("legal", "Appendice — Avviso di Copyright"),
]

BODY = """
<h2 id="s1">1. Oggetto, ambito e metodo</h2>
<p>Il presente attestato riassume gli esiti del <b>collaudo funzionale</b> e della <b>verifica di sicurezza applicativa</b> condotti sul software BusItinera, a supporto della sua messa in esercizio.</p>
<table class="k">
<tr><td>Oggetto</td><td>BusItinera — gestionale viaggi/noleggi e fatturazione elettronica (applicazione web PHP 8.2 / MariaDB 11)</td></tr>
<tr><td>Versione</td><td>1.22.0</td></tr>
<tr><td>Ambito</td><td>Collaudo funzionale delle aree operative e contabili; conformità della fatturazione elettronica FatturaPA; verifica di sicurezza applicativa (autenticazione, autorizzazione, gestione dati). Rispetto al primo collaudo del 29 settembre 2026 (v1.14), la presente verifica estende la copertura alle funzioni introdotte dalla 1.15 alla 1.22: scadenze e promemoria automatici, home mobile per titolari e operatori, accesso con passkey (impronta/Face ID), fatturazione elettronica 2.0 (vista «Da fatturare», fattura cumulativa per evento, frazionamento su più soggetti, archivio ZIP degli XML per periodo, stampa PDF del documento) e azione «Incassato» dagli avvisi.</td></tr>
<tr><td>Metodo</td><td>Analisi statica del codice sorgente (SAST) incrociata con la documentazione operativa; verifica dinamica autenticata sull'applicazione in esercizio, con esercizio diretto delle aree operative, contabili e di fatturazione e del portale autista, sia da desktop sia da telefono; validazione reale degli XML FatturaPA generati dall'applicazione contro lo schema ufficiale dell'Agenzia delle Entrate.</td></tr>
<tr><td>Data</td><td>__DATA__</td></tr>
</table>

<h2 id="s2">2. Attestato di collaudo funzionale</h2>
<div class="verdict"><span class="big">Esito funzionale: CONFORME</span>
<p>I flussi core (pianificazione, preventivi, contabilità, congelamento contabile, fatturazione elettronica, permessi, scadenze e portale autista) operano in modo corretto e coerente con la documentazione. Le discrepanze minori individuate in sede di collaudo sono state corrette e riverificate.</p></div>
<p><b>Controlli funzionali significativi verificati con esito positivo:</b></p>
<ul>
<li>Modello ruoli/permessi granulari, con voci non consentite nascoste all'utente;</li>
<li>Vincolo "ultimo amministratore" e protezione dell'account amministratore;</li>
<li>Sospensione utente con effetto immediato ad ogni richiesta;</li>
<li>Congelamento dei viaggi fatturati/pagati e rilevamento delle modifiche simultanee; sblocco dei soli flag di pagamento sui documenti già chiusi;</li>
<li>Riservatezza delle Note Private verso il ruolo autista, anche a livello di dati;</li>
<li>Ciclo di vita e immutabilità dei preventivi; documento archiviato invariante;</li>
<li>Registro attività immutabile (nessuna via di cancellazione o modifica);</li>
<li>Fatturazione elettronica 2.0: vista «Da fatturare» con scomputo degli acconti, creazione di bozze singole o di fattura cumulativa per evento (un solo XML), frazionamento di una bozza su più soggetti per importo con ripartizione riga per riga, archivio ZIP degli XML per periodo e stampa PDF del documento;</li>
<li>Avvisi e scadenze: campanella con categorie, promemoria automatici a soglie multiple senza doppioni, azione «Incassato» che salda e rimuove l'avviso senza riaprire il documento;</li>
<li>Portale autista e home mobile: viaggi del giorno, km, ordine di servizio e funzione "Viaggio completato", attivabile solo dopo l'orario di rientro (verificata anche lato server);</li>
<li>Accesso con passkey (impronta/Face ID) come alternativa a password e 2FA, con password e 2FA mantenute come via di recupero.</li>
</ul>

<h2 id="s3">3. Conformità FatturaPA (validazione XSD)</h2>
<p>Gli XML sono stati generati dall'applicazione nella versione in collaudo e validati con strumento indipendente (<b>xmllint</b>) contro lo schema ufficiale <b>FatturaPA v1.2</b> dell'Agenzia delle Entrate. La validazione è stata rieseguita in data __DATA__ sul codice 1.22.0.</p>
<table>
<tr><th>Documento</th><th>Scenario</th><th>Esito XSD</th></tr>
<tr><td>Fattura TD01 (FPR12)</td><td>Privato, IVA 10%, esigibilità immediata, recapito via PEC</td><td><b>Valido</b></td></tr>
<tr><td>Fattura TD01 (FPA12)</td><td>Pubblica Amministrazione, split payment, CIG e CUP, Codice Univoco Ufficio, aliquote miste</td><td><b>Valido</b></td></tr>
<tr><td>Nota di credito TD04</td><td>Storno con riferimento alla fattura d'origine</td><td><b>Valido</b></td></tr>
</table>
<p><b>Controlli di merito superati:</b> coerenza dei totali (imponibile + imposta = totale), aliquote e nature IVA corrette per scenario, riepilogo IVA per aliquota, corretto uso dello split payment per la PA (esigibilità «S»), presenza di CIG/CUP e Codice Univoco Ufficio nelle fatture PA, escaping dei caratteri speciali.</p>

<h2 id="s4">4. Attestato di sicurezza applicativa</h2>
<div class="verdict"><span class="big">Esito di sicurezza: nessuna vulnerabilità Critica o Alta</span>
<p>La verifica non ha rilevato vulnerabilità di livello Critico o Alto tra quelle oggetto di analisi. Le poche criticità di livello Medio/Basso individuate sono state corrette e ri-verificate. Le aree introdotte dopo il primo collaudo sono state riesaminate e rispettano l'impianto di sicurezza preesistente.</p></div>
<p><b>Aree verificate con esito positivo:</b></p>
<ul>
<li><b>Autenticazione e sessioni</b> — hashing robusto delle password, protezione contro il brute-force, rigenerazione dell'identificativo di sessione al login, distruzione della sessione al logout, cookie con attributi di sicurezza (HttpOnly, Secure, SameSite).</li>
<li><b>Accesso con passkey (WebAuthn)</b> — verifica della firma dell'autenticatore, sfida monouso a scadenza breve vincolata all'ambito, verifica dell'origine e dell'RP ID, user verification obbligatoria, contatore anti-clonazione; nessuna credenziale riutilizzabile conservata sul server.</li>
<li><b>Controllo degli accessi (RBAC)</b> — autorizzazione applicata lato server su ogni operazione sensibile; nessuna scalata di privilegi individuata; vincoli su ruoli e account amministratore.</li>
<li><b>Iniezioni</b> — uso pervasivo di query parametrizzate (nessuna SQL injection sfruttabile individuata); generazione XML tramite costruzione DOM, con auto-escape del testo e senza parsing di input non fidato (resistente a injection/XXE); output codificato lato interfaccia.</li>
<li><b>Autenticazione a due fattori</b> — verifica a tempo costante, codici di recupero monouso, protezione contro il brute-force del codice.</li>
<li><b>Protezione CSRF</b> e intestazioni di sicurezza HTTP complete (inclusa una Content-Security-Policy restrittiva e HSTS).</li>
<li><b>Riservatezza dei dati</b> — i dati economici e le note riservate non vengono esposti ai ruoli che non devono vederli.</li>
</ul>
<div class="note">Per ragioni di sicurezza, il presente attestato riporta soltanto l'esito complessivo. Il dettaglio tecnico delle verifiche e delle correzioni è documentato in un rapporto tecnico riservato, non destinato alla diffusione pubblica.</div>

<h2 id="s5">5. Interventi di irrobustimento</h2>
<p>A completamento delle verifiche sono stati applicati, nel tempo, alcuni interventi di irrobustimento, tra cui: neutralizzazione delle formule nell'export CSV; invalidazione delle sessioni al cambio password; cifratura opzionale del segreto 2FA a riposo; eliminazione della dipendenza da CDN esterni (componenti serviti localmente); protezione aggiuntiva del login per rete di provenienza; adozione delle passkey come fattore d'accesso forte senza segreti riutilizzabili lato server.</p>

<h2 id="s6">6. Dichiarazione conclusiva e avvertenze</h2>
<p>Sulla base delle attività svolte, alla data del __DATA__ il software BusItinera nella versione <b>1.22.0</b> risulta <b>funzionalmente conforme</b> alla propria documentazione, con fatturazione elettronica <b>validata contro lo schema ufficiale FatturaPA v1.2</b>, e <b>privo di vulnerabilità di sicurezza di livello Critico o Alto</b> tra quelle oggetto di verifica.</p>
<div class="disclaimer">
<p><b>Avvertenze.</b> Il presente attestato è redatto a fini informativi e di collaudo interno. L'audit è stato condotto con l'assistenza di un sistema di intelligenza artificiale (Claude di Anthropic) per conto del titolare del software; non costituisce una certificazione accreditata di terza parte né una garanzia assoluta di assenza di difetti o vulnerabilità. La sicurezza informatica è un processo continuo: l'esito si riferisce all'ambito, alla versione e alla data indicati. Restano impregiudicati i termini di licenza e le limitazioni di responsabilità applicabili al software.</p>
</div>
""".replace("__DATA__", DATA_COLLAUDO)
