from Extract import Extractor
from Transform import Transformer
from LoadDB import DBLoader
from LoadGoogle import GoogleLoader
from EmailSender import EmailSender
from DBUtils import DBConnector
from LoggerSettings import get_log
from dotenv import load_dotenv
import os
load_dotenv()
logger = get_log()

def pipe_run():
    api_url = os.getenv("API_URL")
    start_str = '2023-04-01 00:00:00'
    end_str = '2023-04-01 23:59:59'
    control_date = start_str.split()[0]
    params = {
        'client': os.getenv('CLIENT'),
        'client_key': os.getenv('CLIENT_KEY'),
        'start': start_str,
        'end': end_str
        }
    
    logger.info("-+-=-+-=-+-=-+-=-=-+-=-+-=-+-=-+-+-=-+-=-+-=-+-=-=-+-=-+-=-+-=-+- ЗАПУСК -+-=-+-=-+-=-+-=-=-+-=-+-=-+-=-+-+-=-+-=-+-=-+-=-=-+-=-+-=-+-=-+-")

    db = DBConnector()
    conn = None

    try:
        conn = db.get_conn()
        logger.info("Соединение с БД установлено.")

        raw_data = Extractor(api_url, params).get_raw_data()
        if not raw_data:
            logger.warning("Данные не получены из API. Завершение работы.")
            return
        
        transformer = Transformer(raw_data)
        if transformer.transform():
            db_data = transformer.get_db_file()
            try:
                if not db_data:
                    logger.warning("После трансформации данные для бд пусты. Завершение работы.")
                    return
                db_loader = DBLoader(db_data, conn)
                db_loader.load_data()

            except Exception as e:
                logger.info(f"Ошибка выгрузки в DB: {e}")
  
            google_data = transformer.get_google_file(control_date)
            try:  
                if not google_data:
                    logger.warning("Данные для Google Таблиц пусты. Пропускаю выгрузку.")

                else:
                    spreadsheet_name = 'FinalProjectTable'
                    google_loader = GoogleLoader(google_data, spreadsheet_name)
                    google_loader.export_metrics()
            except Exception as e:
                logger.exception(f"Ошибка выгрузки в Google Sheets: {e}")

            try:      
                if not google_data:
                    logger.warning("Данные для отправки письма пусты. Пропускаю выгрузку.")

                else:
                    EmailSender(google_data, control_date).send_msg()

            except Exception as e:
                logger.exception(f"Ошибка отправки письма: {e}")

    except Exception as e:
        logger.exception(f"Критическая ошибка в процессе: {e}")

    finally:
        if conn:
            conn.close()
            logger.info("Соединение с БД закрыто.")
            logger.info("-+-=-+-=-+-=-+-=-=-+-=-+-=-+-=-+-+-=-+-=-+-=-+-=-=-+-=-+-=-+-=-+- ЗАВЕРШЕНИЕ -+-=-+-=-+-=-+-=-=-+-=-+-=-+-=-+-+-=-+-=-+-=-+-=-=-+-=-+-=-+-=-+-")

if __name__ == '__main__':
    pipe_run()