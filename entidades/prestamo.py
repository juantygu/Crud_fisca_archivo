from data_base.db_connector import BDConnector
import mysql.connector
from datetime import datetime, date
from entidades.expediente import Expediente


class Prestamo: # logica relacionada con la tabla PRESTAMO
    """
       Clase que encapsula la lógica relacionada con la tabla PRESTAMO en la base de datos.
       """
    def __init__(self):
        self.connector = None
        self.expediente = Expediente()

    def insertar_prestamo_vinculacion(self,fecha_entrega, responsable,area,expedientes:list):
        """
                Inserta un préstamo y vincula expedientes a dicho préstamo.

                Parameters:
                - fecha_entrega (str): La fecha de entrega del préstamo.
                - responsable (str): El responsable del préstamo.
                - area (str): El área asociada al préstamo.
                - expedientes (list): Lista de expedientes a vincular al préstamo.

                Returns:
                - tuple: Una tupla con un mensaje descriptivo y un booleano indicando el éxito de la operación.

                Esta función realiza las siguientes acciones:

                Crea una instancia de BDConnector.
                Verifica la existencia de los expedientes en la base de datos.
                Inserta el préstamo en la tabla prestamo.
                Vincula los expedientes al préstamo en la tabla expediente_prestamo.
                Devuelve un mensaje descriptivo y un booleano indicando el éxito de la operación.

                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
            # Iniciar la transacción
            self.connector.start_transaction()
            # Verificar la existencia de expedientes
            mensaje_existencia, verificacion_existencia = self.expediente.verificar_expedientes_existen(expedientes, connection=self.connector)
            if not verificacion_existencia:
                # No todos los expedientes existen, imprimir el mensaje y devolver el resultado
                print(mensaje_existencia)
                return mensaje_existencia, False
            print(mensaje_existencia, verificacion_existencia)

            # verificar si los expedientes estan prestados
            mensaje_en_prestamo ,expedientes_prestados, expedientes_no_prestados, verificacion_en_prestamo = self.expediente.verificar_expedientes_prestados(expedientes,connection=self.connector)
            if verificacion_en_prestamo:
                # algun expediente esta prestado
                print(mensaje_en_prestamo)
                return mensaje_en_prestamo, False
            print(mensaje_en_prestamo, verificacion_en_prestamo)
            #luego de hacer las verificaciones de existencia y si estan en prestamo se procede a hacer la insercion
            # Insertar el préstamo
            mensaje_prestamo,id_generado, verificacion_insertar = self.insertar_prestamo(fecha_entrega,responsable,area,connection=self.connector)
            # verificar la insercion a la tabla prestamo
            if verificacion_insertar: # true si se hizo la insercion a la tabla prestamo
                print(mensaje_prestamo, id_generado, verificacion_insertar)

                mensaje_expediente,verificacion_vincular = self.insertar_id_prestamo_expediente(expedientes, id_generado,connection=self.connector)
                if verificacion_vincular: # true si se asigno a los expedientes
                    # se vinculo a tabla expediente
                    print(mensaje_expediente, verificacion_vincular)
                    # Confirmar la transacción
                    self.connector.connection.commit()
                    return mensaje_expediente , True
                else:
                    # no se vinculo a tabla expediente
                    print(mensaje_expediente, verificacion_vincular)
                    self.connector.connection.rollback()
                    return mensaje_expediente, False
            else:
                # no se hizo la insercion a tabla prestamo
                print(mensaje_prestamo)
                self.connector.connection.rollback()
                return mensaje_prestamo , False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            self.connector.connection.rollback()
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla prestamo.")
                self.connector.connection.rollback()
                return "ID duplicado en la tabla prestamo.", False
            else:
                # Si es otro tipo de error MySQL, podrías lanzar la excepción nuevamente si lo deseas
                print(f"Error de MySQL: {mysql_err}")
                self.connector.connection.rollback()
                return f"Error de MySQL: {mysql_err}", False
        except Exception as e:
            print(f"Error al insertar en la tabla prestamo: {e}")
            self.connector.connection.rollback()
            return f"Error al insertar en la tabla prestamo: {e}", False
        finally:
            # Cerrar la conexión solo si fue creada dentro de la función
            if self.connector:
                self.connector.close_connection()

    def insertar_prestamo(self, fecha_entrega, responsable,area,connection=None):
        """
                Inserta un nuevo registro en la tabla prestamo.

                Parameters:
                - fecha_entrega (str): La fecha de entrega del préstamo.
                - responsable (str): El responsable del préstamo.
                - area (str): El área asociada al préstamo.
                - connection (BDConnector): La conexión a la base de datos. Si es None, se crea una nueva conexión.

                Returns:
                - tuple: Una tupla con un mensaje descriptivo, el ID generado y un booleano indicando el éxito de la operación.
                """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection
            # Consulta SQL para la inserción
            query = "INSERT INTO prestamo ( fecha_entrega, responsable, area) VALUES ( %s, %s, %s)"
            # Parámetros para la consulta
            values = (fecha_entrega,  responsable, area)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios SI no se proporcionó una conexión externa
            if connection is None:
                self.connector.connection.commit()

            # Verificar si se insertó el registro
            if self.connector.cursor.rowcount > 0:
                id_prestamo_generado = self.connector.cursor.lastrowid  # Obtener el id_prestamo generado

                if id_prestamo_generado is not None:
                    print("Inserción exitosa en la tabla prestamo.")
                    return "Inserción exitosa en la tabla prestamo.", id_prestamo_generado, True
                else:
                    print("No se obtuvo el último ID después de la inserción.")
                    return "No se obtuvo el último ID después de la inserción.", None, False
            else:
                print("No se hizo la inserción en la tabla prestamo.")
                return "No se hizo la inserción en la tabla prestamo.", None, False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", None, False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla prestamo.")
                return "ID duplicado en la tabla prestamo.", None, False
            else:
                # Si es otro tipo de error MySQL, podrías lanzar la excepción nuevamente si lo deseas
                print(f"Error de MySQL: {mysql_err}")
                return f"Error de MySQL: {mysql_err}", None, False
        except Exception as e:
            print(f"Error al insertar en la tabla prestamo: {e}")
            return f"Error al insertar en la tabla prestamo: {e}", None, False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def insertar_id_prestamo_expediente(self, id_expedientes: list, id_prestamo,connection=None): # SE HACE UNA ACTULIZACION YA QUE EXPEDIENTE DEBE EXISTIR PARA HACER EL PRESTAMO
        """
                Asocia expedientes existentes a un préstamo.

                Parameters:
                - id_expedientes (list): Lista de IDs de expedientes a vincular.
                - id_prestamo: ID del préstamo al que se vincularán los expedientes.
                - connection (BDConnector): La conexión a la base de datos. Si es None, se crea una nueva conexión.

                Returns:
                - tuple: Una tupla con un mensaje descriptivo y un booleano indicando el éxito de la operación.
                """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection

            # Consulta SQL para la inserción
            placeholders = ",".join(["%s"] * len(id_expedientes))
            query = f"UPDATE expediente SET id_prestamo = %s WHERE id_expediente IN ({placeholders})"
            # Parámetros para la consulta
            values = [id_prestamo] + id_expedientes # Por ejemplo, si id_prestamo es 100 y id_expedientes es [1, 2, 3], entonces values será [100, 1, 2, 3].
            # values = (id_prestamo,) + tuple(id_expedientes)

            # Ejecutar la consulta
            self.connector.execute_query(query, tuple(values))
            # Confirmar los cambios SI no se proporcionó una conexión externa
            if connection is None:
                self.connector.connection.commit()

            expected_rowcount = len(id_expedientes) # numero de expedientes a vincular
            rowcounts = self.connector.cursor.rowcount # numero de registos modificados
            # verificacion si el numero de registros modificados es igual al los expedientes a vincular
            if rowcounts > 0:
                if rowcounts == expected_rowcount:
                    print(f"Modificación exitosa, se asignaron {rowcounts} expedientes al prestamo {id_prestamo}.")
                    return f"Modificación exitosa, se asignaron {rowcounts} expedientes al prestamo {id_prestamo}.",True
                else:
                    print(f"Error: Se esperaban asignar {expected_rowcount} expedientes, pero solo se asignaron {rowcounts}.")
                    return f"Error: Se esperaban asignar {expected_rowcount} expedientes, pero solo se asignaron {rowcounts}.",False
            else:
                print("Error no se hizo ninguna modificacion")
                return "Error no se hizo ninguna modificacion", False
        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
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
            return f"Error al insertar en la tabla expediente: {e}",False
            # Revertir los cambios en caso de error
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def finalizar_prestamo(self, id_prestamo, fecha_devolucion):
        """
            Finaliza un préstamo, marcándolo como devuelto en la base de datos y desvinculando los expedientes asociados.

            Parameters:
            - id_prestamo: El ID del préstamo que se desea finalizar.
            - fecha_devolucion: La fecha en que se devuelve el préstamo.

            Returns:
            - tuple: Una tupla con un mensaje descriptivo y un booleano indicando el éxito de la operación.
              En caso de éxito, el booleano es True; de lo contrario, es False.

            Esta función realiza las siguientes acciones:

            Verifica si el préstamo ya ha sido devuelto previamente.
            Si el préstamo no ha sido devuelto, intenta realizar la devolución.
            Si la devolución es exitosa, desvincula los expedientes asociados al préstamo.
            Devuelve un mensaje descriptivo y un booleano indicando el éxito de la operación.

            """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
            # Se inicia una trasaction
            self.connector.start_transaction()

            # verificar si el id_prestamo existe antes de proceder
            mensaje_existencia, verificacion_existencia = self.verificar_existencia_prestamo(id_prestamo,connection=self.connector)
            if not verificacion_existencia:
                # el id_prestamo no existe
                print(mensaje_existencia)
                return mensaje_existencia, False

            # verificar existencia previa devolucion
            mensaje_devuelto, verificacion_devuelto = self.verificar_prestamo_devuelto(id_prestamo, connection=self.connector)
            if not verificacion_devuelto:
                # el prestamo no tiene devolucion
                print(mensaje_devuelto)
                # devolver prestamo
                mensaje_devolucion, verificacion_devolucion = self.devolver_prestamo(id_prestamo,fecha_devolucion, connection=self.connector)
                if verificacion_devolucion:
                    # se realizo la devolucion
                    print(mensaje_devolucion)
                    mensaje_desvinculacion,verificacion_desvinculacion = self.desvincular_prestamo_expediente(id_prestamo, connection=self.connector)
                    if verificacion_desvinculacion:
                        # se realizo la desvinculacion
                        print(mensaje_desvinculacion)
                        # Confirmar la transacción
                        self.connector.connection.commit()
                        return mensaje_desvinculacion, True
                    else:
                        # no se realizo la desvinculacion
                        print(mensaje_desvinculacion)
                        self.connector.connection.rollback()
                        return mensaje_desvinculacion, False
                else:
                    # NO se realizo la devolucion
                    print(mensaje_devolucion)
                    self.connector.connection.rollback()
                    return mensaje_existencia, False
            else:
                # el prestamo ya tiene devolucion ,  no se puede hacer la devolucion
                print(mensaje_devuelto)
                self.connector.connection.rollback()
                return mensaje_existencia, False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            self.connector.connection.rollback()
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            self.connector.connection.rollback()
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            self.connector.connection.rollback()
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error al actualizar la tabla expediente: {e}")
            self.connector.connection.rollback()
            return f"Error al actualizar la tabla expediente: {e}", False
        finally:
            # Cerrar la conexión solo si fue creada dentro de la función
            self.connector.close_connection()

    def devolver_prestamo(self, id_prestamo, fecha_devolucion,connection=None):
        """
                Registra la devolución de un préstamo.

                Parameters:
                - id_prestamo: ID del préstamo que se va a devolver.
                - fecha_devolucion (str): La fecha de devolución del préstamo.
                - connection (BDConnector, opcional): La instancia de BDConnector a utilizar.

                Returns:
                - tuple: Una tupla con un mensaje descriptivo y un booleano indicando el éxito de la operación.
                """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection
            # Obtener la fecha de entrega del préstamo
            fecha_entrega_prestamo: date = self.obtener_fecha_entrega(id_prestamo, connection=self.connector) # formato datetime.date
            if not fecha_entrega_prestamo:
                print("No se encontro una fecha de entrega.")
                return "No se encontro una fecha de entrega.", False

            fecha_devolucion = datetime.strptime(fecha_devolucion, "%Y-%m-%d").date()

            print(type(fecha_entrega_prestamo), fecha_entrega_prestamo,type(fecha_devolucion), fecha_devolucion)
            if fecha_devolucion < fecha_entrega_prestamo:
                print("La fecha de devolución no puede ser menor que la fecha de entrega.")
                return "La fecha de devolución no puede ser menor que la fecha de entrega.",False
            # Consulta SQL para la actualización
            query = "UPDATE prestamo SET fecha_devolucion = %s WHERE id_prestamo = %s"
            # Parámetros para la consulta
            values = (fecha_devolucion, id_prestamo)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios SI no se proporcionó una conexión externa
            if connection is None:
                self.connector.connection.commit()

            # verificar si se hizo la devolucion
            if self.connector.cursor.rowcount > 0:
                print("devolución exitosa en la tabla prestamo.")
                return " devolución exitosa en la tabla prestamo.", True
            else:
                print("no se hizo la devolución.")
                return "no se hizo la devolución.", False

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
            print(f"Error al actualizar la fecha de devolución: {e}")
            return f"Error al actualizar la fecha de devolución: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def modificar_prestamo(self, id_prestamo, nueva_fecha_entrega, nueva_fecha_devolucion=None, nuevo_responsable=None,nueva_area=None):
        """
            Modifica un préstamo en la base de datos con los nuevos datos proporcionados.

            Parameters:
            - id_prestamo (int): El ID del préstamo a modificar.
            - nueva_fecha_entrega (str): La nueva fecha de entrega del préstamo.
            - nueva_fecha_devolucion (str, opcional): La nueva fecha de devolución del préstamo.
            - nuevo_responsable (str, opcional): El nuevo responsable del préstamo.
            - nueva_area (str, opcional): La nueva área asociada al préstamo.

            Returns:
            - str: Un mensaje descriptivo indicando el resultado de la operación.
            """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()

            # verificar si el id_prestamo existe antes de proceder
            mensaje_existencia, verificacion_existencia = self.verificar_existencia_prestamo(id_prestamo,connection=self.connector)
            if not verificacion_existencia:
                # el id_prestamo no existe
                print(mensaje_existencia)
                return mensaje_existencia, False

            # Construir la consulta SQL y los valores según los datos proporcionados
            query = "UPDATE prestamo SET fecha_entrega = %s"
            values = [nueva_fecha_entrega]

            if nueva_fecha_devolucion is not None:
                nueva_fecha_devolucion = datetime.strptime(nueva_fecha_devolucion, "%Y-%m-%d").date()
                nueva_fecha_entrega = datetime.strptime(nueva_fecha_entrega, "%Y-%m-%d").date()
                # Verificar si la nueva fecha de devolución es menor que la fecha de entrega actual
                if nueva_fecha_devolucion < nueva_fecha_entrega:
                    print("La fecha de devolución no puede ser menor que la fecha de entrega.")
                    return "La fecha de devolución no puede ser menor que la fecha de entrega.",False
                query += ", fecha_devolucion = %s"
                values.append(nueva_fecha_devolucion)

            if nuevo_responsable is not None:
                query += ", responsable = %s"
                values.append(nuevo_responsable)

            if nueva_area is not None:
                query += ", area = %s"
                values.append(nueva_area)

            query += " WHERE id_prestamo = %s"
            values.append(id_prestamo)

            # Ejecutar la consulta
            self.connector.execute_query(query, tuple(values))

            # Confirmar los cambios
            self.connector.connection.commit()

            if self.connector.cursor.rowcount > 0:
                print("Modificación exitosa en la tabla prestamo.")
                return "Modificación exitosa en la tabla prestamo.", True
            else:
                print("Modificación Erronea en la tabla prestamo.")
                return "Modificación Erronea en la tabla prestamo.", False

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
            print(f"Error al modificar en la tabla prestamo: {e}")
            return f"Error al modificar en la tabla prestamo: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def obtener_fecha_entrega(self, id_prestamo,connection=None):
        """
            Obtiene la fecha de entrega de un préstamo dado su ID.

            Parameters:
            - id_prestamo (str): El ID del préstamo.
            - connection (BDConnector): Conexión a la base de datos (opcional).

            Returns:
            - str: La fecha de entrega del préstamo como cadena.
            """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection
            # Consulta SQL para obtener la fecha de entrega
            query = "SELECT fecha_entrega FROM prestamo WHERE id_prestamo = %s"
            # Parámetros para la consulta
            values = (id_prestamo,)
            # Ejecutar la consulta y obtener el resultado
            self.connector.execute_query(query, values)
            result = self.connector.fetch_one()

            if result:
                # Devolver la fecha de entrega como cadena
                fecha_entrega = result[0]
                return fecha_entrega
            else:
                return False

        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error al obtener la fecha de entrega: {e}")
            return f"Error al obtener la fecha de entrega: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def eliminar_prestamo_con_verificacion(self, id_prestamo):
        """
            Verifica si hay expedientes asociados antes de eliminar un préstamo. Si hay expedientes, los desvincula antes de la eliminación.

            Parameters:
            - id_prestamo (str): El ID del préstamo.
            - connection (BDConnector): Conexión a la base de datos (opcional).

            Returns:
            - tuple: Una tupla con un mensaje descriptivo y un booleano indicando el éxito de la operación.
            """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
            # Iniciar la transacción
            self.connector.start_transaction()
            # Verificar si hay expedientes asociados

            # verificar si el id_prestamo existe antes de proceder
            mensaje_existencia, verificacion_existencia = self.verificar_existencia_prestamo(id_prestamo,connection=self.connector)
            if not verificacion_existencia:
                # el id_prestamo no existe
                print(mensaje_existencia)
                return mensaje_existencia, False

            mensaje_asociacion,exp_asociados,verificacion_asociacion = self.verificar_prestamos_asociados(id_prestamo, connection=self.connector)
            if verificacion_asociacion: # si es True
                # Desvincular expedientes antes de eliminar el préstamo
                print(mensaje_asociacion)
                mensaje_desvincular, verificacion_desvincular = self.desvincular_prestamo_expediente(id_prestamo, connection=self.connector)
                if verificacion_desvincular:
                    # se desvinculo los prestamos
                    print(mensaje_desvincular)
                    mensaje_eliminar,verificacion_eliminar = self.eliminar_registro_prestamo(id_prestamo, connection=self.connector)
                    # eliminar prestamos
                    if verificacion_eliminar:
                        print(mensaje_eliminar)
                        # Confirmar la transacción
                        self.connector.connection.commit()
                        return mensaje_eliminar, True
                    else:
                        print(mensaje_eliminar)
                        self.connector.connection.rollback()
                        return mensaje_eliminar, False
                else:
                    print(mensaje_desvincular)
                    self.connector.connection.rollback()
                    return mensaje_asociacion,False
            else: # si es false osea no tiene expediente vinculados con prestamos
                mensaje_eliminar,verificacion_eliminar = self.eliminar_registro_prestamo(id_prestamo, connection=self.connector)
                # Eliminar el préstamo
                if verificacion_eliminar:
                    print(mensaje_eliminar)
                    # Confirmar la transacción
                    self.connector.connection.commit()
                    return mensaje_eliminar, True
                else:
                    print(mensaje_eliminar)
                    self.connector.connection.rollback()
                    return mensaje_eliminar, False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            self.connector.connection.rollback()
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            self.connector.connection.rollback()
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            self.connector.connection.rollback()
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error al eliminar el préstamo: {e}")
            self.connector.connection.rollback()
            return f"Error al eliminar el préstamo: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def eliminar_registro_prestamo(self, id_prestamo, connection=None):  # eliminar prestamo
        """
            Elimina un registro de préstamo de la base de datos.

            Parameters:
            - id_prestamo (str): El ID del préstamo.
            - connection (BDConnector): Conexión a la base de datos (opcional).

            Returns:
            - tuple: Una tupla con un mensaje descriptivo y un booleano indicando el éxito de la operación.
            """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection
        # Consulta SQL para la eliminacion
            query = "DELETE FROM prestamo WHERE id_prestamo = %s"
            values = (id_prestamo,)
        # Ejecutar la consulta
            self.connector.execute_query(query, values)

        # Confirmar los cambios SI no se proporcionó una conexión externa
            if connection is None:
                self.connector.connection.commit()
            # Verificar si se eliminó algún registro
            if self.connector.cursor.rowcount > 0:
                print("Eliminación exitosa en la tabla prestamo.")
                return "Eliminación exitosa en la tabla prestamo.",True
            else:
                print(f"No se realizó ninguna eliminacion con id_prestamo = {id_prestamo}.")
                return f"No se realizó ninguna eliminacion con id_prestamo = {id_prestamo}.",False

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
            print(f"Error al eliminar en la tabla prestamo: {e}")
            return f"Error al eliminar en la tabla prestamo: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def desvincular_prestamo_expediente(self,id_prestamo, connection=None):
        """
            Desvincula un préstamo de los expedientes asociados.

            Parameters:
            - id_prestamo (str): El ID del préstamo.
            - connection (BDConnector): Conexión a la base de datos (opcional).

            Returns:
            - tuple: Una tupla con un mensaje descriptivo y un booleano indicando el éxito de la operación.
            """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection

            # Actualizamos los registros en la tabla expediente
            query = "UPDATE expediente SET id_prestamo = NULL WHERE id_prestamo = %s"
            values = (id_prestamo,)
            self.connector.execute_query(query, values)
            # Confirmar los cambios SI no se proporcionó una conexión externa
            if connection is None:
                self.connector.connection.commit()

            prestamos_desvinculados = self.connector.cursor.rowcount
            #confirmar desvinculacion
            if prestamos_desvinculados != 0:
                # Se hizo la desvinculacion
                print(f"desvinculación exitosa , prestamos desvinculados = {prestamos_desvinculados} para el prestamo = {id_prestamo}.")
                return f"desvinculación exitosa , prestamos desvinculados = {prestamos_desvinculados} para el prestamo = {id_prestamo}.", True
            else:
                # No se hizo la desvinculacion
                print(f"desvinculación erronea , prestamos desvinculados = {prestamos_desvinculados} para el prestamo = {id_prestamo}.")
                return f"desvinculación erronea , prestamos desvinculados = {prestamos_desvinculados} para el prestamo = {id_prestamo}.", False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            self.connector.connection.rollback()
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            self.connector.connection.rollback()
            return f"Error de la base de datos: {db_err}",False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            self.connector.connection.rollback()
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error al actualizar la tabla expediente: {e}")
            self.connector.connection.rollback()
            return f"Error al actualizar la tabla expediente: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def verificar_prestamos_asociados(self, id_prestamo, connection=None):
        """
            Verifica cuántos expedientes están asociados a un préstamo.

            Parameters:
            - id_prestamo (str): El ID del préstamo.
            - connection (BDConnector): Conexión a la base de datos (opcional).

            Returns:
            - tuple: Una tupla con un mensaje descriptivo, la cantidad de expedientes asociados y un booleano indicando el éxito de la operación.
            """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection

            query = "SELECT COUNT(*) FROM expediente WHERE id_prestamo = %s"
            values = (id_prestamo,)
            self.connector.execute_query(query, values)
            result = self.connector.fetch_one()

            count_expedientes = result[0]

            if count_expedientes > 0:
                print(f"El préstamo con id_prestamo={id_prestamo} está asociado a {count_expedientes} expedientes.")
                return f"El préstamo con id_prestamo={id_prestamo} está asociado a {count_expedientes} expedientes.",count_expedientes, True
            else:
                print(f"No hay expedientes asociados al préstamo con id_prestamo={id_prestamo}.")
                return f"No hay expedientes asociados al préstamo con id_prestamo={id_prestamo}.",count_expedientes, False

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
            print(f"Error al verificar expedientes asociados: {e}")
            return f"Error al verificar expedientes asociados: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def verificar_prestamo_devuelto(self, id_prestamo, connection=None):
        """
            Verifica si un préstamo ha sido devuelto.

            Parameters:
            - id_prestamo (str): El ID del préstamo.
            - connection (BDConnector): Conexión a la base de datos (opcional).

            Returns:
            - tuple: Una tupla con un mensaje descriptivo y un booleano indicando si el préstamo ha sido devuelto.
            """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection

            # Consulta SQL para verificar si el préstamo ha sido devuelto
            query = "SELECT fecha_devolucion FROM prestamo WHERE id_prestamo = %s"
            # Parámetros para la consulta
            values = (id_prestamo,)

            self.connector.execute_query(query, values)
            result = self.connector.fetch_one()

            fecha_devolucion = result[0]
            # Verificar la fecha de devolución y devolver mensajes descriptivos
            if fecha_devolucion is not None:
                print("No se puede hacer la devolucion, El préstamo ha sido devuelto en la fecha: " + str(fecha_devolucion))
                return "No se puede hacer la devolucion,El préstamo ha sido devuelto en la fecha: " + str(fecha_devolucion), True
            else:
                print("El préstamo aún no ha sido devuelto.")
                return "El préstamo aún no ha sido devuelto.", False

        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error en la verificación de préstamo devuelto: {e}")
            return f"Error en la verificación de préstamo devuelto: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def verificar_existencia_prestamo(self, id_prestamo, connection=None):
        """
        Verifica la existencia de un préstamo por su ID en la base de datos.

        Parameters:
        - id_prestamo: El ID del préstamo a verificar.
        - connection (BDConnector): La conexión a la base de datos. Si es None, se crea una nueva conexión.

        Returns:
        - tuple: Una tupla con un mensaje descriptivo y un booleano indicando si el préstamo existe.
        """

        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection

            # Consulta SQL para verificar la existencia del préstamo
            query = "SELECT COUNT(*) FROM prestamo WHERE id_prestamo = %s"

            # Ejecutar la consulta
            self.connector.execute_query(query, (id_prestamo,))

            # Obtener el resultado de la consulta
            count = self.connector.cursor.fetchone()[0]
            print(count)
            # Verificar si el préstamo existe
            if count > 0:
                print(f"El préstamo con ID {id_prestamo} existe.")
                return f"El préstamo con ID {id_prestamo} existe.", True
            else:
                print(f"No se encontró el préstamo con ID {id_prestamo}.")
                return f"No se encontró el préstamo con ID {id_prestamo}.", False

        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error en la verificación de préstamo devuelto: {e}")
            return f"Error en la verificación de préstamo devuelto: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()


prestamo = Prestamo()

#=========INSERTAR PRESTAMOS ====================
#prestamo.insertar_prestamo_vinculacion("2024-03-02", "chinga", "tesoreria", ["o009", "o009A"])
#prestamo.insertar_id_prestamo_expediente(["o009A"],12)

#===========FINALIZAR PRESTAMO=====================
#prestamo.finalizar_prestamo(22,"2024-06-0")

#===========MODIFICAR PRESTAMO ===================
#prestamo.modificar_prestamo(1,"2024-02-13", nueva_fecha_devolucion = "2024-02-13",nuevo_responsable="jorgee",nueva_area= "fiscalizacion")

#==============ELIMINAR PRESTAMO =================
#prestamo.eliminar_registro_prestamo(20)
#prestamo.eliminar_prestamo_con_verificacion(16)

#prestamo.desvincular_prestamo_expediente("14")

#fecha_entrega=prestamo.obtener_fecha_entrega(1)
#print (fecha_entrega)
#fecha = "2024-02-15"
#date = datetime.strptime(fecha, "%Y-%m-%d").date()
#date_date = date.date()
#print(type(date),date)

#prestamo.verificar_prestamo_devuelto(6)
#prestamo.verificar_prestamos_asociados(50)
#prestamo.verificar_existencia_prestamo(21)