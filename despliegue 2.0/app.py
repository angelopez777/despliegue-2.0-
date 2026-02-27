from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Configuración de la Base de Datos
def init_db():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)', 
                   (nombre, precio, cantidad))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)