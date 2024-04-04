from data_base.db_connector import BDConnector
import mysql.connector



class Auditor: # logica relacionada con la tabla AUDITOR
    def __init__(self):
        self.connector = None

    def insertar_auditor(self, id_auditor, cedula, nombre_auditor):
        """
                Inserta un nuevo auditor en la tabla AUDITOR.

                Parameters:
                - id_auditor (int): El ID del auditor.
                - cedula (str): La cédula del auditor.
                - nombre_auditor (str): El nombre del auditor.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
            # Consulta SQL para la inserción
            query = "INSERT INTO auditor ( id_auditor,cedula, nombre_auditor) VALUES ( %s, %s, %s)"
            # Parámetros para la consulta
            values = (id_auditor, cedula, nombre_auditor)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()
            # verificar si se inserto un registro
            if self.connector.cursor.rowcount > 0:
                print("Inserción exitosa en la tabla Auditor.")
                return "Inserción exitosa en la tabla Auditor.", True
            else:
                print("no se hizo la insercíonen la tabla Auditor.")
                return "no se hizo la insercíonen la tabla Auditor.", False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla auditor.")
                return "ID duplicado en la tabla auditor.", False
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

    def eliminar_auditor(self, id_auditor):  # eliminar auditor de la entidad auditor
        """
                Elimina un auditor de la tabla AUDITOR.

                Parameters:
                - id_auditor (int): El ID del auditor a eliminar.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
        # Consulta SQL para la eliminacion
            query = "DELETE FROM auditor WHERE id_auditor = %s"
            values = (id_auditor,)
        # Ejecutar la consulta
            self.connector.execute_query(query, values)
        # Confirmar los cambios
            self.connector.connection.commit()
            # Verificar si se eliminó algún registro
            if self.connector.cursor.rowcount > 0:
                print("Eliminación exitosa en la tabla Auditor.")
                return "Eliminación exitosa en la tabla Auditor.", True
            else:
                print(f"No se encontró ningún registro con id_auditor = {id_auditor}.")
                return f"No se encontró ningún registro con id_auditor = {id_auditor}.", False

        except mysql.connector.IntegrityError as integrity_err:
            # Capturar específicamente el error de clave externa (foreign key constraint)
            if integrity_err.errno == 1451:
                print("Error: No se puede eliminar el auditor. Tiene expedientes asociados.")
                return "Error: No se puede eliminar el auditor. Tiene expedientes asociados.", False
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
            print(f"Error al modificar en la tabla Auditor: {e}")
            return f"Error al modificar en la tabla Auditor: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def modificar_datos_auditor(self, id_auditor,nueva_cedula, nuevo_nombre_auditor):  # modificar nombre auditor
        """
                Modifica los datos de un auditor en la tabla AUDITOR.

                Parameters:
                - id_auditor (int): El ID del auditor a modificar.
                - nueva_cedula (str): La nueva cédula del auditor.
                - nuevo_nombre_auditor (str): El nuevo nombre del auditor.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()

            # Verificar si el auditor existe antes de intentar la modificación
            mensaje_auditor, verificacion_auditor = self.verificar_auditor_existe(id_auditor, connection=self.connector)
            if not verificacion_auditor:
                # el auditor no existe
                print(mensaje_auditor)
                return mensaje_auditor, False

            # Consulta SQL para la modificación
            query = "UPDATE auditor SET  cedula =%s , nombre_auditor = %s WHERE id_auditor = %s"
            values = (nueva_cedula,nuevo_nombre_auditor, id_auditor)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()
            # verificar si se modifico un registro
            if self.connector.cursor.rowcount > 0:
                print("modificación exitosa en la tabla Auditor.")
                return "modificación exitosa en la tabla Auditor.", True
            else:
                print("no se hizo la modificación en la tabla Auditor.")
                return "no se hizo la modificación en la tabla Auditor.", False

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
            print(f"Error al modificar en la tabla Auditor: {e}")
            return f"Error al modificar en la tabla Auditor: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def modificar_id_auditor(self,id_viejo_auditor, id_nuevo_auditor):
        """
                Modifica el ID de un auditor en la tabla AUDITOR.

                Parameters:
                - id_viejo_auditor (int): El antiguo ID del auditor.
                - id_nuevo_auditor (int): El nuevo ID del auditor.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()

            # Verificar si el auditor existe antes de intentar la modificación
            mensaje_auditor, verificacion_auditor = self.verificar_auditor_existe(id_viejo_auditor, connection=self.connector)
            if not verificacion_auditor:
                # el auditor no existe
                print(mensaje_auditor)
                return mensaje_auditor, False

            # Consulta SQL para la modificación
            query = "UPDATE auditor SET  id_auditor = %s  WHERE id_auditor = %s"
            values = (id_nuevo_auditor, id_viejo_auditor)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()
            # verificar si se modifico un registro
            if self.connector.cursor.rowcount > 0:
                print("modificación exitosa en la tabla Auditor.")
                return "modificación exitosa en la tabla Auditor.", True
            else:
                print("no se hizo la modificación en la tabla Auditor.")
                return "no se hizo la modificación en la tabla Auditor.", False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla auditor.")
                return "ID duplicado en la tabla auditor.", False
            else:
                # Si es otro tipo de error MySQL, podrías lanzar la excepción nuevamente si lo deseas
                print(f"Error de MySQL: {mysql_err}")
                return f"Error de MySQL: {mysql_err}", False
        except Exception as e:
            print(f"Error al insertar en la tabla auditor: {e}")
            return f"Error al insertar en la tabla auditor: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()



    def verificar_auditor_existe(self,id_auditor, connection=None):
        """
                Verifica si un auditor con el ID dado existe en la tabla AUDITOR.

                Parameters:
                - id_auditor (int): El ID del auditor a verificar.
                - connection (BDConnector, opcional): La instancia de BDConnector a utilizar.

                Returns:
                - bool: True si el auditor existe, False de lo contrario.
                """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection
            # Verificar si el contribuyente existe en la tabla contribuyente
            query = "SELECT nombre_auditor FROM auditor WHERE id_auditor = %s"
            values = (id_auditor,)
            self.connector.execute_query(query, values)
            result = self.connector.fetch_all()
            # Devolver True si se encontró un contribuyente, False de lo contrario
            if result:
                nombre_auditor = result[0][0]
                print(nombre_auditor)
                print(f"se encontro el auditor {nombre_auditor}")
                return f"se encontro el auditor {nombre_auditor}", True
            else:
                print(f"no se encontro el auditor con el id {id_auditor}")
                return f"no se encontro el auditor con el id {id_auditor}", False

        except mysql.connector.DatabaseError as db_err:
            print(f"Error de la base de datos: {db_err}")
            return f"Error de la base de datos: {db_err}", False
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            return f"Error al conectar a la base de datos: {err}", False
        except Exception as e:
            print(f"Error en la verificación del auditor: {e}")
            return f"Error en la verificación del auditor: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def verificar_auditores_asociados(self, id_auditor, connection=None):
        """
                Verifica si un auditor tiene expedientes asociados en la tabla EXPEDIENTE.

                Parameters:
                - id_auditor (int): El ID del auditor a verificar.
                - connection (BDConnector, opcional): La instancia de BDConnector a utilizar.

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
            mensaje_auditor, verificacion_auditor = self.verificar_auditor_existe(id_auditor,connection=self.connector)
            if not verificacion_auditor:
                # el auditor no existe
                print(mensaje_auditor)
                return mensaje_auditor, False

            # Consulta SQL para contar expedientes asociados al préstamo
            # query = "SELECT id_expediente FROM expediente WHERE id_contribuyente = %s"
            query = """ SELECT expediente.id_expediente,expediente.id_auditor, auditor.nombre_auditor
                        FROM expediente 
                        JOIN auditor ON expediente.id_auditor = auditor.id_auditor
                        WHERE expediente.id_auditor = %s 
                    """
            values = (id_auditor,)
            self.connector.execute_query(query, values)
            result = self.connector.fetch_all()
            print(result)
            # Extraer información relevante del resultado
            if result:
                nombre_auditor = result[0][2]
                cantidad_expedientes = len(result)
                expedientes_asociados = [tupla[0] for tupla in result] # me devuelve una lista con lo expedientes asociados
                print(f"el auditor= {nombre_auditor} con el id = {id_auditor} tiene {cantidad_expedientes} expedientes asociados {expedientes_asociados}")
                return f"el auditor= {nombre_auditor} con el id = {id_auditor} tiene {cantidad_expedientes} expedientes asociados {expedientes_asociados}" \
                    , True
            else:
                print(f"No hay expedientes asociados al auditor con id_auditor={id_auditor}.")
                return f"No hay auditor asociados al contribuyente con id_auditor={id_auditor}.", False

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
            print(f"Error al verificar auditores asociados: {e}")
            return f"Error al verificar auditores asociados: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()



# Ejemplo de uso insertar
auditor = Auditor()
#auditor.insertar_auditor("A005", "46848486", "guty")

# ejemplo eliminar
#auditor.eliminar_auditor("A005")
# editar nombre auditor
#auditor.modificar_datos_auditor("A004","1564890", "LINAA")
#editar id_auditor
#auditor.modificar_id_auditor("A001","A004")
#auditor.verificar_auditores_asociados("A001")
#auditor.verificar_auditor_existe("A001")
