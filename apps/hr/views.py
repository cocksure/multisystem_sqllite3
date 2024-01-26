from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView

from apps.hr import models
from apps.hr import serializers
from apps.shared.views import BaseListView
from django.http import HttpResponse
from reportlab.pdfgen import canvas


# ------------------------------Employee-------------------------------------
class EmployeeListCreateView(generics.ListCreateAPIView, BaseListView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    filterset_fields = ['gender', 'department', 'position', 'is_fired']
    search_fields = ['full_name', '=report_card', '=badge_number', '=passport_pin']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EmployeeDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


# ------------------------------Employee----------------------------------------------

class DivisionsListCreateView(generics.ListCreateAPIView):
    queryset = models.Division.objects.all()
    serializer_class = serializers.DivisionSerializer
    search_fields = ['name']


class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    filterset_fields = ['divisions']
    search_fields = ['name', ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PositionListCreateView(generics.ListCreateAPIView):
    queryset = models.Position.objects.all()
    serializer_class = serializers.PositionSerializer

    search_fields = ['name', ]


# ------------------------------export pdf---------------------------------------------------


from django.conf import settings


from reportlab.lib.utils import ImageReader
import os


class ExportEmployeePDFView(APIView):
    def get(self, request, employee_id, *args, **kwargs):
        # Получаем объект сотрудника на основе предоставленного employee_id в URL
        employee = get_object_or_404(models.Employee, id=employee_id)

        # Создаем объект ответа с типом содержимого PDF
        response = HttpResponse(content_type='application/pdf')

        # Устанавливаем заголовок Content-Disposition для принудительного скачивания
        response['Content-Disposition'] = f'attachment; filename="{employee.full_name}_profile.pdf"'

        # Создаем документ PDF
        p = canvas.Canvas(response)

        # Устанавливаем начальные координаты (x, y) для размещения текста и изображения
        x_text = 100
        y_text = 800
        x_image = 400  # Позиция для изображения
        y_image = 750  # Позиция для изображения
        line_height = 20

        # Добавляем текст в документ
        p.drawString(x_text, y_text, 'Личная Информация')
        y_text -= line_height
        p.drawString(x_text, y_text, f'ФИО: {employee.full_name}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Пол: {employee.get_gender_display()}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Дата Рождения: {employee.date_of_birth}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Адрес: {employee.address}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Телефон: {employee.phone_number}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Email: {employee.email}')

        # Создаем объект ImageReader для изображения по умолчанию
        default_image_path = os.path.join(settings.MEDIA_ROOT, 'employee_photos', 'default-profile__picture.jpg')
        default_image_reader = ImageReader(default_image_path)

        # Добавляем изображение в документ
        p.drawInlineImage(default_image_reader, x_image, y_image, width=100, height=100)

        # Перемещаемся на следующую "страницу"
        y_text -= line_height * 3
        p.drawString(x_text, y_text, 'Информация о Трудоустройстве')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Отдел: {employee.department}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Должность: {employee.position}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Заработная плата: {employee.salary}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Дата приема на работу: {employee.date_of_hire}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Дата увольнения: {employee.date_of_fire}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Пользователь: {employee.user}')

        # Перемещаемся на следующую "страницу"
        y_text -= line_height * 3
        p.drawString(x_text, y_text, 'Информация о Документах')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Табельный номер: {employee.report_card}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Серия и номер паспорта: {employee.passport_number_series}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Выдан: {employee.passport_issued_by}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'Дата выдачи: {employee.passport_when_issued}')
        y_text -= line_height
        p.drawString(x_text, y_text, f'ПИН: {employee.passport_pin}')

        # Сохраняем документ PDF
        p.showPage()
        p.save()

        return response
