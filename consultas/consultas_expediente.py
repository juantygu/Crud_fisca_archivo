from data_base.db_connector import BDConnector
import mysql.connector
from entidades.expediente import Expediente


class ConsultasExpediente:
    def __init__(self):
        self.connector = None
        self.expediente = Expediente()

    def buscar_por_id_expediente(self, id_expediente):
        """
        Busca expedientes por ID de expediente.

        Parameters:
        - id_contribuyente (int): ID del expediente.

        Returns:
        - tuple: Una tupla con los expediente encontrados si existen, o None si no se encontraron.
        """
        try:
            self.connector = BDConnector()
            query = "SELECT id_expediente, id_contribuyente, id_auditor, id_proceso, id_prestamo, id_caja, estado, año_gravable FROM expediente WHERE id_expediente = %s"
            values = (id_expediente,)
            self.connector.execute_query(query, values)
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Expedientes encontrados:")
                return "Expedientes encontrados:", expedientes
            else:
                print("No se encontraron expedientes para el ID de expediente especificado.")
                return "No se encontraron expedientes para el ID de expediente especificado.", None
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
            print(f"Error al buscar expedientes por ID de expediente: {e}")
            return "Error al buscar expedientes por ID de expediente", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def buscar_por_id_contribuyente(self, id_contribuyente):
        """
        Busca expedientes por ID de contribuyente.

        Parameters:
        - id_contribuyente (int): ID del contribuyente.

        Returns:
        - tuple: Una tupla con los expedientes encontrados si existen, o None si no se encontraron.
        """
        try:
            self.connector = BDConnector()
            query = "SELECT id_expediente, id_contribuyente, id_auditor, id_proceso,id_prestamo, id_caja, estado, año_gravable FROM expediente WHERE id_contribuyente = %s"
            values = (id_contribuyente,)
            self.connector.execute_query(query, values)
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Expedientes encontrados:")
                return "Expedientes encontrados:", expedientes
            else:
                print("No se encontraron expedientes para el ID de contribuyente especificado.")
                return "No se encontraron expedientes para el ID de contribuyente especificado.", None

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
            print(f"Error al buscar expedientes por ID de contribuyente: {e}")
            return "Error al buscar expedientes por ID de contribuyente", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def buscar_y_verificar_expedientes(self, lista_id_contribuyentes: list, id_proceso, lista_anos_gravables=None):
        """
        Busca expedientes por una lista de IDs de contribuyentes, verifica cuáles existen,
        cuáles están prestados y cuáles no se encontraron.

        Parameters:
        - lista_id_contribuyentes (list): Lista de IDs de contribuyentes.
        - id_proceso (int): ID del proceso.
        - lista_anos_gravables (list, optional): Lista de años gravables. Por defecto es None.

        Returns:
        - dict: Un diccionario con los resultados de la búsqueda y verificación.
        """
        resultados = {
            "exp encontrados": [],  # lista para almacenar expedientes por ID de contribuyente
            "ids encontrados": [],
            "ids no_encontrados": [],  # Lista para almacenar IDs de contribuyentes no encontrados
            "exp prestados": [],  # Lista para almacenar IDs de expedientes que están prestados
            "exp disponibles": []  # Lista para almacenar IDs de expedientes que están disponibles
        }

        try:
            self.connector = BDConnector()

            # Realizar la búsqueda de expedientes para todos los IDs de contribuyentes a la vez
            placeholders = ",".join(["%s"] * len(lista_id_contribuyentes))
            query = f"""
                SELECT id_expediente, id_contribuyente, id_auditor, id_proceso, id_prestamo, id_caja, estado, año_gravable
                FROM expediente WHERE id_contribuyente IN ({placeholders}) AND id_proceso = %s
            """
            values = tuple(lista_id_contribuyentes) + (id_proceso,)

            # Añadir condición sobre los años gravables si se proporciona la lista
            if lista_anos_gravables:
                placeholders_anos = ",".join(["%s"] * len(lista_anos_gravables))
                query += f" AND año_gravable IN ({placeholders_anos})"
                values += tuple(lista_anos_gravables)

            self.connector.execute_query(query, values)
            expedientes = self.connector.fetch_all()
            print(expedientes)

            # Verificar si se encontraron expedientes
            if expedientes:
                contribuyentes_encontrados = []
                for expediente in expedientes:
                    id_contribuyente = expediente[1]
                    if id_contribuyente not in contribuyentes_encontrados:
                        contribuyentes_encontrados.append(id_contribuyente)
                    resultados["exp encontrados"].append(expediente)

                print("Contribuyentes encontrados:", contribuyentes_encontrados)
                print("Expedientes encontrados:", resultados["exp encontrados"])

                # Verificar el estado de préstamo de los expedientes encontrados
                todos_expedientes_raw = [expediente[0] for expediente in expedientes]
                todos_expedientes = list(set(todos_expedientes_raw))

                print("Todos los expedientes:", todos_expedientes)
                if todos_expedientes:  # Verificar solo si hay expedientes encontrados
                    mensaje_prestamos, expedientes_prestados, expedientes_no_prestados, confirmacion = self.expediente.verificar_expedientes_prestados(
                        todos_expedientes, self.connector
                    )
                    resultados["exp prestados"] = list(expedientes_prestados)
                    resultados["exp disponibles"] = list(expedientes_no_prestados)
                    resultados["ids encontrados"] = list(contribuyentes_encontrados)
                    print("Expedientes prestados:", resultados["exp prestados"])
                    print("Expedientes disponibles:", resultados["exp disponibles"])

                ## Identificar contribuyentes no encontrados
                print("resta", set(lista_id_contribuyentes), set(contribuyentes_encontrados))
                resultados["ids no_encontrados"] = list(set(lista_id_contribuyentes) - set(contribuyentes_encontrados))

            else:
                # Si no se encontraron expedientes, todos los contribuyentes se consideran no encontrados
                resultados["ids no_encontrados"] = lista_id_contribuyentes
                resultados["exp disponibles"] = []  # Ningún expediente está disponible

            return resultados

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return "Error de interfaz con MySQL"
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return "Error de la base de datos"
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return "Error de MySQL"
        except Exception as e:
            print(f"Error al buscar y verificar expedientes: {e}")
            return "Error al buscar y verificar expedientes"
        finally:
            if self.connector:
                self.connector.close_connection()

    def buscar_por_id_auditor(self, id_auditor):
        """
        Busca expedientes por ID de auditor.

        Parameters:
        - id_auditor (int): ID del auditor.

        Returns:
        - tuple: Una tupla con los expedientes encontrados si existen, o None si no se encontraron.
        """
        try:
            self.connector = BDConnector()
            query = "SELECT id_expediente, id_contribuyente, id_auditor, id_proceso, id_prestamo, id_caja, estado, año_gravable FROM expediente WHERE id_auditor = %s"
            values = (id_auditor,)
            self.connector.execute_query(query, values)
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Expedientes encontrados:")
                return "Expedientes encontrados:", expedientes
            else:
                print("No se encontraron expedientes para el ID de auditor especificado.")
                return "No se encontraron expedientes para el ID de auditor especificado.", None

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
            print(f"Error al buscar expedientes por ID de auditor: {e}")
            return "Error al buscar expedientes por ID de auditor", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def buscar_por_id_proceso(self, id_proceso):
        """
        Busca expedientes por ID de proceso.

        Parameters:
        - id_proceso (int): ID del proceso.

        Returns:
        - tuple: Una tupla con los expedientes encontrados si existen, o None si no se encontraron.
        """
        try:
            self.connector = BDConnector()
            query = "SELECT id_expediente, id_contribuyente, id_auditor, id_proceso, id_prestamo, id_caja, estado, año_gravable FROM expediente WHERE id_proceso = %s"
            values = (id_proceso,)
            self.connector.execute_query(query, values)
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Expedientes encontrados:")
                return "Expedientes encontrados:", expedientes
            else:
                print("No se encontraron expedientes para el ID de proceso especificado.")
                return "No se encontraron expedientes para el ID de proceso especificado.", None

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
            print(f"Error al buscar expedientes por ID de proceso: {e}")
            return "Error al buscar expedientes por ID de proceso", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def buscar_expedientes_prestados(self):
        """
        Busca expedientes que han sido prestados.

        Returns:
        - tuple: Una tupla con los expedientes encontrados si existen, o None si no se encontraron.
        """
        try:
            self.connector = BDConnector()
            query = "SELECT id_expediente, id_contribuyente, id_auditor, id_proceso, id_prestamo, id_caja, estado, año_gravable FROM expediente WHERE id_prestamo IS NOT NULL"
            self.connector.execute_query(query)
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Expedientes prestados encontrados:")
                return "Expedientes prestados encontrados:", expedientes
            else:
                print("No se encontraron expedientes prestados.")
                return "No se encontraron expedientes prestados.", None

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
            print(f"Error al buscar expedientes prestados: {e}")
            return "Error al buscar expedientes prestados", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def buscar_por_id_caja(self, id_caja):
        """
        Busca expedientes por ID de caja.

        Parameters:
        - id_caja (int): ID de la caja.

        Returns:
        - tuple: Una tupla con los expedientes encontrados si existen, o None si no se encontraron.
        """
        try:
            self.connector = BDConnector()
            query = "SELECT id_expediente, id_contribuyente, id_auditor, id_proceso, id_prestamo, id_caja, estado, año_gravable FROM expediente WHERE id_caja = %s"
            values = (id_caja,)
            self.connector.execute_query(query, values)
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Expedientes encontrados:")
                return "Expedientes encontrados:", expedientes
            else:
                print("No se encontraron expedientes para el ID de caja especificado.")
                return "No se encontraron expedientes para el ID de caja especificado.", None

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
            print(f"Error al buscar expedientes por ID de caja: {e}")
            return "Error al buscar expedientes por ID de caja", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def buscar_por_estado(self, estado):
        """
        Busca expedientes por estado.

        Parameters:
        - estado (str): Estado del expediente.

        Returns:
        - tuple: Una tupla con los expedientes encontrados si existen, o None si no se encontraron.
        """
        try:
            self.connector = BDConnector()
            query = "SELECT id_expediente, id_contribuyente, id_auditor, id_proceso, id_prestamo, id_caja, estado, año_gravable FROM expediente WHERE estado = %s"
            values = (estado,)
            self.connector.execute_query(query, values)
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Expedientes encontrados:")
                return "Expedientes encontrados:", expedientes
            else:
                print("No se encontraron expedientes para el estado especificado.")
                return "No se encontraron expedientes para el estado especificado.", None

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
            print(f"Error al buscar expedientes por estado: {e}")
            return "Error al buscar expedientes por estado", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def buscar_por_año_gravable(self, año_gravable):
        """
        Busca expedientes por año gravable.

        Parameters:
        - año_gravable (int): Año gravable del expediente.

        Returns:
        - tuple: Una tupla con los expedientes encontrados si existen, o None si no se encontraron.
        """
        try:
            self.connector = BDConnector()
            query = "SELECT id_expediente, id_contribuyente, id_auditor, id_proceso, id_prestamo, id_caja, estado, año_gravable FROM expediente WHERE año_gravable = %s"
            values = (año_gravable,)
            self.connector.execute_query(query, values)
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Expedientes encontrados:")
                return "Expedientes encontrados:", expedientes
            else:
                print("No se encontraron expedientes para el año gravable especificado.")
                return "No se encontraron expedientes para el año gravable especificado.", None

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
            print(f"Error al buscar expedientes por año gravable: {e}")
            return "Error al buscar expedientes por año gravable", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def mostrar_expedientes(self):
        """
            Muestra todos los expedientes de la base de datos.

            Returns:
            - mensaje y expedientes: Mensaje de éxito o error de la consulta y una lista de todos los expedientes si la consulta fue exitosa.
            """
        try:
            self.connector = BDConnector()
            query = "SELECT id_expediente, id_contribuyente, id_auditor, id_proceso, id_prestamo, id_caja, estado, año_gravable FROM expediente"
            self.connector.execute_query(query)
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Muestra de expedientes exitosa")
                return "Muestra de expedientes exitosa", expedientes
            else:
                print(" contribuyentes.")
                return "No se encontraron datos de expedientes.", None

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
            print(f"Error al obtener datos de expedientes: {e}")
            return "Error al obtener datos de expedientes", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def obtener_ultimo_expediente(self):
        """
        Función obtener_ultimo_expediente:

        Descripción:
        Esta función obtiene el último expediente modificado o insertado en la tabla 'expediente', junto con otros 10 expedientes
        más recientes o iguales en términos de fecha de modificación.

        Argumentos:
        - No recibe argumentos adicionales. Utiliza la conexión a la base de datos establecida en el objeto 'self.connector'.

        Retorna:
        - Una tupla con un mensaje indicando el resultado de la operación ('Muestra de expedientes exitosa' o 'No se
          encontraron datos de expedientes') y los datos de los expedientes obtenidos de la base de datos. Si no se
          encontraron datos, los datos de los expedientes serán 'None'.
        """
        try:
            self.connector = BDConnector()
            query = """
                SELECT id_expediente, id_contribuyente, id_auditor, id_proceso, id_prestamo, id_caja, estado, año_gravable 
                FROM expediente 
                WHERE fecha_modificacion <= (
                    SELECT fecha_modificacion 
                    FROM expediente 
                    ORDER BY fecha_modificacion DESC 
                    LIMIT 1
                ) 
                ORDER BY fecha_modificacion DESC 
                LIMIT 11
            """
            self.connector.execute_query(query)
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Muestra de expedientes exitosa")
                return "Muestra de expedientes exitosa", expedientes
            else:
                print("No se encontraron datos de expedientes.")
                return "No se encontraron datos de expedientes.", None

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
            print(f"Error al obtener datos de expedientes: {e}")
            return "Error al obtener datos de expedientes", None
        finally:
            if self.connector:
                self.connector.close_connection()



consultas = ConsultasExpediente()
#result = modulo_consultas.buscar_por_id_expediente("i010")
#result = modulo_consultas.buscar_por_id_contribuyente("020"
#result = modulo_consultas.buscar_por_id_auditor("A025")
#result = modulo_consultas.buscar_por_id_proceso("1")
#result = modulo_consultas.buscar_expedientes_prestados()
#result = modulo_consultas.buscar_por_id_caja("o111")
#result = modulo_consultas.buscar_por_estado("activo")
#result = modulo_consultas.buscar_por_año_gravable("2019")
#result = modulo_consultas.mostrar_expedientes()
#result = modulo_consultas.obtener_ultimo_expediente()
#mensaje, resultados = modulo_consultas.buscar_y_verificar_expedientes(["700"],2)
#print(resultados["exp encontrados"])
#print(resultados["ids encontrados"])
#print(resultados["ids no_encontrados"])
#print(resultados["exp prestados"])
#print(resultados["exp disponibles"])
