from data_base.db_connector import BDConnector
import mysql.connector


class ConsultasContribuyente:

    def __init__(self):
        self.connector = None

    def obtener_contribuyente(self, id_contribuyente=None, nombre_contribuyente=None):
        """
            Obtiene datos de un contribuyente basado en su ID o nombre.

            Parameters:
            - id_contribuyente: El ID del contribuyente a buscar.
            - nombre_contribuyente: El nombre del contribuyente a buscar.

            Returns:
            - mensaje y contribuyente: Mensaje de éxito o error de la consulta y los datos del contribuyente si se encuentra.
            """

        if id_contribuyente is None and nombre_contribuyente is None:
            print("Debe proporcionar al menos el ID, el nombre.")
            return "Debe proporcionar al menos el ID, el nombre.", None

        try:
            self.connector = BDConnector()
            query = "SELECT id_contribuyente, nombre_contribuyente, tipo FROM contribuyente WHERE"
            conditions = []
            values = []

            if id_contribuyente is not None:
                conditions.append(" id_contribuyente = %s")
                values.append(id_contribuyente)

            if nombre_contribuyente is not None:
                conditions.append(" nombre_contribuyente = %s")
                values.append(nombre_contribuyente)

            if len(conditions) > 1:
                query += " AND ".join(conditions)
            elif len(conditions) == 1:
                query += conditions[0]

            self.connector.execute_query(query, values)
            result = self.connector.fetch_all()

            if result:
                print("Datos del contribuyente encontrados:", result)
                return "Datos del contribuyente encontrados:", result
            else:
                print("No se encontraron datos para el contribuyente especificado.")
                return "No se encontraron datos para el contribuyente especificado.", None

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
            print(f"Error al obtener datos del contribuyente: {e}")
            return "Error al obtener datos del contribuyente", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def obtener_contribuyentes_por_tipo(self, tipo):
        """
            Obtiene todos los contribuyentes de un tipo específico.

            Parameters:
            - tipo: El tipo de contribuyente a buscar.

            Returns:
            - mensaje y contribuyentes: Mensaje de éxito o error de la consulta y una lista de los contribuyentes encontrados si la consulta fue exitosa.
            """
        try:
            self.connector = BDConnector()
            query = "SELECT id_contribuyente, nombre_contribuyente, tipo FROM contribuyente WHERE tipo = %s"
            self.connector.execute_query(query, (tipo,))
            contribuyentes = self.connector.fetch_all()

            if contribuyentes:
                print(f"Contribuyentes de tipo '{tipo}' encontrados:")
                return f"Contribuyentes de tipo '{tipo}' encontrados:", contribuyentes
            else:
                print(f"No se encontraron contribuyentes de tipo '{tipo}'.")
                return f"No se encontraron contribuyentes de tipo '{tipo}'.", None

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
            print(f"Error al obtener contribuyentes por tipo: {e}")
            return "Error al obtener contribuyentes por tipo", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def mostrar_contribuyentes(self):
        """
            Muestra todos los contribuyentes de la base de datos.

            Returns:
            - mensaje y contribuyentes: Mensaje de éxito o error de la consulta y una lista de todos los contribuyentes si la consulta fue exitosa.
            """
        try:
            self.connector = BDConnector()
            query = "SELECT id_contribuyente, nombre_contribuyente, tipo FROM contribuyente"
            self.connector.execute_query(query)
            contribuyentes = self.connector.fetch_all()

            if contribuyentes:
                print("Muestra de contribuyentes exitosa")
                return "Muestra de contribuyentes exitosa", contribuyentes
            else:
                print(" contribuyentes.")
                return "No se encontraron datos de contribuyentes.", None

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
            print(f"Error al obtener datos de contribuyentes: {e}")
            return "Error al obtener datos de contribuyentes", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def obtener_ultimo_contribuyente(self):
        """
        Función obtener_ultimo_contribuyente:

        Descripción:
        Esta función busca el último registro modificado o insertado en la tabla 'contribuyente' y muestra los 10 registros
        anteriores en términos de fecha de modificación.

        Argumentos:
        - No recibe argumentos adicionales. Utiliza la conexión a la base de datos establecida en el objeto 'self.connector'.

        Retorna:
        - Una tupla con un mensaje indicando el resultado de la operación ('Registros anteriores obtenidos exitosamente' o
          'No se encontraron datos de registros anteriores') y los datos de los registros obtenidos de la base de datos.
          Si no se encontraron datos, los registros serán 'None'.
        """
        try:
            self.connector = BDConnector()
            query = """
                    SELECT id_contribuyente, nombre_contribuyente, tipo 
                    FROM contribuyente 
                    WHERE fecha_modificacion <= (
                        SELECT fecha_modificacion 
                        FROM contribuyente 
                        ORDER BY fecha_modificacion DESC 
                        LIMIT 1
                    ) 
                    ORDER BY fecha_modificacion DESC 
                    LIMIT 11
                """
            self.connector.execute_query(query)
            registros_anteriores = self.connector.fetch_all()

            if registros_anteriores:
                print("Registros anteriores obtenidos exitosamente")
                return "Registros anteriores obtenidos exitosamente", registros_anteriores
            else:
                print("No se encontraron datos de registros anteriores.")
                return "No se encontraron datos de registros anteriores.", None

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
            print(f"Error al obtener los registros anteriores: {e}")
            return "Error al obtener los registros anteriores", None
        finally:
            if self.connector:
                self.connector.close_connection()

#consulta = ConsultasContribuyente()
#contribuyentes = consulta.mostrar_contribuyentes()
#print(contribuyentes[1])
#contribuyente = consulta.obtener_contribuyente()
##print(contribuyentes[1])
#contribuyente = consulta.obtener_ultimo_contribuyente()
#print(contribuyente[1])