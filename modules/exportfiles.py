import pandas as pd
import os

def generar_csv_clientes(df, output_path):
    """
    Genera el fichero clients.csv basado en las especificaciones.

    Parámetros:
    - df: DataFrame de Pandas con los datos de clientes.
    - output_path: Ruta de salida para guardar el archivo clients.csv.
    """
    columnas_requeridas = {
        "SIRET": {"obligatorio": True, "longitud": 14},
        "Customer ID": {"obligatorio": True},
        "Customer title": {"obligatorio": False},
        "Customer name": {"obligatorio": False},
        "Customer address 1": {"obligatorio": False},
        "Customer address 2": {"obligatorio": False},
        "Customer address 3": {"obligatorio": False},
        "Customer post code": {"obligatorio": False},
        "Customer city": {"obligatorio": False},
        "Customer home phone": {"obligatorio": False},
        "Customer office phone": {"obligatorio": False},
        "Customer mobile phone": {"obligatorio": False},
        "Customer email": {"obligatorio": False},
        "Personal data": {"obligatorio": True},
        "Vehicle registration": {"obligatorio": True},
        "VIN": {"obligatorio": False},
        "Km": {"obligatorio": False},
        "Last visit": {"obligatorio": False},
        "Last MOT": {"obligatorio": False},
        "Next MOT": {"obligatorio": False},
        "Last emission test": {"obligatorio": False},
        "Next emission test": {"obligatorio": False},
        "Record status": {"obligatorio": False},
    }

    def validar_fila(fila):
        errores = []
        for columna, reglas in columnas_requeridas.items():
            if reglas["obligatorio"] and pd.isna(fila[columna]):
                errores.append(f"Campo obligatorio '{columna}' está vacío.")
            if columna == "SIRET" and not pd.isna(fila[columna]):
                if len(str(fila[columna])) != 14 or not str(fila[columna]).isalnum():
                    errores.append(f"El campo 'SIRET' debe tener exactamente 14 caracteres alfanuméricos.")
            if columna == "Vehicle registration" and not pd.isna(fila[columna]):
                if any(sep in str(fila[columna]) for sep in [" ", "-", "_"]):
                    errores.append(f"El campo 'Vehicle registration' no debe contener separadores.")
        return errores

    df_validado = df.copy()
    errores = []
    for index, fila in df_validado.iterrows():
        errores_fila = validar_fila(fila)
        if errores_fila:
            errores.append({"Índice": index, "Errores": errores_fila})
            df_validado.drop(index, inplace=True)

    if errores:
        print("Se encontraron las siguientes filas con errores y se omitieron del archivo generado:")
        for error in errores:
            print(f"Índice: {error['Índice']}, Errores: {error['Errores']}")

    columnas_finales = list(columnas_requeridas.keys())
    df_validado[columnas_finales].to_csv(output_path, sep=";", index=False, encoding="utf-8-sig")
    print(f"Archivo 'clients.csv' generado correctamente en {output_path}.")
