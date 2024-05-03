from data_base.db_connector import BDConnector
import mysql.connector
import pandas as pd
from tabulate import tabulate
import time


class ConsultasCompuestas():
    def __init__(self):
        self.connector = None

    def buscar_expedientes_por_auditor(self, id_auditor=None, cedula=None, nombre_auditor=None):
        """
                Busca expedientes basados en el auditor especificado.

                Args:
                    id_auditor (int): ID del auditor a buscar.
                    cedula (str): Cédula del auditor a buscar.
                    nombre_auditor (str): Nombre del auditor a buscar.

                Returns:
                    tuple: Una tupla que contiene el mensaje de estado, los encabezados y los datos de los expedientes encontrados.
                """
        try:
            self.connector = BDConnector()
            query = "SELECT contribuyente.nombre_contribuyente , auditor.nombre_auditor, expediente.id_expediente," \
                    "expediente.id_contribuyente, expediente.id_auditor, expediente.id_proceso, expediente.id_caja," \
                    "expediente.id_prestamo, expediente.estado, expediente.año_gravable" \
                    " FROM expediente " \
                    " INNER JOIN contribuyente ON expediente.id_contribuyente = contribuyente.id_contribuyente" \
                    " INNER JOIN auditor ON expediente.id_auditor = auditor.id_auditor" \
                    " WHERE"

            conditions = []
            values = []

            # Agregar condiciones según los parámetros proporcionados
            if id_auditor:
                conditions.append(" auditor.id_auditor = %s")
                values.append(id_auditor)
            if cedula:
                conditions.append(" auditor.cedula = %s")
                values.append(cedula)
            if nombre_auditor:
                conditions.append(" auditor.nombre_auditor = %s")
                values.append(nombre_auditor)

            # Combinar las condiciones con el operador AND si hay más de una
            if len(conditions) > 1:
                query += " AND ".join(conditions)
            elif len(conditions) == 1:
                query += conditions[0]

            # Ejecutar la consulta
            self.connector.execute_query(query, values)

            # Obtener resultados y encabezados
            encabezados = [i[0] for i in self.connector.cursor.description]

            # Obtener resultados
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Muestra de expedientes exitosa")
                return "Muestra de expedientes exitosa", encabezados, expedientes
            else:
                print("No se encontraron datos de expedientes")
                return "No se encontraron datos de expedientes ", None, None

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return "Error de interfaz ", None, None
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return "Error de la base de datos", None, None
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return "Error de MySQL", None, None
        except Exception as e:
            print(f"Error al obtener datos del auditor: {e}")
            return "Error al obtener datos del auditor", None, None
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def buscar_expedientes_por_contribuyente(self, id_contribuyente=None, nombre_contribuyente=None, tipo=None):
        """
                Busca expedientes basados en el contribuyente especificado.

                Args:
                    id_contribuyente (int): ID del contribuyente a buscar.
                    nombre_contribuyente (str): Nombre del contribuyente a buscar.
                    tipo (str): Tipo del contribuyente a buscar.

                Returns:
                    tuple: Una tupla que contiene el mensaje de estado, los encabezados y los datos de los expedientes encontrados.
                """
        try:
            self.connector = BDConnector()
            query = "SELECT contribuyente.nombre_contribuyente, auditor.nombre_auditor,  expediente.id_expediente," \
                    "expediente.id_contribuyente, expediente.id_auditor, expediente.id_proceso, expediente.id_prestamo," \
                    " expediente.id_caja, expediente.estado, expediente.año_gravable" \
                    " FROM expediente" \
                    " INNER JOIN contribuyente ON expediente.id_contribuyente = contribuyente.id_contribuyente" \
                    " INNER JOIN auditor ON expediente.id_auditor = auditor.id_auditor" \
                    " WHERE"

            conditions = []
            values = []

            # Agregar condiciones según los parámetros proporcionados
            if id_contribuyente:
                conditions.append(" contribuyente.id_contribuyente = %s")
                values.append(id_contribuyente)
            if nombre_contribuyente:
                conditions.append(" contribuyente.nombre_contribuyente = %s")
                values.append(nombre_contribuyente)
            if tipo:
                conditions.append(" contribuyente.tipo = %s")
                values.append(tipo)

            # Combinar las condiciones con el operador AND si hay más de una
            if len(conditions) > 1:
                query += " AND ".join(conditions)
            elif len(conditions) == 1:
                query += conditions[0]


            # Ejecutar la consulta
            self.connector.execute_query(query, values)

            # Obtener resultados y encabezados
            encabezados = [i[0] for i in self.connector.cursor.description]

            # Obtener resultados
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Muestra de expedientes exitosa")
                return "Muestra de expedientes exitosa", encabezados, expedientes
            else:
                print("No se encontraron datos de expedientes")
                return "No se encontraron datos de expedientes ", None, None

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return "Error de interfaz ", None, None
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return "Error de la base de datos", None, None
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return "Error de MySQL", None, None
        except Exception as e:
            print(f"Error al obtener datos del contribuyente: {e}")
            return "Error al obtener datos del contribuyente", None, None
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def buscar_expedientes_por_proceso(self, id_proceso=None, nombre_proceso=None):
        """
                Busca expedientes basados en el proceso especificado.

                Args:
                    id_proceso (int): ID del proceso a buscar.
                    nombre_proceso (str): Nombre del proceso a buscar.

                Returns:
                    tuple: Una tupla que contiene el mensaje de estado, los encabezados y los datos de los expedientes encontrados.
                """
        try:
            self.connector = BDConnector()
            query = "SELECT contribuyente.nombre_contribuyente, auditor.nombre_auditor, procesos.nombre_proceso," \
                    " expediente.id_expediente, expediente.id_caja, expediente.estado, expediente.año_gravable" \
                    " FROM expediente" \
                    " INNER JOIN contribuyente ON expediente.id_contribuyente = contribuyente.id_contribuyente" \
                    " INNER JOIN auditor ON expediente.id_auditor = auditor.id_auditor"\
                    " INNER JOIN procesos ON expediente.id_proceso = procesos.id_proceso"\
                    " WHERE"

            conditions = []
            values = []

            # Agregar condiciones según los parámetros proporcionados
            if id_proceso:
                conditions.append(" expediente.id_proceso = %s")
                values.append(id_proceso)
            if nombre_proceso:
                conditions.append(" procesos.nombre_proceso = %s")
                values.append(nombre_proceso)

            # Combinar las condiciones con el operador AND si hay más de una
            if len(conditions) > 1:
                query += " AND ".join(conditions)
            elif len(conditions) == 1:
                query += conditions[0]

            # Ejecutar la consulta
            self.connector.execute_query(query, values)

            print(self.connector.cursor.description)
            # Obtener resultados y encabezados
            encabezados = [i[0] for i in self.connector.cursor.description]

            # Obtener resultados
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Muestra de expedientes exitosa")
                return "Muestra de expedientes exitosa",encabezados, expedientes
            else:
                print("No se encontraron datos de expedientes")
                return "No se encontraron datos de expedientes ", None, None

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return "Error de interfaz ", None, None
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return "Error de la base de datos",None,  None
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return "Error de MySQL",None,  None
        except Exception as e:
            print(f"Error al obtener datos del proceso: {e}")
            return "Error al obtener datos del proceso",None,  None
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def buscar_expedientes_por_estado(self, estado=None):
        """
        Busca expedientes basados en su estado.

        Args:
            estado (str): El estado del expediente a buscar.

        Returns:
            tuple: Una tupla que contiene un mensaje indicando si la búsqueda fue exitosa o no,
                   los encabezados de los resultados y los datos de los expedientes encontrados.
                   En caso de error, se devuelve None.

        """
        try:
            self.connector = BDConnector()
            query = "SELECT contribuyente.nombre_contribuyente, auditor.nombre_auditor, procesos.nombre_proceso," \
                    " expediente.id_expediente, expediente.id_caja, expediente.estado, expediente.año_gravable" \
                    " FROM expediente" \
                    " INNER JOIN contribuyente ON expediente.id_contribuyente = contribuyente.id_contribuyente" \
                    " INNER JOIN auditor ON expediente.id_auditor = auditor.id_auditor" \
                    " INNER JOIN procesos ON expediente.id_proceso = procesos.id_proceso" \
                    " WHERE expediente.estado = %s"

            values = (estado,)

            # Ejecutar la consulta
            self.connector.execute_query(query, values)

            # Obtener encabezados y datos de los resultados
            encabezados = [i[0] for i in self.connector.cursor.description]
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Búsqueda de expedientes por estado exitosa")
                return "Búsqueda de expedientes por estado exitosa", encabezados, expedientes
            else:
                print("No se encontraron expedientes con el estado especificado")
                return "No se encontraron expedientes con el estado especificado", None, None

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return "Error de interfaz ", None, None
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return "Error de la base de datos", None, None
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return "Error de MySQL", None, None
        except Exception as e:
            print(f"Error al buscar expedientes por estado: {e}")
            return "Error al buscar expedientes por estado", None, None
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def buscar_expedientes_por_año(self, año=None):
        """
        Busca expedientes basados en el año gravable.

        Args:
            año (int): El año gravable de los expedientes a buscar.

        Returns:
            tuple: Una tupla que contiene un mensaje indicando si la búsqueda fue exitosa o no,
                   los encabezados de los resultados y los datos de los expedientes encontrados.
                   En caso de error, se devuelve None.

        """
        try:
            self.connector = BDConnector()
            query = "SELECT contribuyente.nombre_contribuyente, auditor.nombre_auditor, procesos.nombre_proceso," \
                    " expediente.id_expediente, expediente.id_caja, expediente.estado, expediente.año_gravable" \
                    " FROM expediente" \
                    " INNER JOIN contribuyente ON expediente.id_contribuyente = contribuyente.id_contribuyente" \
                    " INNER JOIN auditor ON expediente.id_auditor = auditor.id_auditor" \
                    " INNER JOIN procesos ON expediente.id_proceso = procesos.id_proceso" \
                    " WHERE expediente.año_gravable = %s"

            values = (año,)

            # Ejecutar la consulta
            self.connector.execute_query(query, values)

            # Obtener encabezados y datos de los resultados
            encabezados = [i[0] for i in self.connector.cursor.description]
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Búsqueda de expedientes por año gravable exitosa")
                return "Búsqueda de expedientes por año gravable exitosa", encabezados, expedientes
            else:
                print("No se encontraron expedientes para el año gravable especificado")
                return "No se encontraron expedientes para el año gravable especificado", None, None

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return "Error de interfaz ", None, None
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return "Error de la base de datos", None, None
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return "Error de MySQL", None, None
        except Exception as e:
            print(f"Error al buscar expedientes por año gravable: {e}")
            return "Error al buscar expedientes por año gravable", None, None
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def buscar_expedientes_filtrados(self, filtros):
        """
        Busca expedientes filtrados según los criterios especificados en los filtros.

        Args:
            filtros (dict): Un diccionario que contiene los filtros a aplicar.
                            Los filtros pueden incluir:
                            - 'nombre_auditor': Nombre del auditor.
                            - 'id_contribuyente': ID del contribuyente.
                            - 'nombre_contribuyente': Nombre del contribuyente.
                            - 'tipo_contribuyente': Tipo del contribuyente.
                            - 'nombre_proceso': Nombre del proceso.
                            - 'estado': Estado del expediente.
                            - 'año_gravable': Año gravable del expediente.

        Returns:
            tuple: Una tupla que contiene el mensaje de estado, los encabezados y los datos de los expedientes encontrados.
                   Si se encontraron expedientes, el mensaje de estado será "Muestra de expedientes exitosa",
                   de lo contrario, será "No se encontraron datos de expedientes".
                   Los encabezados son los nombres de las columnas de la tabla de expedientes.
                   Los datos de los expedientes son una lista de tuplas, donde cada tupla representa una fila de datos.
                   En caso de error, se devuelve None para todos los valores de retorno.
        """
        try:
            self.connector = BDConnector()
            query = "SELECT auditor.nombre_auditor, contribuyente.nombre_contribuyente, expediente.id_contribuyente, " \
                    "contribuyente.tipo,procesos.nombre_proceso, expediente.id_expediente, expediente.id_prestamo, " \
                    "expediente.id_caja, expediente.estado, expediente.año_gravable " \
                    "FROM expediente " \
                    "INNER JOIN auditor ON expediente.id_auditor = auditor.id_auditor " \
                    "INNER JOIN contribuyente ON expediente.id_contribuyente = contribuyente.id_contribuyente " \
                    "INNER JOIN procesos ON expediente.id_proceso = procesos.id_proceso"

            conditions = []
            values = []

            # Construir las condiciones de filtro basadas en los filtros proporcionados
            if 'nombre_auditor' in filtros and filtros['nombre_auditor']:
                conditions.append("auditor.nombre_auditor = %s")
                values.append(filtros['nombre_auditor'])
            if 'id_contribuyente' in filtros and filtros['id_contribuyente']:
                conditions.append("expediente.id_contribuyente = %s")
                values.append(filtros['id_contribuyente'])
            if 'nombre_contribuyente' in filtros and filtros['nombre_contribuyente']:
                conditions.append("contribuyente.nombre_contribuyente = %s")
                values.append(filtros['nombre_contribuyente'])
            if 'tipo_contribuyente' in filtros and filtros['tipo_contribuyente']:
                conditions.append("contribuyente.tipo = %s")
                values.append(filtros['tipo_contribuyente'])
            if 'nombre_proceso' in filtros and filtros['nombre_proceso']:
                conditions.append("procesos.nombre_proceso = %s")
                values.append(filtros['nombre_proceso'])
            if 'estado' in filtros and filtros['estado']:
                conditions.append("expediente.estado = %s")
                values.append(filtros['estado'])
            if 'año_gravable' in filtros and filtros['año_gravable']:
                conditions.append("expediente.año_gravable = %s")
                values.append(filtros['año_gravable'])

            # Combinar las condiciones con el operador AND si hay más de una
            if len(conditions) > 1:
                query += " WHERE " + " AND ".join(conditions)
            elif len(conditions) == 1:
                query += " WHERE " + conditions[0]

            # Ejecutar la consulta
            self.connector.execute_query(query, values)

            print (query)

            # Obtener resultados y encabezados
            encabezados = [i[0] for i in self.connector.cursor.description]

            # Obtener los resultados
            expedientes = self.connector.fetch_all()

            if expedientes:
                print("Muestra de expedientes exitosa")
                return "Muestra de expedientes exitosa", encabezados, expedientes
            else:
                print("No se encontraron datos de expedientes")
                return "No se encontraron datos de expedientes ", None, None

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return "Error de interfaz ", None, None
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return "Error de la base de datos", None, None
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return "Error de MySQL", None, None
        except Exception as e:
            print(f"Error al obtener datos del auditor: {e}")
            return "Error al obtener datos del auditor", None, None
        finally:
            if self.connector:
                self.connector.close_connection()

    def imprimir_resultados(self, resultado):
        """
                Imprime los resultados de la consulta en forma tabular.

                Args:
                    resultado (tuple): Una tupla que contiene el mensaje de estado, los encabezados y los datos de los expedientes encontrados.
                """
        if resultado:
            encabezados, datos = resultado[1], resultado[2]
            if encabezados is not None:
                print(tabulate(datos, headers=encabezados, tablefmt="pretty"))
            else:
                print("No se encontraron datos de expedientes")
        else:
            print("Resultado vacío")



consulta = ConsultasCompuestas()

# Inicia el temporizador
start_time = time.time()

#result = consulta.buscar_expedientes_por_auditor(nombre_auditor="luis",id_auditor="A001")
#result = consulta.buscar_expedientes_por_contribuyente(id_contribuyente="004", nombre_contribuyente="vcd s.a.s")
#result = consulta.buscar_expedientes_por_proceso(nombre_proceso="omisos")
#result = consulta.buscar_expedientes_por_estado(estado="activo")
#result = consulta.buscar_expedientes_por_año(2018)

#filtros = {
    #'nombre_auditor': 'luis',
    #'id_contribuyente': '004',
    #'nombre_contribuyente': 'vcd s.a.s',
    #'tipo_contribuyente': 'juridico',
    #'nombre_proceso': 'inexactos',
    #'estado': 'auto archivo',
    #'año_gravable': 2019
#}
#filtross = {'nombre_auditor': 'jorge'}
#result = consulta.buscar_expedientes_filtrados(filtross)
#print(result)

# Detiene el temporizador y calcula el tiempo transcurrido
#elapsed_time = time.time() - start_time

#consulta.imprimir_resultados(result)

# Imprime el tiempo transcurrido
#print("Tiempo transcurrido:", elapsed_time, "segundos")
