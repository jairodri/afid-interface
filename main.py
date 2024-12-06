import pandas as pd
import os
from modules.exportfiles import generar_csv_clientes  

def main():
    # Simular un DataFrame con datos de ejemplo
    datos_clientes = {
        "SIRET": ["12345678901234", "abcdefghij1234"],
        "Customer ID": ["CUST001", None],
        "Customer title": ["Mr", "Ms"],
        "Vehicle registration": ["123ABC", "ABC-123"],
        "Personal data": [31, None],
    }
    df_clientes = pd.DataFrame(datos_clientes)

    # Definir la ruta de salida
    ruta_salida = "data/clients.csv"

    # Crear la carpeta si no existe
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    # Llamar a la función de generación del CSV
    generar_csv_clientes(df_clientes, ruta_salida)

if __name__ == "__main__":
    main()
