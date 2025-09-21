from django.urls import path
from operations import views

urlpatterns = [
    # Attendance
    path("attendance/", views.attendance_list_and_create, name="attendance-list-and-create"),
    path("attendance/<int:pk>/", views.attendance_details_and_modifications, name="attendance-details-and-modifications"),

    # Performance
    path("performance/", views.performance_list_and_create, name="performance-list-and-create"),
    path("performance/<int:pk>/", views.performance_details_and_modifications, name="performance-details-and-modifications"),
]
