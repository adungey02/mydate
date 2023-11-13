import sqlite3

def create_tables():
    conn = sqlite3.connect('data3.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        idUsuario INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
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
    conn = sqlite3.connect('data3.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Profesionales (nombreProfesional) VALUES (?)', (nombre_profesional,))

    conn.commit()
    conn.close()

def get_profesionales():
    return ['Profesional1', 'Profesional2', 'Profesional3']