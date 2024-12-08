# afid_interface
Generate files for atelio fid interface


## Requisitos

- Python 3.x
- Librerías especificadas en `requirements.txt`

## Instalación

1. Clona el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd afid-interface
    ```

2. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Configuración

Configura el archivo `config.ini` con los parámetros necesarios:

```ini
[GENERAL]
siret_code = <CÓDIGO_SIRET>
output_directory = <DIRECTORIO_DE_SALIDA>
error_file_clientes = <ARCHIVO_DE_ERRORES_CLIENTES>

```

## Uso

Ejecuta el script principal:

```sh
python main.py

```

El script realizará las siguientes acciones:

1. Leer la configuración desde `config.ini`.
2. Crear el directorio de salida si no existe.
3. Leer datos de clientes y facturas desde la base de datos.
4. Generar archivos CSV para clientes y facturas.
5. Comprimir los archivos generados en un archivo ZIP.

## Estructura del Código

- `main.py`: Script principal que coordina la ejecución del proyecto.
- `modules/database.py`: Contiene funciones para leer datos de la base de datos.
- `modules/exporters.py`: Contiene funciones para generar archivos CSV.
- `utils/utiles.py`: Contiene funciones utilitarias, como la generación de archivos ZIP.
- `test/tests.py`: Contiene funciones para generar datos de prueba.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
```

