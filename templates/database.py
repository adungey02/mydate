import sqlite3
from flask import g

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with sqlite3.connect(DATABASE) as db:
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())

def get_user_by_username(username):
    conn = sqlite3.connect('database.db') 
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Usuarios WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()
    return user


def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profesionales (
            idProfesional INTEGER PRIMARY KEY,
            nombreProfesional TEXT NOT NULL
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Disponibilidades (
        idDisponibilidad INTEGER PRIMARY KEY,
        idProfesional INTEGER,
        idUsuario INTEGER,
        fechaDisponible DATE NOT NULL,
        horaDisponible TIME NOT NULL,
        UNIQUE (idProfesional, fechaDisponible, horaDisponible),
        FOREIGN KEY (idProfesional) REFERENCES Profesionales(idProfesional),
        FOREIGN KEY (idUsuario) REFERENCES Usuarios(idUsuario)
    )
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            idCliente INTEGER PRIMARY KEY,
            nombreCliente TEXT NOT NULL,
            numeroCelular TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservas (
            idReserva INTEGER PRIMARY KEY,
            idCliente INTEGER,
            idProfesional INTEGER,
            fechaReserva DATE NOT NULL,
            horaReserva TIME NOT NULL,
            numeroReserva INTEGER NOT NULL,
            UNIQUE (idProfesional, fechaReserva, horaReserva),
            FOREIGN KEY (idCliente) REFERENCES Clientes(idCliente),
            FOREIGN KEY (idProfesional) REFERENCES Profesionales(idProfesional)
        )
    ''')

    conn.commit()
    conn.close()

def insert_profesional(nombre_profesional):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Profesionales (nombreProfesional) VALUES (?)', (nombre_profesional,))

    conn.commit()
    conn.close()

def get_profesionales():
    return ['Profesional1', 'Profesional2', 'Profesional3']

