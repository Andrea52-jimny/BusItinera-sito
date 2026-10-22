# -*- coding: utf-8 -*-
"""PDF 3 — Accordo di nomina a Responsabile del trattamento (art. 28 GDPR).

Documento destinato alla firma del cliente: il cliente e' titolare dei dati
che inserisce nel gestionale (propri dipendenti, autisti, clienti finali,
passeggeri), il fornitore li tratta per suo conto e quindi e' responsabile.
Senza questo accordo il trattamento e' privo della base contrattuale che
l'art. 28, par. 3 pretende.

── DA TENERE AGGIORNATO ────────────────────────────────────────────────────
ALLEGATO B (sub-responsabili): e' l'elenco di chi, oltre al fornitore, tocca
i dati. Va corretto ogni volta che l'infrastruttura cambia — un fornitore di
hosting che si aggiunge, uno che si toglie. Un allegato che non corrisponde
alla realta' e' peggio che non averlo: dichiara il falso al cliente.

VERSIONE_ACCORDO / DATA_ACCORDO si spostano quando cambia il testo.
"""

VERSIONE_ACCORDO = "1.1"
DATA_ACCORDO = "22 ottobre 2026"

TOC = [
    ("a0",  "Premesse e parti"),
    ("a1",  "1. Oggetto e durata"),
    ("a2",  "2. Istruzioni del Titolare"),
    ("a3",  "3. Riservatezza"),
    ("a4",  "4. Misure di sicurezza"),
    ("a5",  "5. Sub-responsabili"),
    ("a6",  "6. Diritti degli interessati"),
    ("a7",  "7. Violazioni dei dati personali"),
    ("a8",  "8. Valutazione d'impatto e consultazione preventiva"),
    ("a9",  "9. Trasferimenti fuori dallo Spazio economico europeo"),
    ("a10", "10. Audit e dimostrazione della conformità"),
    ("a11", "11. Restituzione e cancellazione al termine"),
    ("a12", "12. Responsabilità, modifiche e legge applicabile"),
    ("alA", "Allegato A — Dettaglio del trattamento"),
    ("alB", "Allegato B — Sub-responsabili autorizzati"),
    ("alC", "Allegato C — Misure di sicurezza"),
    ("firme", "Sottoscrizione"),
    ("legal", "Appendice — Avviso di Copyright"),
]

BODY = """
<h2 id="a0">Premesse e parti</h2>

<p>Il presente accordo disciplina il trattamento dei dati personali che il Fornitore svolge <b>per conto</b> del Cliente nell'ambito del servizio BusItinera, ai sensi dell'<b>art. 28 del Regolamento (UE) 2016/679</b> (di seguito "Regolamento" o "GDPR") e del D.Lgs. 196/2003 come modificato dal D.Lgs. 101/2018.</p>

<table class="k">
<tr><th>Titolare del trattamento</th><td>
<b>Il Cliente</b> — l'azienda che utilizza BusItinera.<br>
Ragione sociale: ............................................................<br>
Sede: ............................................................<br>
P.IVA / C.F.: ............................................................<br>
Email: ............................................................
</td></tr>
<tr><th>Responsabile del trattamento</th><td>
<b>Andrea Ceol</b> — autore e fornitore del software BusItinera.<br>
Frazione Callibago 50/e<br>
Email: busitinera@gmail.com
</td></tr>
</table>

<div class="note"><b>Perché due ruoli diversi.</b> I dati che finiscono nel gestionale — anagrafiche dei clienti, dati dei passeggeri, nomi e patenti degli autisti, importi e scadenze — appartengono all'azienda che li raccoglie e decide perché trattarli: è lei il <b>Titolare</b>. Il Fornitore quei dati non li raccoglie e non decide che farne: li conserva e li elabora perché il software funzioni, cioè li tratta <b>per conto</b> del Titolare. Questa è esattamente la figura del <b>Responsabile</b>, e l'art. 28 richiede che il rapporto sia messo per iscritto.</div>

<h2 id="a1">1. Oggetto e durata</h2>
<p>1.1. Il Titolare nomina il Fornitore Responsabile del trattamento dei dati personali trattati attraverso il servizio BusItinera, con le modalità e nei limiti descritti nell'<b>Allegato A</b>.</p>
<p>1.2. La nomina decorre dall'attivazione del servizio e resta efficace per tutta la sua durata. Cessa automaticamente con la cessazione del servizio, fatti salvi gli obblighi dell'art. 11 (restituzione e cancellazione) e gli obblighi di riservatezza, che sopravvivono senza limiti di tempo.</p>
<p>1.3. Il Fornitore non acquisisce alcun diritto sui dati personali del Titolare e non può utilizzarli per finalità proprie, in nessuna forma: né per sviluppare o addestrare prodotti, né per analisi commerciali, né per fini statistici al di fuori di quanto strettamente necessario al funzionamento e alla sicurezza del servizio.</p>

<h2 id="a2">2. Istruzioni del Titolare</h2>
<p>2.1. Il Fornitore tratta i dati personali <b>soltanto su istruzione documentata</b> del Titolare (art. 28, par. 3, lett. a). Costituiscono istruzioni documentate: il presente accordo con i suoi allegati, il contratto di servizio, e le richieste che il Titolare invia per iscritto all'indirizzo email indicato in premessa.</p>
<p>2.2. Le operazioni che il software compie per funzionare — salvare, leggere, modificare, esportare, cancellare i dati inseriti dagli utenti del Titolare, generare documenti e file XML, inviare notifiche agli utenti indicati dal Titolare, eseguire backup — si intendono istruite dal Titolare con l'adesione al servizio.</p>
<p>2.3. Il Fornitore informa immediatamente il Titolare se, a suo parere, un'istruzione ricevuta viola il Regolamento o altre norme sulla protezione dei dati (art. 28, par. 3, ultimo periodo), e può sospenderne l'esecuzione fino a chiarimento.</p>
<p>2.4. Il Titolare garantisce di aver raccolto i dati che inserisce nel servizio in modo lecito, di aver fornito agli interessati l'informativa dovuta e di disporre di una base giuridica idonea. Il Fornitore non ha modo di verificarlo e non risponde della liceità della raccolta a monte.</p>

<h2 id="a3">3. Riservatezza</h2>
<p>3.1. Il Fornitore garantisce che chiunque sia autorizzato a trattare i dati personali per suo conto si sia impegnato alla riservatezza o abbia un adeguato obbligo legale di riservatezza (art. 28, par. 3, lett. b).</p>
<p>3.2. L'accesso ai dati del Titolare è limitato alle sole persone a cui serve per erogare il servizio, prestare assistenza o risolvere un guasto, e per il tempo strettamente necessario. Ogni accesso di questo tipo avviene su richiesta o con la consapevolezza del Titolare, salvo gli interventi urgenti necessari a ripristinare il servizio o a contenere un incidente di sicurezza, dei quali il Titolare viene informato senza ritardo.</p>

<h2 id="a4">4. Misure di sicurezza</h2>
<p>4.1. Il Fornitore adotta le misure tecniche e organizzative adeguate previste dall'<b>art. 32</b> del Regolamento, descritte nell'<b>Allegato C</b>, tenendo conto dello stato dell'arte, dei costi, della natura dei dati e dei rischi per i diritti e le libertà degli interessati.</p>
<p>4.2. Le misure possono essere aggiornate nel tempo. Il livello di protezione non può in nessun caso essere ridotto rispetto a quello descritto nell'Allegato C.</p>
<p>4.3. Il Titolare è responsabile delle misure che dipendono da lui: scelta e custodia delle credenziali, attribuzione dei ruoli e dei permessi agli utenti della propria azienda, attivazione della verifica in due passaggi dove opportuno, revoca tempestiva degli accessi di chi lascia l'azienda.</p>

<h2 id="a5">5. Sub-responsabili</h2>
<p>5.1. Il Titolare autorizza il Fornitore a ricorrere ai sub-responsabili elencati nell'<b>Allegato B</b> (autorizzazione specifica, art. 28, par. 2).</p>
<p>5.2. Il Fornitore può aggiungere o sostituire sub-responsabili informandone il Titolare con <b>almeno 30 giorni</b> di anticipo. Entro tale termine il Titolare può opporsi per motivi ragionevoli e documentati legati alla protezione dei dati; in caso di opposizione, le parti cercano una soluzione alternativa e, se non la trovano, il Titolare può recedere dal servizio senza penalità.</p>
<p>5.3. Il Fornitore impone a ciascun sub-responsabile, mediante contratto, gli stessi obblighi di protezione dei dati previsti dal presente accordo, e risponde verso il Titolare dell'operato del sub-responsabile come del proprio (art. 28, par. 4).</p>

<h2 id="a6">6. Diritti degli interessati</h2>
<p>6.1. Il Fornitore assiste il Titolare, con misure tecniche e organizzative adeguate, nel dare seguito alle richieste con cui gli interessati esercitano i diritti previsti dagli artt. 15–22 del Regolamento (art. 28, par. 3, lett. e).</p>
<p>6.2. Il gestionale consente al Titolare di esercitare in autonomia la maggior parte di queste operazioni: consultare, correggere, esportare in formato CSV e cancellare i dati delle proprie anagrafiche. Per quanto non ottenibile dall'interfaccia, il Fornitore presta assistenza entro <b>10 giorni lavorativi</b> dalla richiesta scritta.</p>
<p>6.3. Se un interessato si rivolge direttamente al Fornitore, questi non dà seguito alla richiesta e la trasmette senza ritardo al Titolare, che è l'unico competente a rispondere.</p>

<h2 id="a7">7. Violazioni dei dati personali</h2>
<p>7.1. Il Fornitore notifica al Titolare ogni violazione di dati personali <b>senza ingiustificato ritardo</b> e comunque <b>entro 24 ore</b> da quando ne viene a conoscenza (art. 28, par. 3, lett. f e art. 33, par. 2).</p>
<p>7.2. La notifica descrive, nella misura in cui sono noti: la natura della violazione, le categorie e il numero approssimativo di interessati e di registrazioni coinvolte, le probabili conseguenze, le misure adottate o proposte per porvi rimedio e per attenuarne gli effetti. Le informazioni mancanti vengono fornite man mano che diventano disponibili.</p>
<p>7.3. La notifica all'autorità di controllo e la comunicazione agli interessati, quando dovute, restano in capo al <b>Titolare</b>, che decide se e come effettuarle. Il Fornitore collabora fornendo ogni informazione utile.</p>

<h2 id="a8">8. Valutazione d'impatto e consultazione preventiva</h2>
<p>8.1. Il Fornitore assiste il Titolare, tenuto conto della natura del trattamento e delle informazioni a sua disposizione, nello svolgimento della valutazione d'impatto sulla protezione dei dati (art. 35) e nella consultazione preventiva dell'autorità di controllo (art. 36), quando il Titolare le ritenga necessarie.</p>

<h2 id="a9">9. Trasferimenti fuori dallo Spazio economico europeo</h2>
<p>9.1. I dati del Titolare sono conservati su infrastruttura situata nello <b>Spazio economico europeo</b>.</p>
<p>9.2. Qualora un sub-responsabile comporti un trasferimento verso un paese terzo, il trasferimento avviene soltanto in presenza di una delle garanzie previste dal Capo V del Regolamento: una decisione di adeguatezza della Commissione europea, oppure le clausole contrattuali tipo adottate dalla Commissione, accompagnate dalla valutazione del contesto giuridico del paese di destinazione e, ove necessario, da misure supplementari. I sub-responsabili interessati sono indicati come tali nell'Allegato B.</p>

<h2 id="a10">10. Audit e dimostrazione della conformità</h2>
<p>10.1. Il Fornitore mette a disposizione del Titolare tutte le informazioni necessarie a dimostrare il rispetto degli obblighi dell'art. 28 e consente e contribuisce alle verifiche, comprese le ispezioni, realizzate dal Titolare o da un soggetto da questi incaricato (art. 28, par. 3, lett. h).</p>
<p>10.2. Le verifiche si svolgono con preavviso scritto di almeno <b>15 giorni</b>, in orario lavorativo, senza interferire con la continuità del servizio e nel rispetto della riservatezza dei dati di altri clienti. Salvo che la verifica faccia emergere inadempimenti, i costi del soggetto incaricato dal Titolare restano a carico di quest'ultimo.</p>
<p>10.3. Il Fornitore tiene il registro delle categorie di attività di trattamento svolte per conto del Titolare (art. 30, par. 2) e lo rende disponibile su richiesta.</p>

<h2 id="a11">11. Restituzione e cancellazione al termine</h2>
<p>11.1. Alla cessazione del servizio, a scelta del Titolare, il Fornitore <b>restituisce</b> i dati personali o li <b>cancella</b>, cancellando in ogni caso le copie esistenti (art. 28, par. 3, lett. g).</p>
<p>11.2. La restituzione avviene in un formato strutturato e di uso comune: esportazione delle anagrafiche e dei movimenti in CSV e, su richiesta, copia integrale della base di dati dell'istanza.</p>
<p>11.3. Salvo diversa istruzione scritta, i dati vengono cancellati entro <b>30 giorni</b> dalla cessazione. I backup cifrati esistenti al momento della cessazione vengono cancellati secondo il normale ciclo di rotazione e comunque entro <b>90 giorni</b>: nel frattempo restano cifrati e non vengono utilizzati per alcuna finalità, se non l'eventuale ripristino richiesto dal Titolare.</p>
<p>11.4. Il Fornitore conserva i dati oltre tali termini solo se un obbligo di legge lo impone, e per il tempo da esso previsto, informandone il Titolare.</p>

<h2 id="a12">12. Responsabilità, modifiche e legge applicabile</h2>
<p>12.1. Ciascuna parte risponde dei danni causati dal proprio inadempimento, nei limiti e secondo i criteri dell'art. 82 del Regolamento.</p>
<p>12.2. Il presente accordo prevale, per quanto riguarda il trattamento dei dati personali, su eventuali clausole difformi del contratto di servizio.</p>
<p>12.3. Le modifiche sono valide solo se concordate per iscritto, salvo quelle rese necessarie da mutamenti normativi o da provvedimenti dell'autorità di controllo, che il Fornitore comunica al Titolare con ragionevole preavviso.</p>
<p>12.4. L'accordo è regolato dalla <b>legge italiana</b>. Per ogni controversia è competente il foro del luogo di residenza o sede del convenuto, salvo i fori inderogabili previsti dalla legge.</p>

<h2 id="alA">Allegato A — Dettaglio del trattamento</h2>
<table class="k">
<tr><th>Oggetto</th><td>Erogazione del software gestionale BusItinera per la pianificazione di viaggi e noleggi, la gestione di preventivi, clienti, mezzi, personale, contabilità e fatturazione elettronica.</td></tr>
<tr><th>Durata</th><td>La durata del servizio, più i termini di cancellazione dell'art. 11.</td></tr>
<tr><th>Natura e finalità</th><td>Raccolta, registrazione, organizzazione, strutturazione, conservazione, consultazione, modifica, estrazione, uso, backup e cancellazione dei dati inseriti dagli utenti del Titolare, al solo fine di far funzionare il servizio.</td></tr>
<tr><th>Tipi di dati personali</th><td>
<b>Clienti del Titolare:</b> ragione sociale e nome, indirizzo, telefono, email, partita IVA, codice fiscale, codice destinatario SDI, codice univoco ufficio per la Pubblica Amministrazione.<br>
<b>Personale del Titolare:</b> nome e cognome, email, credenziali di accesso in forma cifrata, ruolo e permessi, numero e categorie di patente, ente e date di rilascio e scadenza, scadenza CQC, stato di servizio.<br>
<b>Conducenti autorizzati indicati dal cliente finale</b> (noleggio senza conducente): nome e cognome, codice fiscale, luogo e data di nascita, residenza, numero di patente con date di emissione e scadenza, telefono.<br>
<b>Dati di servizio:</b> percorsi, orari, tappe, importi, scadenze di pagamento, note operative, note private, chilometraggi, documenti generati (preventivi, conferme, ordini di servizio, contratti, fatture e relativi XML).<br>
<b>Dati tecnici:</b> registro delle attività degli utenti, indirizzi IP dei tentativi di accesso, iscrizioni alle notifiche, credenziali di accesso biometrico (chiavi pubbliche, mai dati biometrici).
</td></tr>
<tr><th>Categorie di interessati</th><td>Dipendenti e collaboratori del Titolare, autisti, clienti del Titolare e loro referenti, conducenti autorizzati indicati dai clienti finali, eventuali passeggeri nominati nelle note operative.</td></tr>
<tr><th>Categorie particolari</th><td>Il servizio <b>non è destinato</b> al trattamento delle categorie particolari di dati dell'art. 9 né dei dati dell'art. 10. Il Titolare si impegna a non inserirne nei campi liberi.</td></tr>
</table>

<h2 id="alB">Allegato B — Sub-responsabili autorizzati</h2>
<p>Elenco aggiornato alla data del presente accordo. Ogni variazione è comunicata al Titolare con il preavviso dell'art. 5.2.</p>
<table>
<tr><th>Sub-responsabile</th><th>Attività svolta</th><th>Ubicazione dei dati</th></tr>
<tr><td><b>Andrea Ceol</b><br>(infrastruttura propria)</td><td>Conservazione ed elaborazione dei dati dell'istanza; console di gestione delle istanze; backup cifrati.</td><td>Italia</td></tr>
<tr><td><b>Aruba S.p.A.</b></td><td>Infrastruttura server e conservazione delle copie di sicurezza cifrate.</td><td>Italia</td></tr>
<tr><td><b>Cloudflare, Inc.</b></td><td>Pubblicazione sicura dell'istanza, protezione dagli attacchi e recapito delle notifiche push.</td><td>Infrastruttura europea; società statunitense. Trasferimenti coperti dalle clausole contrattuali tipo della Commissione europea e dall'adesione al quadro UE–USA sulla protezione dei dati.</td></tr>
</table>
<div class="warn"><b>Nota per il Fornitore.</b> Questo allegato è un elenco di fatto, non una dichiarazione di intenti: va corretto ogni volta che l'infrastruttura cambia. Un sub-responsabile attivo ma non elencato rende il trattamento privo di autorizzazione; uno elencato ma non più usato dichiara al Cliente qualcosa che non è vero.</div>

<h2 id="alC">Allegato C — Misure di sicurezza</h2>
<p>Misure adottate ai sensi dell'art. 32 del Regolamento.</p>
<table class="k">
<tr><th>Controllo degli accessi</th><td>Accesso nominativo con password cifrata con algoritmo a senso unico; verifica in due passaggi (TOTP) con codici di recupero; accesso con impronta, volto o codice del dispositivo (WebAuthn) con verifica dell'utente obbligatoria e controllo anti-clonazione; blocco progressivo dopo tentativi falliti, per utente e per indirizzo di rete; invalidazione delle altre sessioni al cambio password; scadenza delle sessioni inattive.</td></tr>
<tr><th>Permessi</th><td>Quattro ruoli predefiniti più interruttori granulari; le funzioni non consentite non sono raggiungibili, non solo nascoste. Dal telefono gli eventi del calendario sono in sola lettura per tutti i ruoli.</td></tr>
<tr><th>Separazione dei dati</th><td>Ogni azienda ha la propria istanza, con base di dati e credenziali separate: nessun dato è condiviso fra clienti diversi.</td></tr>
<tr><th>Cifratura</th><td>Trasmissione esclusivamente su HTTPS. Backup cifrati. Segreto della verifica in due passaggi cifrato a riposo quando è configurata la chiave applicativa.</td></tr>
<tr><th>Integrità</th><td>Interrogazioni parametrizzate; protezione contro le richieste cross-site (CSRF) su tutte le operazioni di scrittura; insieme completo di intestazioni di sicurezza HTTP, Content Security Policy restrittiva inclusa; neutralizzazione delle formule negli export CSV; operazioni multi-tabella in transazione; controllo di concorrenza sulle modifiche simultanee. Nessun componente dipende da codice eseguibile fornito da terzi attraverso la rete: le librerie sono servite dall'applicazione stessa.</td></tr>
<tr><th>Gestione delle vulnerabilità</th><td>Sorveglianza degli avvisi di sicurezza dei componenti di piattaforma e aggiornamento tempestivo. La versione corretta dell'interprete è imposta da un <b>controllo automatico bloccante</b>: la costruzione di un'immagine applicativa non va a termine se l'interprete non include le correzioni di sicurezza note, così nessuna istanza può entrare in esercizio su una versione vulnerabile. Limiti su dimensione e struttura delle richieste in ingresso, applicati prima dell'elaborazione.</td></tr>
<tr><th>Tracciabilità</th><td>Registro delle attività immutabile su ogni operazione di scrittura, con utente, momento e dettaglio delle modifiche; conservazione configurabile, predefinita a 24 mesi.</td></tr>
<tr><th>Continuità</th><td>Backup automatici periodici e copia offsite cifrata; possibilità di ripristino su richiesta del Titolare. Tetto di risorse per singola istanza, così che un'anomalia su un cliente non possa degradare il servizio degli altri.</td></tr>
<tr><th>Verifiche</th><td>Collaudo funzionale e di sicurezza documentato nell'<i>Attestato di Collaudo</i>; scansione periodica di sicurezza dell'intero stack applicativo — esposizione alle vulnerabilità di piattaforma e verifica per classi di vulnerabilità — documentata nell'<i>Attestato di Cybersecurity</i>. Entrambi disponibili nella sezione Download del sito.</td></tr>
</table>

<h2 id="firme">Sottoscrizione</h2>
<p>Le parti sottoscrivono il presente accordo, che forma parte integrante del contratto di servizio.</p>
<table>
<tr><th style="width:50%">Il Titolare del trattamento<br><span style="font-weight:400">(il Cliente)</span></th><th>Il Responsabile del trattamento<br><span style="font-weight:400">(Andrea Ceol)</span></th></tr>
<tr><td style="height:70px;vertical-align:bottom">Luogo e data ..........................................<br><br>Firma ..........................................</td>
    <td style="height:70px;vertical-align:bottom">Luogo e data ..........................................<br><br>Firma ..........................................</td></tr>
</table>
<div class="note">Ai sensi degli artt. 1341 e 1342 del codice civile, il Titolare approva espressamente le clausole di cui agli articoli <b>5</b> (sub-responsabili), <b>10</b> (modalità e costi delle verifiche), <b>11</b> (termini di cancellazione) e <b>12.4</b> (foro competente).</div>
<table>
<tr><td style="height:52px;vertical-align:bottom">Firma per specifica approvazione ................................................................</td></tr>
</table>
"""
