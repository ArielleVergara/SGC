from app.repositories.usuario_repository import obtener_usuario_por_email
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def autenticar_usuario(email, password):

    user = obtener_usuario_por_email(email)

    if user and bcrypt.check_password_hash(user["password_hash"], password):
        return user

    return None