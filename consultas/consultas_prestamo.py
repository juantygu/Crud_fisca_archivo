from data_base.db_connector import BDConnector
import mysql.connector
import re


class ConsultasPrestamo:
    def __init__(self):
        self.connector = None
        self.patron = None

    def buscar_por_fecha_entrega(self, fecha_inicio=None, fecha_fin=None):
        """
            Busca préstamos por un rango de fechas de entrega.

            Parameters:
            - fecha_inicio (str): Fecha de inicio del rango de búsqueda (en formato 'YYYY-MM-DD').
            - fecha_fin (str): Fecha de fin del rango de búsqueda (en formato 'YYYY-MM-DD').

            Returns:
            - tuple: Una tupla con los préstamos encontrados si los hay, o None si no se encontraron préstamos.
            """
        try:
            self.connector = BDConnector()

            # Validar el formato de la fecha de inicio si se proporciona
            if fecha_inicio:
                mensaje, formato_valido = self.validar_formato_fecha(fecha_inicio)
                if not formato_valido:
                    raise ValueError(mensaje)

            # Validar el formato de la fecha de fin si se proporciona
            if fecha_fin:
                mensaje, formato_valido = self.validar_formato_fecha(fecha_fin)
                if not formato_valido:
                    raise ValueError(mensaje)

            # Validar que la fecha de inicio no sea mayor que la fecha final
            if fecha_inicio and fecha_fin:
                if fecha_inicio > fecha_fin:
                    raise ValueError("La fecha de inicio no puede ser mayor que la fecha final.")

            # Consulta SQL para buscar los préstamos por rango de fechas
            query = "SELECT id_prestamo, fecha_entrega, fecha_devolucion, responsable, area FROM prestamo WHERE "
            values = ()

            if fecha_inicio and fecha_fin:
                query += "fecha_entrega >= %s AND (fecha_entrega <= %s OR fecha_entrega IS NULL)"
                values = (fecha_inicio, fecha_fin)
            elif fecha_inicio:
                query += "fecha_entrega = %s"
                values = (fecha_inicio,)

            self.connector.execute_query(query, values)
            resultados = self.connector.fetch_all()

            if resultados:
                print("Préstamos encontrados:")
                return "Préstamos encontrados:", resultados
            else:
                print("No se encontraron préstamos en el rango de fechas especificado.")
                return "No se encontraron préstamos en el rango de fechas especificado.", None

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return "Error de interfaz ", None
        except mysql.connector.DatabaseError as db_err:
            # Capturar el error específico de fecha incorrecta
            if db_err.errno == 1525:
                print(f"Error de la base de datos, no existe en el calendario: {db_err}")
                return "Fecha incorrecta , no existe en el calendario", None
            else:
                print(f"Error de la base de datos: {db_err}")
                return "Error de la base de datos", None
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return "Error de MySQL", None
        except ValueError as value_err:
            print(f"Error en los parámetros de entrada: {value_err}")
            return f"Error en los parámetros de entrada: {value_err}", None
        except Exception as e:
            print(f"Error al buscar préstamos por fecha de entrega: {e}")
            return "Error al buscar préstamos por fecha de entrega", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def buscar_por_fecha_devolucion(self, fecha_inicio=None, fecha_fin=None):
        """
        Busca préstamos por un rango de fechas de devolución.

        Parameters:
        - fecha_inicio (str): Fecha de inicio del rango de búsqueda (en formato 'YYYY-MM-DD').
        - fecha_fin (str): Fecha de fin del rango de búsqueda (en formato 'YYYY-MM-DD').

        Returns:
        - tuple: Una tupla con los préstamos encontrados si los hay, o None si no se encontraron préstamos.
        """
        try:
            self.connector = BDConnector()

            # Validar el formato de la fecha de inicio si se proporciona
            if fecha_inicio:
                mensaje, formato_valido = self.validar_formato_fecha(fecha_inicio)
                if not formato_valido:
                    raise ValueError(mensaje)

            # Validar el formato de la fecha de fin si se proporciona
            if fecha_fin:
                mensaje, formato_valido = self.validar_formato_fecha(fecha_fin)
                if not formato_valido:
                    raise ValueError(mensaje)

            # Validar que la fecha de inicio no sea mayor que la fecha final
            if fecha_inicio and fecha_fin:
                if fecha_inicio > fecha_fin:
                    raise ValueError("La fecha de inicio no puede ser mayor que la fecha final.")

            # Consulta SQL para buscar los préstamos por rango de fechas
            query = "SELECT id_prestamo, fecha_entrega, fecha_devolucion, responsable, area FROM prestamo WHERE "
            values = ()

            if fecha_inicio and fecha_fin:
                query += "fecha_devolucion >= %s AND (fecha_devolucion <= %s OR fecha_devolucion IS NULL)"
                values = (fecha_inicio, fecha_fin)
            elif fecha_inicio:
                query += "fecha_devolucion = %s"
                values = (fecha_inicio,)

            self.connector.execute_query(query, values)
            resultados = self.connector.fetch_all()

            if resultados:
                print("Préstamos encontrados:")
                return "Préstamos encontrados:", resultados
            else:
                print("No se encontraron préstamos en el rango de fechas de devolución especificado.")
                return "No se encontraron préstamos en el rango de fechas de devolución especificado.", None

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return "Error de interfaz ", None
        except mysql.connector.DatabaseError as db_err:
            # Capturar el error específico de fecha incorrecta
            if db_err.errno == 1525:
                print(f"Error de la base de datos, no existe en el calendario: {db_err}")
                return "Fecha incorrecta , no existe en el calendario", None
            else:
                print(f"Error de la base de datos: {db_err}")
                return "Error de la base de datos", None
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return "Error de MySQL", None
        except ValueError as value_err:
            print(f"Error en los parámetros de entrada: {value_err}")
            return f"Error en los parámetros de entrada: {value_err}", None
        except Exception as e:
            print(f"Error al buscar préstamos por fecha de entrega: {e}")
            return "Error al buscar préstamos por fecha de entrega", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def buscar_por_responsable_area(self, responsable=None, area=None):
        """
        Busca préstamos por responsable y área.

        Parameters:
        - responsable (str): Nombre del responsable.
        - area (str): Nombre del área.

        Returns:
        - tuple: Una tupla con los préstamos encontrados si los hay, o None si no se encontraron préstamos.
        """
        try:
            self.connector = BDConnector()
            #"SELECT * FROM prestamo WHERE responsable = %s AND area = %s"
            query = "SELECT id_prestamo, fecha_entrega, fecha_devolucion, responsable, area FROM prestamo WHERE "
            values = ()

            if responsable and area:
                query += "responsable = %s AND area = %s"
                values = (responsable, area)
            elif responsable:
                query += "responsable = %s"
                values = (responsable,)
            elif area:
                query += "area = %s"
                values = (area,)


            self.connector.execute_query(query, values)
            resultados = self.connector.fetch_all()

            if resultados:
                print("Préstamos encontrados:")
                return "Préstamos encontrados:", resultados
            else:
                print("No se encontraron préstamos para el responsable y área especificados.")
                return "No se encontraron préstamos para el responsable y área especificados.", None

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
            print(f"Error al buscar préstamos por responsable y área: {e}")
            return "Error al buscar préstamos por responsable y área", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def mostrar_prestamos(self, cantidad=None):
        """
        Trae todos los préstamos o los últimos n préstamos.

        Parameters:
        - cantidad (int): Cantidad de préstamos a traer. Si es None, se traen todos los préstamos.

        Returns:
        - tuple: Una tupla con los préstamos encontrados si los hay, o None si no se encontraron préstamos.
        """
        try:
            self.connector = BDConnector()

            query = "SELECT id_prestamo, fecha_entrega, fecha_devolucion, responsable, area FROM prestamo ORDER BY fecha_entrega DESC , id_prestamo DESC"

            # Agregar la cláusula LIMIT si se especifica la cantidad
            if cantidad:
                query += f" LIMIT {cantidad}"

            self.connector.execute_query(query)
            resultados = self.connector.fetch_all()

            if resultados:
                print("Préstamos encontrados:")
                return "Préstamos encontrados:", resultados
            else:
                print("No se encontraron préstamos.")
                return "No se encontraron préstamos.", None

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
            print(f"Error al traer préstamos: {e}")
            return f"Error al traer préstamos: {e}", None
        finally:
            if self.connector:
                self.connector.close_connection()

    def obtener_ultimo_prestamo(self):
        """
        Función obtener_ultimo_prestamo:

        Descripción:
        Obtiene el último préstamo modificado o insertado en la tabla 'prestamo' junto con otros 10 préstamos más recientes
        o iguales en términos de fecha de modificación.

        Argumentos:
        - No recibe argumentos adicionales. Utiliza la conexión a la base de datos establecida en el objeto 'self.connector'.

        Retorna:
        - Una tupla con un mensaje indicando el resultado de la operación ('Muestra de expedientes exitosa' o 'No se
          encontraron datos de expedientes') y los datos de los préstamos obtenidos de la base de datos. Si no se
          encontraron datos, los datos de los préstamos serán 'None'.
        """
        try:
            self.connector = BDConnector()
            query = """
                SELECT id_prestamo, fecha_entrega, fecha_devolucion, responsable, area 
                FROM prestamo 
                WHERE fecha_modificacion <= (
                    SELECT fecha_modificacion 
                    FROM prestamo 
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

    def validar_formato_fecha(self, fecha: str):
        """
        Valida el formato de una fecha en formato 'YYYY-MM-DD'.

        Parameters:
        - fecha (str): La fecha a validar.

        Returns:
        -
        """
        self.patron = re.compile(r'^(20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$')
        match = self.patron.match(fecha)

        if match:
            return "Formato de fecha válido", True
        else:
            if not re.match(r'^20\d{2}', fecha):
                return"El año debe empezar con '20' y tener cuatro dígitos", False
            elif not re.match(r'(0[1-9]|1[0-2])', fecha.split('-')[1]):
                return"El mes debe estar en el rango de '01' a '12'",False
            elif not re.match(r'(0[1-9]|[12]\d|3[01])', fecha.split('-')[2]):
                return "El día debe estar en el rango de '01' a '31'",False
            else:
                return "Formato de fecha inválido", False


#consulta = ConsultasPrestamo()
#result= consulta.buscar_por_fecha_entrega(fecha_inicio="2024-05-29",fecha_fin="2024-03-29")
#result= consulta.buscar_por_fecha_devolucion(fecha_inicio="2024-05-29",fecha_fin="2024-03-29")
#result= consulta.mostrar_prestamos()
#result = consulta.buscar_por_responsable_area(area="fiscalizacion")
#result= consulta.validar_formato_fecha("2020-02-31")
#result = consulta.obtener_ultimo_prestamo()
#print(result)

