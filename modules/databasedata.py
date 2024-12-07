from sqlalchemy import create_engine
import configparser

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
