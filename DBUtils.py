import psycopg2
import logging
import os
from psycopg2 import OperationalError

class DBConnector:
    def __init__(self):
        self.logger = logging.getLogger(f"Grader.{__name__}")

    def get_conn(self):
        self.logger.info(f"Пробую установить соединение с БД - {os.getenv('PG_DB')}")
        try:
            conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            dbname=os.getenv("PG_DB"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD")
            )
            return conn
        
        except OperationalError as e:
            self.logger.exception(f'Не удалось подключиться к БД: {e}')

