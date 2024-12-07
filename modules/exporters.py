import pandas as pd
import os
import csv  
import re

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

    # Verificar y completar columnas faltantes
    for columna in columnas_requeridas.keys():
        if columna not in df.columns:
            df[columna] = None  # Rellenar con valores vacíos

    valores_titulo_permitidos = {"Mr", "Mrs", "Miss", "Company"}

    def es_email_valido(email):
        """Valida el formato de un email."""
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

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

        # Validaciones adicionales
        if not pd.isna(fila["Customer title"]) and fila["Customer title"] not in valores_titulo_permitidos:
            errores.append(f"El campo 'Customer title' contiene un valor no permitido: {fila['Customer title']}.")
        if not pd.isna(fila["Customer email"]) and not es_email_valido(fila["Customer email"]):
            errores.append(f"El campo 'Customer email' no tiene un formato válido: {fila['Customer email']}.")
        campos_contacto = [
            fila["Customer home phone"],
            fila["Customer office phone"],
            fila["Customer mobile phone"],
            fila["Customer email"],
        ]
        if all(pd.isna(campo) for campo in campos_contacto):
            errores.append("Debe haber al menos un campo de contacto relleno (teléfono o email).")
        if not pd.isna(fila["VIN"]) and len(str(fila["VIN"])) != 17:
            errores.append(f"El campo 'VIN' debe tener exactamente 17 caracteres: {fila['VIN']}.")
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
    df_validado[columnas_finales].to_csv(
        output_path,
        sep=";",
        index=False,
        encoding="utf-8-sig",
        quoting=csv.QUOTE_ALL,
        quotechar='"'
    )
    print(f"Archivo 'clients.csv' generado correctamente en {output_path}.")


def generar_csv_facturas(df, output_path):
    """
    Genera el fichero factures.csv basado en las especificaciones.

    Parámetros:
    - df: DataFrame de Pandas con los datos de facturas.
    - output_path: Ruta de salida para guardar el archivo factures.csv.
    """
    columnas_requeridas = {
        "SIRET": {"obligatorio": True, "longitud": 14},
        "Invoice ID": {"obligatorio": True},
        "Invoice date": {"obligatorio": True},
        "Invoice amount": {"obligatorio": False},
        "Vehicle registration": {"obligatorio": True},
        "Km": {"obligatorio": False},
        "VIN": {"obligatorio": False},
        "Customer ID": {"obligatorio": True},
        "Package code": {"obligatorio": False},
        "Package description": {"obligatorio": False},
        "Operation code": {"obligatorio": False},
        "Operation description": {"obligatorio": False},
        "Parts reference": {"obligatorio": False},
        "Parts brand": {"obligatorio": False},
        "Parts quantity": {"obligatorio": False},
        "Parts description": {"obligatorio": False},
    }

    def validar_fila(fila):
        errores = []
        # Validaciones generales
        for columna, reglas in columnas_requeridas.items():
            if reglas["obligatorio"] and pd.isna(fila[columna]):
                errores.append(f"Campo obligatorio '{columna}' está vacío.")
            if columna == "SIRET" and not pd.isna(fila[columna]):
                if len(str(fila[columna])) != 14 or not str(fila[columna]).isalnum():
                    errores.append(f"El campo 'SIRET' debe tener exactamente 14 caracteres alfanuméricos.")
            if columna == "Vehicle registration" and not pd.isna(fila[columna]):
                if any(sep in str(fila[columna]) for sep in [" ", "-", "_"]):
                    errores.append(f"El campo 'Vehicle registration' no debe contener separadores.")
            if columna == "VIN" and not pd.isna(fila[columna]):
                if len(str(fila[columna])) != 17:
                    errores.append(f"El campo 'VIN' debe tener exactamente 17 caracteres.")

        # Validación de Invoice date
        if not pd.isna(fila["Invoice date"]):
            try:
                pd.to_datetime(fila["Invoice date"], format="%Y-%m-%d")
            except ValueError:
                errores.append(f"El campo 'Invoice date' no tiene un formato válido: {fila['Invoice date']}.")

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

    # Asegurarse de que todas las columnas requeridas están presentes
    for columna in columnas_requeridas.keys():
        if columna not in df_validado.columns:
            df_validado[columna] = None  # Rellenar con valores vacíos si la columna falta

    columnas_finales = list(columnas_requeridas.keys())
    df_validado[columnas_finales].to_csv(
        output_path,
        sep=";",
        index=False,
        encoding="utf-8-sig",
        quoting=csv.QUOTE_ALL,
        quotechar='"'
    )
    print(f"Archivo 'factures.csv' generado correctamente en {output_path}.")
