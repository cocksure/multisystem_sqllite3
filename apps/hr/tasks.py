# import smtplib
# import ssl
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# from .views import DailyReport
# from multisys import settings
# from multisys.celery import app
# from celery.utils.log import get_task_logger
#
# logger = get_task_logger(__name__)
#
#
# def send_email(subject, message, recipient_list, attachment_data, attachment_filename):
#     # Create a MIME object
#     msg = MIMEMultipart()
#     msg['From'] = 'sanjar@multisystem.online'
#     msg['To'] = ', '.join(recipient_list)
#     msg['Subject'] = subject
#
#     # Attach the message
#     msg.attach(MIMEBase('application', 'octet-stream'))
#     msg.attach(MIMEBase('application', 'pdf'))
#
#     # Attach the attachment
#     attachment = MIMEBase('application', 'octet-stream')
#     attachment.set_payload(attachment_data)
#     encoders.encode_base64(attachment)
#     attachment.add_header('Content-Disposition', f'attachment; filename="{attachment_filename}"')
#     msg.attach(attachment)
#
#     # Send the email
#     with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
#         server.starttls(context=ssl.create_default_context())
#         server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
#         server.sendmail('sanjar@multisystem.online', recipient_list, msg.as_string())
#
#
# @app.task
# def send_daily_report(subject, message, recipient_list):
#     context = ssl.create_default_context()
#     daily_report = DailyReport()
#     pdf_data = daily_report.generate_pdf_report(context={'ssl_context': context})
#     send_email(subject, message, recipient_list, pdf_data, 'Daily_report.pdf')
#     logger.info('Daily report sent successfully.')
#
#
# recipient_list = ['sanjarwer93@gmail.com']
# subject = 'Ежедневный отчет'
# message = 'Добрый день! Вам прикреплен ежедневный отчет.'
#
# send_daily_report.delay(subject, message, recipient_list)
