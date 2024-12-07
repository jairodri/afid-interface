import pandas as pd
import os
from modules.exportfiles import generar_csv_clientes  
from test.tests import generar_dataframe_prueba_clientes

def main():
    # Simular un DataFrame con datos de ejemplo
    df_prueba = generar_dataframe_prueba_clientes()
    df_clientes = pd.DataFrame(df_prueba)

    # Definir la ruta de salida
    ruta_salida = "data/clients.csv"

    # Crear la carpeta si no existe
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    # Llamar a la función de generación del CSV
    generar_csv_clientes(df_clientes, ruta_salida)

if __name__ == "__main__":
    main()
