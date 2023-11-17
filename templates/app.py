from flask import Flask, render_template, redirect, url_for, flash, request, g
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, ValidationError, DataRequired  # Asegúrate de importar DataRequired
from database import create_tables, get_profesionales, insert_profesional, get_user_by_username  # Reorganiza las importaciones
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, close_db, init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

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


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_users_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    db.commit()

# Configuración de la base de datos
app.teardown_appcontext(close_db)
init_db()

def insert_user(username, password):
    db = get_db()
    cursor = db.cursor()
    hashed_password = generate_password_hash(password, method='sha256')
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    db.commit()


def check_password(user, password):
    return check_password_hash(user['password'], password)


class ProfesionalForm(FlaskForm):
    nombre_profesional = StringField('Nombre del Profesional', validators=[DataRequired()])
    fecha_disponible = StringField('Fecha Disponible', validators=[DataRequired()])
    hora_disponible = StringField('Hora Disponible', validators=[DataRequired()])
    submit_profesional = SubmitField('Agregar Profesional')


class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

users = [
    User(1, 'usuario1', 'clave1'),
    User(2, 'usuario2', 'clave2')
]

@login_manager.user_loader
def load_user(user_id):
    return next((user for user in users if user.id == int(user_id)), None)

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if request.method == 'POST':
        form = ProfesionalForm(request.form)
        if form.validate():
            nombre_profesional = form.nombre_profesional.data
            fecha_disponible = form.fecha_disponible.data
            hora_disponible = form.hora_disponible.data

            insert_profesional(nombre_profesional, fecha_disponible, hora_disponible)

            flash('Profesional y disponibilidad agregados con éxito', 'success')

            return render_template_string("""
                {% extends "agregar_disponibilidad.html" %}
                {% block content %}
                    {{ super() }}
                {% endblock %}
            """, nombre_profesional=nombre_profesional, form=ProfesionalForm())

    profesionales = get_profesionales()
    return render_template('admin_dashboard.html', profesionales=profesionales, form=ProfesionalForm())

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = get_user_by_username(username) 

        if user and user.password == password:
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin_dashboard'))

        else:
            flash('Credenciales incorrectas', 'danger')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if get_user_by_username(username):
            flash('Este nombre de usuario ya está en uso. Por favor, elige otro.', 'danger')
        else:
            insert_user(username, password)
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))


@app.route('/agregar_disponibilidad/<nombre_profesional>', methods=['GET', 'POST'])
def agregar_disponibilidad(nombre_profesional):
    # Lógica para manejar la página de agregar_disponibilidad
    return render_template('agregar_disponibilidad.html', nombre_profesional=nombre_profesional, form=ProfesionalForm())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reservar')
def reservar():
    return render_template('reservar.html')

@app.route('/cancelar')
def cancelar():
    return render_template('cancelar.html')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Registrarse')

    def validate_username(self, field):
        if get_user_by_username(field.data):
            raise ValidationError('Este nombre de usuario ya está en uso. Por favor, elige otro.')

if __name__ == '__main__':
    with app.app_context():
        create_users_table()
    app.run(debug=True)
