from flask import Blueprint, render_template, request, redirect, session, flash
from app.services.auth_service import autenticar_usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def home():
    return redirect("/login")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = autenticar_usuario(email, password)
        if user:
            session["usuario"] = user
            session["user_id"] = user["id"]
            session["tienda_id"] = user["tienda_id"]
            session["rol"] = user["rol"]
            return redirect("/dashboard")

        flash("Credenciales incorrectas", "error")
        return render_template("login.html")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")