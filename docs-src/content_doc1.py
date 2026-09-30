# -*- coding: utf-8 -*-
"""PDF 1 — Documentazione delle Funzionalità.
Aggiornato alla v1.15.1 (promemoria automatici + home mobile amministratori).
"""

TOC = [
    ("s1",  "1. Introduzione, ruoli e dispositivi"),
    ("s2",  "2. Calendario e pianificazione"),
    ("s3",  "3. Viaggi"),
    ("s4",  "4. Assegnazione autisti"),
    ("s5",  "5. Noleggi"),
    ("s6",  "6. Appuntamenti"),
    ("s7",  "7. Preventivi"),
    ("s8",  "8. Acconto e saldo"),
    ("s9",  "9. Contabilità: flag di stato e congelamento"),
    ("s10", "10. Lista viaggi, filtri ed export CSV"),
    ("s11", "11. Avvisi, scadenze e promemoria automatici"),
    ("s12", "12. Clienti"),
    ("s13", "13. Veicoli"),
    ("s14", "14. Utenti e permessi granulari"),
    ("s15", "15. Dati Azienda e banche"),
    ("s16", "16. Password, 2FA e accesso con impronta"),
    ("s17", "17. Registro attività"),
    ("s18", "18. Fatturazione elettronica (FatturaPA)"),
    ("s19", "19. Portale Autista, Mobile e notifiche"),
    ("s20", "20. Moduli stampabili"),
    ("s21", "21. Solidità e controlli"),
    ("legal", "Appendice — Avviso di Copyright"),
]

BODY = """
<h2 id="s1">1. Introduzione, ruoli e dispositivi</h2>
<p>BusItinera è un gestionale completo per aziende di trasporto e noleggio con autista: pianificazione dei viaggi su calendario, preventivi, contabilità, fatturazione elettronica FatturaPA e portale mobile dedicato agli autisti.</p>

<h3>1.1 I quattro ruoli (preset)</h3>
<p>Dalla versione 1.5.0 i permessi funzionano con un preset (il ruolo di base) più, se serve, alcuni interruttori per affinare cosa quella persona può fare.</p>
<table>
<tr><th>Ruolo</th><th>Cosa può fare</th><th>A chi serve</th></tr>
<tr><td><b>Amministratore</b></td><td>Tutto: operatività, contabilità, gestione utenti e permessi, sblocchi. Ha sempre tutti gli interruttori accesi.</td><td>Titolare, socio, IT di riferimento</td></tr>
<tr><td><b>Operatore</b></td><td>Operatività quotidiana (viaggi, preventivi, noleggi, appuntamenti, clienti), modulabile con gli interruttori.</td><td>Ufficio, addetti operativi</td></tr>
<tr><td><b>Autista</b></td><td>Solo il portale mobile in sola lettura sui propri viaggi assegnati.</td><td>Autisti aziendali</td></tr>
<tr><td><b>Consultazione</b></td><td>Sola lettura su tutta l'operatività. Nessuna scrittura.</td><td>Contabile esterno, revisore, direzione</td></tr>
</table>
<p><b>Menu su misura:</b> le voci e i pulsanti che un utente non può usare vengono nascosti del tutto, non solo disabilitati: ognuno vede solo ciò che gli compete.</p>

<h3>1.2 Dispositivi</h3>
<p>Il pannello amministratore completo si usa da <b>computer e da tablet</b> (iPad, tablet Android): i tablet sono equiparati al desktop. Dal <b>telefono</b> l'applicazione presenta invece l'interfaccia adatta al ruolo, riconosciuto al momento dell'accesso:</p>
<ul>
<li><b>Autisti</b> → <b>Portale Autista</b> (cap. 19), con i propri viaggi assegnati.</li>
<li><b>Amministratori e operatori</b> → <b>Home mobile</b> (par. 19.2), una schermata di sola lettura con la giornata e le scadenze. La gestione completa resta su computer e tablet.</li>
</ul>
<div class="note"><b>Cambio di dispositivo.</b> Il tipo di dispositivo viene rivalutato a ogni ripresa della sessione: una sessione aperta al computer e ripresa dal telefono (o viceversa) porta automaticamente all'interfaccia giusta, senza dover rifare l'accesso.</div>

<h2 id="s2">2. Calendario e pianificazione</h2>
<p>Viste Mese / Settimana / Giorno, pulsante Oggi, navigazione con le frecce e schermo intero. Ogni evento è colorato con il colore del veicolo assegnato; le icone distinguono viaggio, noleggio e appuntamento. I viaggi multi-giorno appaiono come barre orizzontali. I veicoli fuori servizio e gli autisti sospesi fanno apparire l'evento in grigio con icona di avvertimento.</p>
<h3>2.1 Date e orari</h3>
<p>Tutti i campi data usano il formato gg/mm/aaaa e gli orari il formato 24 ore. Ogni campo si compila da tastiera (le barre e i due punti si inseriscono da soli) o dal selettore grafico. I filtri compatti "Da / A" della lista viaggi si compilano solo dal selettore.</p>

<h2 id="s3">3. Viaggi</h2>
<p>Un viaggio rappresenta un servizio di trasporto con partenza, arrivo, tappe intermedie, veicolo e autisti. Si apre da <b>Nuovo Viaggio</b> nella topbar (solo admin/editor) o cliccando un giorno vuoto sul calendario.</p>
<ul>
<li><b>Cliente:</b> ricerca in anagrafica con card riepilogativa; possibilità di creare un cliente "al volo" senza uscire dal form.</li>
<li><b>Percorso:</b> luogo di partenza e arrivo con autocompletamento Google Maps e nomi personalizzati; tappe intermedie con rinumerazione automatica.</li>
<li><b>Veicolo:</b> ricerca per targa o soprannome; badge OCCUPATO per i mezzi già impegnati; opzione veicolo esterno. Obbligatorio almeno un veicolo interno o un'azienda esterna.</li>
<li><b>Autisti:</b> uno o più; blocco dell'assegnazione se già impegnati, con messaggio d'errore contenente il nome.</li>
<li><b>Dati economici:</b> prezzo, CIG/ordine, metodo di pagamento, modalità (unico o acconto+saldo), costi extra con somma automatica, accompagnatore con recapito visibile all'autista.</li>
<li><b>Note:</b> Nota di Viaggio condivisa con gli autisti; Note Private visibili solo ad admin/editor (mai esposte agli autisti, nemmeno via risposta API grezza).</li>
</ul>
<p>Al salvataggio il sistema controlla automaticamente conflitti di veicolo e autisti. Dal dettaglio si modifica (anche inline le località, con l'icona matita) o si elimina, con pulizia dei collegamenti (autisti, tappe, servizi).</p>

<h2 id="s4">4. Assegnazione autisti</h2>
<p>Nella sezione Autisti del form si cerca per nome; gli autisti già impegnati mostrano il badge OCCUPATO e finiscono in fondo alla lista, quelli sospesi non appaiono. Selezione multipla con chip rimovibili.</p>

<h2 id="s5">5. Noleggi</h2>
<p>Il noleggio traccia la locazione di un veicolo aziendale (veicolo interno obbligatorio, nessuna opzione esterna), con numero contratto, date e luogo di riconsegna, controllo automatico di sovrapposizione. Dal dettaglio si stampa il contratto di locazione senza conducente, con la tabella degli utilizzatori autorizzati.</p>

<h2 id="s6">6. Appuntamenti</h2>
<p>Eventi generici (riunioni, manutenzioni, formazioni) non collegati a veicoli o autisti, visibili solo ad admin ed editor. Titolo obbligatorio, durata minima 15 minuti (default 60), icona campanella su sfondo giallo.</p>

<h2 id="s7">7. Preventivi</h2>
<p>La sezione Preventivi formula offerte per viaggi e noleggi, ne segue lo stato e le trasforma in eventi reali. Un preventivo può contenere più blocchi indipendenti con ricalcolo del totale generale.</p>
<h3>7.1 Ciclo di vita e immutabilità</h3>
<p>Un preventivo nasce come <b>Bozza</b> (liberamente modificabile). Quando lo si <b>Invia</b> viene congelato: da quel momento non è più modificabile, così la copia ricevuta dal cliente non cambia. Stati: Bozza → Inviato → Convertito; una revisione sostituita diventa Sostituito; una chiusa senza conversione diventa Annullato (con motivo); Scaduto è automatico.</p>
<ul>
<li><b>Converti:</b> genera gli eventi reali (uno per blocco); dopo la conversione il pulsante sparisce. Il preventivo resta congelato nello storico.</li>
<li><b>Revisioni:</b> su un preventivo inviato si crea una nuova revisione; lo storico è mantenuto, la versione precedente passa a "Sostituito".</li>
<li><b>Eliminazione:</b> consentita solo su bozze mai inviate e solo all'amministratore.</li>
</ul>
<h3>7.2 Stampa e documento archiviato</h3>
<p>PDF Preventivo (senza banche/scadenze) e PDF Conferma (con scadenze e IBAN predefinito, dopo la conversione). All'invio viene archiviata la copia esatta del documento: resta identica anche se in futuro cambiano listino o dati aziendali.</p>

<h2 id="s8">8. Acconto e saldo</h2>
<p>Nei form di viaggio, noleggio e preventivo si sceglie tra pagamento unico (una scadenza, un flag Pagato) e acconto + saldo (due scadenze e due flag). La percentuale (tra 1 e 99) e l'importo in € si calcolano in modo bidirezionale; la scadenza dell'acconto deve precedere quella del saldo.</p>

<h2 id="s9">9. Contabilità: flag di stato e congelamento</h2>
<p>Ogni viaggio e noleggio ha tre flag: <b>Fatturato</b>, <b>Pagato</b>, <b>Busta</b>. Modifica istantanea, riservata ad admin ed editor; i viewer/autisti non li vedono.</p>
<div class="warn"><b>Viaggi congelati:</b> quando un viaggio è fatturato o pagato viene congelato — non più modificabile né eliminabile dall'operatività normale. Solo chi ha l'interruttore "Può modificare viaggi già fatturati o pagati" (di norma l'amministratore) può forzare la modifica, e ogni forzatura resta scritta nel Registro attività. Anche la chiusura (lucchetto) blocca la modifica finché non si riapre.</div>
<p><b>Modifiche simultanee:</b> se due persone salvano quasi insieme lo stesso viaggio/cliente/preventivo, il secondo salvataggio viene fermato con un avviso (nessuna sovrascrittura silenziosa).</p>

<h2 id="s10">10. Lista viaggi, filtri ed export CSV</h2>
<p>Filtri combinabili (ricerca testuale, mese, intervallo date, autista, veicolo) e pulsante Reset. L'<b>Esporta CSV</b> apre una modale con 8 gruppi di colonne selezionabili; il file usa separatore <b>;</b>, codifica UTF-8 e rispetta i filtri attivi. Le celle sono neutralizzate contro l'esecuzione come formula nei fogli di calcolo.</p>

<h2 id="s11">11. Avvisi, scadenze e promemoria automatici</h2>
<p>Il gestionale sorveglia le scadenze aziendali in due modi complementari: la <b>campanella Avvisi</b>, che si consulta quando si vuole, e i <b>promemoria automatici</b>, che arrivano da soli senza che nessuno debba ricordarsi di guardare.</p>

<h3>11.1 La campanella Avvisi</h3>
<p>Raccoglie le scadenze aziendali in 4 categorie (Pagamenti, Bollo, Assicurazione, Azienda), con preavviso di 15 giorni. Le scadenze di bollo, assicurazione e licenza sono calcolate dai dati di veicoli e azienda (il Bollo l'ultimo giorno del mese successivo, regola italiana). "Segna come pagato" fa avanzare la data (Bollo +1 anno, Licenza +4 anni, Assicurazione secondo formula) e aggiorna la scheda del mezzo. I mezzi fuori servizio non generano scadenze; l'autista vede solo quelle del proprio mezzo.</p>

<h3>11.2 Promemoria automatici <span class="badge">NUOVO</span></h3>
<p>L'applicazione esegue da sola un <b>giro di controllo giornaliero</b>, a un orario configurabile (di norma le 18:00), e invia i promemoria a chi di competenza. Non richiede alcun servizio esterno: gira dentro l'installazione, sul server dell'azienda o nel cloud.</p>
<ul>
<li><b>"Viaggio di domani" agli autisti.</b> La sera prima, ogni autista riceve l'elenco dei viaggi che lo riguardano il giorno seguente, con orario e tratta.</li>
<li><b>Scadenze in avvicinamento ai titolari.</b> Amministratori e operatori ricevono un preavviso su bollo, assicurazione, revisione, tagliando, patente, CQC e licenza. Le patenti e le CQC in scadenza vengono segnalate <b>anche all'autista interessato</b>.</li>
<li><b>Tre preavvisi, nessun assillo.</b> Di norma a <b>30, 7 e 1 giorno</b> dalla scadenza (soglie modificabili). Se una scadenza è già entro l'ultima soglia utile, parte solo quella: non si ricevono due avvisi per lo stesso motivo.</li>
</ul>
<div class="note"><b>Niente doppioni, niente buchi.</b> Ogni promemoria viene inviato una volta sola, anche se il controllo viene ripetuto. Se il server era spento all'ora prevista, il primo controllo utile recupera il giro mancato. Se una scadenza viene aggiornata, il ciclo di preavvisi riparte sulla nuova data.</div>
<p>I promemoria arrivano nella <b>campanella Notifiche</b> personale e, se le notifiche push sono attive, anche sul telefono ad applicazione chiusa (par. 19.3).</p>

<h2 id="s12">12. Clienti</h2>
<p>Creazione e modifica dell'anagrafica (con controllo formale di Partita IVA e Codice Fiscale, inclusa l'omocodia del CF). Non è possibile eliminare un cliente associato a servizi. L'amministratore può <b>unire clienti doppioni</b>: viaggi, noleggi, preventivi e fatture del doppione vengono migrati sul cliente principale; l'operazione è irreversibile e tracciata.</p>

<h2 id="s13">13. Veicoli</h2>
<p>Gestione flotta (solo amministratore): anagrafica completa (targa univoca, telaio, posti, colore identificativo nel calendario), autista assegnato, dati di assicurazione e bollo con formula di scadenza. Un mezzo "Fuori servizio" non appare nelle ricerche né tra le scadenze. Non è eliminabile se associato a viaggi.</p>

<h2 id="s14">14. Utenti e permessi granulari</h2>
<p>Sezione riservata all'amministratore. Alla creazione lo username è generato automaticamente in formato <b>nome.cognome</b>; password minima 8 caratteri; al primo accesso è obbligatorio cambiarla. Il flag <b>Autista</b> abilita il portale mobile e il blocco scadenze patente/CQC.</p>
<h3>14.1 Gli interruttori</h3>
<table>
<tr><th>Interruttore</th><th>Cosa consente</th><th>Preset</th><th>Default</th></tr>
<tr><td>Può gestire i preventivi</td><td>Creare, modificare, inviare i preventivi</td><td>Operatore</td><td>Acceso</td></tr>
<tr><td>Può convertire un preventivo in viaggio</td><td>Trasformare un preventivo inviato in un viaggio</td><td>Operatore</td><td>Acceso</td></tr>
<tr><td>Può registrare pagamenti</td><td>Segnare acconti, saldi, fatturato/pagato</td><td>Operatore</td><td>Acceso</td></tr>
<tr><td>Può emettere fatture elettroniche</td><td>Generare l'XML FatturaPA, note di credito, download</td><td>Operatore</td><td>Acceso</td></tr>
<tr><td>Può eliminare clienti, veicoli e autisti</td><td>Cancellare le anagrafiche</td><td>Operatore</td><td>Acceso</td></tr>
<tr><td>Può consultare il registro attività</td><td>Aprire il Registro attività in sola lettura</td><td>Operatore, Consultazione</td><td>Spento</td></tr>
<tr><td>Può consultare le fatture</td><td>Aprire il modulo Fatture in sola lettura (anteprima e download XML), senza emetterle</td><td>Operatore, Consultazione</td><td>Spento</td></tr>
<tr><td>Può modificare viaggi già fatturati o pagati</td><td>Forzare la modifica dei viaggi congelati (tracciato)</td><td>Operatore</td><td>Spento</td></tr>
<tr><td>Può marcare i viaggi come completati (mobile)</td><td>Segnare come completato un viaggio assegnato, dal portale autista, dopo l'orario di rientro</td><td>Autista</td><td>Spento</td></tr>
</table>
<p><b>Vincolo "ultimo amministratore":</b> il sistema non permette di declassare, sospendere o eliminare l'unico amministratore rimasto. L'admin non può nemmeno modificare il proprio ruolo.</p>
<p><b>Altre azioni:</b> sospensione utente ("Non in servizio", con disconnessione immediata), reset password (senza richiedere quella attuale), disattivazione 2FA di un altro utente.</p>

<h2 id="s15">15. Dati Azienda e banche</h2>
<p>Anagrafica aziendale, contatti, dati fiscali (regime, licenza comunitaria, PEC) e gestione di più banche con flag "predefinita" (l'impostazione di una nuova deseleziona la precedente). IBAN e BIC/SWIFT vengono salvati in maiuscolo senza spazi. Nella card "Testi dei documenti" si personalizzano i testi di preventivo, conferma e contratto di noleggio (un campo vuoto mantiene il testo predefinito).</p>

<h2 id="s16">16. Password, 2FA e accesso con impronta</h2>
<p>Ogni utente può cambiare la propria password (min. 8 caratteri, attiva immediatamente). Il <b>2FA</b> (per Amministratore e Operatore) aggiunge un codice TOTP a 6 cifre generato da app come Google Authenticator: attivazione con QR o secret manuale, 8 codici di recupero monouso, opzione "Ricordami" per 15 giorni sullo stesso browser. Cambiando password i dispositivi fidati vengono invalidati. Ogni attivazione/disattivazione del 2FA è registrata nel Registro attività; i login e i codici inseriti non vengono tracciati.</p>

<h3>16.1 Accesso con impronta o Face ID (passkey) <span class="badge">NUOVO</span></h3>
<p>In alternativa a password e codice, si può entrare con l'<b>impronta digitale</b>, il <b>riconoscimento del volto</b> o il <b>codice di sblocco</b> del proprio dispositivo. È lo stesso gesto con cui si sblocca il telefono; la funzione è disponibile a tutti i ruoli, autisti compresi.</p>
<ul>
<li><b>Come si attiva:</b> una volta sola per dispositivo, da dentro l'applicazione (quindi già connessi, senza reinserire le credenziali). Dal pannello "Accesso con impronta" — raggiungibile dal menu del proprio nome nel gestionale, e dall'icona in alto nel portale autista e nella home mobile — si tocca "Registra questo dispositivo".</li>
<li><b>Come si entra:</b> nella schermata di accesso, il pulsante "Entra con impronta o Face ID" — il dispositivo propone l'account, senza digitare nome utente né password.</li>
<li><b>Più dispositivi:</b> se ne registrano quanti se ne vuole (telefono, tablet, computer), ognuno con un nome riconoscibile, rinominabile o rimovibile in qualsiasi momento.</li>
</ul>
<div class="note"><b>Sicurezza.</b> La passkey sostituisce sia la password sia il 2FA, senza indebolire l'accesso: per entrare servono il dispositivo registrato <b>e</b> la verifica biometrica di chi lo possiede (due fattori in un gesto). La chiave privata non lascia mai il dispositivo e sul server non è conservato alcun segreto riutilizzabile. <b>Password e 2FA restano sempre attivi come alternativa:</b> se un dispositivo si perde o si sostituisce, si accede come sempre e se ne registra uno nuovo. Ogni registrazione e rimozione è annotata nel Registro attività.</div>
<p>La funzione richiede una connessione sicura (HTTPS) ed è compatibile con iPhone/iPad (Face ID, Touch ID), Android (impronta), Windows Hello, Mac e chiavette di sicurezza.</p>

<h2 id="s17">17. Registro attività</h2>
<p>Diario di bordo immutabile: annota ogni azione di scrittura andata a buon fine (creazioni, modifiche, eliminazioni di viaggi, preventivi, noleggi, clienti, veicoli, utenti; pagamenti; cambi di ruolo/permessi; unione clienti; attivazioni 2FA), spesso con il dettaglio di cosa è cambiato. Le voci non si possono cancellare né modificare. Filtri per tipo e per data/utente/cliente/n. preventivo. Conservazione 24 mesi. Per riservatezza, login e logout non vengono tracciati.</p>

<h2 id="s18">18. Fatturazione elettronica (FatturaPA)</h2>
<p>Dalla voce <b>Fatture</b> si genera il file FatturaPA (XML per lo SdI) a partire da viaggi e noleggi. L'app produce il file (non lo invia allo SdI): lo si carica poi sul proprio canale o lo si passa al commercialista. Il tracciato prodotto segue la versione ufficiale ed è costruito internamente, senza servizi esterni.</p>
<table class="k">
<tr><th>Regime</th><th>Come esce la fattura</th></tr>
<tr><td>RF01 — Ordinario</td><td>Con IVA (l'aliquota del viaggio/noleggio, es. 10%).</td></tr>
<tr><td>RF19 — Forfettario</td><td>Senza IVA: Natura N2.2 e, se l'importo supera 77,47 €, bollo da 2 €.</td></tr>
</table>
<p><b>Funzioni principali:</b> editor con anteprima modificabile prima dell'emissione; numerazione progressiva annuale (serie unica con le note di credito); fattura dal dettaglio del viaggio; acconto + saldo separati (il viaggio risulta fatturato solo dopo il saldo); riepilogativa multi-viaggio dello stesso cliente; Nota di Credito TD04 (storno totale che libera i viaggi, o parziale). Per la Pubblica Amministrazione il formato passa a FPA12 con Codice Univoco Ufficio, split payment, CIG e CUP; senza CIG e Codice Ufficio il viaggio non si chiude. Il testo digitato viene ripulito dai caratteri non ammessi dal tracciato (es. la freccia → e il trattino lungo — diventano un trattino semplice).</p>
<div class="tip"><b>Conformità verificata:</b> in sede di collaudo gli XML generati sono stati validati con successo contro lo schema ufficiale FatturaPA v1.2 (fattura ordinaria privata con IVA, fattura PA con split payment e CIG/CUP, nota di credito TD04).</div>

<h2 id="s19">19. Portale Autista, Mobile e notifiche</h2>
<p>Dal telefono l'applicazione si presenta in forma adatta al ruolo di chi accede: <b>Portale Autista</b> per gli autisti, <b>Home mobile</b> per amministratori e operatori. I tablet sono equiparati al desktop e mostrano il pannello completo.</p>

<h3>19.1 Portale Autista</h3>
<p>Interfaccia dedicata che mostra solo i viaggi assegnati all'autista.</p>
<ul>
<li><b>Card "In corso" e "In partenza":</b> timeline con link di navigazione GPS e countdown che si aggiorna da solo.</li>
<li><b>Km di partenza e ritorno:</b> inseriti dall'autista e salvati nel viaggio; bloccati dopo la chiusura.</li>
<li><b>Ordine di servizio</b> stampabile dal telefono; accompagnatore con chiamata diretta al referente a bordo.</li>
</ul>
<div class="new"><b>Viaggio completato.</b> L'autista abilitato (interruttore "Può marcare i viaggi come completati") trova nel portale una sezione "Da completare" con il pulsante <b>Viaggio completato</b> per i propri viaggi. Il pulsante è attivabile solo dopo la data e ora di rientro previste del viaggio; la regola è applicata anche lato server (un tentativo anticipato viene rifiutato). Ogni segnalazione è tracciata nel Registro attività. Il controllo è limitato ai soli viaggi effettivamente assegnati all'autista.</div>

<h3>19.2 Home mobile per amministratori e operatori <span class="badge">NUOVO</span></h3>
<p>Aprendo l'applicazione dal telefono, chi gestisce l'azienda trova una schermata pensata per lo schermo piccolo, invece del gestionale desktop rimpicciolito. È una vista di <b>sola lettura</b>, per capire in pochi secondi come sta andando la giornata:</p>
<ul>
<li><b>Oggi e Domani:</b> i viaggi con orario, tratta, autisti e mezzo. Un segnale di avvertimento evidenzia gli impegni con un autista sospeso o un mezzo fuori servizio.</li>
<li><b>Scadenze imminenti:</b> ordinate per urgenza, con l'etichetta della categoria (Bollo, Revisione, Patente…) e i giorni che mancano.</li>
<li><b>Pagamenti in scadenza:</b> chi deve ancora pagare e quando.</li>
<li><b>Campanella Notifiche:</b> la stessa casella personale disponibile sul pannello completo.</li>
</ul>
<p>Per creare o modificare — viaggi, preventivi, fatture — si usa il computer o il tablet, dove il pannello è completo.</p>

<h3>19.3 Notifiche e app sul telefono</h3>
<p>La <b>campanella Notifiche</b> è la casella personale dell'utente (distinta dagli Avvisi) e raccoglie due tipi di messaggi:</p>
<ul>
<li><b>Al momento del fatto:</b> l'autista riceve un messaggio quando gli viene assegnato un nuovo viaggio o cambia orario, luogo o cliente di uno dei suoi.</li>
<li><b>In anticipo:</b> i promemoria automatici del giro giornaliero — "viaggio di domani" e scadenze in avvicinamento (par. 11.2).</li>
</ul>
<p>Con le <b>notifiche push</b> attivate l'avviso arriva anche ad app chiusa. L'app è <b>installabile sulla schermata Home</b> (PWA): su Android l'installazione è diretta, su iPhone/iPad un breve tutorial guida "Condividi → Aggiungi a Home" (su iOS le push funzionano dopo l'aggiunta alla Home).</p>

<h2 id="s20">20. Moduli stampabili</h2>
<p><b>Ordine di Servizio</b> (viaggi) con i dati presenti e le righe da compilare a mano; le voci mancanti mostrano "da compilare". <b>Contratto di locazione</b> (noleggi) con anagrafica cliente, dati del veicolo, tabella degli utilizzatori e dati patente, e condizioni generali personalizzabili.</p>

<h2 id="s21">21. Solidità e controlli</h2>
<p>L'applicazione include protezioni pensate per il lavoro condiviso: congelamento dei documenti contabili, rilevamento delle modifiche simultanee, controllo formale di P.IVA/CF, unione clienti tracciata e irreversibile, registro attività immutabile. Gli accessi sono protetti da ruoli e permessi granulari, autenticazione a due fattori e sessioni irrobustite.</p>
"""
