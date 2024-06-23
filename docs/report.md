# Introduzione

La variante del progetto da noi scelta è quella dell'"e-commerce", che abbiamo personalizzato come una piattaforma specializzata nella vendita di libri. Questa piattaforma supporta la ricerca delle singole opere, affinabile tramite filtri, e il conseguente acquisto delle stesse da parte degli utenti registrati. Ogni utente può successivamente decidere di vendere i propri libri al prezzo desiderato e, se l'opera non è ancora presente nel database, può aggiungerla fornendo i relativi metadata, come il genere, l'autore, la copertina, ecc.

# Funzionalità principali

Le funzionalità principali che abbiamo implementato sono le seguenti:

## Sistema di Autenticazione

`auth.py`

Il sistema di autenticazione implementato si occupa di gestire le registrazioni, i login, i logout e la validazione dei token di sessione.

I login sono gestiti come segue: l'utente invia tramite l'apposito form utente e password, si recupera l'oggetto corrispondente allo username dato. Se un utente è stato trovato, allora si controlla la password sfruttando la funzione `check_password_hash` fornita da `bcrypt`, e se il controllo passa si genera un nuovo token tramite la funzione `getNewToken()`, la quale invoca `secrets.token_hex(tokenSize)` per ottenere una stringa randomica esadecimale che verrà assegnata ad un cookie (`session["token"]`) usando la libreria session

Le registrazioni sono gestite come segue: si controlla che tutti i parametri siano stati passati e non siano `None`, si procede controllando che il nome utente contenga solo lettere o numeri, che il nome e il cognome contengano solo lettere e che le password passate corrispondano. Una volta fatto questo si interroga il database per trovare un'altro eventuale utente, se non esiste si procede all'inserzione del nuovo utente a cui si assegna anche un token di sessione generato al momento, altrimenti si blocca l'inserione.

Il logout funziona andando a trovare l'utente con un dato token si sessione all'interno del database, per poi andarlo a porre a `NULL`. Viene sempre e comunque rimosso il token di sessione, ma solamente se viene cancellato il token a lato database viene mostrato il messaggio di logout eseguiro con successo.

Nel caso in cui avvenga un errore con il token csrf, ovvero un valore randomico univoco per la richiesta fatta in fase di registrazione, allora viene mostrata una pagina d'errore (cosa che non dovrebbe mai accadere se non, ad esempio, in caso di attacchi MITM)

Le funzioni `checkLoggedIn` e `getLoggedInUser` funzionano essenzialmente alla stessa maniera: entrambe prendono il token di sessione e lo cercano sul database per recuperare l'utente corrispondente, controllano che sia ancora valido (durata di 1 giorno) e ritornano di conseguenza `True` o l'oggetto corrispondente di tipo `User` in caso di successo, `False` o `None` altrimenti.

## Visualizzazione singolo Libro e relative Inserzioni

`book.py`

La pagina prima cerca il libro con l'`id` passato come parametro e, se non è presente, ritorna `404`.

Se il libro esiste, invece, viene visualizzata la copertina e tutte le relative informazioni (come autore e generi) tramite la macro `display_book`.

Inoltre il sistema cerca tutte le inserzioni relative al libro, rimuove quelle appartenenti all'utente attualmente loggato per far si che non vengano visualizzate, le raggruppa per venditore e le ordina con il criterio specificato dall'utente.

L'ordinamento si basa sulle stelle totali o medie dei venditori tramite il parametro `sort` e l'ordine è crescente o decrescente a seconda del parametro `order`. Tutti i venditori che non hanno ancora stelle verranno sempre mostrati alla fine

Altre operazioni che offre `/book/` sono:
 - `add` che visualizza un form per aggiungere un libro mancante, da riempire con tutti i parametri del libro (come titolo, data di pubblicazione, ISBN, etc.) e supporta il caricamento di una foto della copertina
 - `add/genre` per aggiungere un genere non già presente nel database
 - `add/author` per aggiungere un autore non già presente nel database
 - `add/publisher` per aggiungere una casa editrice non già presente nel database

## Gestione del Carrello

`cart.py`

Il carrello raccoglie tutte le inserzioni che l'utente ha aggiunto e la rispettiva quantità, calcola il prezzo totale e offre la possibilità di rimuovere un'inserzione o modificarne la quantità.

Prima di confermare la transazione controlla:
 - che il libro sia in vendita e la rispettiva inserzione sia presente
 - che la quantità di ogni inserzione sia minore o uguale a quella disponibile e che sia positiva
 - che il compratore abbia abbastanza soldi per comprare tutti i libri
Se anche solo una di queste non e' valida, esegue il rollback

Inoltre supporta l'aggiunta e la rimozione di un'inserzione:
 - `/cart/add` dove controlla che l'inserzione esista, che la quantità non superi quella presente e che l'utente sia loggato
 - `/cart/remove` dove evita di cancellare inserzioni non presenti nel carrello

## Visualizzazione degli Acquisti

`history.py`

Lo storico, una volta controllato che l'utente sia loggato e che abbia ricevuto l'id dell'acquisto fatto (id nello storico), una recensione e una valutazione, procede a controllare che i dati passati siano validi (quindi non `None` e con una recensione almeno lunga 2 caratteri), per poi modificare l'oggetto `History` corrispondente al prodotto nello storico, andando ad aggiungere la recensione e la valutazione. In caso di errori viene eseguito un rollback esplicitamente e viene mostrato un messaggio d'errore. Infine vengono ricaricati gli oggetti aggiornati presenti nello storico con lo scopo di visualizzarli

## Homepage

`index.py`

La homepage (o root `/`) visualizza multiple liste di libri suddivise per genere e ordinati randomicamente tramite la funzione `generate_book_list`.

Se c'è un utente loggato visualizza anche due pulsanti, rispettivamente per accedere alla libreria personale e per visualizzare lo storico degli ordini.

Inoltre, se l'utente è un venditore, mostra un pulsante extra per accedere alla lista degli ordini.

## Gestione delle Inserzioni

`inserionmanager.py`

Il sistema di gestione delle inserzioni di occupa di ricevere alcune informazioni come l'id del libro, il suo stato ecc... e di apportare le modifiche richieste dall'utente tramite i form ad esso forniti.

Le operazioni che un utente può svolgere sono:

- creazione di un'inserzione
- aggiornamento di un'inserzione
- eliminazione di un'inserzione

Ognuna di queste operazioni ha una funzione che si occupa di controllare che una serie di dati necessari (es. per creare un'inserzione è necessario conoscere l'id e lo stato del libro che si vuole vendere), per poi ritornare il form in cui vengono richieste le informazioni mancanti (es. sempre per l'inserzione, la quantità di libri da vendere e il relativo prezzo)

Le singole operazioni effettive gestite tramite richieste `POST` sono poi elaborate da funzioni differenti:

- Aggiornamento Inserzione

    l'operazione di aggiornamento di un'inserzione inizia controllando che l'utente sia un venditore abilitato, per poi appoggiarsi alla funzione `retriveExistingBooks` al fine di recuperare i libri con lo stesso id che sono in vendita o meno. Una volta controllato che ci siano sufficienti libri a cui apportare la modifica, la si applica al record esistente, oppure se ne crea uno nuovo con quest'ultima già applicata. In caso di errori avviene un rollback. Questa operazione, quindi, permette solamente di aggiornare i prezzi e non di rimuovere libri dalla vendita
- Creazione Inserzione

    una volta controllato che l'utente sia un venditore, si recuperano i libri sia in vendita che quelli che non lo sono tramite la funzione `retriveBooks`, e se la quantità di libri è sufficiente viene chiamata la funzione `manageInsertion` abilitando l'aggiunta tramite l'ultimo parametro impostato a `true`
- Eliminazione Inserzione

    l'operazione di eliminazione controlla che l'utente sia un venditore, recupera i libri tramite l'operazione `retriveBooks`, controlla che ci sia quantità sufficiente di libri da rimuovere, in caso affermativo viene chiamata la funzione `manageInsertion` abilitando la rimozione tramite l'ultimo parametro impostato a `False`

La funzione `retriveBooks` si occupa di recuperare i libri in vendita e quelli che non sono in vendita, sopo aver opportunamente controllato che l'utente abbia passato tutti i parametri corretti tramite il form

La funzione `retriveExistingBooks` compie un'operazione simile a `retriveBooks`, se non per il fatto che opera con libri che sono esclusivamente in vendita

La funzione `manageInsertion` si occupa di gestire tutti i casi in cui l'aggiunta e la rimozione di libri comportino il dover creare, eliminare o aggiornare dei record all'interno della tabella [`owns`](#tabella-owns). In caso di errori, si occupa autonomamente di effettuare un rollback esplicitamente, mentre se va tutto a buon fine effettua un commit


## Visualizzazione della propria Libreria

`library.py`

La libreria raccoglie tutti i libri posseduti dall'utente corrente. Rimanda alla pagina di login se l'utente non è ancora loggato.

Le funzioni offerte dalla libreria sono:
 - Aggiunta di un nuovo libro non presente nel database
 - Paginazione per suddividerla in sezioni e non sovraccaricare il database per ogni richiesta
 - Informazioni sul libro posseduto, quantità e stato

Inoltre, solo se l'utente corrente è un venditore, offre anche la possibilità di aggiungere, modificare e rimuovere un'inserzione.

## Visualizzazione delle Notifiche

`notifications.py`

Le notifiche sono divise in "Unread" e "Archived" e divise per utente, dove ogni utente può visualizzare solo le proprie.

Offre anche due funzioni `/notifications/read` e `/notifications/read/:id` rispettivamente per segnare tutte le notifiche come lette, quindi archiviarle, e per leggerne una sola specificatamente.

Entrambe le funzioni rimandano a `/notifications` per aggiornare la pagina in seguito

E' anche presente un badge visualizzato sulla navbar che riporta il numero di notifiche non lette, tramite il metodo `user.unread_count()`

Questo metodo esegue una query sulla view `NotificationCount` dato l'utente `self` e ritorna un numero che, se maggiore di 0, viene mostrato sopra il badge

## Gestione degli Ordini

`orders.py`

Per il venditore loggato visualizza tutti gli ordini suddivisi in "Da spedire", "Spediti" e "Consegnati". Solo i venditori hanno accesso a questa pagina.

Per gli ordini in "Da spedire" e "Spediti" è possibile aggiornare lo stato dell'ordine. Viene automaticamente aggiornato e viene mandata una notifica all'utente interessato se il nuovo stato è tra quelli accettati.

Per gli ordini già consegnati viene visualizzata anche la review ricevuta dall'utente oppure, se non presente, un messaggio di attesa.

## Gestione del Profilo

`profile.py`

La visualizzazione del profilo permette all'utente di modificare alcuni attributi che esso ha, tra cui il nome e il cognome, la password, il proprio saldo (scelta fatta in quanto non abbiamo un vero e proprio modo di aggiungere effettivamente della valuta all'account o gestire delle carte). Viene anche data la possibilità all'utente di effettuare un upgrade al suo account e diventare un venditore.

Le operazioni di aggiornamento avvengono controllando se sono avvenuti dei cambiamenti ai dati passati al form rispetto a quelli che sono presenti all'interno del database. Una volta che un cambiamento avviene, le modifica vengono validate (es. il nome e il cognome devono contenere solamente lettere, la password deve avere una certa lunghezza, il balance deve essere un numero...) e vengono applicate sull'oggetto `usr`, il quale aggiornerà automaticamente anche il database a seguito del commit presente alla riga successiva. In caso siano presenti degli errori, essi vengono mostrati tutti in una volta sola, senza andare ad applicare modifiche alla base di dati

## Gestione della Ricerca

`search.py`

Normalmente visibile solamente come input testuale nella navbar, si arricchisce di ulteriori filtri una volta visitata la pagina `/search`.

I filtri sono raccolti nella classe interna `UserInput` e sono:
 - `search` per l'input testuale, 
 - `genres` per i libri che hanno almeno uno dei generi selezionati
 - `publishers` per i libri pubblicati da una delle case editoriali selezionate
 - `available` per mostrare solo i libri acquistabili
 - `min` per ritornare tutti i libri con un prezzo superiore
 - `max` per ritornare tutti i libri con un prezzo inferiore 

 Dati i filtri, che possono anche essere `None` o liste vuote, la funzione `generate_book_list` crea una query utilizzando solo i filtri abilitati, per evitare controlli extra.

Inoltre le checkboxes `genres` e `publishers` vengono automaticamente create in base al contenuto delle rispettive tabelle nel database.

Inoltre le checkboxes `genres` e `publishers` vengono automaticamente create in base al contenuto delle rispettive tabelle nel database.

## Visualizzazione Venditore

`seller.py`

La pagina del venditore, visibile solo se l'utente cercato è un venditore, visualizza le stelle medie, una lista dei libri attualmente in vendita e le recensioni ricevute. 

Le stelle di un venditore vengono calcolate dalla view `star_count` come media delle stelle di tutte le recensioni ricevute da coloro che hanno effettuato un ordine da quel venditore. Questo avviene tramite il metodo `user.stars()`.

Tutti i libri nella lista hanno anche un link che rimanda alla corrispondenti pagine del libro, dove sarà possibile poterli comprare e/o valutare inserzioni di altri venditori più vantaggiose.

# Progettazione Concettuale e Logica

A seguito della progettazione concettuale abbiamo individuato le seguenti entità:

## Entità

### Entità `Users`

Rappresentano gli utenti che accedono all'e-commerce e hanno i seguenti attributi:

- `username`: Nome utente usato per effettuare il login che gli identifica univocamente
- `first_name` e `last_name`: nome e cognome per dare un grado di personalizzazione all'account in più
- `password`: password già hashata e salata utilizzata nella fase di login per provare l'identità dell'utente
- `created_at`: data di creazione dell'account
- `balance`: quantità di denaro in centesimi che l'utente ha caricato nell'account
- `last_logged_in_at`: data di ultimo login, utilizzata per controllare la validità del token salvato come cookie
- `token`: valore generato randomicamente che viene passato all'utente in fase di registrazione o login, viene utilizzato per autorizzare tutte le operazioni che esso andrà a fare (es. accedere alla propria libreria)

Viene aggiunta un'invariante che controlla che il `balance` dell'account non posso mai andare negativo (la piattaforma non offre, quindi, la possibilità di fare credito all'utente)

### Entità `Sellers`

L'entità specializza utenti, e serve per distinguere quali di essi sono abilitati alla vendita e quali no

### Entità `Carts`

Questa entità rappresenta un a serie di libri uguali che l'utente vuole comprare. Collega quindi l'utente al libro e al realtivo venditore, specificando una data quantità. L'attributo dell'entità è:

- `quantità`: rappresenta la quantità di uno specifico libro che è stato aggiunto al carrello

Vengono specificate tre invarianti: una che controlla che la quantità sia positiva, una che controlla che il libro che si vuole comprare faccia parte dei libri appartenenti al venditore e un'ultima che controlla che il libro che si intende acquistare sia effettivamente in vendita

### Entità `History`

L'entità rappresenta lo storico degli acquisti effettuati dall'utente, includendo un campo per lasciare una recensione sull'esperienza d'acquisto e relativa valutazione in stelle. Gli attributi sono i seguenti:

- `id`: identifica lo specifico record nello storico
- `date`: data di quando si è effettuato l'acquisto
- `quantity`: quantità di libri che sono stati acquistati
- `status`: indica stato della spedizione, in modo da informare l'utente sui movimenti del suo acquisto
- `price`: salva il prezzo di acquisto in centesimi
- `review`: campo dedicato alla recensione scritta da parte dell'utente
- `stars`: campo dedicato a lasciare la propria valutazione in stelle

Vengono specificati anche tre invarianti, una che controlla che la quantità acquistata sia maggiore di 0, un'altra che controlla che il prezzo non sia negativo e un'ultima che controlla che le notifiche generate dall'acquisto e conseguenti aggiornamenti di spedizione facciano riferimento all'acquirente corretto

### Entità `Books`

L'entità rappresenta i libri presenti all'interno del database come "entità" astratta, quindi non il singolo libro posseduto da un certo utente. L'entità ha anche i seguenti campi:

- `id`: identifica il libro univocamente all'interno della base di dati
- `title`: titolo del libro
- `published`: data di pubblicazione del libro
- `pages`: numero di pagine
- `isbn`: codice isbn del libro

Viene specificata anche un'invariante che controlla che le pagine siano in numero maggiore di $0$

### Entità `Genres`

Entità rappresentante i possibili generi dei libri. Il suo unico attributo è:

- `nome`: nome del genere che lo identifica anche

### Entità `Authors`

Entità rappresentante gli autori dei libri. I suoi attributi sono:

- `id`: id dell'autore che lo identifica
- `first_name`: nome dell'autore
- `last_name`: cognome dell'autore

### Entità `Publishers`

Entità rappresentante una casa editoriale di libri. Il suo unico attributo è:

- `nome`: nome identificativo della casa editoriale

### Entità `Notifications`

Entità rappresentante le singole notifiche di un certo utente. Essa ha i seguenti attributi:

- `id`: identificativo della notifica
- `message`: messaggio della notifica
- `archived`: valore booleano usato per segnare quanto un utente fa l'acknowledge della notifica

### Entità `Orders`

Entità che specializza `Notifications` al fine di contenere maggiori informazioni per gli ordini andando ad aggiunge 2 attributi:

- `status_old`: vecchio stato della spedizione
- `status_new`: nuovo stato della spedizione

## Relazioni

Di seguito sono riportate le relazioni che abbiamo deciso di implementare nel nostro schema ER

### Relazione `afferisce`

Collega la singola notifica al singolo utente, non ha attributi

### Relazione `own`

Collega l'utente ai libri da esso posseduti e ha i seguenti attributi:

- `quantity`; indica la quantità dello specifico libro posseduta dall'utente
- `state`: indica lo stato fisico del libro
- `price`: se il libro è in vendita, allora il prezzo viene popolato con la quantità di valuta desiderata dall'utente

Vengono aggiunte anche due invarianti che fanno si che la quantità sia sempre maggiore di $0$ e che il prezzo sia positivo o nullo

### Relazione `appartiene`

Collega il libro ai suoi generi

### Relazione `scritto da`

Collega il libro al suo autore

### Relazione `pubblicato da`

Collega il libro alla sua casa editoriale

### Relazione `contiene`

Collega il record del carrello al libro a cui esso si riferisce

### Relazione `possiede`

Collega l'utente al suo carrello, ovvero ai vari record di prodotti che vuole comprare

### Relazione `riguarda`

Collega un record nella cronologia al libro che un'utente ha comprato

### Relazione `ha prodotti in`

Collega il venditore ai prodotti che gli utenti hanno nel loro carrello (sempre considerando il fatto che per ogni prodotto distinto nel carrello c'è un record)

### Relazione `é riferito in`

Collega ogni record nella cronologia al venditore da cui si è comprato un determinato prodotto

### Relazione `si riferisce a`

Collega la notifica specifica notifica di un aggiornamento riguardante un ordine al record presente nello storico degli ordini (es. nel caso il libro venga spedito)

## Schema ER Risultante

![](./docs/database_ER.png)

## Rappresentazione Logica

### Tabella `genres`

genres([name]{.underline}: string)

- PK(name)

Rispecchia la sua corrispettiva [entità](#entità-genres), mantenendo come campi:

- `nome` che ha tipo `TEXT` ed è `PRIMARY KEY`

### Tabella `authors`

authors([id]{.underline}: int, first_name: string, last_name: string)

- PK(id)

Rispecchia la sua corrispettiva [entità](#entità-authors), mantenendo come campi:

- `id` che ha tipo `SERIAL` ed è `PRIMARY KEY`, in modo da evere un modo comodo di gestire le omonimie tramite un contatore autoincrementale
- `first_name` che ha tipo `CHARACTER VARYING(255)`, quindi una stringa di caratteri di dimensione variabile che non può essere `NULL`
- `last_name` che ha le stesse caratteristiche di `first_name` per eguali motivi

### Tabella `publishers`

publishers([name]{.underline}: string)

- PK(name)

Rispecchia la sua corrispettiva [entità](#entità-publishers), mantenendo come campi:
- `name` che ha tipo `TEXT` ed è `PRIMARY KEY`

### Tabella `books`

books([id]{.underline}: int, title: string, published: date, pages: int, isbn: string, fk_author*: int, fk_publisher*: string)

- PK(id)
- fk_author FK author(id)
- fk_publisher FK publishers(name)

Per quanto rispecchi in parte la sua [entità](#entità-books), questa tabella va anche ad aggiungere agli attributi anche le relazioni qui riportate:

- `id`: identificativo artificiale del libro, motivo per cui è `SERIAL PRIMARY KEY`
- `title`: titolo del libro, quindi è `TEXT NOT NULL`
- `published`: data di pubblicazione, quindi `DATE NOT NULL`
- `pages`: numero di pagine obbligatorio (`INTEGER NOT NULL`), a cui viene integrato il seguente controllo che le obbliga ad essere in numero positivo: `CONSTRAINT pages_gt CHECK (pages > 0)`
- `isbn`: sequenza di caratteri che deve coprire diversi standard, per cui è `CHARACTER VARYING(20)`, e può essere omessa
- `fk_author`: chiave esterna, come richiesto dalla relazione [`scritto da`](#relazione-scritto-da), quindi diventa `REFERENCES authors(id)` e ne mantiene il tipo `INTEGER`
- `fk_publisher`: chiave esterna, come richiesto dalla relazione [`pubblicato da`](#relazione-pubblicato-da), quindi diventa `REFERENCES publishers(name)` e ne mantiene il tipo `TEXT`

### Tabella `booksgenres`

booksgenres([fk_idB*]{.underline}: int, [fk_genre*]{.underline}: string)

- PK(fk_idB, fk_genre)
- fk_idB FK books(id)
- fk_genre FK genres(name)

Questa tabella rappresenta la relazione [`appartiene`](#relazione-appartiene), che è una `n-n`. Ne consegue che abbia come attributi:

- `fk_idB`: chiave esterna di `books(id)` con tipo `INTEGER` e anche parte della chiave primaria
- `fk_genre`: chiave esterna di `genres(name)` con tipo `TEXT` e anche parte della chiave primaria

### Tabella `users`

users([username]{.underline}: int, first_name: string, last_name: string, password: string, created_at: timestamp, balance: int, seller: bool, last_logged_in_at: timestamp, token: string)

- PK(username)

La seguente tabella rispecchia fedelmente la struttura di [`Users`](#entità-users), per cui ha i seguenti attributi:

- `username`: nome utente identificativo, ha quindi tipo `VARCHAR(100)` ed è `PRIMARY KEY`
- `first_name`: nome dell'utente, ha tipo `VARCHAR(255)` e non può essere vuoto (`NOT NULL`)
- `last_name`: cognome dell'utente, ha tipo `VARCHAR(255)` e non può essere vuoto (`NOT NULL`)
- `password`: ha tipo `TEXT`, in modo da poter supportare cambiamenti dell'algoritmo di hashing e salting con dimensioni dell'hash differenti. Ovviamente è `NOT NULL`
- `created_at`: `TIMESTAMP` della creazione, deve essere `NOT NULL`
- `balance`: centesimi presenti all'interno dell'account, per cui è `INTEGER` ed è `NOT NULL`. Essendo che deve essere rispettata l'invariante, viene aggiunto il seguente controllo: `CONSTRAINT balance_ge CHECK (balance >= 0)`
- `seller`: flag che sta ad indicare se l'account è abilitato a vendere prodotti, quindi ha tipo `BOOLEAN` ed è `NOT NULL`
- `last_logged_in_at`: orario in cui è stato fatto l'ultimo login, ha tipo `TIMESTAMP WITHOUT TIME ZONE`, siccome devono essere confrontate indifferentemente dalla time zone e non vengono visualizzate agli utenti, ed è `NOT NULL`
- `token`: token di autenticazione generato a tempo di login, ha tipo `CHARACTER(64)[]` e può essere `NULL` (in tal caso non esite un token valido)

### Tabella `owns`

owns([id]{.underline}: int, fk_username*: string, fk_book*: int, quantity: int, state: state, price: int)

- PK(id)
- fk_username FK users(username)
- fk_book FK books(id)

La tabella segue la struttura della realzione [`own`](#relazione-own), collegandosi a [`Users`](#entità-users) e a [`Books`](#entità-books). Per questo ha i seguenti attributi:

- `id`: identificativo dell'oggetto posseduto (rappresenta il libro/i fisico, non il "modello" astratto presente in [`Books`](#entità-books)). Per questo è `SERIAL` ed è anche `PRIMARY KEY`
- `fk_username`: chiave esterna che si riferisce al possessore del libro/i, per questo è un `VARCHAR(100)`, è `NOT NULL` e si riferisce a `users(username)`
- `fk_book`: chiave esterna del "modello" del libro, per questo ha tipo `INTEGER`, è `NOT NULL` e si riferisce a `books(id)`
- `quantity`: indica la quantità di libri posseduta, è quindi `INTEGER NOT NULL`. Non è presente un `CHECK` in quanto il controllo è eseguito da un [trigger](#trigger-check_quantity_zero_trigger) che offre anche altre funzionalità.
- `state`: stato fisico di "usura" dell'oggetto, ha un tipo custom `state` e deve essere `NOT NULL`
- `price`: prezzo in centesimi che l'utente può decidere nel caso volesse vendere il libro, altrimenti è impostato a `NULL`. È quindi `INTEGER` e ha il constraint `price_ge_owns CHECK (price >= 0)`, al fine di evitare di poter mettere prezzi negativi

È presente anche un ulteriore vincolo `UNIQUE(fk_username, fk_book, state, price)`, in modo da prevenire la presenza di più record di libri posseduti dallo stesso utente con lo stesso stato e prezzo

### Tabella `carts`

carts([fk_buyer*]{.underline}: string, [fk_own*]{.underline}: int, quantity: int)

- PK(fk_buyer, fk_own)
- fk_buyer FK users(username)
- fk_own FK owns(id)

La tabella `carts` ricalca l'entità [`Carts`](#entità-carts), aggiungendo le relazioni [`possiede`](#relazione-possiede) e [`ha prodotti in`](#relazione-ha-prodotti-in). Per cui ha i seguenti attributi:

- `fk_buyer`: chiave esterna che si riferisce all'utente compratore, ha quindi tipo `VARCHAR(100)` e fa parte della chiave primaria e referenzia `users(username)`
- `fk_own`: chiave esterna del libro posseduto che l'utente è intenzionato a comprare, ha quindi tipo `INTEGER` e fa parte della chiave primaria e referenzia `owns(id)` andando a specificare `ON DELETE CASCADE`, in modo da rimuovere automaticamente dal carrello un oggetto che viene esaurito
- `quantity`: quantità di prodotto che l'utente è interessato a comprare, ha tipo `INTEGER`, è `NOT NULL` e ha il constraint `quantity_gt_carts CHECK (quantity > 0)`

### Tabella `history`

history([id]{.underline}: int, date: timestamp, quantity: int, status: status, price: int, review: string, stars: int, fk_buyer*: string, fk_seller*: string, fk_book*: int, state: state)

- fk_buyer FK users(username)
- fk_seller FK users(username)
- fk_book FK books(id)

La tabella `history` segue la struttura dell'entità [`History`](#entità-history), aggiungendo le

- `id`: identificativo artificiale autoincrement, per cui è `SERIAL` e `PRIMARY KEY`
- `date`: data di acquisto, quindi è `TIMESTAMP` ed anche `NOT NULL`
- `quantity`: quantità di prodotti acquistata, quindi è `INTEGER`, `NOT NULL` e possiede il constraint `quantity_gt_history CHECK (quantity > 0)` che fa si che la quantità acquistabile non sia nulla o negativa
- `status`: stato dell'ordine/spedizione, ha tipo custom `status` ed è `NOT NULL`
- `price`: prezzo di acquisto in centesimi, è quindi `INTEGER`, `NOT NULL` e ha il constraint `price_ge_history CHECK (price >= 0)` che fa si che il prezzo sia positivo
- `review`: recensione che l'utente può lasciare (non obbligatoriamente e successivamente all'acquisto), ha tipo `TEXT`
- `stars`: valutazione in stelle, ha tipo `INTEGER` e ha `CONSTRAINT stars_btw CHECK (stars IS NULL OR stars BETWEEN 0 AND 5)` che fa si che il numero di stelle sia compreso tra $1$ e $5$
- `fk_buyer`: chiave esterna dell'utente che ha comprato, ha quindi tipo `VARCHAR(100)` e si riferisce a `users(username)`
- `fk_seller`: chiave esterna che si riferisce all'utente venditore, ha quindi tipo `VARCHAR(100)` e si riferisce a `users(username)`
- `fk_book`: chiave esterna che si riferisce al "modello" del libro comprato, ha quindi tipo `INTEGER` e si riferisce a `books(id)`
- `state`: stato di usura del prodotto comprato, ha tipo custom `state`

### Tabella `notifications`

notifications([id]{.underline}: int , context: disc_notif, fk_username*: string, message: string, archived: bool, fk_history*: int, order_status_old: status , order_status_new: status)

- PK(id)
- fk_username FK users(username)
- fk_history FK history(id)

Questa tabella è frutto dell'unione di due entità: [`Notifications`](#entità-notifications) e [`Orders`](#entità-orders). Ha i seguenti attributi:

- `id`: identificativo della notifica autoincrement, ha tipo `SERIAL` ed è `PRIMARY KEY`
- `context`: tipo di notifica, ha tipo custom `disc_notif` ed è `NOT NULL`
- `fk_username`: chiave esterna dell'utente a cui è destina ta la notifica, ha quindi tipo `VARCHAR(100)`, è `NOT NULL` e si riferisce a `users(username)`
- `message`: messaggio della notifica, ha tipo `TEXT`
- `archived`: flag usato a seguito della visualizzazione del messaggio, ha tipo `BOOLEAN` ed è `NOT NULL`
- `fk_history`: riferimento all'eventuale ordine che ha subito un aggiornamento, ha tipo `INTEGER` e si riferisce a `history(id)`
- `order_status_old`: ha tipo custom `status` ed indica il vecchio stato dell'ordine nel caso fosse stato aggiornato
- `order_status_new`: ha tipo custom `status` ed indica il nuovo stato dell'ordine nel caso fosse stato aggiornato

# Query Interessanti

Avendo utilizzato il più possibile le features di SQLALchemy, come l'ORM, non abbiamo alcuna query scritta direttamente in SQL, se non per lo script di inizializzazione del database (`db.sql`) e lo script di inserzione dei dati di prova (`insert.sql`). Per questo motivo alcune query verranno convertite da python a SQL.

## Query 1

La seguente query l'abbiamo usata per creare un tipo di dato custom, al fine di facilitare la scrittura delle tabelle, oltre ad avere anche il vantaggio della presenza di un controllo automatico dei dati da noi inseriti

```sql
CREATE TYPE state AS ENUM ('new', 'as new', 'used');
```

## Query 2

La seguente query è stata presa da `library.py`, e ha il compito di recuperare del database i libri posseduti dall'utente andando limitare il numero di risultati con lo scopo di averne solo un certo numero per pagina, il quale numero determinerà anche l'offset

```python
db.session.scalars(
        sq.select(Own)
        .filter(Own.fk_username == user.username)
        .limit(limit)
        .offset((page - 1) * limit)
    ).all()
```

e può essere tradotta come segue (i valori racchiusi in `_` sono i parametri che verrebbero sostituiti):

```sql
SELECT *
FROM owns
WHERE owns.fk_username = _user.username_
LIMIT _limit_ OFFSET _(page-1)*limit_
```

## Query 3

Questa query è stata presa da `book.py`, e ha lo scopo di recuperare le inserzioni (lo capiamo da `Own.price != None`) per un determinato libro (`Own.fk_book == id`) che non appartengono all'utente (`Own.fk_username != username`)

```python
db.session.query(Own)
        .filter(Own.fk_book == id, Own.price != None, Own.fk_username != username)
        .order_by(Own.fk_username)
        .all()
```

In SQL la query sarebbe stata (i valori racchiusi in `_` sono i parametri che verrebbero sostituiti):

```sql
SELECT *
FROM owns
WHERE owns.fk_book = _book.id_ AND owns.price IS NOT NULL AND owns.fk_username != _username_ ORDER BY owns.fk_username
```

## Query 4

La seguente query è stata estratta da `history.py`, e ha lo scopo di caricare tutti gli acquisti che sono stati effettuati dall'utente loggato (motivo di `History.fk_buyer == usr.username`), andandoli ad ordinare in ordine cronologico decrescente (questo lo si fa tramite l'id facendo `.order_by(History.id.desc()`)

```python
db.session.scalars(
        sq.select(History)
        .where(History.fk_buyer == usr.username)
        .order_by(History.id.desc())
```

La query in linguaggio SQL sarebbe stata (i valori racchiusi in `_` sono i parametri che verrebbero sostituiti):

```sql
SELECT *
FROM history
WHERE history.fk_buyer = _user.username_ ORDER BY _History.id_ DESC
```

## Query 5

La seguente query ha lo scopo di recuperare i libri filtrati secondo diversi criteri:

- titolo (`Book.title.icontains(input.search)`)
- nome dell'autore (`Book.author.has(Author.first_name.icontains(input.search))`)
- cognome dell'autore (`Book.author.has(Author.last_name.icontains(input.search))`)
- casa editoriale (`Book.publisher.has(Publisher.name.icontains(input.search))`)

L'utilizzo dell'`or_` permette il funzionamento simultaneo di tutti i filtri. Il risultato della query verrà, in realtà, successivamente rifinito in base ai filtri ulteriori richiesti dall'utente tramite l'aggiunta di ulteriori `WHERE`. Di seguito un esempio

```python
query = db.session.query(Book).filter(
        or_(
            Book.title.icontains(input.search),
            Book.author.has(Author.first_name.icontains(input.search)),
            Book.author.has(Author.last_name.icontains(input.search)),
            Book.publisher.has(Publisher.name.icontains(input.search)),
        )
    )

    if len(input.genres):
        query = query.filter(Book.genres.any(Genre.name.in_(input.genres)))

    if len(input.publishers):
        query = query.filter(Book.publisher.has(Publisher.name.in_(input.publishers)))

    if input.available or input.min or input.max:
        query = query.join(Own)

        if input.available:
            query = query.filter(Own.price != None)
        if input.min:
            query = query.filter(Own.price >= input.min * 100.0)
        if input.max:
            query = query.filter(Own.price <= input.max * 100.0)

    return query.all()
```

La query in linguaggio SQL sarebbe stata indicativamente (i valori racchiusi in `_` sono i parametri che verrebbero sostituiti):

```sql
SELECT *
FROM books
JOIN owns ON books.id = owns.fk_book
WHERE ((books.title ILIKE '%%' || _title_ || '%%')
OR (EXISTS (SELECT 1 FROM authors WHERE authors.id = books.fk_author AND authors.first_name ILIKE '%%' || _first_name_ || '%%'))
OR (EXISTS (SELECT 1 FROM authors WHERE authors.id = books.fk_author AND authors.last_name ILIKE '%%' || _last_name_ || '%%'))
OR (EXISTS (SELECT 1 FROM publishers WHERE publishers.name = books.fk_publisher AND publishers.name ILIKE '%%' || _name_ || '%%')))
AND (EXISTS (SELECT 1 FROM genres, booksgenres WHERE books.id = booksgenres.fk_idb AND genres.name = booksgenres.fk_genre AND genres.name IN _('genre1', 'genre2')_))
AND (EXISTS (SELECT 1 FROM publishers WHERE publishers.name = books.fk_publisher AND publishers.name IN _('publisher1', 'publisher2')_))
AND owns.price IS NOT NULL
AND owns.price <= _price_
```

# Scelte Progettuali

## Trigger

Al fine di garantire l'integrità della base di dati ed implementare alcune features, sono stati usati i seguenti trigger:

### Trigger `check_quantity_zero_trigger`

Questo è il trigger che, come anticipato, potrebbe essere stato sostituito da un `CHECK`. La scelta di utilizzare un trigger è stata fatta al fine di poter sollevare una specifica eccezione all'interno della funzione, che viene poi catturata python come se fosse una sorta di "segnale" di un determinato problema avvenuto nell'inserimento. Ovviamente, il rollback avviene automaticamente, in quanto a lato SQL l'eccezione non viene mai esplicitamente catturata

```sql
CREATE OR REPLACE FUNCTION remove_if_quantity_zero()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.quantity < 0 THEN --se la quantità è invalida
        RAISE EXCEPTION 'Quantity must be positive';
    ELSIF NEW.quantity = 0 THEN --se il libro è stato "esaurito"...
        DELETE FROM owns WHERE id = NEW.id; -- ...cancellalo di conseguenza
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_quantity_zero_trigger
AFTER INSERT OR UPDATE OF quantity ON owns
FOR EACH ROW
EXECUTE FUNCTION remove_if_quantity_zero();
```

### Trigger `trigger_status_change`

Il seguente trigger fa si che a seguito di un cambiamento di stato di un ordine (es. quando questo viene spedito), venga generata automaticamente una notifica lo informi dell'avvenimento

```sql
CREATE OR REPLACE FUNCTION notify_status_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO notifications (fk_username, context, archived, fk_history, order_status_old, order_status_new) -- inserici la notifica
    VALUES (NEW.fk_buyer, 'order updated', FALSE, NEW.id, OLD.status, NEW.status); -- ne dati inserisci lo stato vecchio e quello aggiornato
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_status_change
AFTER UPDATE ON history
FOR EACH ROW
WHEN (OLD.status IS DISTINCT FROM NEW.status) -- previene la creazione automatica di notifiche se
                                              -- non in caso di cambiamenti di stato
EXECUTE FUNCTION notify_status_change();
```

### Trigger `trigger_notifications`

Il seguente trigger viene utilizzato per aggiornare la vista materializzata [`notifications_count`](#vista-notifications_count) a seguito dell'aggiunta di una nuova notifica. Per questo motivo il trigger che chiama la funzione `notifications_count_refresh` è un `AFTER TRIGGER`

```sql
CREATE OR REPLACE FUNCTION notifications_count_refresh()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW notifications_count; -- aggiorna la view materializzata
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_notifications
AFTER INSERT OR UPDATE OR DELETE ON notifications -- a seguito di qualsiasi cambiamento
EXECUTE FUNCTION notifications_count_refresh();
```

### Trigger `trigger_user_rating`

Il seguente trigger ha lo scopo di mantenere aggiornata la view [`star_count`](#vista-star_count) a seguito di un'aggiunta di un ordine nella history o nel caso venga scritta una recensione con relativa valutazione

```sql
CREATE OR REPLACE FUNCTION refresh_star_count()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    REFRESH MATERIALIZED VIEW star_count; -- aggiorna la vista
    RETURN NULL;
END;
$$;

CREATE TRIGGER trigger_user_rating
AFTER INSERT OR UPDATE ON history -- a seguito di un'aggiunta o di un'aggiornamento
FOR EACH STATEMENT
EXECUTE PROCEDURE refresh_star_count();
```

### Trigger `trigger_carts_owner`

Questo trigger serve a mantenere la consistenza della base di dati, in quanto va a controllare che l'oggetto che si sta per inserire nel carrello appartenga ad un utente che è abilitato alla vendita

```postgres
CREATE OR REPLACE FUNCTION if_seller_is_seller()
RETURNS TRIGGER
AS $$
BEGIN
    IF EXISTS(SELECT 1 FROM users -- controlla che il venditore sia abilitato
                WHERE users.username = NEW.fk_own
                    AND users.seller) THEN
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_carts_owner
BEFORE INSERT OR UPDATE ON carts -- in caso di inserimento/aggiornamento del carrello
FOR EACH ROW
EXECUTE PROCEDURE if_seller_is_seller();
```

### Trigger `trigger_history_notifications`

Il seguente trigger controlla che se una notifica si riferisce ad un ordine, colui che ha comprato il prodotto deve essere anche colui a cui è diretta la notifica

```postgres
CREATE OR REPLACE FUNCTION check_notification()
RETURNS TRIGGER
AS $$
BEGIN
    IF NEW.fk_history IS NOT NULL AND NOT EXISTS( -- se non c'è l'utente a cui è diretta la notifica
        SELECT 1 FROM history AS h                -- con il dato id della history
            WHERE h.id = NEW.fk_history AND
            NEW.fk_username = h.fk_buyer
            ) THEN
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_history_notifications
BEFORE INSERT OR UPDATE ON notifications -- in caso di inserzione/aggiornamento nelle notifiche
FOR EACH ROW
EXECUTE FUNCTION check_notification();
```

### Trigger `trigger_carts_selling`

Questo trigger fa si che un oggetto all'interno del carrello debba obbligatoriamente essere anche un oggetto che è messo in vendita (cotrolla quindi che l'oggetto abbia un prezzo assegnato)

```sql
CREATE OR REPLACE FUNCTION check_selling()
RETURNS TRIGGER
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM owns
                WHERE id = NEW.fk_own AND price IS NOT NONE) THEN -- se esiste l'oggetto
        RETURN NEW;                                               -- con il prezzo non
    END IF;                                                       -- NULL, quindi che è
    RETURN NULL;                                                  -- in vendita
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_carts_selling
BEFORE INSERT OR UPDATE ON carts
FOR EACH ROW
EXECUTE FUNCTION check_selling();
```

## View Materializzate

Al fine di migliorare le performance, sono state introdotte le seguenti view materializzate

### Vista `notifications_count`

La seguente vista salva per ogni utente il suo numero di notifiche da visualizzare nella barra principale, andando ad escludere quelle già viste

```sql
CREATE MATERIALIZED VIEW notifications_count (username, count)
AS SELECT fk_username, COUNT(*) FROM notifications WHERE archived = false GROUP BY fk_username;

CREATE INDEX idx_username_notifications_count ON notifications_count(fk_username);
```

### Vista `star_count`

La seguente vista conteggia la media delle stelle per ogni utente venditore e il numero totale di recensioni che esso ha

```sql
CREATE MATERIALIZED VIEW star_count
AS
SELECT fk_seller, CAST(SUM(stars) AS DECIMAL)/COUNT(*) AS vote, COUNT(*) AS total FROM history
WHERE review IS NOT NULL
GROUP BY fk_seller
WITH NO DATA;
```

## Indici

Al fine di migliorare le performance, sono stati creati i seguenti indici:

- `idx_title_books`: Ottimizzare la ricerca per titolo dei libri, per cui l'indice viene creato su [`books`](#tabella-books) sulla colonna `title`
- `idx_isbn_books`: Ottimizza la ricerca dei libri per isbn, per cui l'indice viene creato su [`books`](#tabella-books) sulla colonna `isbn`
- `idx_author_books`: Ottimizza la ricerca dei libri tramite la chiave esterna dell'autore salvata per ognuno, per cui l'indice viene creato su [`books`](#tabella-books) sulla colonna `fk_author`
- `idx_publisher_books`: Ottimizza la ricerca dei libri tramite la chiave esterna della casa editoriale salvata per ognuno, per cui l'indice viene creato su [`books`](#tabella-books) sulla colonna `fk_publisher`
- `idx_token_users`: Ottimizza la ricerca degli utenti tramite il token a loro assegnato una volta fatto il login/registrazione, per cui l'indice viene creato su [`users`](#tabella-users) sulla colonna `token`
- `idx_own`: Ottimizza la ricerca di un determinato libro posseduto da un certo utente in un dato stato di usura, per cui l'indice è stato creato su [`owns`](#tabella-owns) per gli attributi `fk_book`, `fk_username`, `state`
- `idx_history`: Ottimizza la ricerca di un libro comprato da un certo utente in un certo stato ad un dato prezzo, per cui l'indice è stato creato su [`history`](#tabella-history) per gli attributi `fk_buyer`, `fk_book`, `state`, `price`
- `idx_seller_history`: Ottimizza la ricerca degli ordini di un determinato venditore, per cui è stato fatto sulla tabella [`Histroy`](#tabella-history) e sull'attributo `fk_seller`
- `idx_buyer_history`: Ottimizza la ricerca degli ordini di un determinato acquirente, per cui è stato fatto sulla tabella [`Histroy`](#tabella-history) e sull'attributo `fk_buyer`
- `idx_username_notifications`: Ottimizza la ricerca delle notifiche di un determinato utente, per cui è stato fatto sulla tabella [`notifications`](#tabella-notifications) e sull'attributo `fk_username`
- `idx_username_notifications_count`: Ottimizza la ricerca del numero di notifiche non lette di un determinato utente, per cui è stato fatto sulla vista [`notifications_count`](#vista-notifications_count) e sull'attributo `fk_username`
- `idx_seller_star_count`: Ottimizza la ricerca della media delle valutazioni di un determinato venditore, per cui è stato fatto sulla vista [`star_count`](#vista-star_count) e sull'attributo `fk_seller`

## Controlli Ulteriori

### Validazione degli Input

Ulteriori controlli, di cui la maggior parte sono preventivi, sono stati fatti tramite il codice python. Questa scelta è stata fatta sia per ottenere maggiori performance, potendo considerare una quantità inferiore di dati, sia a causa della complessità algoritmica degli stessi.
Un esempio banale è il controllo sulla validità del codice `isbn`, il quale viene controllato tramite una libreria esterna.
Un altro esempio consiste nella validazione degli input, andando a controllare che tutti i dati richiesti siano stati compilati correttamente (es. che siano diversi da `None` e che, ad esempio, il valore sia positivo).

### Utilizzo dell'ORM

Un'altra tecnica che abbiamo usato al fine di limitare errori nell'inserimento/aggiornamento dei dati è stato l'utilizzo esclusivo dell'ORM e i relativi costruttori, permettendoci quindi di evitare typo e l'utilizzo di dati con tipo incompatibile (permesso anche da mypy, come vedremo poi). Un ulteriore vantaggio è stato quello di poter accedere comodamente alle relazioni semplicemente usando il `.` (es. `libro.autore.first_name`) evitando ancora "errori di distrazione" che avrebbero potuto intaccare la consistenza del database.

### Utilizzo di Trigger e Check

Una buona parte del lavoro atto a mantenere la consistenza viene permessa dalla presenza dei [trigger](#trigger) visti sopra, dai `check` e dalla struttura stessa del database.

### Autenticazione e Validazione

Un'ulteriore misura di sicurezza è fornita dal sistema di autenticazione, il quale consente di identificare l'utente che vuole eseguire una specifica operazione. Questo processo di autenticazione non solo verifica l'identità dell'utente tramite il token assegnatoli ma, fornendo all'utilizzatore delle chiamate `getLoggedInUser()` un oggetto `User`, permette di estrarre comodamente gli attributi associati al profilo utente. Tra di essi c'è anche lo stato, che viene utilizzato per determinare se l'utente è un venditore, e quindi se può compiere determinate azioni. Questi controlli ulteriori permettono un maggiore controllo sui dati e le azioni degli utenti, garantendo più facilmente la consistenza della base di dati

### Utente e Database dedicati

Un'ultimo tassello è permesso dall'utilizzo di un utente e un database dedicato per accedere al DBMS (nel nostro specifico caso Postgres), cosa che permette di limitare le azioni che esso può fare in caso di eventi come la compromissione del server Flask. Un permesso banale quanto importante che è stato revocato è la possibilità di creare/modificare/cancellare tabelle, trigger, viste... Il database specifico usato è stato chiamato `library` e l'utente è stato denominato `librarian`

# Ulteriori informazioni

Di seguito alcuni aspetti interessanti del progetto

## Libreria `MyPy`

MyPy, insieme alle sue relative estensioni, ci ha permesso di effettuare il controllo statico dei tipi, ed individuare di conseguenza prima ancora di eseguire il codice potenziali problemi, come dei cast errati. Il codice risultante risulta quindi essere più facile da leggere e mantenere.

Nonostante i vantaggi da esso offerti, abbiamo incontrato alcune problematiche, principalmente causate da errori sui tipi scorretti. L'errore più comune è causato a seguito di un controllo per evitare che una serie di variabili non sia `None`, come il seguente:

```python
var1: int | None
var2: int | None
var3: int | None

if None in [var1, var2, var3]: # problematico, mypy si lamenta che le
                               # variabili potrebbero essere None
    return

if var1 is None or var2 is None or var3 is None:  # nessun problema
    return

fun(var1) # qui è dove mypy potrebbe dare errori

fun(var: int):
    print(var)
```

Un'altra noia è stata causata se nelle classi rappresentanti le tabelle non è presente il costruttore esplicitamente. In questo caso, ogni volta che abbiamo instanziato un oggetto, mypy ha prodotto un fastidioso errore riguardante l'assenza di esso

## Libreria `python-dotenv`

Questa libreria ci permette di specificare dei parametri come `SQLALCHEMY_DATABASE_URI` o la chiave segreta `SECRET_KEY` usata per la cifratura in un comodo file `.env`. Questa feature ci ha permesso di evitare di dover cambiare ogni volta il primo parametro, essendo che abbiamo utilizzato database installati diversamente (container docker o baremetal) con credenziali differenti durante lo sviluppo.

## Componenti Riutilizzabili

L'utilizzo delle macro e delle componenti riutilizzabili è stato permesso da flask, e ci ha permesso di diminuire la duplicazione del codice, aumentando al tempo stesso la sua riusabilità (basti pensare alla navbar). Il codice ottenuto risulta quindi essere estremamente modulare, cosa che ci ha permesso di sviluppare concorrentemente diverse parti dell'interfaccia del progetto, pur mantenendo una certa coerenza grafica.

Le macro si sono rivelate estremamente comode per inserire, e talvolta anche elaborare (ad esempio, bastia guardare come vengono elaborati i libri da visualizzare in `index.html`), i dati processati da python direttamente nella pagina html.

## Libreria `wtform`

Questa libreria è stata utilizzata nel form di login, al fine di poter utilizzare la feature del token csrf, ovvero un valore randomico che viene inserito per evitare, in questo caso, che un altra pagina possa far registrare forzatamente l'utente tramite un iframe o usando una richiesta ajax tramite javascript.
Per il resto dei form si è rivelata leggermente più scomoda rispetto alla creazione diretta in html del form desiderato, quindi non è stata ulteriormente utilizzata.

## Libreria `bcrypt`

Questa libreria è stata utilizzata per calcolare l'hash della password e, al tempo stesso, effettuare il salting. Ci ha, quindi, permesso di ottenere una maggiore sicurezza pur avendo un singolo campo per la password nel database, oltre alla flessibilità di poter aumentare la complessità del calcolo dell'hash.

## Libreria `session`

La libreria session ci ha permesso di salvare in maniera cifrata in un cookie il token utilizzato nelle varie pagine per autentificare l'utente e verificare che sia effettivamente lui


# Contributo al progetto

Lo sviluppo del progetto è iniziato scrivendo lo schema ER collaborativamente, in modo da evitare di non accorgersi di parti salienti da implementare nel progetto, successivamente Luca Saccarola ha implementato il tooling che abbiamo usato per l'interezza del progetto come, ad esempio, mypy o il file `compose.yml` usato per il database e Paolo Mozzoni ha implementato la struttura base delle pagine (quindi la suddivisione in `routes`, `model`, `templates`, file `__init__`...)

Dopo questa fase iniziale ci siamo divisi i compiti in task da svolgere settimanalmente, escludendo quale ritardo dovuto alla presenza della sessione d'esame nell'ultima fase del progetto. La suddivisione è stata facilitata dal fatto che abbiamo usato git, per poi lavorare su singoli branch mergiandoli dopo aver creato e approvato le relative pr. Se non consideriamo i contributi minori a parti non assegnate direttamente ad altri interessati, possiamo suddividere le assegnazioni come segue:

- Luca Saccarola:
    - **homepage:** creazione della pagina con libri consigliati scelti randomicamente
    - **searchbar:** barra di ricerca per nome del libro, autore, casa editoriale...
    - **libro:** visualizzazione dei dettagli di un singolo libro
    - **css e design grafico:** buona parte di scelte principali di design, nonché gli scheletri base delle pagine utilizzate per tutta la piattaforma
    - **componentizzazione delle pagine:** rimozione di codice duplicato e conseguente creazione di componenti singole per le pagine scritte da Paolo Mozzoni e luca
    - **logo:** perché anche l'occhio vuole la sua parte
- Paolo Mozzoni:
    - **libreria:** visualizzazione di libri posseduti e in vendita dell'utente
    - **carrello:** gestione degli acquisti che l'utente vuole fare
    - **libro:** visualizzazione delle relative inserzioni disponibili
    - **notifiche:** visualizzazione delle notifiche
    - **venditore:** visualizzazione delle recensioni e delle inserzioni di un venditore
    - **visualizzazione ordini:** pagina di gestione degli ordini
- Luca Barban:
    - **sistema autenticazione:** gestioni dei login, registrazioni, autenticazione
    - **storico:** visualizzazione degli ordini effettuati per recensirli 
    - **gestione inserzioni:** creazione, aggiornamento e rimozione di inserzioni
    - **profilo:** visualizzazione dei dati del proprio profilo
