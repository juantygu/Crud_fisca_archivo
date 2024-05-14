from data_base.db_connector import BDConnector
import mysql.connector

class ConsultasAuditor: # define la logica de las consultas a la entidad auditor

    def __init__(self):
        self.connector = None

    def obtener_auditor(self, id_auditor=None, cedula=None, nombre_auditor=None):
        """
        Obtiene los datos de un auditor basándose en su ID, cédula o nombre.

        Parameters:
        - id_auditor (int): El ID del auditor (opcional).
        - cedula (str): La cédula del auditor (opcional).
        - nombre_auditor (str): El nombre del auditor (opcional).

        Returns:
        - tuple: Una tupla con los datos del auditor si se encontró, o None si no se encontraron datos.
        """
        # Validar si se proporciona al menos uno de los tres criterios de búsqueda
        if id_auditor is None and cedula is None and nombre_auditor is None:
            print("Debe proporcionar al menos el ID, la cédula o el nombre del auditor.")
            return "Debe proporcionar al menos el ID, la cédula o el nombre del auditor.",None

        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()

            # Consulta SQL para obtener los datos del auditor
            query = "SELECT id_auditor, cedula, nombre_auditor FROM auditor WHERE"
            conditions = []
            values = []

            if id_auditor is not None:
                conditions.append(" id_auditor = %s")
                values.append(id_auditor)

            if cedula is not None:
                conditions.append(" cedula = %s")
                values.append(cedula)

            if nombre_auditor is not None:
                conditions.append(" nombre_auditor = %s")
                values.append(nombre_auditor)

            # Combinar las condiciones con el operador AND si hay más de una
            if len(conditions) > 1:
                query += " AND ".join(conditions)
            elif len(conditions) == 1:
                query += conditions[0]
            print(query)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            result = self.connector.fetch_one()

            if result:
                print("Datos del auditor encontrados:", result)
                return "Datos del auditor encontrados:",result
            else:
                print("No se encontraron datos para el auditor especificado.")
                return "No se encontraron datos para el auditor especificado.", None

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
            print(f"Error al obtener datos del auditor: {e}")
            return "Error al obtener datos del auditor", None
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def mostrar_auditores(self):
        """
            Muestra todos los auditores de la base de datos.

            Returns:
            - mensaje y auditores: Mensaje de éxito o error de la consulta y una lista de los auditores si la consulta fue exitosa.
            """
        try: # Crear una instancia de BDConnector
            self.connector = BDConnector()
            # Consulta SQL para la modificación
            query = "SELECT id_auditor, cedula, nombre_auditor from auditor"
            resultado = self.connector.execute_query(query)
            auditores = resultado.fetchall()
            if auditores:
                print("Muestra de auditores exitosa")
                return "Muestra de auditores exitosa", auditores
            else:
                print("No se encontraron datos de auditores")
                return "No se encontraron datos de auditores ", None

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
            print(f"Error al obtener datos del auditor: {e}")
            return "Error al obtener datos del auditor", None
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def mostrar_nombre_id_auditores(self):
        """
            Muestra los nombres y el id de todos los auditores de la base de datos.

            Returns:
            - mensaje y auditores: Mensaje de éxito o error de la consulta y una lista de los nombres e ids de los auditores si la consulta fue exitosa.
            """

        try: # Crear una instancia de BDConnector
            self.connector = BDConnector()
            # Consulta SQL para la modificación
            query = "SELECT id_auditor,nombre_auditor from auditor"
            resultado = self.connector.execute_query(query)
            auditores = resultado.fetchall()
            if auditores:
                print("Muestra de auditores exitosa")
                return "Muestra de auditores exitosa", auditores
            else:
                print("No se encontraron datos de auditores")
                return "No se encontraron datos de auditores ", None

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
            print(f"Error al obtener datos del auditor: {e}")
            return "Error al obtener datos del auditor", None
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()




#consulta = ConsultasAuditor()
#auditor= consulta.obtener_auditor(id_auditor="A001",cedula=900085)
#print(auditor[1])
#auditores = consulta.mostrar_auditores()
#auditores = consulta.mostrar_nombre_id_auditores()
#print(auditores)