import smtplib
import ssl
from email.message import EmailMessage
import os
import logging

class EmailSender:
    def __init__(self, data, control_date):
        self.data = data
        self.control_date = control_date
        self.smtp_server = "smtp.gmail.com"
        self.port = 465
        self.sender_email = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.receiver_email = os.getenv("EMAIL_RECEIVER")
        self.logger = logging.getLogger(f"Grader.{__name__}")

    def _format_html(self):
        style = """
        <style>
            table { border-collapse: collapse; width: 100%; max-width: 500px; font-family: Arial, sans-serif; }
            th { background-color: #4CAF50; color: white; text-align: left; padding: 10px; }
            td { border: 1px solid #ddd; padding: 8px; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .header { font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #333; }
        </style>
        """
        
        rows_html = ""
        for i, row in enumerate(self.data[1:]):
            # Если индекс четный, добавляем серый фон прямо в тег
            bg_color = 'background-color: #f2f2f2;' if i % 2 == 0 else ''
            
            rows_html += f"""
                <tr style="{bg_color}">
                    <td style="border: 1px solid #ddd; padding: 8px;">{row[0]}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;"><b>{row[1]}</b></td>
                </tr>
            """

        html_body = f"""
        <html>
            <head>{style}</head>
            <body>
                <div class="header">Отчет ETL за {self.control_date}</div>
                <table>
                    <tr>
                        <th>Показатель</th>
                        <th>Значение</th>
                    </tr>
                    {rows_html}
                </table>
                <p style="color: #777; font-size: 12px;">Это автоматическое уведомление системы Grader.</p>
            </body>
        </html>
        """
        return html_body

    def send_msg(self):
        msg = EmailMessage()
        msg.set_content(f"Данные за {self.control_date}: {self.data}")
        msg.add_alternative(self._format_html(), subtype='html')
        msg['Subject'] = f"Отчёт ETL: {self.control_date}"
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                server.login(self.sender_email, self.password)
                server.send_message(msg)
            self.logger.info("Письмо успешно отправлено!")
        except Exception as e:
            self.logger.exception(f"Ошибка при отправке почты: {e}")


