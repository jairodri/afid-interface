from sqlalchemy import create_engine
import configparser
import pandas as pd
import sys
from utils.utiles import limpiar_separadores
from test.tests import generar_dataframe_prueba_clientes, generar_dataframe_prueba_facturas


def conectar_base_datos():
    """
    Establece una conexión a la base de datos Access usando SQLAlchemy.

    Retorna:
        sqlalchemy.engine.base.Connection: Objeto de conexión para realizar consultas.
    """
    # Leer configuración del archivo config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    db_path = config["DATABASE"].get("db_path")
    driver = config["DATABASE"].get("driver", "Microsoft Access Driver (*.mdb)")

    if not db_path:
        raise ValueError("El parámetro 'db_path' no está definido en config.ini")

    # Crear la cadena de conexión
    conn_str = (
        r"access+pyodbc:///?"
        r"odbc_connect=DRIVER={%s};DBQ=%s;"
    ) % (driver, db_path)

    # Crear el engine de SQLAlchemy
    engine = create_engine(conn_str)
    return engine.connect()


def leer_datos_clientes():
    """
    Recupera los datos de clientes desde un `JOIN` entre las tablas de clientes y vehículos,
    utilizando el mapeo configurado en config.ini.

    Retorna:
        pd.DataFrame: DataFrame con los datos necesarios.
    """
    # Leer configuración del archivo config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")

    if "CLIENTES" not in config:
        raise ValueError("La sección 'CLIENTES' no está definida en config.ini")

    # Recuperar las tablas y claves para el JOIN
    clientes_table = config["CLIENTES"].get("clientes_table")
    vehiculos_table = config["CLIENTES"].get("vehiculos_table")
    join_clientes_key = config["CLIENTES"].get("join_clientes_key")
    join_vehiculos_key = config["CLIENTES"].get("join_vehiculos_key")

    if not (clientes_table and vehiculos_table and join_clientes_key and join_vehiculos_key):
        raise ValueError("Los parámetros para las tablas y el JOIN no están completamente definidos en config.ini")

    # Construir el mapeo de campos
    field_map = {
        field: value for field, value in config.items("CLIENTES")
        if field not in ["clientes_table", "vehiculos_table", "join_clientes_key", "join_vehiculos_key"]
    }

    # Construir los campos para la consulta SQL
    campos_sql = ", ".join(
        [f"{valor} AS {campo}" if valor else f"NULL AS {campo}" for campo, valor in field_map.items()]
    )

    # Construir la consulta SQL con el JOIN
    query = f"""
        SELECT {campos_sql}
        FROM {clientes_table} AS c
        LEFT JOIN {vehiculos_table} AS v
        ON c.{join_clientes_key} = v.{join_vehiculos_key}
        ORDER BY c.{join_clientes_key}
    """

    # Conectar a la base de datos y ejecutar la consulta
    conn = conectar_base_datos()
    try:
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()

    # inicializar la columna personal_data con 0
    df['personal_data'] = '0'

    # Limpiar los separadores de la columna vehicle_registration
    df = limpiar_separadores(df, "vehicle_registration", [" ", "-", "_"])

    # inicializar la columna record_status con el valor 'Active'
    df['record_status'] = 'Active'

    return df


def leer_datos_facturas():
    """
    Recupera los datos de facturas desde un `JOIN` entre las tablas de facturas y clientes,
    utilizando el mapeo configurado en config.ini.

    Retorna:
        pd.DataFrame: DataFrame con los datos necesarios.
    """
    # Leer configuración del archivo config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")

    if "FACTURAS" not in config:
        raise ValueError("La sección 'FACTURAS' no está definida en config.ini")

    # Recuperar las tablas y claves para el JOIN
    facturas_table = config["FACTURAS"].get("facturas_table")

    if not (facturas_table):
        df = generar_dataframe_prueba_facturas()
        return df
        raise ValueError("Los parámetros para las tablas y el JOIN no están completamente definidos en config.ini")

    # Construir el mapeo de campos
    field_map = {
        field: value for field, value in config.items("FACTURAS")
        if field not in ["facturas_table"]
    }

    # Construir los campos para la consulta SQL
    campos_sql = ", ".join(
        [f"{valor} AS {campo}" if valor else f"NULL AS {campo}" for campo, valor in field_map.items()]
    )

    # Construir la consulta SQL con el JOIN
    query = f"""
        SELECT {campos_sql}
        FROM {facturas_table} AS f

    """

    # Conectar a la base de datos y ejecutar la consulta
    conn = conectar_base_datos()
    try:
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()

    return df

