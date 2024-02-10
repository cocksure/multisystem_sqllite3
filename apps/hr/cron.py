from django_cron import CronJobBase, Schedule
from django.core.mail import EmailMessage
from django.conf import settings
from .views import DailyReport
import ssl
from email.mime.base import MIMEBase
from email import encoders


class SendDailyReport(CronJobBase):
    RUN_EVERY_MORNING = Schedule(run_every_mins=1440)

    schedule = RUN_EVERY_MORNING
    code = 'hr_send_daily_report'

    def do(self):
        context = ssl.create_default_context()
        daily_report = DailyReport()
        pdf_data = daily_report.generate_pdf(context={'ssl_context': context})
        attachments = [('Daily_report.pdf', pdf_data, 'application/pdf')]

        subject = 'Ежедневный отчет'
        message = 'Добрый день! Вам прикреплен ежедневный отчет.'
        recipient_list = ['sanjarwer93@gmail.com']

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        for file_name, content, content_type in attachments:
            mime_attachment = MIMEBase('application', 'octet-stream')
            mime_attachment.set_payload(content)
            encoders.encode_base64(mime_attachment)

            mime_attachment.add_header('Content-Type', content_type)
            mime_attachment.add_header('Content-Disposition', f'attachment; filename={file_name}')

            email.attach(mime_attachment)

        try:
            email.send()
        except Exception as e:
            print(f'Ошибка при отправке ежедневного отчета: {e}')
