from data_base.db_connector import BDConnector
import mysql.connector


class ConsultasProceso:
    def __init__(self):
        self.connector = None

    def obtener_proceso(self, id_proceso=None, nombre_proceso=None):
        """
        Obtiene los datos de un proceso basándose en su ID o nombre.

        Parameters:
        - id_proceso (int): El ID del proceso (opcional).
        - nombre_proceso (str): El nombre del proceso (opcional).

        Returns:
        - tuple: Una tupla con los datos del proceso si se encontró, o None si no se encontraron datos.
        """
        # Validar si se proporciona al menos uno de los dos criterios de búsqueda
        if id_proceso is None and nombre_proceso is None:
            print("Debe proporcionar al menos el ID o el nombre del proceso.")
            return "Debe proporcionar al menos el ID o el nombre del proceso.", None

        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()

            # Consulta SQL para obtener los datos del proceso
            query = "SELECT id_proceso, nombre_proceso FROM procesos WHERE"
            conditions = []
            values = []

            if id_proceso is not None:
                conditions.append(" id_proceso = %s")
                values.append(id_proceso)

            if nombre_proceso is not None:
                conditions.append(" nombre_proceso = %s")
                values.append(nombre_proceso)

            # Combinar las condiciones con el operador AND si hay más de una
            if len(conditions) > 1:
                query += " AND ".join(conditions)
            elif len(conditions) == 1:
                query += conditions[0]

            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            result = self.connector.fetch_one()

            if result:
                print("Datos del proceso encontrados:", result)
                return "Datos del proceso encontrados:", result
            else:
                print("No se encontraron datos para el proceso especificado.")
                return "No se encontraron datos para el proceso especificado.", None

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz ", None
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return "Error de la base de datos", None
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return "Error de MySQL", None
        except Exception as e:
            print(f"Error al obtener datos del proceso: {e}")
            return "Error al obtener datos del proceso", None
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def mostrar_procesos(self):
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()

            # Consulta SQL para obtener todos los procesos
            query = "SELECT id_proceso, nombre_proceso FROM procesos"
            resultado = self.connector.execute_query(query)
            procesos = resultado.fetchall()

            if procesos:
                print("Muestra de procesos exitosa:")
                return "Muestra de procesos exitosa:", procesos
            else:
                print("No se encontraron datos de procesos:")
                return "No se encontraron datos de procesos:", procesos

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return "Error de interfaz ", None
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return "Error de la base de datos", None
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return "Error de MySQL", None
        except Exception as e:
            print(f"Error al obtener los procesos: {e}")
            return "Error al obtener los procesos", None
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

consultas = ConsultasProceso()
#procesoo = consultas.obtener_proceso(id_proceso="3",nombre_proceso="sancionatorio")
#print(procesoo)
procesoss = consultas.mostrar_procesos()
print(procesoss[1])