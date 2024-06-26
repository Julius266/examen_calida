from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS

# Crear una instancia de la aplicación Flask
app = Flask(__name__, template_folder='html')  # Especifica la carpeta para las plantillas HTML
app.secret_key = '123456'  # Clave secreta para la sesión de la aplicación

# Configuración de la conexión a la base de datos MySQL
app.config['MYSQL_HOST'] = 'bjnk2mgpopjuzitgbt7g-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'ueeuuwsc0bcvuj6a'
app.config['MYSQL_PASSWORD'] = 'Gl4xJoiqIIUOOd8s2jqL'
app.config['MYSQL_DB'] = 'bjnk2mgpopjuzitgbt7g'

# Inicialización de la extensión MySQL para la aplicación
mysql = MySQL(app)

# Configuración de CORS (Cross-Origin Resource Sharing) para permitir solicitudes desde cualquier origen
CORS(app)

# Ruta principal que renderiza la plantilla index.html
@app.route('/')
def index():
    return render_template('index.html')

### Operaciones CRUD para la tabla Productos ###

# Obtener todos los productos (GET)
# Obtener todos los productos (GET)
@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Productos")
        productos = cur.fetchall()
        cur.close()
        return render_template('productos.html', productos=productos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Obtener un producto por su ID (GET)
@app.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Productos WHERE id = %s", (id,))
        producto = cur.fetchone()
        cur.close()
        if producto:
            return render_template('producto_detalle.html', producto=producto) # Asegúrate de tener esta plantilla
        else:
            return render_template('productos.html', error='Producto no encontrado'), 404
    except Exception as e:
        return render_template('productos.html', error=str(e)), 500

@app.route('/productos/add', methods=['POST'])
def add_producto():
    try:
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Productos (nombre, precio, stock) VALUES (%s, %s, %s)", (nombre, precio, stock))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensaje': 'Producto agregado correctamente'}), 201
    except KeyError as e:
        return jsonify({'error': f'Falta el campo requerido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Actualizar un producto por su ID (PUT)
@app.route('/productos/update/<int:id>', methods=['POST'])
def update_producto(id):
    try:
        if request.form['_method'] == 'PUT':
            nombre = request.form['nombre']
            precio = request.form['precio']
            stock = request.form['stock']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Productos SET nombre=%s, precio=%s, stock=%s WHERE id=%s", (nombre, precio, stock, id))
            mysql.connection.commit()
            cur.close()
            return jsonify({'mensaje': 'Producto actualizado correctamente'}), 200
    except KeyError as e:
        return jsonify({'error': f'Falta el campo requerido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Eliminar un producto por su ID (DELETE)
@app.route('/productos/delete/<int:id>', methods=['POST'])
def delete_producto(id):
    try:
        if request.form['_method'] == 'DELETE':
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM Productos WHERE id = %s", (id,))
            mysql.connection.commit()
            cur.close()
            return jsonify({'mensaje': 'Producto eliminado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
### Operaciones CRUD para la tabla Clientes ###

# Obtener todos los clientes (GET)
@app.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Clientes")
        clientes = cur.fetchall()
        cur.close()
        return render_template('clientes.html', clientes=clientes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Clientes WHERE id = %s", (id,))
        cliente = cur.fetchone()
        cur.close()

        if cliente:
            return jsonify(cliente), 200
        else:
            return jsonify({'mensaje': 'Cliente no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clientes/add', methods=['POST'])
def add_cliente():
    try:
        nombre = request.form['nombre']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Clientes (nombre, email) VALUES (%s, %s)", (nombre, email))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('get_clientes'))
    except KeyError as e:
        return jsonify({'error': f'Falta el campo requerido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clientes/update/<int:id>', methods=['POST'])
def update_cliente(id):
    try:
        if request.form['_method'] == 'PUT':
            nombre = request.form['nombre']
            email = request.form['email']

            cur = mysql.connection.cursor()
            cur.execute("UPDATE Clientes SET nombre=%s, email=%s WHERE id=%s", (nombre, email, id))
            mysql.connection.commit()
            cur.close()

        return redirect(url_for('get_clientes'))
    except KeyError as e:
        return jsonify({'error': f'Falta el campo requerido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clientes/delete/<int:id>', methods=['POST'])
def delete_cliente(id):
    try:
        if request.form['_method'] == 'DELETE':
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM Clientes WHERE id = %s", (id,))
            mysql.connection.commit()
            cur.close()

        return redirect(url_for('get_clientes'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
### Operaciones CRUD para la tabla Pedidos ###

@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Pedidos.id, Clientes.nombre AS cliente_nombre, Pedidos.fecha_pedido FROM Pedidos JOIN Clientes ON Pedidos.cliente_id = Clientes.id")
        pedidos = cur.fetchall()
        cur.close()

        return render_template('pedidos.html', pedidos=pedidos)

    except Exception as e:
        return render_template('error.html', message=str(e)), 500


# Obtener un pedido por su ID (GET)
@app.route('/pedidos/<int:id>', methods=['GET'])
def get_pedido(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Pedidos.id, Clientes.nombre AS cliente_nombre, Pedidos.fecha_pedido FROM Pedidos JOIN Clientes ON Pedidos.cliente_id = Clientes.id WHERE Pedidos.id = %s", (id,))
        pedido = cur.fetchone()
        cur.close()

        if pedido:
            return jsonify(pedido), 200
        else:
            return jsonify({'mensaje': 'Pedido no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Agregar un nuevo pedido (POST)
@app.route('/pedidos/add', methods=['POST'])
def add_pedido():
    try:
        data = request.get_json()
        cliente_id = data['cliente_id']
        fecha_pedido = data['fecha_pedido']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Pedidos (cliente_id, fecha_pedido) VALUES (%s, %s)", (cliente_id, fecha_pedido))
        mysql.connection.commit()
        cur.close()

        return jsonify({'mensaje': 'Pedido agregado correctamente'}), 201
    except KeyError as e:
        return jsonify({'error': f'Falta el campo requerido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Actualizar un pedido por su ID (PUT)
@app.route('/pedidos/update/<int:id>', methods=['PUT'])
def update_pedido(id):
    try:
        cliente_id = request.json['cliente_id']
        fecha_pedido = request.json['fecha_pedido']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE Pedidos SET cliente_id=%s, fecha_pedido=%s WHERE id=%s", (cliente_id, fecha_pedido, id))
        mysql.connection.commit()
        cur.close()

        return jsonify({'mensaje': 'Pedido actualizado correctamente'}), 200
    except KeyError as e:
        return jsonify({'error': f'Falta el campo requerido: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Eliminar un pedido por su ID (DELETE)
@app.route('/pedidos/delete/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Pedidos WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        return jsonify({'mensaje': 'Pedido eliminado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)  # Inicia la aplicación en modo debug para facilitar la depuración
