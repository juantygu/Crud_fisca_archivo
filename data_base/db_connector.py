import json
import mysql.connector


class BDConnector:
    """
    Clase que proporciona una interfaz para conectar y realizar operaciones en una base de datos MySQL.

    Attributes:
        connection: La conexión a la base de datos MySQL.
        cursor: El cursor utilizado para ejecutar modulo_consultas SQL.
        in_transaction: Un indicador del estado de la transacción actual.
    """
    def __init__(self): # que sirve como una interfaz para conectar y realizar operaciones en la base de datos.
        """
                Constructor de la clase BDConnector.

                Inicializa la conexión a la base de datos y crea un cursor.
                """
        self.host = None
        self.user = None
        self.password = None
        self.database = None
        self.load_config_bd()

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        # Variable de instancia para realizar un seguimiento del estado de la transacción
        self.in_transaction = False

    def load_config_bd(self):
        """
        Carga la configuración de la base de datos desde el archivo JSON.
        """
        try:
            with open('D:/pythonProject/Crud_fisca_archivo/config.json') as config_file:
                config = json.load(config_file)
                self.host = config["DB_HOST"]
                self.user = config["DB_USER"]
                self.password = config["DB_PASSWORD"]
                self.database = config["DB_DATABASE"]
        except FileNotFoundError:
            print("No se encontró el archivo de configuración.")
        except KeyError as e:
            print(f"Error: La clave {e} no está presente en el archivo de configuración.")

    def execute_query(self, query, values=None):
        """
                Ejecuta una consulta en la base de datos.

                Parameters:
                - query (str): La consulta SQL a ejecutar.
                - values (tuple, opcional): Los valores a sustituir en la consulta.

                Returns:
                - MySQLCursor: El cursor después de ejecutar la consulta.
                """
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        return self.cursor

    def fetch_all(self):
        """
                Obtiene todos los resultados de la última consulta.

                Returns:
                - list: Una lista de tuplas con los resultados.
                """
        return self.cursor.fetchall()

    def fetch_one(self):
        """
                Obtiene el primer resultado de la última consulta.

                Returns:
                - tuple: Una tupla con el primer resultado.
                """
        return self.cursor.fetchone()

    def close_connection(self):
        """
        Cierra la conexión a la base de datos.
        """
        try:
            if self.connection:
                self.connection.close()
                print("Conexión cerrada exitosamente.")
        except mysql.connector.Error as err:
            print(f"Error al cerrar la conexión: {err}")

    def mostrar_conexiones_activas(self):
        """
                Muestra las conexiones activas a la base de datos.

                Prints:
                - str: Filas que representan conexiones activas.
                """
        try:
            # Ejecutar la consulta para mostrar conexiones activas
            query = "SHOW PROCESSLIST"
            self.cursor.execute(query)

            # Obtener y mostrar los resultados
            results = self.cursor.fetchall()
            for row in results:
                print(row)

        except mysql.connector.Error as err:
            print(f"Error al mostrar conexiones activas: {err}")

    def start_transaction(self):
        """
        Inicia una transacción en la base de datos.
        """
        self.connection.start_transaction()

# Uso del nuevo método
#connector = BDConnector()
#connector.connection.cmd_query("KILL 300")
#connector.mostrar_conexiones_activas()
#connector.close_connection()

# Después de crear la instancia de BDConnector
#bd_connector = BDConnector()

# Verificar el estado actual de autocommit
#print("Autocommit activado:" if bd_connector.connection.autocommit else "Autocommit desactivado:")
