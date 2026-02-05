from psycopg2.extras import execute_values
import logging

class DBLoader:
    def __init__(self, transformed_data, conn):
        self.transformed_data = transformed_data
        self.conn = conn
        self.logger = logging.getLogger(f"Grader.{__name__}")

    def load_data(self):
        self.logger.info(f"Начинается загрузка данных в БД")
        try:
            with self.conn.cursor() as cur:
                query = """
                        insert into data.final_project
                        (
                        user_id, oauth_consumer_key, lis_result_sourcedid, lis_outcome_service_url, is_correct, attempt_type, created_at, hash
                        )
                        values %s
                        on conflict (hash) do nothing;
                        """
                execute_values(cur, query, self.transformed_data)
                added_values = cur.rowcount

            self.logger.info(f'Загрузка в БД завершена успешно. Новых записей: {added_values}')
            self.conn.commit()

        except Exception as e:
            self.logger.exception(f'Ошибка загрузки в БД: {e}')
            self.conn.rollback()
            