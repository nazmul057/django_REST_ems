
from django.urls import path
from structures import views

urlpatterns = [
    # Department
    path("departments/", views.department_list_and_create, name="department-list-and-create"),
    path("departments/<int:pk>/", views.department_details_and_modifications, name="department-details-and-modifications"),

    # Employee
    path("employees/", views.employee_list_and_create, name="employee-list-and-create"),
    path("employees/<int:pk>/", views.employee_details_and_modifications, name="employee-details-and-modifications"),
]
