import mysql.connector
from mysql.connector import Error
import pandas as pd
import os


def load_data_from_excel_to_mysql(excel_file_path, sheet_name, table_name):
    connection = None
    cursor = None
    temp_csv_path = None

    try:
        # Verificar que el archivo existe
        if not os.path.exists(excel_file_path):
            raise FileNotFoundError(f"El archivo {excel_file_path} no existe.")

        # Leer los datos de la hoja de Excel
        try:
            data = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        except Exception as e:
            raise ValueError(f"Error al leer la hoja {sheet_name} del archivo Excel: {e}")

        # Convertir el DataFrame a CSV temporal en la ruta permitida
        secure_file_priv_path = 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads'
        temp_csv_path = os.path.join(secure_file_priv_path, f'temp_{sheet_name}.csv')
        data.to_csv(temp_csv_path, index=False, sep=',', lineterminator='\n')

        # Verificar que el archivo CSV temporal se ha creado
        if not os.path.exists(temp_csv_path):
            raise FileNotFoundError(f"No se pudo crear el archivo CSV temporal en {temp_csv_path}")

        # Conectar a la base de datos
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1693',
            database='Archivo_DB',
            allow_local_infile=True
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Permitir la carga de archivos locales si es necesario
            cursor.execute("SET GLOBAL local_infile = 1;")

            # Cambiar a la base de datos deseada
            cursor.execute("USE Archivo_DB;")

            # Comando para cargar los datos desde el archivo CSV temporal
            load_data_query = """
            LOAD DATA LOCAL INFILE '{}'
            INTO TABLE {}
            FIELDS TERMINATED BY ','
            ENCLOSED BY '"'
            LINES TERMINATED BY '\n'
            IGNORE 1 ROWS
            """.format(temp_csv_path.replace("\\", "/"), table_name)

            cursor.execute(load_data_query)
            connection.commit()
            print(f"Datos cargados exitosamente en la tabla {table_name} desde la hoja {sheet_name}")

            # Verificar si se insertaron filas en la tabla
            if cursor.rowcount > 0:
                print(f"Datos cargados exitosamente en la tabla {table_name} desde la hoja {sheet_name}")
            else:
                print(f"No se insertaron datos en la tabla {table_name} desde la hoja {sheet_name}")


    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as ve:
        print(ve)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Conexión a MySQL cerrada")

        # Eliminar el archivo CSV temporal
        if os.path.exists(temp_csv_path):
            os.remove(temp_csv_path)


if __name__ == "__main__":
    # Ajusta la ruta del archivo a una ubicación accesible
    excel_file_path = 'D:\PROYECTO CRUD ARCHIVO FISCALIZACION\data auditores\carga_datos.xlsx'

    # Cargar datos desde diferentes hojas de Excel en diferentes tablas
    load_data_from_excel_to_mysql(excel_file_path, 'Auditores', 'auditor')
    load_data_from_excel_to_mysql(excel_file_path, 'Contribuyentes', 'contribuyente')
    load_data_from_excel_to_mysql(excel_file_path, 'Expedientes', 'expediente')