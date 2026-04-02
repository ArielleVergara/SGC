from flask import Blueprint, render_template, request, redirect, session
from app.database import get_connection
from app.utils.auth import login_required

inventario_bp = Blueprint("inventario", __name__)

@inventario_bp.route("/inventario")
@login_required
def inventario():
    conn = get_connection()
    cur = conn.cursor()

    tienda_id = session["tienda_id"]
    print(tienda_id)

    cur.execute("""
        SELECT p.id, p.nombre, c.nombre, v.precio, v.stock
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        LEFT JOIN variantes_producto v ON v.producto_id = p.id
        WHERE p.tienda_id = %s AND p.activo = TRUE
    """, (tienda_id,))

    productos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("inventario.html", productos=productos)

@inventario_bp.route("/inventario/agregar", methods=["GET", "POST"])
@login_required
def agregar_producto():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria_id = request.form["categoria"]
        precio = request.form["precio"]
        stock = request.form["stock"]
        tienda_id = session["tienda_id"]

        cur.execute("""
            INSERT INTO productos (tienda_id, categoria_id, nombre)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (tienda_id, categoria_id, nombre))

        producto_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO variantes_producto (producto_id, sku, precio, stock)
            VALUES (%s, %s, %s, %s)
        """, (producto_id, f"SKU-{producto_id}", precio, stock))

        conn.commit()
        return redirect("/inventario")

    cur.execute("SELECT id, nombre FROM categorias WHERE tienda_id = %s", (session["tienda_id"],))
    categorias = cur.fetchall()

    return render_template("inventario.html", categorias=categorias)

@inventario_bp.route("/inventario/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        cur.execute("UPDATE productos SET nombre=%s WHERE id=%s", (nombre, id))
        cur.execute("""
            UPDATE variantes_producto
            SET precio=%s, stock=%s
            WHERE producto_id=%s
        """, (precio, stock, id))

        conn.commit()
        return redirect("/inventario")

    cur.execute("""
        SELECT p.nombre, v.precio, v.stock
        FROM productos p
        JOIN variantes_producto v ON v.producto_id = p.id
        WHERE p.id = %s
    """, (id,))

    producto = cur.fetchone()

    return render_template("editar_producto.html", producto=producto)

@inventario_bp.route("/inventario/eliminar/<int:id>")
@login_required
def eliminar_producto(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE productos SET activo = FALSE WHERE id = %s", (id,))
    conn.commit()

    return redirect("/inventario")

@inventario_bp.route("/categorias/agregar", methods=["POST"])
@login_required
def agregar_categoria():
    conn = get_connection()
    cur = conn.cursor()

    nombre = request.form["nombre"]
    tienda_id = session["usuario"]["tienda_id"]

    cur.execute("""
        INSERT INTO categorias (tienda_id, nombre)
        VALUES (%s, %s)
    """, (tienda_id, nombre))

    conn.commit()
    return redirect("/inventario")

@inventario_bp.route("/categorias/editar/<int:id>", methods=["POST"])
def editar_categoria(id):
    conn = get_connection()
    cur = conn.cursor()

    nombre = request.form["nombre"]

    cur.execute("""
        UPDATE categorias SET nombre=%s WHERE id=%s
    """, (nombre, id))

    conn.commit()
    return redirect("/inventario")

@inventario_bp.route("/categorias/eliminar/<int:id>")
def eliminar_categoria(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE categorias SET activo = FALSE WHERE id=%s
    """, (id,))

    conn.commit()
    return redirect("/inventario")