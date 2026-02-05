import logging
import pandas as pd
import ast
import hashlib
from io import StringIO

class Transformer:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.logger = logging.getLogger(f"Grader.{__name__}")
        self.final_df = None

    def safe_parse(self, x):
        try:
            if isinstance(x, str) and x.strip():
                return ast.literal_eval(x)
        except:
            pass
        return {}
    
    def generate_hash(self, row):
        dt_str = row["created_at"].strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(row["created_at"]) else "None"
        payload = f'{row["user_id"]}{row["attempt_type"]}{dt_str}'
        return hashlib.sha256(payload.encode()).hexdigest()

    def transform(self):
        if not self.raw_data:
            self.logger.error(f"Нет данных для обработки")
            return None
        
        self.logger.info(f"Данные получены, начинается обработка")
        try:
            df = pd.read_json(StringIO(self.raw_data))
            params_df = pd.json_normalize(df['passback_params'].apply(self.safe_parse))
            df = pd.concat([df.drop(columns=['passback_params']), params_df], axis=1)

            self.final_df = pd.DataFrame()
            self.final_df['user_id'] = df['lti_user_id'].fillna('').astype(str)
            self.final_df['oauth_consumer_key'] = df['oauth_consumer_key'].fillna('').astype(str)
            self.final_df['lis_result_sourcedid'] = df['lis_result_sourcedid'].fillna('').astype(str)
            self.final_df['lis_outcome_service_url'] = df['lis_outcome_service_url'].fillna('').astype(str)
            self.final_df['is_correct'] = pd.to_numeric(df['is_correct'], errors='coerce').astype('Int64')
            self.final_df['attempt_type'] = df['attempt_type'].fillna('').astype(str)
            self.final_df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
            self.final_df['hash'] = self.final_df.apply(self.generate_hash, axis=1)
            return True
        
        except Exception as e:
            self.logger.exception(f"Ошибка обработки полученных данных: {e}")
            return False
        
    def get_db_file(self):
        if self.final_df is None or self.final_df.empty: 
            return None

        db_data_values = self.final_df.values.tolist()
        db_data = [
            tuple(None if pd.isna(item) else item for item in row)
            for row in db_data_values
        ]
        self.logger.info(f"Данные для БД обработаны успешно. К загрузке подготовлено {len(self.final_df)} строк.")
        return db_data
    
    def get_google_file(self, control_date):
        if self.final_df is None: return None

        attempts_per_user = self.final_df.groupby('user_id')['user_id'].count()

        median_attempts = attempts_per_user.median()

        metrics = {
            'Попыток совершено': int(len(self.final_df)),
            'Успешных попыток': int(self.final_df['is_correct'].sum()),
            '% успешных попыток': f"{float((self.final_df['is_correct'].mean() * 100)):.2f}%",
            'Уникальных юзеров': int(self.final_df['user_id'].nunique()),
            'Медианное кол-во попыток на юзера': f"{int(median_attempts):.2f}",
            'Контрольная дата': str(control_date)
        }
        metrics_df = pd.DataFrame(list(metrics.items()), columns=['Показатель', 'Значение'])

        headers = metrics_df.columns.values.tolist()
        data_rows = metrics_df.values.tolist()
        gog_data = [headers] + data_rows
        self.logger.info(f"Данные для Гугл таблицы обработаны успешно. К загрузке подготовлено {len(metrics_df)} строк.")
        return gog_data
