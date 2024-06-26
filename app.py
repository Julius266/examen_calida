from flask import Flask, request, redirect, flash, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = '123456'

# Configuración de la conexión a la base de datos MySQL
app.config['MYSQL_HOST'] = 'bzdf4a8ltfb2sfsssjs9-postgresql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'u3ljkkzyh5kepo1sevpj'
app.config['MYSQL_PASSWORD'] = '5c89s9wamgCe6yoL2F2nOK3iQQTFw1'
app.config['MYSQL_DB'] = 'bzdf4a8ltfb2sfsssjs9'

# Inicialización de la extensión MySQL
mysql = MySQL(app)
cors = CORS(app)

# Rutas
@app.route('/')
def hello():
    return jsonify({'message': 'Your Backend is working!'})

# Esta función maneja las solicitudes GET a la raíz de la aplicación.
# Retorna todos los productos en formato JSON.

@app.route('/products')
def index():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM productos")
    if result_value > 0:
        products = cur.fetchall()
        return jsonify(products)
    return jsonify([])



if __name__ == '__main__':
    app.run(debug=True)