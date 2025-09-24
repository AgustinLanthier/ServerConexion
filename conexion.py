import mysql.connector
from mysql.connector import Error

def conectar_mysql():
    
    try: 
        conexion = mysql.connector.connect(
            host = 'localhost',
            database = 'EjemploBD',
            user = 'root',
            password = ''
        )
        if conexion.is_connected():
            print("Conexion existosa a MySQL")
            info_servidor = conexion.get_server_info()
            print(f"Informacion del servidor: MySQL{info_servidor}")

            cursor = conexion.cursor()
            cursor.execute("SELECT DATABASE();")
            bd_actual = cursor.fetchone()
            print(f"Base de datos actual: {bd_actual[0]}")

            return conexion
        
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
    
def crear_tabla_usuarios(conexion):
    try:
        cursor = conexion.cursor()
        crear_tabla = """
        CREATE TABLE IF NOT EXISTS usuarios(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            edad INT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        cursor.execute(crear_tabla)
        print("Tabla 'usuarios' creada o verificada correctamente")

    except Error as e:
        print(f"Error al crear tabla: {e}")

def insertar_usuario(conexion,nombre,email,edad):
    try:
        cursor = conexion.cursor()

        insertar_sql = "INSERT INTO usarios (nombre,email,edad) VALUES (%s,%s,%s)"
        datos_usuario = (nombre,email,edad)

        cursor.execute(insertar_sql,datos_usuario)
        conexion.commit()

        print(f"Usuario '{nombre}' insetado correctamente (ID: {cursor.lastrowid})")

    except Error as e:
        print(f"Error al insertar usuario: {e}")

def consultar_usuarios(conexion):
    try:
        cursor = conexion.cursor()

        consulta_sql = "SELECT * FROM usuarios"
        cursor.execute(consulta_sql)

        usuarios = cursor.fetchall()

        print("\n Lista de usuarios: ")
        print("-" * 80)
        print(f"{'ID':<5}{'Nombre':<20}{'Email':<30}{'Edad':<5}{'Fecha Creacion'}")
        print("-" * 80)

        for usuario in usuarios:
            id_usuario, nombre, email, edad, fecha = usuario
            print(f"{id_usuario:<5}{nombre:<20}{email:<30}{edad:<5}{fecha}")

        print(f"\nTotal de usuarios: {len(usuarios)}")

    except Error as e:
        print(f"Error al consultar usuarios: {e}")

def buscar_usuario_por_email(conexion,email):
    try:
        cursor = conexion.cursor()

        buscar_sql = "SELECT * FROM usuarios WHERE email = %s"

        cursor.execute(buscar_sql,(email,))
        usuario = cursor.fetchone()
        if usuario:
            print(f"\n Usuario encontrado:")
            print(f"   ID: {usuario[0]}")
            print(f"   Nombre: {usuario[1]}")
            print(f"   Email: {usuario[2]}")
            print(f"   Edad: {usuario[3] or 'N/A'}")
            print(f"   Fecha de creacion: {usuario[4]}")

        else:
            print(f"No se encontró usuario con email: {email}")
    except Error as e:
        print(f"Error al consultar el email: {e}")

def main():
    print("Ejemplo de conexion a MySQL")
    print("=" * 50)

    conexion = conectar_mysql()

    if conexion:
        try: 
            crear_tabla_usuarios(conexion)

            print("\nInsertando usuario de ejemplo...")
            insertar_usuario(conexion,"Juan Perez","juan.perez@email.com",25)
            insertar_usuario(conexion,"Maria Gonzalez","maria.gonzalez@email.com",30)
            insertar_usuario(conexion,"Carlos Rodriguez","carlos.rodriguez@email.com",23)

            consultar_usuarios(conexion)
            print("\nBuscando usuario por email...")
            buscar_usuario_por_email(conexion,"juan.perez@email.com")
        
        except Exception as e:
            print(f"Error en operaciones: {e}")
        
        finally:
            if conexion.is_connected():
                conexion.close()
                print("\nConexion cerrada")

    else:
        print("No se pudo establecer conexion con MySQL")
        print("\nVerifique:")
        print("- Que MySQL este ejecutandose")
        print("- Las credenciales de conexion")
        print("- Que exista la base de datos 'EjemploBD'")
        
if __name__ == "__main__":
    main()
