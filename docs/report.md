# Tabella dei Contenuti
1. [Introduzione](#introduzione)
2. [Funzionalità Principali](#funzionalità-principali)
    1. [Entità](#entità)
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
    2. [Relazioni](#relazioni)
    3. [Schema ER Risultante](#schema-er-risultante)
    4. [Rappresentazione Logica](#rappresentazione-logica)
3. [Progettazione Concettuale e Logica](#progettazione-concettuale-e-logica)
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
### Users
Rappresentano gli utenti che accedono all'e-commerce e hanno i seguenti attributi:
- `username`: Nome utente usato per effettuare il login che gli identifica univocamente
- `first_name` e `last_name`: nome e cognome per dare un grado di personalizzazione all'account in più
- `password`: password già hashata e salata utilizzata nella fase di login per provare l'identità dell'utente
- `created_at`: data di creazione dell'account
- `balance`: quantità di denaro in centesimi che l'utente ha caricato nell'account
- `last_logged_in_at`: data di ultimo login, utilizzata per controllare la validità del token salvato come cookie
- `token`: valore generato randomicamente che viene passato all'utente in fase di registrazione o login, viene utilizzato per autorizzare tutte le operazioni che esso andrà a fare (es. accedere alla propria libreria)

Viene aggiunta un'invariante che controlla che il `balance` dell'account non posso mai andare negativo (la piattaforma non offre, quindi, la possibilità di fare credito all'utente)

### Sellers
L'entità specializza utenti, e serve per distinguere quali di essi sono abilitati alla vendita e quali no

### Carts
Questa entità rappresenta un a serie di libri uguali che l'utente vuole comprare. Collega quindi l'utente al libro e al realtivo venditore, specificando una data quantità. L'attributo dell'entità è:
- `quantità`: rappresenta la quantità di uno specifico libro che è stato aggiunto al carrello

Viene specificata un'invariante che controlla che la quantità sia positiva e che il libro/i che si vuole comprare faccia parte dei libri appartenenti al venditore

### History
L'entità rappresenta lo storico degli acquisti effettuati dall'utente, includendo un campo per lasciare una recensione sull'esperienza d'acquisto e relativa valutazione in stelle. Gli attributi sono i seguenti:

- `id`: identifica lo specifico record nello storico
- `date`: data di quando si è effettuato l'acquisto
- `quantity`: quantità di libri che sono stati acquistati
- `status`: indica stato della spedizione, in modo da informare l'utente sui movimenti del suo acquisto
- `price`: salva il prezzo di acquisto in centesimi
- `review`: campo dedicato alla recensione scritta da parte dell'utente
- `stars`: campo dedicato a lasciare la propria valutazione in stelle

Vengono specificati anche tre invarianti, una che controlla che la quantità acquistata sia maggiore di 0, un'altra che controlla che il prezzo non sia negativo e un'ultima che controlla che le notifiche generate dall'acquisto e conseguenti aggiornamenti di spedizione facciano riferimento all'acquirente corretto

### Books
L'entitò rappresenta i libri presenti all'interno del database come "entità" astratta, quindi non il singolo libro posseduto da un certo utente. L'entità ha anche i seguenti campi:

- `id`: identifica il libro univocamente all'interno della base di dati
- `title`: titolo del libro
- `published`: data di pubblicazione del libro
- `pages`: numero di pagine 
- `isbn`: codice isbn del libro

Viene specificata anche un'invariante che controlla che le pagine siano in numero maggiore di $0$

### Genres
Entità rappresentante i possibili generi dei libri. Il suo unico attributo è:
- `nome`: nome del genere che lo identifica anche

### Authors
Entità rappresentante gli autori dei libri. I suoi attributi sono:
- `id`: id dell'autore che lo identifica
- `first_name`: nome dell'autore
- `last_name`: cognome dell'autore

### Publishers
Entità rappresentante una casa pubblicatrice di libri. Il suo unico attributo è:
- `nome`: nome identificativo della casa pubblicatrice

### Notifications
Entità rappresentante le singole notifiche di un certo utente. Essa ha i seguenti attributi:
- `id`: identificativo della notifica
- `message`: messaggio della notifica
- `archived`: valore booleano usato per segnare quanto un utente fa l'acknowledge della notifica

### Orders
Enità che specializza `Notifications` al fine di contenere maggiori informazioni per gli ordini andando ad agginge 2 attributi:
- `status_old`: vecchio stato della spedizione
- `status_new`: nuovo stato della spedizione

## Relazioni
###

## Schema ER Risultante
![Schema ER](./database_ER.png)

## Rappresentazione Logica
:D

Progettazione Concettuale e Logica della basi di dati opportunamente spiegate e motivate La presentazione deve seguire la notazione grafica introdotta nel Modulo 1 del corso.

# Query Principali
una descrizione di una selezione delle query più interessanti che sono state implementate all’interno dell’applicazione, utilizzando una sintassi SQL opportuna.

# Scelte Progettuali
politiche di integrità e come sono state garantite in pratica (es. trigger), definizione di ruoli e politiche di autorizzazione, uso di indici, ecc. Tutte le principali scelte progettuali devono essere opportunamente commentate e motivate.


# Ulteriori informazioni
scelte tecnologiche specifiche (es. librerie usate) e qualsiasi altra informazione sia necessaria per apprezzare il progetto.

# Contributo al progetto
una spiegazione di come i diversi membri del gruppo hanno contribuito al design ed allo sviluppo.
