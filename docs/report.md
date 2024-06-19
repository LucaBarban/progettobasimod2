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
### Carts
### History
### Books
### Genres
### Authors
### Publishers
### Notifications
### Orders

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
