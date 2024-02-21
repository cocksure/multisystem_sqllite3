from rest_framework import generics
from apps.hr import models
from apps.hr import serializers
from apps.shared.views import BaseListView
from .models import Employee, Department, Division, Position
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from weasyprint import HTML, CSS


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

class DailyReport(View):
    template_name = 'daily_report.html'

    def get(self, request):
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

        return render(request, self.template_name, context)

    @staticmethod
    def generate_pdf_report(template_name, context):
        template = get_template(template_name)
        html = template.render(context)

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

        pdf_data = HTML(string=html).write_pdf(stylesheets=[CSS(string=css)])

        return pdf_data


class EmployeePDFExportView(View):
    template_name = 'employee_info.html'

    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        context = {'employee': employee}

        if 'pdf' in request.GET:
            pdf_data = self.generate_pdf(context)
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = f'filename="{employee.full_name}_profile.pdf"'
            return response
        else:
            return render(request, self.template_name, context)

    def generate_pdf(self, context):
        template = get_template(self.template_name)
        html = template.render(context)

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

        pdf_data = HTML(string=html).write_pdf(stylesheets=[CSS(string=css)])

        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="employee_info.pdf"'
        return response
