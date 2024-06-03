# Conexion con la Base de datos

import mysql.connector
from mysql.connector import Error
from api.config_db import db_config

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
