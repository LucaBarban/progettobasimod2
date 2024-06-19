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
### Tabella `users`
### Tabella `owns`
### Tabella `carts`
### Tabella `history`
### Tabella `notifications`

Progettazione Concettuale e Logica della basi di dati opportunamente spiegate e motivate La presentazione deve seguire la notazione grafica introdotta nel Modulo 1 del corso.

# Query Principali
una descrizione di una selezione delle query più interessanti che sono state implementate all’interno dell’applicazione, utilizzando una sintassi SQL opportuna.


# Scelte Progettuali
politiche di integrità e come sono state garantite in pratica (es. trigger), definizione di ruoli e politiche di autorizzazione, uso di indici, view, ecc. Tutte le principali scelte progettuali devono essere opportunamente commentate e motivate.


# Ulteriori informazioni
scelte tecnologiche specifiche (es. librerie usate) e qualsiasi altra informazione sia necessaria per apprezzare il progetto.

# Contributo al progetto
una spiegazione di come i diversi membri del gruppo hanno contribuito al design ed allo sviluppo.
