from flask import Flask, render_template, redirect, url_for, flash, request
from database import create_tables, get_profesionales
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from forms import LoginForm


class ProfesionalForm(FlaskForm):
    nombre_profesional = StringField('Nombre del Profesional', validators=[DataRequired()])
    fecha_disponible = StringField('Fecha Disponible', validators=[DataRequired()])
    hora_disponible = StringField('Hora Disponible', validators=[DataRequired()])
    submit_profesional = SubmitField('Agregar Profesional')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

create_tables()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Crea una instancia del formulario de inicio de sesión

    if form.validate_on_submit():
        # Verifica las credenciales
        if form.username.data == 'admin' and form.password.data == 'password':
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin_dashboard'))  # Redirige al panel de administración
        else:
            flash('Credenciales incorrectas', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    # Puedes agregar lógica para cerrar sesión aquí
    return redirect(url_for('login'))


@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        form = ProfesionalForm(request.form)
        if form.validate():
            nombre_profesional = form.nombre_profesional.data
            fecha_disponible = form.fecha_disponible.data
            hora_disponible = form.hora_disponible.data

            # Aquí debes agregar la lógica para insertar en la base de datos
            # Puedes llamar a la función insert_profesional(fecha_disponible, hora_disponible, nombre_profesional)

            flash('Profesional y disponibilidad agregados con éxito', 'success')

            return render_template_string("""
                {% extends "agregar_disponibilidad.html" %}
                {% block content %}
                    {{ super() }}
                {% endblock %}
            """, nombre_profesional=nombre_profesional, form=ProfesionalForm())

    profesionales = get_profesionales()
    return render_template('admin_dashboard.html', profesionales=profesionales, form=ProfesionalForm())

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

if __name__ == '__main__':
    app.run(debug=True)
