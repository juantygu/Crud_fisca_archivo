from data_base.db_connector import BDConnector
from entidades.contribuyente import Contribuyente
from entidades.auditor import Auditor
from entidades.proceso import Proceso
import mysql.connector


class Expediente:

    def __init__(self):
        self.connector = None
        self.contribuyente = Contribuyente()
        self.auditor = Auditor()
        self.proceso = Proceso()

    def insertar_expediente(self,id_expediente, id_contribuyente, id_auditor, id_proceso, id_caja, estado, anos_gravable: list):
        expedientes_insertados = []  # Lista para almacenar los expedientes insertados exitosamente
        # Verificar si hay valores duplicados en la lista
        if len(anos_gravable) != len(set(anos_gravable)):
            print("Error: La lista de años gravables contiene valores duplicados.")
            return "La lista de años gravables contiene valores duplicados.", False

        # Verificar que la lista anos_gravable no tenga más de 5 elementos
        if len(anos_gravable) > 5:
            print("Error: La lista de años gravables no puede tener más de 5 elementos.")
            return "La lista de años gravables no puede tener más de 5 elementos.", False
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()

            # Iniciar la transacción
            self.connector.start_transaction()

            # verificar existencia del expediente
            mensaje_expediente, verificacion_expediente = self.verificar_expedientes_existen(id_expediente, connection=self.connector)
            if verificacion_expediente:
                # el expediente existe , por lo tanto no se puede ingresar ya que ya tiene un proceso , si se desea agregar otro año gravable
                # debera ser por otro metodo agregar año agravable a  expediente existente " tener en cuanta que maximo son 5 años gravables por expediente
                print(mensaje_expediente)

                # Verificar cantidad de años gravables
                mensaje_años, verificacion_años = self.contar_anos_gravables(id_expediente)
                if verificacion_años: # el expediente tiene menos de 5 años gravables
                    print(mensaje_años)
                    print(f"No se puede ingresar ya que tiene  un proceso.{mensaje_años}, si desea agregar otro año debera ser por otro metodo")
                    return f"No se puede ingresar ya que tiene  un proceso.{mensaje_años} , si desea agregar otro año debera ser por otro metodo", False
                else: # el expediente tiene mas de 5 años gravables
                    print(mensaje_años)
                    print(f"No se puede ingresar ya que tiene  un proceso, en los años {mensaje_años}")
                    return f"No se puede ingresar ya que tiene  un proceso, en los años {mensaje_años}", False

            print("puede continuar con la inserción")

            # Verificar si el contribuyente existe , las 3 verificacion usan la misma conexion de base de datos
            mensaje_contribuyente, verificacion_contribuyente = self.contribuyente.verificar_contribuyente_existe(id_contribuyente, connection=self.connector)
            if not verificacion_contribuyente:
                # el contribuyente no existe
                print(mensaje_contribuyente)
                return mensaje_contribuyente, False
            # el contribuyente existe
            print(mensaje_contribuyente,verificacion_contribuyente)

            # verificar si el auditor existe
            mensaje_auditor, verificacion_auditor = self.auditor.verificar_auditor_existe(id_auditor, connection=self.connector)
            if not verificacion_auditor:
                # el auditor no existe
                print(mensaje_auditor)
                return mensaje_auditor, False
            # el auditor existe
            print(mensaje_auditor)

            # verificar si el proceso existe
            mensaje_proceso, verificacion_proceso = self.proceso.verificar_proceso_existe(id_proceso, connection=self.connector)
            if not verificacion_proceso:
                # el proceso no existe
                print(mensaje_proceso)
                return mensaje_proceso, False
            # el proceso existe
            print(mensaje_proceso, verificacion_proceso)


            # Consulta SQL para la inserción
            query = "INSERT INTO expediente ( id_expediente,id_contribuyente, id_auditor," \
                    "id_proceso,id_caja, estado,año_gravable) " \
                    "VALUES ( %s, %s, %s, %s, %s, %s, %s)"

            rows_affected = 0
            for ano_gravable in anos_gravable:
                # Parámetros para la consulta
                values = (id_expediente, id_contribuyente, id_auditor,id_proceso,id_caja,estado,ano_gravable)
                # Ejecutar la consulta
                self.connector.execute_query(query, values)
                rows_affected += self.connector.cursor.rowcount  # Obtener la cantidad de filas afectadas
                # Si la inserción se realizó correctamente, agregar los datos a la lista
                expedientes_insertados.append(values)

            # Confirmar la transacción
            self.connector.connection.commit()
            # Imprimir los expedientes insertados ordenadamente
            print("Expedientes insertados exitosamente:")
            for exp in expedientes_insertados:
                print(exp)

            # verificar si se hizo completa la insercion
            if rows_affected == len(anos_gravable):
                # las filas afectadas son iguales al numero de años gravables
                print(f"Inserción exitosa en la tabla expediente. se insertaron {rows_affected} expedientes"
                      f"en los años gravables  {anos_gravable}")
                return f"Inserción exitosa en la tabla expediente. se insertaron {rows_affected} expedientes \n en los años gravables  {anos_gravable}", True
            else:
                print("no se pudo hacer la insercion")
                self.connector.connection.rollback()
                return "no se pudo hacer la insercion",False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            self.connector.connection.rollback()
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla expediente.")
                self.connector.connection.rollback()
                return "ID duplicado en la tabla expediente.", False
            else:
                # Si es otro tipo de error MySQL, podrías lanzar la excepción nuevamente si lo deseas
                print(f"Error de MySQL: {mysql_err}")
                self.connector.connection.rollback()
                return f"Error de MySQL: {mysql_err}", False
        except Exception as e:
            print(f"Error al insertar en la tabla expediente: {e}")
            self.connector.connection.rollback()
            return f"Error al insertar en la tabla expediente: {e}", False
        finally:
            if self.connector:
                self.connector.close_connection()

    def agregar_ano_gravable(self, id_expediente, id_contribuyente, id_auditor, id_proceso, id_caja, estado, nuevo_ano_gravable, connection=None):
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection

            # Verificar si el expediente existe
            mensaje_expediente, verificacion_expediente = self.verificar_expedientes_existen(id_expediente,connection=self.connector)
            if not verificacion_expediente:
                # el expediente no existe
                print(mensaje_expediente)
                return mensaje_expediente, False
            print(mensaje_expediente)

            # verificar si el expediente esta prestamo , como logica el expediente no puede ser modificado
            mensaje_en_prestamo, verificacion_en_prestamo = self.verificar_expedientes_prestados(id_expediente,connection=self.connector)
            if verificacion_en_prestamo:
                # el expediente esta prestado
                print(mensaje_en_prestamo)
                return mensaje_en_prestamo, False
            print(mensaje_en_prestamo, verificacion_en_prestamo)

            # Verificar si el expediente tiene menos de 5 años gravables
            mensaje_años, verificacion_años = self.contar_anos_gravables(id_expediente,connection=self.connector)
            if not verificacion_años:
                # el expediente tiene mas de 5 años gravables
                print(mensaje_años)
                return mensaje_años, False
            print(mensaje_años)

            # Verificar si la combinación de id_expediente y año_gravable ya existe
            mensaje_combinacion, verificacion_combinacion = self.verificar_combinacion_existe(id_expediente,nuevo_ano_gravable,connection=self.connector)
            if verificacion_combinacion:
                # la combinacion de expediente y año existen
                print(mensaje_combinacion)
                return mensaje_combinacion, False
            print(mensaje_combinacion)

            # Verificar si el contribuyente existe
            mensaje_contribuyente, verificacion_contribuyente = self.contribuyente.verificar_contribuyente_existe(id_contribuyente, connection=self.connector)
            if not verificacion_contribuyente:
                # el contribuyente no existe
                print(mensaje_contribuyente)
                return mensaje_contribuyente, False
            # el contribuyente existe
            print(mensaje_contribuyente)

            # verificar si el auditor existe
            mensaje_auditor, verificacion_auditor = self.auditor.verificar_auditor_existe(id_auditor,connection=self.connector)
            if not verificacion_auditor:
                # el auditor no existe
                print(mensaje_auditor)
                return mensaje_auditor, False
            # el auditor existe
            print(mensaje_auditor)

            # verificar si el proceso existe
            mensaje_proceso, verificacion_proceso = self.proceso.verificar_proceso_existe(id_proceso,connection=self.connector)
            if not verificacion_proceso:
                # el proceso no existe
                print(mensaje_proceso)
                return mensaje_proceso, False
            # el proceso existe
            print(mensaje_proceso, verificacion_proceso)

            # Consulta SQL para la inserción
            query = "INSERT INTO expediente ( id_expediente,id_contribuyente, id_auditor," \
                    "id_proceso,id_caja, estado,año_gravable) " \
                    "VALUES ( %s, %s, %s, %s, %s, %s, %s)"

            values = (id_expediente, id_contribuyente, id_auditor, id_proceso, id_caja, estado, nuevo_ano_gravable)
            self.connector.execute_query(query, values)

            # Confirmar la transacción
            self.connector.connection.commit()

            # Verificar si se insertó el registro
            if self.connector.cursor.rowcount > 0:
                print(f"Año gravable {nuevo_ano_gravable} agregado al expediente {id_expediente} exitosamente.")
                return f"Año gravable {nuevo_ano_gravable} agregado al expediente {id_expediente} exitosamente.", True
            else:
                print("no se inserto el nuevo año gravable")
                return "no se inserto el nuevo año gravable", False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla expediente.")
                return "ID duplicado en la tabla expediente.", False
            else:
                # Si es otro tipo de error MySQL, podrías lanzar la excepción nuevamente si lo deseas
                print(f"Error de MySQL: {mysql_err}")
                return f"Error de MySQL: {mysql_err}", False
        except Exception as e:
            print(f"Error al agregar año gravable al expediente: {e}")
            return f"Error al agregar año gravable al expediente: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def eliminar_expediente_por_id(self,id_expediente, connection=None):
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection
        # Consulta SQL para la eliminacion
            query = "DELETE FROM expediente WHERE id_expediente = %s"
            values = (id_expediente,)
        # Ejecutar la consulta
            self.connector.execute_query(query, values)
        # Confirmar los cambios
            self.connector.connection.commit()
            # Verificar si se eliminó algún registro
            if self.connector.cursor.rowcount > 0:
                print("Eliminación exitosa en la tabla expediente.")
                return "Eliminación exitosa en la tabla expediente.", True
            else:
                print(f"No se encontró ningún registro con id_expediente = {id_expediente}.")
                return f"No se encontró ningún registro con id_expediente = {id_expediente}.", False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error al modificar en la tabla expediente: {e}")
            return f"Error al modificar en la tabla expediente: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def eliminar_expediente_por_ano(self,id_expediente, ano_gravable):
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
        # Consulta SQL para la eliminacion
            query = "DELETE FROM expediente WHERE id_expediente = %s AND año_gravable = %s"
            values = (id_expediente, ano_gravable)
        # Ejecutar la consulta
            self.connector.execute_query(query, values)
        # Confirmar los cambios
            self.connector.connection.commit()
            # Verificar si se eliminó algún registro
            if self.connector.cursor.rowcount > 0:
                print("Eliminación exitosa en la tabla expediente.")
                return "Eliminación exitosa en la tabla expediente.", True
            else:
                print(f"No se encontró ningún registro con id_expediente = {id_expediente} y año gravable {ano_gravable}.")
                return print(f"No se encontró ningún registro con id_expediente = {id_expediente} y año gravable {ano_gravable}."), False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error al modificar en la tabla expediente: {e}")
            return f"Error al modificar en la tabla expediente: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def contar_anos_gravables(self, id_expediente, connection=None):
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection
            # Consulta SQL para contar los años gravables asociados a un expediente
            query = "SELECT año_gravable FROM expediente WHERE id_expediente = %s"
            values = (id_expediente,)
            self.connector.execute_query(query, values)
            result = self.connector.fetch_all()
            print(result)
            anos_gravables =[año[0]for año in result]
            cantidad_anos = len(anos_gravables)
            """
            anos_gravables = []
            for año in result:
                valor = año[0]
                anos_gravables.append(valor)
            """
            print(anos_gravables)
            if cantidad_anos > 5:
                print(f"el expediente tiene mas de 5 años gravables")
                return f"el expediente tiene mas de 5 años gravables", False
            else:
                print(f"el expediente = {id_expediente} tiene {cantidad_anos} años gravables. ({anos_gravables})")
                return f"el expediente = {id_expediente} tiene {cantidad_anos} años gravables. ({anos_gravables})", True

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error al contar años gravables: {e}")
            return f"Error al contar años gravables: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def modificar_datos_expediente(self,id_expediente,ano_gravable,id_nuevo_expediente,id_nuevo_contribuyente, id_nuevo_auditor,id_nuevo_proceso,id_nueva_caja,nuevo_estado, nuevo_ano_gravable):
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()

            # Verificar si la combinación de id_expediente y  nuevo año_gravable ya existe
            mensaje_combinacion, verificacion_combinacion = self.verificar_combinacion_existe(id_expediente,nuevo_ano_gravable,connection=self.connector)
            if verificacion_combinacion:
                # la combinacion de expediente y año existen
                print(mensaje_combinacion)
                return mensaje_combinacion, False
            print(mensaje_combinacion)

            # verificar si el expediente esta prestamo , como logica el expediente no puede ser modificado si esta prestado por seguridad
            mensaje_en_prestamo, verificacion_en_prestamo = self.verificar_expedientes_prestados(id_expediente, connection=self.connector)
            if verificacion_en_prestamo:
                # algun expediente esta prestado
                print(mensaje_en_prestamo)
                return mensaje_en_prestamo, False
            print(mensaje_en_prestamo, verificacion_en_prestamo)

            # Verificar si el id_nuevo_contribuyente existe , las 3 verificacion usan la misma conexion de base de datos
            mensaje_contribuyente, verificacion_contribuyente = self.contribuyente.verificar_contribuyente_existe(id_nuevo_contribuyente, connection=self.connector)
            if not verificacion_contribuyente:
                # el contribuyente no existe
                print(mensaje_contribuyente)
                return mensaje_contribuyente, False
            # el contribuyente existe
            print(mensaje_contribuyente, verificacion_contribuyente)

            # verificar si el auditor existe
            mensaje_auditor, verificacion_auditor = self.auditor.verificar_auditor_existe(id_nuevo_auditor,connection=self.connector)
            if not verificacion_auditor:
                # el auditor no existe
                print(mensaje_auditor)
                return mensaje_auditor, False
            # el auditor existe
            print(mensaje_auditor)

            # verificar si el proceso existe
            mensaje_proceso, verificacion_proceso = self.proceso.verificar_proceso_existe(id_nuevo_proceso,connection=self.connector)
            if not verificacion_proceso:
                # el proceso no existe
                print(mensaje_proceso)
                return mensaje_proceso, False
            # el proceso existe
            print(mensaje_proceso, verificacion_proceso)

            # Consulta SQL para la modificación
            query = "UPDATE expediente SET id_expediente=%s, id_contribuyente = %s,id_auditor = %s,id_proceso = %s,id_caja = %s" \
                    ",estado = %s, año_gravable = %s  WHERE id_expediente = %s AND año_gravable =%s"
            values = (id_nuevo_expediente,id_nuevo_contribuyente, id_nuevo_auditor, id_nuevo_proceso, id_nueva_caja, nuevo_estado, nuevo_ano_gravable, id_expediente, ano_gravable)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()
            if self.connector.cursor.rowcount > 0:
                print(self.connector.cursor.rowcount, "Modificación exitosa del expediente.")
                return "Modificación exitosa del expediente.", True
            else:
                print(self.connector.cursor.rowcount, "Modificación erronea , revise id_expediente y año_gravable.")
                return "Modificación erronea , revise id_expediente y año_gravable." , False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla expediente.")
                return "ID duplicado en la tabla expediente.", False
            else:
                # Si es otro tipo de error MySQL, podrías lanzar la excepción nuevamente si lo deseas
                print(f"Error de MySQL: {mysql_err}")
                return f"Error de MySQL: {mysql_err}", False
        except Exception as e:
            print(f"Error al insertar en la tabla expediente: {e}")
            return f"Error al insertar en la tabla expediente: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def modificar_id_expediente(self,id_viejo_expediente,id_nuevo_expediente):
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
            # Verificar si el expediente existe antes de intentar la modificación
            mensaje_expediente , verificacion_expediente = self.verificar_expedientes_existen(id_nuevo_expediente,connection=self.connector)
            if verificacion_expediente:
                # el expediente existe
                print(f"el expediente ={id_nuevo_expediente} ya existe")
                return f"el expediente ={id_nuevo_expediente} ya existe",False

            # Consulta SQL para la modificación
            query = "UPDATE expediente SET  id_expediente = %s WHERE id_expediente = %s"
            values = (id_nuevo_expediente,id_viejo_expediente)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()

            if self.connector.cursor.rowcount > 0:
                print(f"Modificación exitosa del id_expediente. se modifico el id={id_viejo_expediente} por id= {id_nuevo_expediente}")
                return f"Modificación exitosa del id_expediente. se modifico el id={id_viejo_expediente} por id= {id_nuevo_expediente}", True
            else:
                print("Modificación erronea del id_expediente.")
                return "Modificación erronea del id_expediente.", False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla id_expediente.")
                return "ID duplicado en la tabla id_expediente.", False
            else:
                # Si es otro tipo de error MySQL, podrías lanzar la excepción nuevamente si lo deseas
                print(f"Error de MySQL: {mysql_err}")
                return f"Error de MySQL: {mysql_err}", False
        except Exception as e:
            print(f"Error al insertar en la tabla expediente: {e}")
            return f"Error al insertar en la tabla expediente: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def cambiar_estado_expediente(self, id_expediente, anos_gravables, nuevo_estado, connection=None):
        try:
            # Verificar si hay valores duplicados en la lista
            if len(anos_gravables) != len(set(anos_gravables)):
                print("Error: La lista de años gravables contiene valores duplicados.")
                return "La lista de años gravables contiene valores duplicados.", False

            # Crear una instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection

            # verificar existencia del expediente
            mensaje_expediente, verificacion_expediente = self.verificar_expedientes_existen(id_expediente,connection=self.connector)
            if not verificacion_expediente:
                print("el expediente no existe")
                return "el expediente no existe", False
             # Verificar si anos_gravables es una lista
            if isinstance(anos_gravables, list):
                # Si es una lista, crear placeholders para cada año gravable
                placeholders = ",".join(["%s"] * len(anos_gravables))
                # Consulta SQL para actualizar el estado para cada año gravable en la lista
                query = f"UPDATE expediente SET estado = %s WHERE id_expediente = %s AND año_gravable IN ({placeholders})"
                # Valores para la consulta
                # Construir values como una tupla
                values = tuple([nuevo_estado, id_expediente] + anos_gravables)
            else:
                # Si no es una lista, tratarlo como un solo año gravable
                query = "UPDATE expediente SET estado = %s WHERE id_expediente = %s AND año_gravable = %s"
                values = (nuevo_estado, id_expediente, anos_gravables)

            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()

            if self.connector.cursor.rowcount > 0:
                print(self.connector.cursor.rowcount, "Expediente(s) actualizado(s) exitosamente.")
                return "Expediente(s) actualizado(s) exitosamente.", True
            else:
                print("No se encontró ningún expediente para actualizar, Verifica los años.")
                return "No se encontró ningún expediente para actualizar, Verifica los años.", False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error al cambiar estado del expediente: {e}")
            return f"Error al cambiar estado del expediente: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def verificar_expedientes_existen(self, id_expedientes: list, connection=None):
        """
        Verifica la existencia de expedientes en la base de datos.

        Parameters:
        - id_expedientes : Lista o un id_expediente a verificar
        - connection (BDConnector): La conexión a la base de datos. Si es None, se crea una nueva conexión.

        Returns:
        - mensaje si existen o no los expedientes
        - bool: True si todos los expedientes existen, False si al menos uno no existe.

        explicacion de expedientes_encontrados = [row[0] for row in result]
        expedientes_encontrados = []  # Creamos una lista vacía para almacenar los expedientes encontrados
        for row in result:
            expediente = row[0]  # Accedemos al primer elemento de la tupla (la posición 0)
            expedientes_encontrados.append(expediente)  # Agregamos el expediente a la lista

        La operación set(id_expedientes) - set(expedientes_encontrados) realiza una diferencia de conjuntos.
        En este caso, id_expedientes y expedientes_encontrados son listas de strings, pero al convertirlas a
        conjuntos usando set(), se están tratando como conjuntos de elementos únicos.

        La resta de conjuntos (-) devuelve un nuevo conjunto que contiene todos los elementos que están en el
        primer conjunto pero no en el segundo. En este contexto, expedientes_no_encontrados contendrá los
        elementos que están en id_expedientes pero no están en expedientes_encontrados.
        """
        try:
            # Si id_expedientes es una cadena, conviértela en una lista con un solo elemento
            if not isinstance(id_expedientes, list):
                id_expedientes = [id_expedientes]

            # Verificar si hay valores duplicados en la lista
            if len(id_expedientes) != len(set(id_expedientes)):
                print("Error: La lista de ID de expedientes contiene valores duplicados.")
                return "La lista de ID de expedientes contiene valores duplicados.", False
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection

            # Consulta SQL para verificar la existencia de expedientes
            placeholders = ",".join(["%s"] * len(id_expedientes))
            query = f"SELECT DISTINCT id_expediente FROM expediente WHERE id_expediente IN ({placeholders})"
            # Parámetros para la consulta
            values = tuple(id_expedientes)
            self.connector.execute_query(query, values)
            result = self.connector.fetch_all() #  result = [('o005',), ('o009',)] ejemplo
            if result:
                #print(f"expedientes a vincular ={id_expedientes}")
                print(result)
                expedientes_encontrados = [row[0] for row in result] #itera sobre result para obtener ['o005', 'o009']
                print(f"expedientes encontrados = {expedientes_encontrados}, id_expedientes {id_expedientes}")

                if set(expedientes_encontrados) == set(id_expedientes):
                    print("Todos los expedientes existen en la base de datos.")
                    return "Todos los expedientes existen en la base de datos.", True
                else:
                    expedientes_no_encontrados = set(id_expedientes) - set(expedientes_encontrados)
                    print(f" uno o varios expeidentes no existen, Expedientes no encontrados: {expedientes_no_encontrados}")
                    return f"uno o varios expeidentes no existen,Expedientes no encontrados: {expedientes_no_encontrados}", False
            else:
                print("no existen los expedientes")
                return "no existen los expedientes", False

        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error en la verificación de expedientes: {e}")
            return f"Error en la verificación de expedientes: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()
                print("conexion cerrada")

    def verificar_expedientes_prestados(self, id_expedientes, connection=None):
        """
        Verifica el estado de préstamo de los expedientes de la lista.

        Parameters:
        - id_expedientes : puede ser una lista o un string , igula dentro la funcion convierte a una lista
        - connection (BDConnector): Conexión a la base de datos (opcional).

        Returns:
        - mensaje y booleano ( si es True todos los expedientes estas disponibles para prestamo )
        (si es False muestra los expedientes que estan prestados)
        """
        # Si id_expedientes es una cadena, conviértela en una lista con un solo elemento
        if not isinstance(id_expedientes, list):
            id_expedientes = [id_expedientes]

        # Verificar si hay valores duplicados en la lista
        if len(id_expedientes) != len(set(id_expedientes)):
            print("Error: La lista de ID de expedientes contiene valores duplicados.")
            return "La lista de ID de expedientes contiene valores duplicados.", False
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection

            # Consulta SQL para verificar el estado de préstamo de los expedientes
            placeholders = ",".join(["%s"] * len(id_expedientes))
            query = f"SELECT id_expediente, id_prestamo FROM expediente WHERE id_expediente IN ({placeholders})"
            # Parámetros para la consulta
            values = tuple(id_expedientes)
            self.connector.execute_query(query, values)
            result = self.connector.fetch_all()
            print(result)
            resultado = set(result)
            print(resultado)
            expedientes_prestados = {id_exp for id_exp, id_prestamo in resultado if id_prestamo is not None}
            """ 
            explicacion set comprehension
            {id_exp for id_exp, id_prestamo in resultado if id_prestamo is not None}
            {expresion for elemento in iterable if condicion}
            
            forma convencional
            expedientes_prestados = set()
            for id_exp, id_prestamo in resultado:
                if id_prestamo is not None:
                    expedientes_prestados.add(id_exp)
            """
            todos_expedientes = set(id_expedientes)
            expedientes_no_prestados = todos_expedientes - expedientes_prestados
            print(f"expedientes prestados={expedientes_prestados}")
            print(f"expedientes no prestados={expedientes_no_prestados}")

            if expedientes_prestados and not expedientes_no_prestados: # todos los expedientes prestados
                print(f"los siguientes expedientes estan prestados {expedientes_prestados}")
                return f"los siguientes expedientes estan prestados {expedientes_prestados}", True
            elif expedientes_prestados and expedientes_no_prestados: # algun expediente esta prestado
                print(f"expedientes disponibles {expedientes_no_prestados} , expedientes prestados {expedientes_prestados}")
                return f"expedientes disponibles {expedientes_no_prestados}, expedientes prestados {expedientes_prestados}", True
            elif expedientes_no_prestados and not expedientes_prestados:
                print(f"los siguientes expedientes estan disponibles {expedientes_no_prestados}")
                return f"los siguientes expedientes estan disponibles {expedientes_no_prestados}", False


        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error al verificar expedientes prestados: {e}")
            return f"Error al verificar expedientes prestados: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def verificar_combinacion_existe(self, id_expediente, nuevo_ano_gravable, connection=None):
        """
        Verifica si la combinación de id_expediente y año_gravable ya existe en la base de datos.

        Parameters:
        - id_expediente : ID del expediente a verificar.
        - nuevo_ano_gravable : Año gravable a verificar.

        Returns:
        - mensaje y booleano: True si la combinación ya existe, False si no existe.
        """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection

            # Consulta SQL para verificar la existencia de la combinación
            query = "SELECT COUNT(*) FROM expediente WHERE id_expediente = %s AND año_gravable = %s"
            values = (id_expediente, nuevo_ano_gravable)
            self.connector.execute_query(query, values)
            resultado = self.connector.fetch_one()

            if resultado[0] > 0:
                mensaje = f"La combinación de id_expediente {id_expediente} y nuevo_año_gravable {nuevo_ano_gravable} ya existe."
                print(mensaje)
                return mensaje, True
            else:
                mensaje = f"La combinación de id_expediente {id_expediente} y nuevo_año_gravable {nuevo_ano_gravable} no existe."
                print(mensaje)
                return mensaje, False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.Error as mysql_err:
            print(f"Error de MySQL: {mysql_err}")
            return f"Error de MySQL: {mysql_err}", False
        except Exception as e:
            print(f"Error al verificar la combinación: {e}")
            return f"Error al verificar la combinación: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()
                print("conexion cerrada")




expediente = Expediente()
#expediente.insertar_expediente("o0199", "006", "A005", "3", "o10", "activo", [2021,2022])
#expediente.agregar_ano_gravable("i010", "006", "A003", "3", "o10", "activo", 2022)
#expediente.eliminar_expediente_por_ano("i010", "2022")
#expediente.eliminar_expediente_por_id("o015")
#expediente.modificar_datos_expediente("i011", 2023, "i011", "007", "A003", "2", "o11", "auto archivo", 2022)
#expediente.modificar_id_expediente("o010","o011")
#expediente.verificar_expedientes_existen(["i009"])
#expediente.verificar_expedientes_prestados(["o009","o009A","o010"])
#expediente.contar_anos_gravables("i010")
#expediente.cambiar_estado_expediente("o011",[2021,2022],"auto archivo")
#expediente.verificar_combinacion_existe("i011",2015)
