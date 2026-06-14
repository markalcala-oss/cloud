# CloudContacts (Agenda de Contactos en la Nube)

Aplicación web responsiva en Flask que gestiona una lista de contactos. Desplegada en una arquitectura de dos capas en Amazon Web Services (AWS) siguiendo buenas prácticas de aislamiento y seguridad.

---

## 1. Arquitectura del Sistema
Para proteger los datos, la infraestructura se dividió en dos servidores independientes:
* **EC2-WEB (Capa Web):** Instancia Ubuntu expuesta a internet. Corre la app de Flask con Gunicorn usando una **IP Elástica** fija.
* **EC2-DB (Capa de Datos):** Instancia Ubuntu aislada. Contiene MySQL Server (Puerto 3306) y solo responde a peticiones de la EC2-WEB.

---

## 2. Configuración de AWS (Security Groups)

### SG-WEB (Servidor Web)
* **SSH (Puerto 22):** Permitido temporalmente desde `0.0.0.0/0` para administración segura.
* **Custom TCP (Puerto 5000):** Abierto a `0.0.0.0/0` (Anywhere) para permitir el acceso público a la aplicación.

### SG-DB (Base de Datos)
* **MYSQL/Aurora (Puerto 3306):** Abierto a `0.0.0.0/0` para habilitar el enlace con el script de la web.

---

## 3. Configuración de la Base de Datos (EC2-DB)

1. **Instalación:**
```bash
   sudo apt update && sudo apt install mysql-server -y
Acceso Externo: En /etc/mysql/mysql.conf.d/mysqld.cnf se cambió a bind-address = 0.0.0.0. Se aplicó con sudo systemctl restart mysql.

Estructura y Permisos (sudo mysql):

SQL
   CREATE DATABASE cloudcontacts_db;
   USE cloudcontacts_db;

   CREATE TABLE contactos (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nombre VARCHAR(100) NOT NULL,
       email VARCHAR(100) NOT NULL UNIQUE,
       fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE USER 'cloud_user'@'IP_PUBLICA_DE_EC2_WEB' IDENTIFIED BY 'TuContraseñaSegura123!';
   GRANT ALL PRIVILEGES ON cloudcontacts_db.* TO 'cloud_user'@'IP_PUBLICA_DE_EC2_WEB';
   FLUSH PRIVILEGES;
4. Despliegue de la Aplicación (EC2-WEB)
Preparación del Entorno:

Bash
   sudo apt update && sudo apt install python3-pip python3-venv git -y
   git clone [https://github.com/markalcala-oss/cloud.git](https://github.com/markalcala-oss/cloud.git) && cd cloud
   python3 -m venv venv && source venv/bin/activate
   pip install Flask mysql-connector-python python-dotenv gunicorn
Variables de Entorno (.env): Creado en la raíz para proteger credenciales fuera de GitHub:

Fragmento de código
   DB_HOST=IP_PUBLICA_DE_TU_EC2_DB
   DB_USER=cloud_user
   DB_PASSWORD=TuContraseñaSegura123!
   DB_NAME=cloudcontacts_db
Persistencia con Systemd: Se creó el servicio en /etc/systemd/system/cloudcontacts.service:

Ini, TOML
   [Unit]
   Description=Gunicorn CloudContacts
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/cloud
   ExecStart=/home/ubuntu/cloud/venv/bin/gunicorn -b 0.0.0.0:5000 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
Se activó con: sudo systemctl daemon-reload && sudo systemctl enable --now cloudcontacts.

5. Bitácora de Errores Solucionados (Troubleshooting)
Error 1: ERR_CONNECTION_REFUSED en puerto 5000

Causa: Se intentó acceder al puerto 5000 en el navegador cuando Gunicorn escuchaba originalmente en el puerto 80, además faltaba abrir el puerto 5000 en el Security Group de AWS.

Solución: Se reconfiguró Gunicorn para amarrarse al puerto 5000 y se agregó la regla de entrada correspondiente en el SG-WEB.

Error 2: Connection timed out en SSH (Puerto 22)

Causa: Bloqueo de AWS debido a cambios automáticos en la IP pública local del administrador (IP dinámica del módem de casa).

Solución: Se modificó la regla de entrada de SSH en el Security Group de My IP a 0.0.0.0/0 de manera temporal para recuperar el control.

Error 3: Could not resolve hostname / Host desconocido

Causa: Error de tipeo en la terminal al escribir la dirección DNS pública de AWS (.co en lugar de .com).

Solución: Se simplificó la conexión utilizando directamente la dirección IP elástica numérica (3.91.191.2).