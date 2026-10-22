# -*- coding: utf-8 -*-
"""PDF 4 — Attestato di Cybersecurity (scansione dello stack applicativo).

ATTENZIONE: come l'Attestato di Collaudo, questo documento e' il verbale di una
verifica realmente svolta. DATA_SCANSIONE e l'esito non vanno aggiornati "per
allineamento" all'uscita di una release: si spostano solo dopo aver rieseguito
davvero la scansione sul codice di quella versione.

Stato: scansione del 22 ottobre 2026 sull'intero stack (gestionale, console di
deploy, sito pubblico e suo worker), motivata dal rilascio di sicurezza PHP del
21 ottobre 2026 (CVE-2026-109618 e CVE-2026-109619, noti come "PHP2Shell") ed
estesa su richiesta a una verifica completa di sicurezza applicativa.

Il documento e' PUBBLICO e volutamente sanitizzato: riporta esiti e misure, non
percorsi, configurazioni o dettagli sfruttabili. Il dettaglio tecnico sta nel
rapporto riservato nel repository del gestionale.
"""

DATA_SCANSIONE = "22 ottobre 2026"
VERSIONE_SCANSIONATA = "1.28.3"

TOC = [
    ("s1", "1. Oggetto, ambito e metodo"),
    ("s2", "2. Esito complessivo"),
    ("s3", "3. Componenti in ambito"),
    ("s4", "4. Vulnerabilità PHP di piattaforma (PHP2Shell)"),
    ("s5", "5. Verifica di sicurezza applicativa"),
    ("s6", "6. Separazione fra sito pubblico e console di gestione"),
    ("s7", "7. Interventi applicati"),
    ("s8", "8. Vigilanza e manutenzione"),
    ("s9", "9. Dichiarazione conclusiva e avvertenze"),
    ("legal", "Appendice — Avviso di Copyright"),
]

BODY = """
<h2 id="s1">1. Oggetto, ambito e metodo</h2>
<p>Il presente attestato riporta l'esito di una <b>scansione di sicurezza dell'intero stack applicativo BusItinera</b>, svolta il __DATA__. L'attività è stata avviata in risposta al rilascio di sicurezza PHP del <b>21 ottobre 2026</b>, che ha corretto due vulnerabilità critiche dell'interprete, ed è stata poi estesa a una verifica completa di sicurezza applicativa su tutti i componenti.</p>
<table class="k">
<tr><td>Oggetto</td><td>Lo stack BusItinera nel suo complesso: il gestionale, la console di gestione della flotta, il sito pubblico e il servizio che lo serve</td></tr>
<tr><td>Versione</td><td>Gestionale __VERS__; console e sito nello stato in linea alla data indicata</td></tr>
<tr><td>Ambito</td><td>Esposizione alle vulnerabilità PHP di piattaforma del 21 ottobre 2026; autenticazione e gestione delle sessioni; controllo degli accessi su tutti gli endpoint; iniezioni (base dati, comandi di sistema, XML, interfaccia); protezione CSRF; crittografia, gestione delle password e dei segreti; caricamento di file; attraversamento dei percorsi; richieste verso l'esterno; catena di fornitura delle librerie di terze parti; intestazioni di sicurezza HTTP; postura di contenimento dei container e della rete; superficie di esecuzione raggiungibile dal web</td></tr>
<tr><td>Metodo</td><td>Analisi statica del codice sorgente di tutti i componenti, condotta per classi di vulnerabilità e non a campione: enumerazione sistematica degli endpoint con verifica della guardia di autorizzazione su ciascuno; tracciamento dei dati non fidati dal punto d'ingresso fino a base dati, shell, interfaccia e filesystem; riscontro delle misure dichiarate contro la configurazione effettiva. Le correzioni sono state <b>verificate funzionalmente</b>: le configurazioni del server web sono state caricate in un'istanza reale e i controlli d'accesso provati con richieste HTTP, confrontando lo stato precedente con quello successivo; il controllo automatico di versione dell'interprete è stato provato su tutti i suoi casi; i file modificati sono stati sottoposti a controllo sintattico</td></tr>
<tr><td>Data</td><td>__DATA__</td></tr>
</table>
<div class="note"><b>Nota sul livello di dettaglio.</b> Questo attestato è un documento pubblico e dichiara, per ogni classe di vulnerabilità esaminata, <b>l'esito</b> e, dove è stato individuato un rilievo, la sua <b>gravità</b> e la conferma che è stato <b>corretto e riverificato</b>. Non riporta invece nulla che possa agevolare un attacco: né percorsi, nomi di file, frammenti di codice o parametri di configurazione, né il componente, la funzione o le condizioni in cui un rilievo si manifestava. La ragione è concreta: il software è distribuito a più clienti, e un elenco circostanziato delle debolezze delle versioni precedenti sarebbe una lista di cose da provare su ogni copia non ancora aggiornata. Il dettaglio tecnico completo esiste, in un rapporto riservato non destinato alla diffusione.</div>

<h2 id="s2">2. Esito complessivo</h2>
<div class="verdict"><span class="big">Esito: stack protetto dalle vulnerabilità PHP del 21 ottobre 2026; tutti i rilievi corretti e riverificati</span>
<p>Lo stack è stato messo in sicurezza rispetto a entrambe le vulnerabilità di piattaforma, con la correzione dell'interprete resa <b>obbligatoria e verificata automaticamente</b> e con l'adozione integrale delle misure di mitigazione raccomandate. La verifica applicativa ha individuato <b>un rilievo di livello Alto</b> e <b>alcuni di livello Medio e Basso</b>, tutti sanati nel corso dell'attività e riverificati. Nessun rilievo è rimasto aperto alla data di chiusura.</p></div>
<p>Il rilievo di livello Alto <b>non riguardava il gestionale usato dalle aziende clienti</b>, ma uno strumento interno del fornitore, che per progetto non è esposto su Internet ed è raggiungibile solo da rete riservata: una misura perimetrale già in essere al momento della verifica, indipendente dalle protezioni applicative. Il rilievo è stato chiuso su <b>due livelli indipendenti</b> e la chiusura verificata con richieste reali, confrontando il comportamento prima e dopo l'intervento.</p>
<p>Gli esiti per classe di vulnerabilità esaminata sono riportati al capitolo 5.</p>

<h2 id="s3">3. Componenti in ambito</h2>
<p>La scansione ha coperto <b>tutti</b> i componenti dello stack. Nessuno è stato escluso.</p>
<table>
<tr><th>Componente</th><th>Natura</th><th>Esito</th></tr>
<tr><td><b>Gestionale</b></td><td>Applicazione web usata dalle aziende clienti: pianificazione, noleggi, contabilità, fatturazione elettronica, portale autista. È il componente esposto agli utenti finali.</td><td>Protetto dalle vulnerabilità di piattaforma; rilievi applicativi di livello Basso e Medio corretti</td></tr>
<tr><td><b>Console di gestione</b></td><td>Strumento interno del fornitore per creare e governare le istanze dei clienti. Non è accessibile ai clienti ed è raggiungibile solo da rete riservata.</td><td>Protetta dalle vulnerabilità di piattaforma; un rilievo di livello Alto e alcuni Medi corretti</td></tr>
<tr><td><b>Sito pubblico</b></td><td>Sito vetrina e pagine informative, composto da contenuti statici.</td><td>Non interessato dalle vulnerabilità di piattaforma: non impiega l'interprete in questione</td></tr>
<tr><td><b>Servizio del sito</b></td><td>Servizio che gestisce le notifiche agli iscritti e raccoglie le richieste di prova dal sito.</td><td>Non interessato dalle vulnerabilità di piattaforma; verificato l'isolamento dalla console (capitolo 6)</td></tr>
</table>

<h2 id="s4">4. Vulnerabilità PHP di piattaforma (PHP2Shell)</h2>
<p>Il 21 ottobre 2026 il progetto PHP ha pubblicato un rilascio di sicurezza che corregge <b>due vulnerabilità di esecuzione di codice remoto</b> nell'interprete, identificate come <b>CVE-2026-109618</b> e <b>CVE-2026-109619</b> e divulgate con il nome collettivo <b>PHP2Shell</b>. Entrambe hanno gravità <b>9,2 su 10</b> secondo la metrica CVSS v4.0.</p>
<p>Le due vulnerabilità risiedono nella gestione della memoria e degli errori dell'interprete, cioè in meccanismi attraversati da qualunque richiesta: <b>un'applicazione può essere colpita anche se il proprio codice è corretto</b>. Sono raggiungibili da richieste <b>non autenticate</b> e il rischio è più elevato nella modalità di esecuzione impiegata dallo stack. Le vulnerabilità sono state individuate con il contributo di strumenti di intelligenza artificiale impiegati da gruppi di ricerca indipendenti, e alla data della scansione risultavano pubblicamente segnalati tentativi di sfruttamento.</p>
<p>Il rimedio definitivo indicato dal progetto PHP è <b>l'aggiornamento dell'interprete</b>: le misure di configurazione riducono l'esposizione ma non sostituiscono la correzione. Lo stack ha adottato entrambe le vie. Le misure qui elencate sono quelle raccomandate pubblicamente dal progetto PHP e dai ricercatori: riportarle non aggiunge nulla a quanto già noto.</p>
<p><b>Misure adottate su gestionale e console:</b></p>
<ul>
<li><b>Correzione dell'interprete resa obbligatoria e verificata automaticamente.</b> È stato introdotto un controllo che, alla costruzione di ogni immagine applicativa, accerta che l'interprete includa la correzione di sicurezza e <b>interrompe la procedura</b> in caso contrario. Il controllo copre tutti i rami di versione supportati e fallisce deliberatamente anche su un ramo non previsto, in modo che una versione non valutata non possa passare inosservata. È quindi impossibile mettere in esercizio un'immagine costruita su un interprete non corretto senza che la procedura segnali l'errore. Il controllo è stato provato su tutti i suoi casi, compresi quelli di rifiuto.</li>
<li><b>Adozione integrale delle mitigazioni raccomandate</b> per entrambe le vulnerabilità, mantenute come difesa in profondità anche a interprete corretto, e applicate <b>in modo non sovrascrivibile dal codice applicativo</b>, così che nessuna impostazione dell'applicazione possa reintrodurre la condizione vulnerabile.</li>
<li><b>Disattivazione delle funzionalità non necessarie</b> individuate dai ricercatori come inneschi dell'attacco, con particolare riguardo a quelle che entrano in azione <i>prima</i> del codice applicativo e che quindi non potrebbero essere intercettate a livello di applicazione.</li>
<li><b>Limiti sulle richieste in ingresso</b> fatti rispettare dal server web, cioè prima che l'interprete elabori la richiesta: non solo sulla dimensione complessiva, ma anche sulla struttura del contenuto, poiché le tecniche di attacco pubblicate agiscono durante l'analisi della richiesta. I limiti si applicano anche alle richieste che non dichiarano correttamente la propria lunghezza.</li>
<li><b>Contenimento della memoria spostato al livello corretto.</b> Il tetto di memoria è ora imposto dal contenitore e non dall'interprete: così un eccesso abbatte il singolo processo interessato, invece di innescare all'interno dell'interprete la condizione da cui nasce la vulnerabilità. È stata evitata la tecnica di limitazione che i ricercatori segnalano come controproducente.</li>
<li><b>Riduzione della superficie di errore raggiungibile dall'esterno.</b> Una delle due vulnerabilità si innesca a partire da errori fatali provocabili dall'esterno: la superficie da cui tali errori potevano originare è stata ridotta.</li>
</ul>
<p>Il sito pubblico e il suo servizio <b>non impiegano l'interprete interessato</b> e non sono quindi esposti a queste due vulnerabilità. Anche per essi è stata comunque svolta la verifica applicativa descritta ai capitoli 5 e 6.</p>

<h2 id="s5">5. Verifica di sicurezza applicativa</h2>
<p>Oltre alle vulnerabilità di piattaforma è stata svolta, su richiesta, una verifica estesa a tutti i componenti. Di seguito le classi esaminate e il relativo esito. Dove la verifica ha prodotto un rilievo, è indicata la gravità e la conferma della correzione; la natura tecnica del rilievo resta nel rapporto riservato, per le ragioni spiegate al capitolo 1.</p>
<table>
<tr><th>Classe esaminata</th><th>Esito</th></tr>
<tr><td><b>Controllo degli accessi</b> — guardia di autorizzazione su ogni endpoint</td><td><b>Conforme.</b> Enumerazione completa degli endpoint di entrambe le applicazioni: ciascuna operazione risulta protetta lato server dalla guardia appropriata al proprio livello di privilegio. Le sole operazioni prive di guardia sono quelle che per natura precedono l'autenticazione. Nessuna scalata di privilegi né accesso a dati di altri soggetti individuati.</td></tr>
<tr><td><b>Iniezione su base dati</b></td><td><b>Conforme.</b> Uso pervasivo di interrogazioni parametrizzate. Le interrogazioni costruite per composizione sono state esaminate una per una: gli elementi variabili provengono esclusivamente da elenchi fissi nel codice o da valori convertiti a numero intero, mai da dati forniti dall'utente. Nessuna iniezione sfruttabile individuata.</td></tr>
<tr><td><b>Iniezione di comandi di sistema</b></td><td><b>Conforme.</b> Dove l'applicazione invoca strumenti esterni, ogni argomento è sottoposto a protezione e gli identificativi che concorrono a comporre i comandi sono normalizzati a un insieme ristretto di caratteri prima dell'uso. Nessuna iniezione individuata.</td></tr>
<tr><td><b>Iniezione in interfaccia</b></td><td><b>Conforme.</b> Tutti i dati di provenienza esterna mostrati nelle interfacce risultano codificati prima dell'inserimento nella pagina, compresi quelli che possono essere immessi da visitatori anonimi.</td></tr>
<tr><td><b>Iniezione e XXE su XML</b></td><td><b>Conforme.</b> L'XML della fatturazione elettronica viene costruito con codifica automatica del testo; non viene effettuata alcuna analisi di XML di provenienza non fidata, quindi la classe XXE non è applicabile.</td></tr>
<tr><td><b>Deserializzazione non sicura</b></td><td><b>Non applicabile.</b> Nessun impiego di deserializzazione di dati su tutto lo stack.</td></tr>
<tr><td><b>Autenticazione e sessioni</b></td><td><b>Conforme.</b> Password protette con algoritmo dedicato e parametro di costo adeguato; confronto a tempo costante anche per utenze inesistenti, così da non rivelarne l'esistenza; rigenerazione dell'identificativo di sessione all'accesso; secondo fattore e accesso con passkey; limitazione dei tentativi ripetuti; cookie con attributi di sicurezza.</td></tr>
<tr><td><b>Protezione CSRF</b></td><td><b>Rilievo di livello Basso, corretto e riverificato.</b> Un gruppo ristretto di operazioni di scrittura non applicava questa specifica verifica, pur restando protetto da un secondo meccanismo che già impediva l'attacco nei browser aggiornati. La verifica è ora applicata a tutte le operazioni di scrittura, per non dipendere da quel solo presupposto.</td></tr>
<tr><td><b>Crittografia e gestione dei segreti</b></td><td><b>Conforme.</b> Cifratura autenticata con algoritmo e parametri corretti, valore di inizializzazione casuale per ogni operazione e validazione della lunghezza della chiave. Generazione di valori casuali affidata esclusivamente a sorgenti crittograficamente sicure: nessun impiego di generatori deboli nei percorsi di sicurezza. Nessun segreto presente nel codice sorgente o nella cronologia dei repository.</td></tr>
<tr><td><b>Credenziali iniziali</b></td><td><b>Rilievo di livello Medio, corretto e riverificato.</b> Una procedura interna generava credenziali iniziali non sufficientemente distinte fra loro. Il cambio obbligatorio al primo accesso era già previsto. Ogni credenziale iniziale è ora casuale e univoca.</td></tr>
<tr><td><b>Caricamento di file</b></td><td><b>Conforme.</b> L'unico caricamento previsto verifica esito, dimensione, provenienza effettiva del file e tipo reale del contenuto, non la sola estensione dichiarata. La destinazione non è una posizione eseguibile.</td></tr>
<tr><td><b>Attraversamento dei percorsi</b></td><td><b>Conforme.</b> I riferimenti ai file gestiti dall'applicazione sono validati sia contro la presenza di separatori di percorso sia contro un formato atteso, con doppio controllo indipendente.</td></tr>
<tr><td><b>Richieste verso l'esterno (SSRF)</b></td><td><b>Conforme.</b> Tutte le destinazioni delle richieste uscenti derivano da parametri di configurazione dell'amministratore o da dati interni, e nessuna è influenzabile da un utente non autenticato.</td></tr>
<tr><td><b>Catena di fornitura (librerie di terze parti)</b></td><td><b>Rilievo di livello Medio, corretto e riverificato.</b> Una libreria di terze parti non era servita con garanzie di integrità adeguate. <b>Nessun componente dello stack dipende più da codice eseguibile fornito da terzi attraverso la rete</b>: tutte le librerie sono ora servite dall'applicazione stessa.</td></tr>
<tr><td><b>Intestazioni di sicurezza HTTP</b></td><td><b>Rilievo di livello Medio, corretto e riverificato.</b> Un componente non inviava l'insieme completo di intestazioni di sicurezza. Tutti i componenti applicativi dispongono ora di un insieme completo, politica restrittiva dei contenuti inclusa, verificato nelle risposte effettive.</td></tr>
<tr><td><b>Superficie di esecuzione raggiungibile dal web</b></td><td><b>Rilievo di livello Alto, corretto e riverificato.</b> In entrambe le applicazioni risultavano raggiungibili dal web porzioni di codice destinate al solo uso interno. Nel gestionale si trattava di codice inerte, senza esposizione di dati; il rilievo di livello Alto riguardava lo strumento interno del fornitore, non esposto su Internet. La chiusura è stata realizzata su <b>due livelli indipendenti</b> — uno nel codice, che lo accompagna ovunque sia installato, e uno nella configurazione del server — ed è stata verificata con richieste reali, confrontando il comportamento prima e dopo l'intervento.</td></tr>
<tr><td><b>Contenimento di container e rete</b></td><td><b>Conforme, con tetto di memoria introdotto.</b> La base dati non è esposta all'host; i segreti non sono presenti nei repository; le comunicazioni fra componenti restano su rete interna. È stato introdotto un tetto di memoria per contenitore, necessario a completare le mitigazioni descritte al capitolo 4.</td></tr>
</table>

<h2 id="s6">6. Separazione fra sito pubblico e console di gestione</h2>
<p>È stata svolta una verifica specifica, su richiesta, per accertare che <b>il servizio del sito pubblico non possa in alcun modo impartire comandi alla console di gestione</b>. L'esito è negativo per l'attaccante.</p>
<div class="verdict"><span class="big">Esito: nessun canale dal sito verso la console</span>
<p>La direzione della comunicazione è unidirezionale e <b>opposta</b> a quella che renderebbe possibile un attacco di questo tipo.</p></div>
<ul>
<li><b>È la console a interrogare il servizio, mai il contrario.</b> Tutte le interazioni sono avviate dalla console. Il servizio non avvia alcuna connessione verso la console, non ne conosce l'indirizzo e non possiede credenziali per raggiungerla. Un attaccante che ottenesse il pieno controllo del servizio non acquisirebbe con ciò alcun canale verso la console.</li>
<li><b>Non esiste alcun punto d'ingresso della console invocabile dal servizio.</b> Le credenziali impiegate dalla console per interrogare il servizio restano lato server e non vengono mai esposte al browser.</li>
<li><b>Il solo flusso di dati dal sito alla console è la coda delle richieste di prova</b>, alimentata dal modulo pubblico del sito. Questo flusso è stato tracciato dall'ingresso fino a destinazione: i dati sono trattati come <b>dati</b> e non diventano mai istruzioni, in nessuno dei punti in cui vengono conservati, mostrati o impiegati. <b>Nessun percorso conduce dai contenuti di una richiesta di prova all'esecuzione di un comando.</b></li>
<li><b>Il modulo pubblico è protetto contro l'abuso</b> con validazione dei campi lato server, verifica anti-robot, limitazione per indirizzo di provenienza, trappola per automatismi, consenso al trattamento verificato lato server e conservazione a termine.</li>
</ul>

<h2 id="s7">7. Interventi applicati</h2>
<p>Tutti gli interventi sono stati applicati durante l'attività e verificati. In sintesi, e nei termini sanitizzati di questo documento:</p>
<table>
<tr><th>Intervento</th><th>Componenti</th></tr>
<tr><td>Controllo automatico, bloccante alla costruzione dell'immagine, che l'interprete includa la correzione di sicurezza del 21 ottobre 2026</td><td>Gestionale, console</td></tr>
<tr><td>Adozione integrale delle mitigazioni raccomandate per entrambe le vulnerabilità, in forma non sovrascrivibile dal codice applicativo</td><td>Gestionale, console</td></tr>
<tr><td>Disattivazione delle funzionalità individuate come inneschi dell'attacco e non necessarie al servizio</td><td>Gestionale, console</td></tr>
<tr><td>Limiti su dimensione e struttura delle richieste, imposti dal server web prima dell'interprete</td><td>Gestionale, console</td></tr>
<tr><td>Tetto di memoria per contenitore, a contenere un eccesso senza coinvolgere l'interprete</td><td>Gestionale, console</td></tr>
<tr><td>Riduzione, su due livelli indipendenti, della superficie di esecuzione interna raggiungibile dal web</td><td>Gestionale, console</td></tr>
<tr><td>Insieme completo di intestazioni di sicurezza, con politica dei contenuti restrittiva, su tutti i componenti applicativi</td><td>Console</td></tr>
<tr><td>Eliminazione di ogni dipendenza da codice eseguibile fornito da terzi attraverso la rete</td><td>Console</td></tr>
<tr><td>Impostazioni di produzione dell'interprete, con messaggi diagnostici esclusi dalle risposte</td><td>Console</td></tr>
<tr><td>Estensione della verifica CSRF a tutte le operazioni di scrittura</td><td>Gestionale</td></tr>
<tr><td>Credenziali iniziali casuali e univoche per ciascun account</td><td>Gestionale</td></tr>
</table>

<h2 id="s8">8. Vigilanza e manutenzione</h2>
<p>La messa in sicurezza rispetto a una vulnerabilità di piattaforma non è un atto concluso. Sono previste le seguenti attività.</p>
<ul>
<li><b>Ricostruzione delle immagini con interprete aggiornato</b> per tutte le istanze in esercizio: la correzione è efficace solo dopo la ricostruzione e il riavvio dei processi. Il controllo automatico introdotto rende l'operazione verificabile, perché una ricostruzione su interprete non corretto non va a termine.</li>
<li><b>Sorveglianza degli indicatori di attacco</b> segnalati dai ricercatori per queste due vulnerabilità, sulla registrazione degli eventi delle istanze.</li>
<li><b>Programmazione del passaggio a un ramo dell'interprete con supporto esteso.</b> Il ramo attualmente impiegato cessa di ricevere correzioni di sicurezza il <b>31 dicembre 2026</b>: il passaggio va completato entro tale data, e il controllo automatico introdotto copre già i rami successivi.</li>
<li><b>Mantenimento degli strumenti interni su rete riservata</b>, non esposti su Internet, come misura perimetrale indipendente dalle protezioni applicative.</li>
</ul>

<h2 id="s9">9. Dichiarazione conclusiva e avvertenze</h2>
<p>Sulla base delle attività svolte, alla data del __DATA__ lo stack applicativo <b>BusItinera</b> risulta <b>protetto rispetto alle vulnerabilità PHP CVE-2026-109618 e CVE-2026-109619</b>, con la correzione dell'interprete resa obbligatoria e verificata automaticamente e con le misure di mitigazione raccomandate integralmente adottate; i <b>rilievi di sicurezza applicativa individuati durante la scansione sono stati tutti corretti e riverificati</b>, e nessuno è rimasto aperto; è stata accertata l'<b>assenza di qualunque canale</b> che consenta al servizio del sito pubblico di impartire comandi alla console di gestione.</p>
<p>Si richiama l'attenzione sul fatto che l'efficacia della correzione di piattaforma sulle singole istanze in esercizio è subordinata alla ricostruzione delle immagini e al riavvio dei processi, secondo quanto indicato al capitolo 8.</p>
<div class="disclaimer">
<p><b>Avvertenze.</b> Il presente attestato è redatto a fini informativi e di verifica interna. L'attività è stata condotta con l'assistenza di un sistema di intelligenza artificiale (Claude di Anthropic) per conto del titolare del software; non costituisce una certificazione accreditata di terza parte, né un test di penetrazione su sistemi in esercizio, né una garanzia assoluta di assenza di difetti o vulnerabilità. La verifica è stata svolta mediante analisi del codice sorgente e delle configurazioni, con riscontro funzionale delle correzioni in ambiente di prova. La sicurezza informatica è un processo continuo: l'esito si riferisce all'ambito, ai componenti, alle versioni e alla data indicati, e non si estende a vulnerabilità divulgate successivamente. Le informazioni sulle vulnerabilità di piattaforma sono riprese dagli avvisi pubblici del progetto PHP e dei gruppi di ricerca che le hanno segnalate. Restano impregiudicati i termini di licenza e le limitazioni di responsabilità applicabili al software.</p>
</div>
""".replace("__DATA__", DATA_SCANSIONE).replace("__VERS__", VERSIONE_SCANSIONATA)
