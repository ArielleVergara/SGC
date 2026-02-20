import psycopg2

try:
    def get_connection():
        conn = psycopg2.connect(
            host="localhost",
            database="GC_PlantaCalma",
            user="postgres",
            password="1234",
            port="5432"
        )
        print("Conexión exitosa 🎉")
        conn.close()

except psycopg2.OperationalError as e:
    print("Error de conexión:")
    print(e)