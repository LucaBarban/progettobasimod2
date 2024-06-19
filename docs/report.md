# Tabella dei Contenuti
1. [Introduzione](#introduzione)
2. [Funzionalità Principali](#funzionalità-principali)
    1. [Sistema di Autenticazione](#sistema-di-autenticazione)
    2. [Visualizzazione singolo Libro e relative Inserzioni](#visualizzazione-singolo-libro-e-relative-inserzioni)
    3. [Gestione del Carrello](#gestione-del-carrello)
    4. [Visualizzazione degli Acquisti](#visualizzazione-degli-acquisti)
    5. [Struttura delle Pagine](#struttura-delle-pagine)
    6. [Gestione delle Inserzioni](#gestione-delle-inserzioni)
    7. [Visualizzazione della propria Libreria](#visualizzazione-della-propria-libreria)
    8. [Visualizzazione delle Notifiche](#visualizzazione-delle-notifiche)
    9. [Gestione degli Ordini](#gestione-degli-ordini)
    10. [Gestione del Profilo](#gestione-del-profilo)
    11. [Gestione della Ricerca](#gestione-della-ricerca)
    12. [Visualizzazione Venditore](#visualizzazione-venditore)
3. [Progettazione Concettuale e Logica](#progettazione-concettuale-e-logica)
    1. [Entità](#entità)
        1. [Entità `Users`](#entità-users)
        2. [Entità `Sellers`](#entità-sellers)
        3. [Entità `Carts`](#entità-carts)
        4. [Entità `History`](#entità-history)
        5. [Entità `Books`](#entità-books)
        6. [Entità `Genres`](#entità-genres)
        7. [Entità `Authors`](#entità-authors)
        8. [Entità `Publishers`](#entità-publishers)
        9. [Entità `Notifications`](#entità-notifications)
        10. [Entità `Orders`](#entità-orders)
    2. [Relazioni](#relazioni)
        1. [Relazione `afferisce`](#relazione-afferisce)
        2. [Relazione `own`](#relazione-own)
        3. [Relazione `appartiene`](#relazione-appartiene)
        4. [Relazione `scritto da`](#relazione-scritto-da)
        5. [Relazione `pubblicato da`](#relazione-pubblicato-da)
        6. [Relazione `contiene`](#relazione-contiene)
        7. [Relazione `possiede`](#relazione-possiede)
        8. [Relazione `riguarda`](#relazione-riguarda)
        9. [Relazione `ha prodotti in`](#relazione-ha-prodotti-in)
        10. [Relazione `é riferito in](#relazione-é-riferito-in)
        11. [Relazione `si riferisce a`](#relazione-si-riferisce-a)
    3. [Schema ER Risultante](#schema-er-risultante)
    4. [Rappresentazione Logica](#rappresentazione-logica)
        1. [Tabella `genres`](#tabella-genres)
        2. [Tabella `authors`](#tabella-authors)
        3. [Tabella `publishers`](#tabella-publishers)
        4. [Tabella `books`](#tabella-books)
        5. [Tabella `booksgenres`](#tabella-booksgenres)
        6. [Tabella `users`](#tabella-users)
        7. [Tabella `owns`](#tabella-owns)
        8. [Tabella `carts`](#tabella-carts)
        9. [Tabella `history`](#tabella-history)
        10. [Tabella `notifications`](#tabella-notifications)
4. [Query Principali](#query-principali)
5. [Scelte Progettuali](#scelte-progettuali)
6. [Ulteriori informazioni](#ulteriori-informazioni)
7. [Contributo al Progetto](#contributo-al-progetto)



# Introduzione
La variante del progetto da noi scelta è quella dell'"e-commerce", che abbiamo personalizzato come una piattaforma specializzata nella vendita di libri. Questa piattaforma supporta la ricerca delle singole opere, affinabile tramite filtri, e la conseguente acquisto da parte degli utenti registrati. Ogni utente può successivamente decidere di vendere i propri libri al prezzo desiderato e, se l'opera non è ancora presente nel database, può aggiungerla fornendo i relativi metadata, come il genere, l'autore, la copertina, ecc.


# Funzionalità principali
Le funzionalità pricipali che abbiamo implementato sono le seguenti:
## Sistema di Autenticazione
## Visualizzazione singolo Libro e relative Inserzioni
## Gestione del Carrello
## Visualizzazione degli Acquisti
## Struttura delle Pagine
## Gestione delle Inserzioni
## Visualizzazione della propria Libreria
## Visualizzazione delle Notifiche
## Gestione degli Ordini
## Gestione del Profilo
## Gestione della Ricerca
## Visualizzazione Venditore

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

Viene specificata un'invariante che controlla che la quantità sia positiva e che il libro/i che si vuole comprare faccia parte dei libri appartenenti al venditore

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
L'entitò rappresenta i libri presenti all'interno del database come "entità" astratta, quindi non il singolo libro posseduto da un certo utente. L'entità ha anche i seguenti campi:

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
Entità rappresentante una casa pubblicatrice di libri. Il suo unico attributo è:
- `nome`: nome identificativo della casa pubblicatrice

### Entità `Notifications`
Entità rappresentante le singole notifiche di un certo utente. Essa ha i seguenti attributi:
- `id`: identificativo della notifica
- `message`: messaggio della notifica
- `archived`: valore booleano usato per segnare quanto un utente fa l'acknowledge della notifica

### Entità `Orders`
Enità che specializza `Notifications` al fine di contenere maggiori informazioni per gli ordini andando ad agginge 2 attributi:
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
Collega il libro alla sua casa pubblicatrice

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
![Schema ER](./database_ER.png)

## Rappresentazione Logica

### Tabella `genres`
Rispecchia la sua corrispettiva [entità](#entità-genres), mantenendo come campi:
- `nome` che ha tipo `TEXT` ed è `PRIMARY KEY`

### Tabella `authors`
Rispecchia la sua corrispettiva [entità](#entità-authors), mantenendo come campi:
- `id` che ha tipo `SERIAL` ed è `PRIMARY KEY`, in modo da evere un modo comodo di gestire le omonimie tramite un contatore autoincrementale
- `first_name` che ha tipo `CHARACTER VARYING(255)`, quindi una stringa di caratteri di dimensione variabile che non può essere `NULL`
- `last_name` che ha le stesse caratteristiche di `first_name` per eguali motivi

### Tabella `publishers`
Rispecchia la sua corrispettiva [entità](#entità-publishers), mantenendo come campi:
- `name` che ha tipo `TEXT` ed è `PRIMARY KEY`

### Tabella `books`
Per quanto rispecchi in parte la sua [entità](#entità-books), questa tabella va anche ad aggiungere agli attributi anche le relazioni qui riportate:
- `id`: identificativo artificiale del libro, motivo per cui è `SERIAL PRIMARY KEY`
- `title`: titolo del libro, quindi è `TEXT NOT NULL`
- `published`: data di pubblicazione, quindi `DATE NOT NULL`
- `pages`: numero di pagine obbligatorio (`INTEGER NOT NULL`), a cui viene integrato il seguente controllo che le obbliga ad essere in numero positivo: `CONSTRAINT pages_gt CHECK (pages > 0)`
- `isbn`: sequenza di caratteri che deve coprire diversi standard, per cui è `CHARACTER VARYING(20)`, e può essere omessa
- `fk_author`: chiave esterna, come richiesto dalla relazione [`scritto da`](#relazione-scritto-da), quindi diventa `REFERENCES authors(id)` e ne mantiene il tipo `INTEGER`
- `fk_publisher`: chiave esterna, come richiesto dalla relazione [`pubblicato da`](#relazione-pubblicato-da), quindi diventa `REFERENCES publishers(name)` e ne mantiene il tipo `TEXT`

### Tabella `booksgenres`
Questa tabella rappresenta la relazione [`appartiene`](#relazione-appartiene), che è una `n-n`. Ne consegue che abbia come attributi:
- `fk_idB`: chiave esterna di `books(id)` con tipo `INTEGER` e anche parte della chiave primaria
- `fk_genre`: chiave esterna di `genres(name)` con tipo `TEXT` e anche parte della chiave primaria

### Tabella `users`
La seguente tabella rispecchia fedelmente la struttura di [`Users`](#entità-users), per cui ha i seguenti attributi:
- `username`: nome utente identificativo, ha quindi tipo `VARCHAR(100)` ed è `PRIMARY KEY`
- `first_name`: nome dell'utente, ha tipo `VARCHAR(255)` e non può essere vuoto (`NOT NULL`)
- `last_name`: cognome dell'utente, ha tipo `VARCHAR(255)` e non può essere vuoto (`NOT NULL`)
- `password`: ha tipo `TEXT`, in modo da poter supportare cambiamenti dell'algoritmo di hashing e salting con dimensioni dell'hash differenti. Ovviamente è `NOT NULL`
- `created_at`: `TIMESTAMP` della creazione, deve essere `NOT NULL`
- `balance`: centesimi presenti all'interno dell'account, per cui è `INTEGER` ed è `NOT NULL`. Essendo che deve essere rispettata l'invariante, viene aggiunto il seguente controllo: `CONSTRAINT balance_ge CHECK (balance >= 0)`
- `seller`: flag che sta ad indicare se l'account è abilitato a vendere prodotti, quindi ha tipo `BOOLEAN` ed è `NOT NULL`
- `last_logged_in_at`: orario in cui è stato fatto l'ultimo login, ha tipo `TIMESTAMP WITHOUT TIME ZONE` in modo da avere un oriario consistente tra tutti gli utenti, per quanto ci sia il server flask di mezzo, ed è `NOT NULL`
- `token`: token di autenticazione generato a tempo di login, ha tipo `CHARACTER(64)[]` e può essere `NULL` (in tal caso non esite un token valido)

### Tabella `owns`
La tabella segue la struttura della realzione [`own`](#relazione-own), collegandosi a [`Users`](#entità-users) e a [`Books`](#entità-books). Per questo ha i seguenti attributi:
- `id`: identificativo dell'oggetto posseduto (rappresenta il libro/i fisico, non il "modello" astratto presente in [`Books`](#entità-books)). Per questo è `SERIAL` ed è anche `PRIMARY KEY`
- `fk_username`: chiave esterna che si riferisce al possessore del libro/i, per questo è un `VARCHAR(100)`, è `NOT NULL` e si riferisce a `users(username)`
- `fk_book`: chiave esterna del "modello" del libro, per questo ha tipo `INTEGER`, è `NOT NULL` e si riferisce a `books(id)`
- `quantity`: indica la quantità di libri posseduta, è quindi `INTEGER NOT NULL`. Non è presente un `CHECK` in quanto il controllo è eseguito da un [trigger](#trigger-remove_if_quantity_zero) che offre anche altre funzionalità.
- `state`: stato fisico di "usura" dell'oggetto, ha un tipo custom `state` e deve essere `NOT NULL`
- `price`: prezzo in centesimi che l'utente può decidere nel caso volesse vendere il libro, altrimenti è impostato a `NULL`. È quindi `INTEGER` e ha il constraint `price_ge_owns CHECK (price >= 0)`, al fine di evitare di poter mettere prezzi negativi

È presente anche un ulteriore vincolo `UNIQUE(fk_username, fk_book, state, price)`, in modo da prevenire la presenza di più record di libri posseduti dallo stesso utente con lo stesso stato e prezzo

### Tabella `carts`
La tabella `carts` ricalca l'entità [`Carts`](#entità-carts), aggiungendo le relazioni [`possiede`](#relazione-possiede) e [`ha prodotti in`](#relazione-ha-prodotti-in). Per cui ha i seguenti attributi:
- `fk_buyer`: chiave esterna che si riferisce all'utente compratore, ha quindi tipo `VARCHAR(100)` e fa parte della chiave primaria e referenzia `users(username)`
- `fk_own`: chiave esterna del libro posseduto che l'utente è intenzionato a comprare, ha quindi tipo `INTEGER` e fa parte della chiave primaria e referenzia `owns(id)` andando a specificare `ON DELETE CASCADE`, in modo da rimuovere autoamticamente dal carrello un oggetto che viene esaurito
- `quantity`: quantità di prodotto che l'utente è interessato a comprare, ha tipo `INTEGER`, è `NOT NULL` e ha il constraint `quantity_gt_carts CHECK (quantity > 0)`

### Tabella `history`
La tabella `history` segue la struttura dell'entità [`History`](#entità-history), aggiungendo le 
- `id`: identificativo artificiale autoincrement, pre cui è `SERIAL` e `PRIMARY KEY` 
- `date`: data di acquisto, quindi è `TIMESTAMP` ed anche `NOT NULL`
- `quantity`: quantità di prodotti acquistata, quindi è `INTEGER`, `NOT NULL` e possiede il constraint `quantity_gt_history CHECK (quantity > 0)` che fa si che la quantità acquistabile non sia nulla o negativa
- `status`: stato dell'ordine/spedizione, ha tipo custom `status` ed è `NOT NULL`
- `price`: prezzo di acquisto in centesimi, è quindi `INTEGER`, `NOT NULL` e ha il constraint `price_ge_history CHECK (price >= 0)` che fa si che il prezzo sia positivo
- `review`: recensione che l'utente può lasciare (non obligatoriamente e successivamente all'acquisto), ha tipo `TEXT`
- `stars`: valutazione in stelle, ha tipo `INTEGER` e ha `CONSTRAINT stars_btw CHECK (stars IS NULL OR stars BETWEEN 0 AND 5)` che fa si che il numero di stelle sia compreso tra $1$ e $5$
- `fk_buyer`: chiave esterna dell'utente che ha comprato, ha quindi tipo `VARCHAR(100)` e si riferisce a `users(username)`
- `fk_seller`: chiave esterna che si riferisce all'utente venditore, ha quindi tipo `VARCHAR(100)` e si riferisce a `users(username)`
- `fk_book`: chiave esterna che si riferisce al "modello" del libro comprato, ha quindi tipo `INTEGER` e si riferisce a `books(id)`
- `state`: stato di usura del prodotto comprato, ha tipo custom `state`

### Tabella `notifications`
Questa tabella è frutto dell'unione di due entità: [`Notifications`](#entità-notifications) e [`Orders`](#entità-orders). Ha i seguenti attributi:
- `id`: identificativo della notifica autoincrement, ha tipo `SERIAL` ed è `PRIMARY KEY`
- `context`: tipo di notifica, ha tipo custom `disc_notif` ed è `NOT NULL`
- `fk_username`: chiave esterna dell'utente a cui è destina ta la notifica, ha quindi tipo `VARCHAR(100)`, è `NOT NULL` e si riferisce a `users(username)`
- `message`: messaggio della notifica, ha tipo `TEXT`
- `archived`: flag usato a seguito della visualizzazione del messaggio, ha tipo `BOOLEAN` ed è `NOT NULL`
- `fk_history`: riferimento all'eventuale ordine che ha subito un aggiornamento, ha tipo `INTEGER` e si riferisce a `history(id)`
- `order_status_old`: ha tipo custom `status` ed indica il vecchio stato dell'ordine nel caso fosse stato aggiornato
- `order_status_new`: ha tipo custom `status` ed indica il nuovo stato dell'ordine nel caso fosse stato aggiornato

# Query Principali
una descrizione di una selezione delle query più interessanti che sono state implementate all’interno dell’applicazione, utilizzando una sintassi SQL opportuna.


# Scelte Progettuali
politiche di integrità e come sono state garantite in pratica (es. trigger), definizione di ruoli e politiche di autorizzazione, uso di indici, view, ecc. Tutte le principali scelte progettuali devono essere opportunamente commentate e motivate.


# Ulteriori informazioni
scelte tecnologiche specifiche (es. librerie usate) e qualsiasi altra informazione sia necessaria per apprezzare il progetto.

# Contributo al progetto
una spiegazione di come i diversi membri del gruppo hanno contribuito al design ed allo sviluppo.
