from data_base.db_connector import BDConnector
import mysql.connector

class Contribuyente: # logica relacionada con la tabla CONTRIBUYENTE
    def __init__(self):
        self.connector = None

    def insertar_contribuyente(self,id_contribuyente,nombre_contribuyente,tipo):
        """
                Inserta un nuevo contribuyente en la tabla CONTRIBUYENTE.

                Parameters:
                - id_contribuyente (int): El ID del contribuyente.
                - nombre_contribuyente (str): El nombre del contribuyente.
                - tipo (str): El tipo de contribuyente.

                Returns:
                - tuple: Un mensaje indicando el resultado de la inserción y un booleano indicando el éxito.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
            # Consulta SQL para la inserción
            query = "INSERT INTO contribuyente (id_contribuyente, nombre_contribuyente,tipo) VALUES (%s,%s,%s)"
            # Parámetros para la consulta
            values = (id_contribuyente, nombre_contribuyente,tipo)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()
            #verificar si se inserto un registro
            if self.connector.cursor.rowcount > 0:
                print("Inserción exitosa en la tabla Contribuyente.")
                return "Inserción exitosa en la tabla Contribuyente.",True
            else:
                print("no se hizo la insercíon en la tabla Contribuyente.")
                return "no se hizo la insercíon en la tabla Contribuyente.", False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla contribuyente.")
                return "ID duplicado en la tabla contribuyente.", False
            else:
                # Si es otro tipo de error MySQL, podrías lanzar la excepción nuevamente si lo deseas
                print(f"Error de MySQL: {mysql_err}")
                return f"Error de MySQL: {mysql_err}", False
        except Exception as e:
            print(f"Error al insertar en la tabla contribuyente: {e}")
            return f"Error al insertar en la tabla contribuyente: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def eliminar_contribuyente(self,id_contribuyente):
        """
                Elimina un contribuyente de la tabla CONTRIBUYENTE.

                Parameters:
                - id_contribuyente (int): El ID del contribuyente a eliminar.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()
        # Consulta SQL para la eliminacion
            query = "DELETE FROM contribuyente WHERE id_contribuyente = %s"
            values = (id_contribuyente,)
        # Ejecutar la consulta
            self.connector.execute_query(query, values)
        # Confirmar los cambios
            self.connector.connection.commit()
            # Verificar si se eliminó algún registro
            if self.connector.cursor.rowcount > 0:
                print("Eliminación exitosa en la tabla contribuyente.")
                return "Eliminación exitosa en la tabla contribuyente.",True
            else:
                print(f"No se encontró ningún registro con id_contribuyente = {id_contribuyente}.")
                return f"No se encontró ningún registro con id_contribuyente = {id_contribuyente}.", False

        except mysql.connector.IntegrityError as integrity_err:
            # Capturar específicamente el error de clave externa (foreign key constraint)
            if integrity_err.errno == 1451:
                print("Error: No se puede eliminar el contribuyente. Tiene expedientes asociados.")
                return "Error: No se puede eliminar el contribuyente. Tiene expedientes asociados.", False
            else:
                print(f"Error de integridad en la base de datos: {integrity_err}")
                return f"Error de integridad en la base de datos: {integrity_err}",False
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
            print(f"Error al eliminar en la tabla contribuyente: {e}")
            return f"Error al eliminar en la tabla contribuyente: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def modificar_datos_contribuyente(self, id_contribuyente, nuevo_nombre_contribuyente, nuevo_tipo):  # modificar nombre auditor
        """
                Modifica los datos de un contribuyente en la tabla CONTRIBUYENTE.

                Parameters:
                - id_contribuyente (int): El ID del contribuyente a modificar.
                - nuevo_nombre_contribuyente (str): El nuevo nombre del contribuyente.
                - nuevo_tipo (str): El nuevo tipo de contribuyente.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()

            # Verificar si el contribuyente existe antes de intentar la modificación
            mensaje_contribuyente, verificacion_contribuyente = self.verificar_contribuyente_existe(id_contribuyente, connection=self.connector)
            if not verificacion_contribuyente:
                # el contribuyente no existe
                print(mensaje_contribuyente)
                return mensaje_contribuyente, False
            # Consulta SQL para la modificación
            query = "UPDATE contribuyente SET  nombre_contribuyente = %s, tipo = %s  WHERE id_contribuyente = %s"
            values = (nuevo_nombre_contribuyente, nuevo_tipo, id_contribuyente)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()
            # verificar si se modificó un registro
            if self.connector.cursor.rowcount > 0:
                print("modificación exitosa en la tabla Contribuyente.")
                return "modificación exitosa en la tabla Contribuyente.", True
            else:
                print("no se hizo la modificación.")
                return "no se hizo la modificación.", False

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
            print(f"Error al modificar en la tabla contribuyente: {e}")
            return f"Error al modificar en la tabla contribuyente: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def modificar_id_contribuyente(self,id_viejo_contribuyente, id_nuevo_contribuyente):
        """
                Modifica el ID de un contribuyente en la tabla CONTRIBUYENTE.

                Parameters:
                - id_viejo_contribuyente (int): El antiguo ID del contribuyente.
                - id_nuevo_contribuyente (int): El nuevo ID del contribuyente.

                Returns:
                - tuple: Un mensaje indicando el resultado de la operación y un valor booleano.
                """
        try:
            # Crear una instancia de BDConnector
            self.connector = BDConnector()

            # Verificar si el contribuyente existe antes de intentar la modificación
            mensaje_contribuyente, verificacion_contribuyente = self.verificar_contribuyente_existe(id_viejo_contribuyente, connection=self.connector)
            if not verificacion_contribuyente:
                # el contribuyente no existe
                print(mensaje_contribuyente)
                return mensaje_contribuyente, False

            # Consulta SQL para la modificación
            query = "UPDATE contribuyente SET  id_contribuyente = %s  WHERE id_contribuyente = %s"
            values = (id_nuevo_contribuyente, id_viejo_contribuyente)
            # Ejecutar la consulta
            self.connector.execute_query(query, values)
            # Confirmar los cambios
            self.connector.connection.commit()
            # verificar si se modificó un registro
            if self.connector.cursor.rowcount > 0:
                print("modificación exitosa en la tabla Contribuyente.")
                return "modificación exitosa en la tabla Contribuyente.", True
            else:
                print("no se hizo la modificación.")
                return "no se hizo la modificación.", False

        except mysql.connector.InterfaceError as interface_err:
            print(f"Error de interfaz con MySQL: {interface_err}")
            return f"Error de interfaz con MySQL: {interface_err}", False
        except mysql.connector.Error as mysql_err:
            # Verificar si el error es debido a un ID duplicado
            if mysql_err.errno == 1062 and "Duplicate entry" in str(mysql_err):
                print("ID duplicado en la tabla contribuyente.")
                return "ID duplicado en la tabla contribuyente.", False
            else:
                # Si es otro tipo de error MySQL, podrías lanzar la excepción nuevamente si lo deseas
                print(f"Error de MySQL: {mysql_err}")
                return f"Error de MySQL: {mysql_err}", False
        except Exception as e:
            print(f"Error al insertar en la tabla contribuyente: {e}")
            return f"Error al insertar en la tabla contribuyente: {e}", False
        finally:
            if self.connector:
                # Cerrar la conexión
                self.connector.close_connection()

    def verificar_contribuyente_existe(self,id_contribuyente,connection=None):
        """
                Verifica si un contribuyente con el ID dado existe en la tabla CONTRIBUYENTE.

                Parameters:
                - id_contribuyente (int): El ID del contribuyente a verificar.
                - connection (BDConnector, opcional): La instancia de BDConnector a utilizar.

                Returns:
                - bool: True si el contribuyente existe, False de lo contrario.
                """
        try:
            # Utilizar la conexión proporcionada o crear una nueva instancia de BDConnector
            if connection is None:
                self.connector = BDConnector()
            else:
                self.connector = connection
            # Verificar si el contribuyente existe en la tabla contribuyente
            query = "SELECT id_contribuyente,nombre_contribuyente FROM contribuyente WHERE id_contribuyente = %s"
            values = (id_contribuyente,)
            self.connector.execute_query(query, values)
            result = self.connector.fetch_all()

            # Devolver True si se encontró un contribuyente, False de lo contrario
            if result:
                documento_contribuyente = result[0][0]
                nombre_contribuyente = result[0][1]
                print(nombre_contribuyente, documento_contribuyente)
                print(f"se encontró el contribuyente {nombre_contribuyente} con su numero de documento = {documento_contribuyente}")
                return f"se encontró el contribuyente {nombre_contribuyente} con su numero de documento = {documento_contribuyente}", True
            else:
                print(f"No se econtro el contribuyente con el numero de documento = {id_contribuyente}")
                return f"No se econtro el contribuyente con el numero de documento = {id_contribuyente}", False

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
            print(f"Error en la verificación del contribuyente: {e}")
            return f"Error en la verificación del contribuyente: {e}", False
        finally:
            if connection is None and self.connector:
                # Cerrar la conexión solo si fue creada dentro de la función
                self.connector.close_connection()

    def verificar_contribuyentes_asociados(self, id_contribuyente,connection=None):
        """
                Verifica si un contribuyente tiene expedientes asociados en la tabla EXPEDIENTE.

                Parameters:
                - id_contribuyente (int): El ID del contribuyente a verificar.
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

            # Verificar si el contribuyente existe
            mensaje_contribuyente, verificacion_contribuyente = self.verificar_contribuyente_existe(id_contribuyente, connection=self.connector)
            if not verificacion_contribuyente:
                # el contribuyente no existe
                print(mensaje_contribuyente)
                return mensaje_contribuyente, False

            # Consulta SQL para contar expedientes asociados al préstamo
            # query = "SELECT id_expediente FROM expediente WHERE id_contribuyente = %s"
            query = """
                        SELECT expediente.id_expediente,expediente.id_contribuyente, contribuyente.nombre_contribuyente 
                        FROM expediente
                        JOIN contribuyente ON expediente.id_contribuyente = contribuyente.id_contribuyente
                        WHERE expediente.id_contribuyente = %s
                    """
            values = (id_contribuyente,)
            self.connector.execute_query(query, values)
            result = self.connector.fetch_all()
            print(result)
            # Extraer información relevante del resultado
            if result:
                nombre_contribuyente = result[0][2]
                cantidad_expedientes = len(result)
                expedientes_asociados = [tupla[0] for tupla in result] # me devuelve una lista con lo expedientes asociados
                print(f"el contribuyente= {nombre_contribuyente} con el id = {id_contribuyente} tiene {cantidad_expedientes} expedientes asociados {expedientes_asociados}")
                return f"el contribuyente= {nombre_contribuyente} con el id = {id_contribuyente} tiene {cantidad_expedientes} expedientes asociados {expedientes_asociados}" \
                    , True
            else:
                print(f"No hay expedientes asociados al contribuyente con id_contribuyente={id_contribuyente}.")
                return f"No hay expedientes asociados al contribuyente con id_contribuyente={id_contribuyente}.", False

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



# Ejemplo de uso
contribuyente = Contribuyente()
#contribuyente.insertar_contribuyente("009","jac sas","juridica",)
#contribuyente.eliminar_contribuyente("009")
#contribuyente.modificar_datos_contribuyente("020", "vcd s.a.s", "juridico", )
#contribuyente.verificar_contribuyentes_asociados("004")
#contribuyente.modificar_id_contribuyente("003","004")
#contribuyente.verificar_contribuyente_existe("4654")

