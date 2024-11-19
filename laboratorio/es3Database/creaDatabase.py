import sqlite3

# Funzione per creare il database e la tabella senza ID
def create_db():
    conn = sqlite3.connect('alphabot.db')  # Crea o apre il database
    c = conn.cursor()

    # Creazione della tabella 'commands' con lettera e comando
    c.execute('''
        CREATE TABLE IF NOT EXISTS commands (
            letter TEXT NOT NULL,
            command TEXT NOT NULL
        )
    ''')

    # Salva e chiudi la connessione
    conn.commit()
    conn.close()

# Funzione per popolare il database
def populate_db():
    conn = sqlite3.connect('alphabot.db')
    c = conn.cursor()

    # Dati da inserire: lettera e comando per Alphabot
    commands = [
        ('i', "'f10', 'l10', ''"),
        ('o', 'ciao'),
        ('p', 'miao')
    ]

    # Inserimento dei dati nella tabella 'commands'
    c.executemany('INSERT INTO commands (letter, command) VALUES (?, ?)', commands)

    # Salva e chiudi la connessione
    conn.commit()
    conn.close()

# Funzione per mostrare i dati nel database
def show_db():
    conn = sqlite3.connect('alphabot.db')
    c = conn.cursor()

    # Recupera tutti i dati dalla tabella 'commands'
    c.execute('SELECT * FROM commands')
    rows = c.fetchall()

    # Stampa i dati
    print("Comandi per Alphabot:")
    for row in rows:
        print(f"Lettera: {row[0]}, Comando: {row[1]}")

    # Chiudi la connessione
    conn.close()

# Codice principale
if __name__ == "__main__":
    create_db()    # Crea il database e la tabella
    populate_db()  # Popola la tabella con i comandi
    show_db()      # Mostra i comandi nel database