from django.urls import path
from operations import views

urlpatterns = [
    # Attendance
    # URL query samples
    # curl -X GET "http://127.0.0.1:8000/api-operations/attendance/?employee=2&page=1&page_size=20" # Filter by employee
    path("attendance/", views.attendance_list_and_create, name="attendance-list-and-create"),
    path("attendance/<int:pk>/", views.attendance_details_and_modifications, name="attendance-details-and-modifications"),

    # Performance
    # URL query samples
    # http://127.0.0.1:8000/api-operations/performance/?employee=2&page=1&page_size=20 # Filter by employee
    path("performance/", views.performance_list_and_create, name="performance-list-and-create"),
    path("performance/<int:pk>/", views.performance_details_and_modifications, name="performance-details-and-modifications"),
]
