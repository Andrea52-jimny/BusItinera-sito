# -*- coding: utf-8 -*-
"""PDF 2 — Attestato di Collaudo (funzionale e di sicurezza).

ATTENZIONE: il contenuto di questo documento è il verbale di una verifica
realmente svolta. Non va aggiornato "per allineamento" quando esce una nuova
versione: la data in DATA_COLLAUDO e l'esito vanno cambiati solo dopo che la
verifica è stata effettivamente rieseguita sul codice di quella versione.

Stato: collaudo del 29 settembre 2026, eseguito sul codice allora in linea
(v1.14 piu' le funzioni rilasciate il giorno dopo come v1.15). Le versioni
1.15 e 1.16 nel loro complesso NON sono coperte: vanno collaudate a parte.
"""

DATA_COLLAUDO = "29 settembre 2026"
VERSIONE_COLLAUDATA = "1.14 (codice del 29 settembre 2026)"

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
<tr><td>Ambito</td><td>Collaudo funzionale delle aree operative e contabili; conformità della fatturazione elettronica FatturaPA; verifica di sicurezza applicativa (autenticazione, autorizzazione, gestione dati)</td></tr>
<tr><td>Metodo</td><td>Analisi statica del codice sorgente (SAST) incrociata con la documentazione operativa; verifica dinamica autenticata sull'applicazione in esecuzione; validazione reale degli XML FatturaPA contro lo schema ufficiale</td></tr>
<tr><td>Data</td><td>__DATA__</td></tr>
</table>

<h2 id="s2">2. Attestato di collaudo funzionale</h2>
<div class="verdict"><span class="big">Esito funzionale: CONFORME</span>
<p>I flussi core (pianificazione, preventivi, contabilità, congelamento contabile, fatturazione elettronica, permessi e portale autista) operano in modo corretto e coerente con la documentazione. Le discrepanze minori individuate in sede di collaudo sono state corrette e riverificate.</p></div>
<p><b>Controlli funzionali significativi verificati con esito positivo:</b></p>
<ul>
<li>Modello ruoli/permessi granulari, con voci non consentite nascoste all'utente;</li>
<li>Vincolo "ultimo amministratore" e protezione dell'account amministratore;</li>
<li>Sospensione utente con effetto immediato ad ogni richiesta;</li>
<li>Congelamento dei viaggi fatturati/pagati e rilevamento delle modifiche simultanee;</li>
<li>Riservatezza delle Note Private verso il ruolo autista, anche a livello di dati;</li>
<li>Ciclo di vita e immutabilità dei preventivi; documento archiviato invariante;</li>
<li>Registro attività immutabile (nessuna via di cancellazione o modifica);</li>
<li>Funzione "Viaggio completato" da portale autista, attivabile solo dopo l'orario di rientro (verificata anche lato server).</li>
</ul>

<h2 id="s3">3. Conformità FatturaPA (validazione XSD)</h2>
<p>Gli XML sono stati generati dall'applicazione in esercizio e validati con strumento indipendente (<b>xmllint</b>) contro lo schema ufficiale <b>FatturaPA v1.2</b> dell'Agenzia delle Entrate.</p>
<table>
<tr><th>Documento</th><th>Scenario</th><th>Esito XSD</th></tr>
<tr><td>Fattura TD01 (FPR12)</td><td>Privato, IVA 10%, esigibilità immediata, recapito via PEC</td><td><b>Valido</b></td></tr>
<tr><td>Fattura TD01 (FPA12)</td><td>Pubblica Amministrazione, split payment, CIG e CUP, Codice Univoco Ufficio</td><td><b>Valido</b></td></tr>
<tr><td>Nota di credito TD04</td><td>Storno con riferimento alla fattura d'origine</td><td><b>Valido</b></td></tr>
</table>
<p><b>Controlli di merito superati:</b> coerenza dei totali (imponibile + imposta = totale), aliquote e nature IVA corrette per scenario, corretto uso dello split payment per la PA, escaping dei caratteri speciali.</p>

<h2 id="s4">4. Attestato di sicurezza applicativa</h2>
<div class="verdict"><span class="big">Esito di sicurezza: nessuna vulnerabilità Critica o Alta</span>
<p>La verifica non ha rilevato vulnerabilità di livello Critico o Alto. Le poche criticità di livello Medio/Basso individuate sono state corrette e ri-verificate. L'impianto di sicurezza è progettato con cura difensiva coerente.</p></div>
<p><b>Aree verificate con esito positivo:</b></p>
<ul>
<li><b>Autenticazione e sessioni</b> — hashing robusto delle password, protezione contro il brute-force, rigenerazione dell'identificativo di sessione al login, distruzione della sessione al logout, cookie con attributi di sicurezza (HttpOnly, Secure, SameSite).</li>
<li><b>Controllo degli accessi (RBAC)</b> — autorizzazione applicata lato server su ogni operazione sensibile; nessuna scalata di privilegi individuata; vincoli su ruoli e account amministratore.</li>
<li><b>Iniezioni</b> — uso pervasivo di query parametrizzate (nessuna SQL injection sfruttabile); generazione XML resistente a injection/XXE; output codificato lato interfaccia.</li>
<li><b>Autenticazione a due fattori</b> — verifica a tempo costante, codici di recupero monouso, protezione contro il brute-force del codice.</li>
<li><b>Protezione CSRF</b> e intestazioni di sicurezza HTTP complete (inclusa una Content-Security-Policy restrittiva e HSTS).</li>
<li><b>Riservatezza dei dati</b> — i dati economici e le note riservate non vengono esposti ai ruoli che non devono vederli.</li>
</ul>
<div class="note">Per ragioni di sicurezza, il presente attestato riporta soltanto l'esito complessivo. Il dettaglio tecnico delle verifiche e delle correzioni è documentato in un rapporto tecnico riservato, non destinato alla diffusione pubblica.</div>

<h2 id="s5">5. Interventi di irrobustimento</h2>
<p>A completamento della verifica sono stati applicati alcuni interventi di irrobustimento, tra cui: neutralizzazione delle formule nell'export CSV; invalidazione delle sessioni al cambio password; cifratura opzionale del segreto 2FA a riposo; eliminazione della dipendenza da CDN esterni (componenti serviti localmente); protezione aggiuntiva del login per rete di provenienza.</p>

<h2 id="s6">6. Dichiarazione conclusiva e avvertenze</h2>
<p>Sulla base delle attività svolte, alla data del __DATA__ il software BusItinera risulta <b>funzionalmente conforme</b> alla propria documentazione, con fatturazione elettronica <b>validata contro lo schema ufficiale FatturaPA</b>, e <b>privo di vulnerabilità di sicurezza di livello Critico o Alto</b> tra quelle oggetto di verifica.</p>
<div class="note">
<p><b>Versione coperta da questo collaudo.</b> Le verifiche sono state eseguite il __DATA__ sul codice allora in linea: la versione 1.14, comprensiva delle funzioni rilasciate il giorno successivo come 1.15 — fra cui «Viaggio completato» del portale autista, elencata al capitolo 2. Le versioni 1.15 e 1.16 nel loro complesso <b>non sono oggetto del presente attestato</b>; in particolare l'accesso con impronta o Face ID (passkey), introdotto con la 1.16, non è stato sottoposto a questa verifica.</p>
</div>
<div class="disclaimer">
<p><b>Avvertenze.</b> Il presente attestato è redatto a fini informativi e di collaudo interno. L'audit è stato condotto con l'assistenza di un sistema di intelligenza artificiale (Claude di Anthropic) per conto del titolare del software; non costituisce una certificazione accreditata di terza parte né una garanzia assoluta di assenza di difetti o vulnerabilità. La sicurezza informatica è un processo continuo: l'esito si riferisce all'ambito, alla versione e alla data indicati. Restano impregiudicati i termini di licenza e le limitazioni di responsabilità applicabili al software.</p>
</div>
""".replace("__DATA__", DATA_COLLAUDO)
