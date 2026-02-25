from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from functools import wraps
from db import get_connection

app = Flask(__name__)
app.secret_key = "clave_super_secreta"
bcrypt = Bcrypt(app)

app.secret_key = "clave_super_secreta"

@app.route("/")
def home():
    return redirect("/login")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, password_hash, tienda_id, rol
            FROM usuarios
            WHERE email = %s
              AND activo = TRUE
        """, (email,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["tienda_id"] = user[2]
            session["rol"] = user[3]
            return redirect("/dashboard")

        flash("Correo o contraseña incorrectos", "error")
        return redirect("/login")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return f"""
    <h1>Dashboard</h1>
    <p>User ID: {session['user_id']}</p>
    <p>Tienda ID: {session['tienda_id']}</p>
    <p>Rol: {session['rol']}</p>
    """
if __name__ == "__main__":
    app.run(debug=True)