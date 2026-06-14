from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_cursor
import mysql.connector

app = Flask(__name__)
app.secret_key = 'un_secreto_muy_seguro_para_los_flashes'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono') or None

        try:
            with get_db_cursor() as (conn, cursor):
                query = "INSERT INTO contactos (nombre, email, telefono) VALUES (%s, %s, %s)"
                cursor.execute(query, (nombre, email, telefono))
            flash("¡Contacto guardado exitosamente!", "success")
            return redirect(url_for('contacts'))
        
        except mysql.connector.Error as err:
            if err.errno == 1062: # Código de error para duplicados (UNIQUE)
                flash("Error: El correo electrónico ya está registrado.", "error")
            else:
                flash(f"Error de conexión a la base de datos: {err}", "error")
                
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    try:
        with get_db_cursor() as (conn, cursor):
            cursor.execute("SELECT nombre, email, telefono, fecha_registro FROM contactos ORDER BY fecha_registro DESC")
            lista_contactos = cursor.fetchall()
        return render_template('contacts.html', contactos=lista_contactos)
    except mysql.connector.Error as err:
        flash(f"No se pudieron cargar los contactos: {err}", "error")
        return render_template('contacts.html', contactos=[])

if __name__ == '__main__':
    app.run(debug=True)