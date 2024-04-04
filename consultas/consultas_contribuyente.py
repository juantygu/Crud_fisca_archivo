from data_base.db_connector import BDConnector
import mysql.connector


class ConsultasContribuyente:

    def __init__(self):
        self.connector = None

    def obtener_contribuyente(self, id_contribuyente=None, nombre_contribuyente=None):
        if id_contribuyente is None and nombre_contribuyente is None:
            print("Debe proporcionar al menos el ID, el nombre.")
            return "Debe proporcionar al menos el ID, el nombre.", None

        try:
            self.connector = BDConnector()
            query = "SELECT * FROM contribuyente WHERE"
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
            result = self.connector.fetch_one()

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
        try:
            self.connector = BDConnector()
            query = "SELECT * FROM contribuyente WHERE tipo = %s"
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
        try:
            self.connector = BDConnector()
            query = "SELECT * FROM contribuyente"
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

consulta = ConsultasContribuyente()
#contribuyentes = consulta.mostrar_contribuyentes()
#print(contribuyentes[1])
#contribuyente = consulta.obtener_contribuyente()
##print(contribuyentes[1])