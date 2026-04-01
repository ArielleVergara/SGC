from flask import Blueprint, render_template, request, redirect, session, flash
from app.utils.auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    if "usuario" not in session:
        return redirect("/login")
    return render_template("dashboard.html", usuario=session["usuario"])