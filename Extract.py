import requests
import logging

class Extractor:
    def __init__(self, api_url, params=None):
        self.api_url = api_url
        self.params = params
        self.logger = logging.getLogger(f"Grader.{__name__}")

    def get_raw_data(self):
        self.logger.info(f"Попытка получения данных по API - {self.api_url} за период с {self.params['start']} по {self.params['end']}")
        try:
            r = requests.get(self.api_url, params=self.params, timeout=(15, 120)) 
            if r.status_code == 200:
                self.logger.info('Данные получены успешно')
                return r.text
            else:
                self.logger.error(f"Ошибка API. Код - {r.status_code}. Ответ - {r.text}")
                r.raise_for_status

        except requests.exceptions.RequestException as e:
            self.logger.exception(f'Ошибка получения данных по API: {e}')
            return None