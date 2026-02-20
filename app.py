from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from db import get_connection

app = Flask(__name__)
app.secret_key = "clave_super_secreta"
bcrypt = Bcrypt(app)

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, password_hash FROM usuarios WHERE email = %s AND activo = TRUE", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return "Login exitoso 🎉"

        return "Credenciales incorrectas ❌"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)