from app.database import get_connection

def obtener_usuario_por_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, password_hash, tienda_id, rol
        FROM usuarios
        WHERE email = %s AND activo = TRUE
    """, (email,))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    if data:
        return {
            "id": data[0],
            "password_hash": data[1],
            "tienda_id": data[2],
            "rol": data[3]
        }

    return None