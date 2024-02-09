# import smtplib
# import ssl
# from celery.utils.log import get_task_logger
# from datetime import datetime, timedelta
# from django.conf import settings
# from django.core.mail import EmailMessage
# from django.utils import timezone
# from weasyprint import HTML, CSS
#
# from multisys.celery import app
# from .views import DailyReport
#
# logger = get_task_logger(__name__)
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = settings.EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD = settings.EMAIL_HOST_PASSWORD


# @app.task
# def send_daily_report(subject, message, recipient_list):
#     now = timezone.now()
#     nine_am_today = now.replace(hour=12, minute=52, second=0, microsecond=0)
#
#     if now >= nine_am_today:
#         daily_report = DailyReport()
#         pdf_data = daily_report.generate_pdf()
#         email = EmailMessage(
#             subject,
#             message,
#             'multisystemdb@gmail.com',
#             recipient_list,
#         )
#         email.attach('Daily_report.pdf', pdf_data, 'application/pdf')
#         email.send()
#         logger.info('Daily report sent successfully.')
#     else:
#         logger.info('Not the right time for the daily report.')
# @app.task
# def send_daily_report(subject, message, recipient_list):
#     now = timezone.now()
#     nine_am_today = now.replace(hour=12, minute=52, second=0, microsecond=0)
#     context = ssl.create_default_context()
#     daily_report = DailyReport()
#     pdf_data = daily_report.generate_pdf(context={'ssl_context': context})
#
#     email = EmailMessage(
#         subject,
#         message,
#         'multisystemdb@gmail.com',
#         recipient_list,
#     )
#     email.attach('Daily_report.pdf', pdf_data, 'application/pdf')
#     email.send()
#     logger.info('Daily report sent successfully.')
#
#     with smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_PORT) as server:
#         server.starttls(context=context)
#         server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#         server.send_message(email)
#
#
# recipient_list = ['sanjarwer93@gmail.com']
# subject = 'Ежедневный отчет'
# message = 'Добрый день! Вам прикреплен ежедневный отчет.'
#
# send_daily_report.delay(subject, message, recipient_list)
import base64
import os
import sib_api_v3_sdk
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from sib_api_v3_sdk import SendSmtpEmail, ApiClient, TransactionalEmailsApi
from sib_api_v3_sdk.configuration import Configuration

from multisys.celery import app
from .views import DailyReport

logger = get_task_logger(__name__)

from multisys import settings

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = settings.API_KEY
configuration.api_key['partner-key'] = settings.PARTNER_KEY

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


@app.task
def send_daily_report(subject, message, recipient_list):
    divisions = Division.objects.all()
    departments = Department.objects.all()
    positions = Position.objects.all()
    employees = Employee.objects.all()

    context = {
        'divisions': divisions,
        'departments': departments,
        'positions': positions,
        'employees': employees,
    }

    pdf_data = generate_pdf(context)
    filename = f'daily_report_{datetime.now().strftime("%Y-%m-%d")}.pdf'

    subject = 'Daily Report PDF'
    message = 'Please find attached the daily report PDF.'
    from_email = settings.EMAIL_HOST_USER
    to_email = ['recipient@example.com']  # Replace with recipient email
    attachment = (filename, pdf_data, 'application/pdf')

    send_mail(subject, message, from_email, to_email, fail_silently=False, attachments=[attachment])


def generate_pdf(context):
    template_name = 'daily_report.html'
    template = render_to_string(template_name, context)

    css = """
        @page {
            size: A4;
            margin: 1cm;
        }
        body {
            font-size: 12pt;
            line-height: 1.6;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        """

    pdf_data = HTML(string=template).write_pdf(stylesheets=[CSS(string=css)])

    return pdf_data


recipient_list = ['sanjarwer93@gmail.com']
subject = 'Ежедневный отчет'
message = 'Добрый день! Вам прикреплен ежедневный отчет.'

send_daily_report.delay(subject, message, recipient_list)
