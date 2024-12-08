import datetime
import zipfile
import os
import pandas as pd


def generar_fichero_zip(output_directory, siret_code):
    """
    Genera un archivo ZIP que contiene los ficheros CSV de clientes y facturas.

    Parámetros:
    - output_directory: Ruta del directorio donde se guardan los archivos CSV.
    - siret_code: Código SIRET que será parte del nombre del archivo ZIP.
    """
    # Obtener la fecha actual en formato YYYYMMDD
    fecha_actual = datetime.datetime.now().strftime("%Y%m%d")
    
    # Nombre del archivo ZIP
    nombre_zip = f"{fecha_actual}-{siret_code}.zip"
    ruta_zip = os.path.join(output_directory, nombre_zip)
    
    # Crear el archivo ZIP
    with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Agregar los archivos CSV al ZIP
        ruta_clientes = os.path.join(output_directory, "clients.csv")
        ruta_facturas = os.path.join(output_directory, "factures.csv")
        
        if os.path.exists(ruta_clientes):
            zipf.write(ruta_clientes, arcname="clients.csv")
        else:
            print(f"Advertencia: No se encontró el archivo {ruta_clientes}, no será incluido en el ZIP.")
        
        if os.path.exists(ruta_facturas):
            zipf.write(ruta_facturas, arcname="factures.csv")
        else:
            print(f"Advertencia: No se encontró el archivo {ruta_facturas}, no será incluido en el ZIP.")
    
    print(f"Archivo ZIP generado correctamente: {ruta_zip}")
    return ruta_zip


def limpiar_separadores(df, columna, separadores=["-"]):
    """
    Elimina los separadores especificados de los valores de una columna en un DataFrame.

    Parámetros:
    - df (pd.DataFrame): El DataFrame que contiene los datos.
    - columna (str): El nombre de la columna a limpiar.
    - separadores (list): Lista de separadores a eliminar (por defecto, ["-"]).

    Retorna:
        pd.DataFrame: El DataFrame con la columna limpia.
    """
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el DataFrame.")

    # Crear una expresión regular para los separadores
    separadores_regex = f"[{''.join(separadores)}]"

    # Limpiar la columna eliminando los separadores
    df[columna] = df[columna].astype(str).str.replace(separadores_regex, "", regex=True).replace("nan", None)

    return df
