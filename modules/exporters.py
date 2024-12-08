import pandas as pd
import os
import csv  
import re

def generar_csv_clientes(df, output_path, error_file_path):
    """
    Genera el fichero clients.csv basado en las especificaciones y un archivo de errores.

    Parámetros:
    - df: DataFrame de Pandas con los datos de clientes.
    - output_path: Ruta de salida para guardar el archivo clients.csv.
    - error_file_path: Ruta de salida para guardar el archivo de errores.
    """
    columnas_requeridas = {
        "siret": {"obligatorio": True, "longitud": 14},
        "customer_id": {"obligatorio": True},
        "customer_title": {"obligatorio": False},
        "customer_name": {"obligatorio": False},
        "customer_address_1": {"obligatorio": False},
        "customer_address_2": {"obligatorio": False},
        "customer_address_3": {"obligatorio": False},
        "customer_post_code": {"obligatorio": False},
        "customer_city": {"obligatorio": False},
        "customer_home_phone": {"obligatorio": False},
        "customer_office_phone": {"obligatorio": False},
        "customer_mobile_phone": {"obligatorio": False},
        "customer_email": {"obligatorio": False},
        "personal_data": {"obligatorio": True},
        "vehicle_registration": {"obligatorio": True},
        "vin": {"obligatorio": False},
        "km": {"obligatorio": False},
        "last_visit": {"obligatorio": False},
        "last_mot": {"obligatorio": False},
        "next_mot": {"obligatorio": False},
        "last_emission_test": {"obligatorio": False},
        "next_emission_test": {"obligatorio": False},
        "record_status": {"obligatorio": False},
    }

    # Verificar y completar columnas faltantes
    for columna in columnas_requeridas.keys():
        if columna not in df.columns:
            df[columna] = None  # Rellenar con valores vacíos

    valores_titulo_permitidos = {"Mr", "Mrs", "Miss", "Company"}

    def es_email_valido(email):
        """Valida el formato de un email. Devuelve True si el email está vacío o tiene un formato válido."""
        if pd.isna(email) or str(email).strip() == "":
            return True  # Considerar como válido si está vacío o tiene solo blancos
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))


    def validar_fila(fila):
        errores = []
        for columna, reglas in columnas_requeridas.items():
            if reglas["obligatorio"] and pd.isna(fila[columna]):
                errores.append(f"Campo obligatorio '{columna}' está vacío.")
            if columna == "siret" and not pd.isna(fila[columna]):
                if len(str(fila[columna])) != 14 or not str(fila[columna]).isalnum():
                    errores.append(f"El campo 'SIRET' debe tener exactamente 14 caracteres alfanuméricos.")
            if columna == "vehicle_registration" and not pd.isna(fila[columna]):
                if any(sep in str(fila[columna]).strip() for sep in [" ", "-", "_"]):
                    errores.append(f"El campo 'Vehicle registration' no debe contener separadores: {fila['vehicle_registration']}.")

        # Validaciones adicionales
        if not pd.isna(fila["customer_title"]) and fila["customer_title"] not in valores_titulo_permitidos:
            errores.append(f"El campo 'Customer title' contiene un valor no permitido: {fila['customer_title']}.")
        if not pd.isna(fila["customer_email"]) and not es_email_valido(fila["customer_email"]):
            errores.append(f"El campo 'Customer email' no tiene un formato válido: {fila['customer_email']}.")
        campos_contacto = [
            fila["customer_home_phone"],
            fila["customer_office_phone"],
            fila["customer_mobile_phone"],
            fila["customer_email"],
        ]
        if all(pd.isna(campo) for campo in campos_contacto):
            errores.append("Debe haber al menos un campo de contacto relleno (teléfono o email).")
        if not pd.isna(fila["vin"]) and len(str(fila["vin"]).strip()) > 0 and len(str(fila["vin"])) != 17:
            errores.append(f"El campo 'VIN' debe tener exactamente 17 caracteres: {fila['vin']}.")
        return errores

    df_validado = df.copy()
    errores = []

    for index, fila in df_validado.iterrows():
        errores_fila = validar_fila(fila)
        if errores_fila:
            errores.append({
                "Índice": index,
                "Customer ID": fila.get("customer_id", "N/A"),
                "Errores": errores_fila,
            })
            df_validado.drop(index, inplace=True)

    if errores:
        # Crear el archivo de errores
        with open(error_file_path, "w", encoding="utf-8-sig") as error_file:
            error_file.write("Customer ID;Errores\n")
            for error in errores:
                error_file.write(f"{error['Customer ID']};{' | '.join(error['Errores'])}\n")
        print(f"Archivo de errores generado en {error_file_path}")

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
