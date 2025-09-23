
from django.urls import path
from structures import views

urlpatterns = [
    # Department
    # URL query samples
    # http://127.0.0.1:8000/api-structures/departments/?page=1&page_size=2 
    path("departments/", views.department_list_and_create, name="department-list-and-create"),
    path("departments/<int:pk>/", views.department_details_and_modifications, name="department-details-and-modifications"),
    path("reports/employees-per-department/", views.employees_per_department_chart, name="employees_per_department_pie"),

    # Employee
    path("employees/", views.employee_list_and_create, name="employee-list-and-create"),
    path("employees/<int:pk>/", views.employee_details_and_modifications, name="employee-details-and-modifications"),
    path("employees/filters/", views.employees_query_filters, name="employees-query-filters"),
    path("reports/attendance/monthly/<int:employee_id>/", views.employee_monthly_attendance, name="employee_monthly_attendance"),
]
