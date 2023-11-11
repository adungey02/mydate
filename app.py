from flask import Flask, render_template
import os

app = Flask(__name__)

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
