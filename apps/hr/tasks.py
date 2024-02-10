import smtplib
import ssl
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
from .views import DailyReport

logger = get_task_logger(__name__)

@app.task
def send_daily_report(subject, message, recipient_list):
    context = ssl.create_default_context()
    daily_report = DailyReport()
    pdf_data = daily_report.generate_pdf(context={'ssl_context': context})
    attachments = {'Daily_report.pdf': ('application/pdf', pdf_data)}

    email = EmailMessage(subject, message, 'sanjar@multisystem.online', recipient_list)
    email.attachments = attachments

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls(context=context)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(email)
        logger.info('Daily report sent successfully.')
    except Exception as e:
        logger.error(f'Failed to send daily report: {e}')

recipient_list = ['sanjarwer93@gmail.com']
subject = 'Ежедневный отчет'
message = 'Добрый день! Вам прикреплен ежедневный отчет.'

send_daily_report.delay(subject, message, recipient_list)
