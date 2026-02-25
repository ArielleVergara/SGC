import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="GC_PlantaCalma",
            user="postgres",
            password="1234",
            port="5432"
        )
        return conn
    except Exception as e:
        print("Error conectando a la base de datos:")
        print(e)
        return None