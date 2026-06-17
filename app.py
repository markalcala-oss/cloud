from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, insert_lead, get_all_leads

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash_messages' # Necesario para mostrar alertas de éxito/error

# Inicializar la base de datos al arrancar la app
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form.get('nombre_completo')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        servicio = request.form.get('interes_servicio')
        
        # Validación básica en el backend
        if not nombre or not email or not telefono or not servicio:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('index'))
            
        # Intentar insertar en la base de datos AWS RDS
        exito = insert_lead(nombre, email, telefono, servicio)
        
        if exito:
            flash('¡Registro exitoso! Nos pondremos en contacto contigo pronto.', 'success')
        else:
            flash('Hubo un error al registrar tus datos. Es posible que el correo ya esté registrado.', 'error')
            
        return redirect(url_for('index'))
        
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    # Esta ruta servirá para ver la lista de leads capturados (CRUD - SELECT)
    leads = get_all_leads()
    return render_template('contacts.html', leads=leads)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)