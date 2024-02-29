# from django_cron import CronJobBase, Schedule
# from django.core.mail import EmailMessage
# from django.conf import settings
# from .views import DailyReport
# import ssl
# from email.mime.base import MIMEBase
# from email import encoders
# import os
#
#
# class SendDailyReport(CronJobBase):
#     RUN_EVERY_MORNING = Schedule(run_every_mins=1440)
#
#     schedule = RUN_EVERY_MORNING
#     code = 'hr_send_daily_report'
#
#     def do(self):
#         context = ssl.create_default_context()
#         daily_report = DailyReport()
#         pdf_data = daily_report.generate_pdf_report(context={'ssl_context': context})
#         attachments = [('Daily_report.pdf', pdf_data, 'application/pdf')]
#
#         subject = 'Ежедневный отчет'
#         message = 'Добрый день! Вам прикреплен ежедневный отчет.'
#         recipient_list = ['sanjarwer93@gmail.com']
#
#         email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
#
#         for file_name, content, content_type in attachments:
#             mime_attachment = MIMEBase('application', 'octet-stream')
#             mime_attachment.set_payload(content)
#             encoders.encode_base64(mime_attachment)
#
#             mime_attachment.add_header('Content-Type', content_type)
#             mime_attachment.add_header('Content-Disposition', f'attachment; filename={file_name}')
#
#             email.attach(mime_attachment)
#
#         try:
#             email.send()
#         except Exception as e:
#             print(f'Ошибка при отправке ежедневного отчета: {e}')
#
#
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
#
# if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
#     settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#     settings.EMAIL_HOST = 'smtp-relay.brevo.com'
#     settings.EMAIL_PORT = 587
#     settings.EMAIL_USE_TLS = True
#     settings.EMAIL_HOST_USER = EMAIL_HOST_USER
#     settings.EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
#     cron_job = SendDailyReport()
#     cron_job.do()
# else:
#     print(
#         "Отсутствуют настройки для отправки электронной почты. Пожалуйста, укажите EMAIL_HOST_USER и EMAIL_HOST_PASSWORD в файле .env.")
