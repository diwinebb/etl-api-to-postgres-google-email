import gspread
from pathlib import Path
import logging

class GoogleLoader:
    def __init__(self, data, spreadsheet_name):
        self.BASE_DIR = Path(__file__).resolve().parent
        self.creds_path = self.BASE_DIR / 'credentials.json'
        self.gc = gspread.service_account(filename=self.creds_path)
        self.sh = self.gc.open(spreadsheet_name)
        self.data = data
        self.logger = logging.getLogger(f"Grader.{__name__}")

    def export_metrics(self):
        self.logger.info("Начинается выгрузка в Google Таблицу...")
        try:
            worksheet = self.sh.get_worksheet(0)
            worksheet.clear()
            
            worksheet.update(range_name='A1', values=self.data)
            
            self.logger.info("Выгрузка в Google Таблицу прошла успешно")
        except Exception as e:
            self.logger.exception(f"Ошибка при выгрузке в Google Таблицы: {e}")
