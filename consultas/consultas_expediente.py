from data_base.db_connector import BDConnector
import mysql.connector


class ConsultasExpediente:
    def __init__(self):
        self.connector = None

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
            query = "SELECT * FROM expediente WHERE id_expediente = %s"
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
            query = "SELECT * FROM expediente WHERE id_contribuyente = %s"
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
            query = "SELECT * FROM expediente WHERE id_auditor = %s"
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
            query = "SELECT * FROM expediente WHERE id_proceso = %s"
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
            query = "SELECT * FROM expediente WHERE id_prestamo IS NOT NULL"
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
            query = "SELECT * FROM expediente WHERE id_caja = %s"
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
            query = "SELECT * FROM expediente WHERE estado = %s"
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
            query = "SELECT * FROM expediente WHERE año_gravable = %s"
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

consultas = ConsultasExpediente()
#result = consultas.buscar_por_id_expediente("i010")
#result = consultas.buscar_por_id_contribuyente("020"
#result = consultas.buscar_por_id_auditor("A025")
#result = consultas.buscar_por_id_proceso("1")
#result = consultas.buscar_expedientes_prestados()
#result = consultas.buscar_por_id_caja("o111")
#result = consultas.buscar_por_estado("activo")
#result = consultas.buscar_por_año_gravable("2019")
#print(result)