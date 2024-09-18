from flask import Flask, request, jsonify
import mysql.connector  # Para MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir peticiones del frontend React

# Configuración para conectarse a la base de datos MySQL
DB_HOST = '54.197.24.118'  # IP o dominio de la instancia DB
DB_NAME = 'usuarios_db'  # Nombre de la base de datos
DB_USER = 'flask_user'  # Nombre de usuario
DB_PASSWORD = 'Dani#0803'  # Contraseña de MySQL
DB_PORT = '3306'  # Puerto por defecto de MySQL

# Ruta para recibir los datos del frontend (POST)
@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json  # Recibe datos en formato JSON
    nombres = data.get('nombres')
    apellido = data.get('apellido')
    fecha_nacimiento = data.get('fecha_nacimiento')
    password = data.get('password')

    # Insertar datos en la base de datos
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = connection.cursor()
        insert_query = """INSERT INTO usuarios (nombres, apellidos, fecha_nacimiento, password) 
                          VALUES (%s, %s, %s, %s)"""
        cursor.execute(insert_query, (nombres, apellidos, fecha_nacimiento, password))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Datos insertados correctamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al insertar datos"}), 500

# Ruta para obtener los datos de los usuarios (GET)
@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM usuarios"
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(users), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Error al obtener usuarios"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
