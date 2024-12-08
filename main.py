import pandas as pd
import os
import configparser
from modules.exporters import generar_csv_clientes, generar_csv_facturas
from modules.database import leer_datos_clientes
from test.tests import generar_dataframe_prueba_clientes, generar_dataframe_prueba_facturas
from utils.utiles import generar_fichero_zip
import sys


def main():
    # Leer configuración desde el archivo .INI
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Recuperar parámetros
    siret_code = config["GENERAL"].get("siret_code")
    output_directory = config["GENERAL"].get("output_directory", "data")
    error_file = config["GENERAL"].get("error_file", "errors.csv")

    # Crear la carpeta si no existe
    os.makedirs(output_directory, exist_ok=True)
   
    # Leer datos de clientes desde la base de datos
    df_clientes = leer_datos_clientes()
    # # Generar datos de prueba para clientes
    # df_clientes = generar_dataframe_prueba_clientes()

    # Agregar el código SIRET a todos los registros de clientes
    if siret_code:
        df_clientes["siret"] = siret_code

    # Rutas de salida
    ruta_salida_clientes = os.path.join(output_directory, "clients.csv")
    ruta_archivo_errores = os.path.join(output_directory, error_file)

    # Generar el archivo CSV de clientes
    generar_csv_clientes(df_clientes, ruta_salida_clientes, ruta_archivo_errores)

    # Generar datos de prueba para facturas
    df_facturas = generar_dataframe_prueba_facturas()

    # Agregar el código SIRET a todos los registros de facturas
    if siret_code:
        df_facturas["SIRET"] = siret_code

    # Generar el archivo CSV de facturas
    ruta_salida_facturas = os.path.join(output_directory, "factures.csv")
    generar_csv_facturas(df_facturas, ruta_salida_facturas)

    # Generar el archivo ZIP
    if siret_code:
        generar_fichero_zip(output_directory, siret_code)
    else:
        print("Error: No se encontró un código SIRET válido en la configuración.")

if __name__ == "__main__":
    main()
