from flask import Flask, request, redirect, render_template
import sqlite3
from datetime import datetime   # agregado para registrar fecha y hora

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('negocio.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear tablas si no existen
conn = get_db_connection()

conn.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    contraseña TEXT NOT NULL,
    rol TEXT NOT NULL
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS platos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    descripcion TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS adicionales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    descripcion TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    plato_id INTEGER,
    adicional_id INTEGER,
    bebida_id INTEGER,
    fecha TEXT NOT NULL,
    metodo_pago TEXT,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(plato_id) REFERENCES platos(id),
    FOREIGN KEY(adicional_id) REFERENCES adicionales(id),
    FOREIGN KEY(bebida_id) REFERENCES platos(id)
)
""")

# Insertar usuario de prueba si no existe
existe = conn.execute("SELECT * FROM usuarios WHERE nombre=?", ("El Chavalo Nica",)).fetchone()
if not existe:
    conn.execute("INSERT INTO usuarios (nombre, contraseña, rol) VALUES (?, ?, ?)",
                 ("El Chavalo Nica", "Hola123*", "admin"))

# Menús Principales
platos_principales = [
    ("Pollo Asado", 40.00, "Marinado en naranja agría y achiote."),
    ("Carne Asada de Res", 40.00, "Clásica, con sal, ajo y naranja agría"),
    ("Lengua con Verduras", 40.00, "En salsa criolla de tomates, chiltomate y zanahoria."),
    ("Carne Desmenuzada", 40.00, "Res desmechada sofrita con base de vegetales frescos."),
    ("Bistec Encebollado", 40.00, "Lámina de res en su propio jugo con cama de cebollas")
]
for nombre, precio, descripcion in platos_principales:
    existe = conn.execute("SELECT * FROM platos WHERE nombre=?", (nombre,)).fetchone()
    if not existe:
        conn.execute("INSERT INTO platos (nombre, precio, descripcion) VALUES (?, ?, ?)", (nombre, precio, descripcion))

# Especialidades
especialidades = [
    ("Nacatamales", 30.00, "Masa de maíz con achiote, posta de cerdo y arroz, y hierba buena envuelto en hoja de platano."),
    ("Chancho con Yuca", 55.00, "Cerdo Marinado en achiote sobre cama de yuca suave.")
]
for nombre, precio, descripcion in especialidades:
    existe = conn.execute("SELECT * FROM platos WHERE nombre=?", (nombre,)).fetchone()
    if not existe:
        conn.execute("INSERT INTO platos (nombre, precio, descripcion) VALUES (?, ?, ?)", (nombre, precio, descripcion))

# Extras
adicionales = [
    ("Gallo Pinto (porción)", 15.00, "Arroz y frijoles rojos salteados con chiltoma."),
    ("Queso Frito (porción)", 8.00, "Auténtico queso nica de exportación, crujiente."),
    ("Maduro", 8.00, "Plátano maduro frito y caramelizado"),
    ("Coditos ensalada (porción)", 8.00, "Coditos con base cremora de mayonesa"),
    ("Repollo (porción)", 8.00, "Con chile cabro y cebollita curtida, Picante."),
    ("Remolacha (porción)", 8.00, "Con cebollita blanca, limón y sal."),
    ("Banano cocido", 8.00, "Banano verde suave y firme"),
    ("Tortillas (porción)", 5.00, "100% maíz blanco, palmeada a mano."),
    ("Tajadas", 15.00, "Platano verde tajadeadas y fritas.")
]
for nombre, precio, descripcion in adicionales:
    existe = conn.execute("SELECT * FROM adicionales WHERE nombre=?", (nombre,)).fetchone()
    if not existe:
        conn.execute("INSERT INTO adicionales (nombre, precio, descripcion) VALUES (?, ?, ?)", (nombre, precio, descripcion))

# Menús Suaves
menus_suaves = [
    ("Quesillos", 35.00, "Tortilla caliente, quesillo de trenza, cebollitas y abundante crema."),
    ("Tajadas con queso", 35.00, "Con ensalada de repollo y miltomate."),
    ("Taco", 35.00, "Tacos nicaragüenses crujientes rellenos de carne sazonada, acompañada de ensalada fresca de repollo, salsa y crema.")
]
for nombre, precio, descripcion in menus_suaves:
    existe = conn.execute("SELECT * FROM platos WHERE nombre=?", (nombre,)).fetchone()
    if not existe:
        conn.execute("INSERT INTO platos (nombre, precio, descripcion) VALUES (?, ?, ?)", (nombre, precio, descripcion))

# Bebidas
bebidas = [
    ("Cacao con leche (La estrella)", 30.00, "Cacao puro, canela y leche."),
    ("Chicha", 20.00, "Maíz rosado fermentado artesanal, aroma a vainilla."),
    ("Calala (Maracuya)", 25.00, "Fruta 100% natural"),
    ("Chía con tamarindo", 15.00, "Fruta 100% natural"),
    ("Arroz con piña", 15.00, "Cocinado con Canela, clavo y un toque de frambuesa")
]
for nombre, precio, descripcion in bebidas:
    existe = conn.execute("SELECT * FROM platos WHERE nombre=?", (nombre,)).fetchone()
    if not existe:
        conn.execute("INSERT INTO platos (nombre, precio, descripcion) VALUES (?, ?, ?)", (nombre, precio, descripcion))

conn.commit()
conn.close()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM usuarios WHERE nombre=? AND contraseña=?',
                        (usuario, contraseña)).fetchone()
    conn.close()
    if user:
        return redirect('/menu')
    else:
        return "Usuario o contraseña incorrectos"

@app.route('/menu')
def menu():
    conn = get_db_connection()
    platos = conn.execute("SELECT * FROM platos").fetchall()
    adicionales = conn.execute("SELECT * FROM adicionales").fetchall()
    conn.close()
    return render_template('menu.html', platos=platos, adicionales=adicionales)

import requests

GOOGLE_FORM_URL = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSedNDbBCFR7Cmo97ELsZMiLdiR8nST7QzeiomYF-tXRT1GRQQ/formResponse"

@app.route('/registrar_venta', methods=['POST'])
def registrar_venta():
    usuario_id = 1  # El Chavalo Nica (admin fijo por ahora)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metodo_pago = request.form.get("metodo_pago")  # <-- capturamos el método de pago

    conn = get_db_connection()

    # Obtener todos los platos y adicionales de la BD
    platos = conn.execute("SELECT * FROM platos").fetchall()
    adicionales = conn.execute("SELECT * FROM adicionales").fetchall()

    # Guardar platos con cantidad
    platos_seleccionados = []
    for plato in platos:
        cantidad = int(request.form.get(f"platos_id_{plato['id']}", 0))
        for _ in range(cantidad):
            conn.execute("INSERT INTO ventas (usuario_id, plato_id, fecha, metodo_pago) VALUES (?, ?, ?, ?)",
                         (usuario_id, plato['id'], fecha, metodo_pago))
            platos_seleccionados.append(plato)

    # Guardar adicionales con cantidad
    adicionales_seleccionados = []
    for adicional in adicionales:
        cantidad = int(request.form.get(f"adicionales_id_{adicional['id']}", 0))
        for _ in range(cantidad):
            conn.execute("INSERT INTO ventas (usuario_id, adicional_id, fecha, metodo_pago) VALUES (?, ?, ?, ?)",
                         (usuario_id, adicional['id'], fecha, metodo_pago))
            adicionales_seleccionados.append(adicional)

    # Guardar bebidas con cantidad (filtradas desde platos)
    bebidas_seleccionadas = []
    for plato in platos:
        if any(b in plato['nombre'] for b in ["Cacao", "Chicha", "Calala", "Chía", "Arroz con piña"]):
            cantidad = int(request.form.get(f"bebidas_id_{plato['id']}", 0))
            for _ in range(cantidad):
                conn.execute("INSERT INTO ventas (usuario_id, bebida_id, fecha, metodo_pago) VALUES (?, ?, ?, ?)",
                             (usuario_id, plato['id'], fecha, metodo_pago))
                bebidas_seleccionadas.append(plato)

    conn.commit()
    conn.close()

    # Calcular total
    total = sum([p['precio'] for p in platos_seleccionados])
    total += sum([a['precio'] for a in adicionales_seleccionados])
    total += sum([b['precio'] for b in bebidas_seleccionadas])

    # Enviar datos al Google Form (cada entry.xxxxx corresponde a un campo del formulario)
    data = {
        "entry.360908093": fecha,
        "entry.1059433338": metodo_pago,
        "entry.377586060": total,
        "entry.1886728710": ", ".join([p['nombre'] for p in platos_seleccionados]),
        "entry.690270562": ", ".join([b['nombre'] for b in bebidas_seleccionadas]),
        "entry.1668748071": ", ".join([a['nombre'] for a in adicionales_seleccionados])
    }
    requests.post(GOOGLE_FORM_URL, data=data)

    # Renderizar recibo
    return render_template('recibo.html',
                           fecha=fecha,
                           platos=platos_seleccionados,
                           adicionales=adicionales_seleccionados,
                           bebidas=bebidas_seleccionadas,
                           total=total,
                           metodo_pago=metodo_pago)

if __name__ == '__main__':
    app.run(debug=True)