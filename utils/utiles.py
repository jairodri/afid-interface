import datetime
import zipfile
import os


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