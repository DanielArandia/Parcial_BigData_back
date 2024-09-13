from flask import Flask, request, jsonify
import psycopg2  # Para PostgreSQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir peticiones del frontend Angular

# Configuración para conectarse a la base de datos en otra instancia
DB_HOST = '54.197.24.118'  # IP o dominio de la instancia DB
DB_NAME = 'usuarios_db'  # Nombre de la base de datos
DB_USER = 'flask_user'  # Nombre de usuario
DB_PASSWORD = ''  # Contraseña vacía si no se requiere
DB_PORT = '5432'  # Puerto por defecto de PostgreSQL

# Ruta para recibir los datos del frontend
@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json  # Recibe datos en formato JSON
    nombre = data.get('nombre')
    email = data.get('email')

    # Insertar datos en la base de datos
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = connection.cursor()
        insert_query = """INSERT INTO usuarios (nombre, email) VALUES (%s, %s)"""
        cursor.execute(insert_query, (nombre, email))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Datos insertados correctamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al insertar datos"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

