from data_base.db_connector import BDConnector
import mysql.connector


class Proceso: # logica relacionada con la tabla PROCESOS
    def __init__(self):
        self.connector = None

    def insertar_proceso(self, id_proceso, nombre_proceso):
        """
                Inserta un nuevo proceso en la tabla PROCESOS.

                Parameters:
                - id_proceso (int): El ID del nuevo proceso.
                - nombre_proceso (str): El nombre del nuevo proceso.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
            # Consulta SQL para la inserción
            query = "INSERT INTO procesos ( id_proceso, nombre_proceso) VALUES ( %s, %s)"
            # Parámetros para la consulta
            values = (id_proceso,  nombre_proceso)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()
            # verificar si se inserto un registro
            if self.connector.cursor.rowcount > 0:
                print("Inserción exitosa en la tabla procesos.")
                return "Inserción exitosa en la tabla procesos.", True
            else:
                print("no se hizo la insercíonen la tabla procesos.")
                return "no se hizo la insercíonen la tabla procesos.", False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}",False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla procesos.")
                return "ID duplicado en la tabla procesos.", False
            else:
                # Si es otro tipo de error MySQL, podrías lanzar la excepción nuevamente si lo deseas
                print(f"Error de MySQL: {mysql_err}")
                return f"Error de MySQL: {mysql_err}", False
        except Exception as e:
            print(f"Error al insertar en la tabla r: {e}")
            return f"Error al insertar en la tabla r: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def eliminar_proceso(self, id_proceso):  # eliminar proceso de la entidad procesos
        """
                Elimina un proceso de la tabla PROCESOS.

                Parameters:
                - id_proceso (int): El ID del proceso a eliminar.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
        # Consulta SQL para la eliminacion
            query = "DELETE FROM procesos WHERE id_proceso = %s"
            values = (id_proceso,)
        # Ejecutar la consulta
            self.connector.execute_query(query, values)
        # Confirmar los cambios
            self.connector.connection.commit()
            # Verificar si se eliminó algún registro
            if self.connector.cursor.rowcount > 0:
                print("Eliminación exitosa en la tabla procesos.")
                return "Eliminación exitosa en la tabla procesos.", True
            else:
                print(f"No se encontró ningún registro con id_proceso = {id_proceso}.")
                return f"No se encontró ningún registro con id_proceso = {id_proceso}.", False

        except mysql.connector.IntegrityError as integrity_err:
            # Capturar específicamente el error de clave externa (foreign key constraint)
            if integrity_err.errno == 1451:
                print("Error: No se puede eliminar el proceso. Tiene expedientes asociados.")
                return "Error: No se puede eliminar el proceso. Tiene expedientes asociados.", False
            else:
                print(f"Error de integridad en la base de datos: {integrity_err}")
                return f"Error de integridad en la base de datos: {integrity_err}", False
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
            print(f"Error al modificar en la tabla proceso: {e}")
            return f"Error al modificar en la tabla proceso: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def modificar_datos_proceso(self, id_proceso, nuevo_nombre_proceso):  # modificar nombre proceso
        """
                Modifica el nombre de un proceso en la tabla PROCESOS.

                Parameters:
                - id_proceso (int): El ID del proceso a modificar.
                - nuevo_nombre_proceso (str): El nuevo nombre para el proceso.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
            # Verificar si el auditor existe antes de intentar la modificación
            mensaje_proceso, verificacion_proceso = self.verificar_proceso_existe(id_proceso, connection=self.connector)
            if not verificacion_proceso:
                print("El proceso no existe.")
                return "El proceso no existe.",False
            # Consulta SQL para la modificación
            query = "UPDATE procesos SET  nombre_proceso =%s  WHERE id_proceso = %s"
            values = (nuevo_nombre_proceso, id_proceso)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()
            # verificar si se modifico un registro
            if self.connector.cursor.rowcount > 0:
                print("Modificación exitosa en la tabla procesos.")
                return "Modificación exitosa en la tabla procesos.", True
            else:
                print(f"No se hizo ninguna modificación = {id_proceso}.")
                return f"No se hizo ninguna modificación = {id_proceso}.", False

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
            print(f"Error al modificar en la tabla proceso: {e}")
            return f"Error al modificar en la tabla proceso: {e}",False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def modificar_id_proceso(self,id_viejo_proceso, id_nuevo_proceso):
        """
                Modifica el ID de un proceso en la tabla PROCESOS.

                Parameters:
                - id_viejo_proceso (int): El antiguo ID del proceso.
                - id_nuevo_proceso (int): El nuevo ID para el proceso.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()

            # Verificar si el auditor existe antes de intentar la modificación
            mensaje_proceso, verificacion_proceso = self.verificar_proceso_existe(id_viejo_proceso, connection=self.connector)
            if not verificacion_proceso:
                print("El proceso no existe.")
                return "El proceso no existe.", False

            # Consulta SQL para la modificación
            query = "UPDATE procesos SET  id_proceso = %s  WHERE id_proceso = %s"
            values = (id_nuevo_proceso, id_viejo_proceso)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()
            # verificar si se modifico un registro
            if self.connector.cursor.rowcount > 0:
                print("Modificación exitosa en la tabla procesos.")
                return "Modificación exitosa en la tabla procesos.", True
            else:
                print(f"No se hizo ninguna modificación = {id_nuevo_proceso}.")
                return f"No se hizo ninguna modificación = {id_nuevo_proceso}.", False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla proceso.")
                return "ID duplicado en la tabla proceso.", False
            else:
                # Si es otro tipo de error MySQL, podrías lanzar la excepción nuevamente si lo deseas
                print(f"Error de MySQL: {mysql_err}")
                return f"Error de MySQL: {mysql_err}", False
        except Exception as e:
            print(f"Error al insertar en la tabla proceso: {e}")
            return f"Error al insertar en la tabla proceso: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def verificar_proceso_existe(self, id_proceso, connection=None):
        """
                Verifica si un proceso existe en la tabla PROCESOS.

                Parameters:
                - id_proceso (int): El ID del proceso a verificar.
                - connection (BDConnector, optional): Una instancia de BDConnector para reutilizar la conexión.

                Returns:
                - bool: True si el proceso existe, False de lo contrario.
                """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection
            # Verificar si el contribuyente existe en la tabla contribuyente
            query = "SELECT nombre_proceso FROM procesos WHERE id_proceso = %s"
            values = (id_proceso,)
            self.connector.execute_query(query, values)
            result = self.connector.fetch_all()
            if result:
                nombre_proceso = result[0][0]
                print(nombre_proceso)
                print(f"se encontro el proceso {nombre_proceso}")
                return f"se encontro el proceso {nombre_proceso}", True
            else:
                print(f"no se encontro el proceso con el id ={id_proceso}")
                return f"no se encontro el proceso con el id ={id_proceso}", False

        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error en la verificación del proceso: {e}")
            return f"Error en la verificación del proceso: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def verificar_procesos_asociados(self, id_proceso,connection=None):
        """
                Verifica si un proceso tiene expedientes asociados en la tabla EXPEDIENTE.

                Parameters:
                - id_proceso (int): El ID del proceso a verificar.
                - connection (BDConnector, optional): Una instancia de BDConnector para reutilizar la conexión.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection

            # Verificar si el auditor existe
            mensaje_proceso, verificacion_proceso = self.verificar_proceso_existe(id_proceso, connection=self.connector)
            if not verificacion_proceso:
                print("El proceso no existe.")
                return "El proceso no existe.", False

            # Consulta SQL para contar expedientes asociados al préstamo
            query = "SELECT COUNT(*) FROM expediente WHERE id_proceso = %s"
            values = (id_proceso,)
            self.connector.execute_query(query, values)
            result = self.connector.fetch_one()

            count_expedientes = result[0]

            if count_expedientes > 0:
                print(f"El proceso con id_proceso={id_proceso} está asociado a {count_expedientes} expedientes.")
                return f"El proceso con id_proceso={id_proceso} está asociado a {count_expedientes} expedientes.",True
            else:
                print(f"No hay expedientes asociados al proceso con id_proceso={id_proceso}.")
                return f"No hay expedientes asociados al proceso con id_proceso={id_proceso}.",False

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


#proceso = Proceso()
#proceso.insertar_proceso("4","nuevo")
#proceso.eliminar_proceso("4")
#proceso.modificar_datos_proceso("5", "nuevoo")
#proceso.verificar_procesos_asociados("1")
#proceso.modificar_id_proceso("5","4")
#proceso.verificar_proceso_existe("4")