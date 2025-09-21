from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from structures.models import Employee
from operations.models import Attendance, Performance
from operations.serializers import AttendanceSerializer, PerformanceSerializer
from common.helpers import SmallResultsSetPagination

# Create your views here.
# -------------------- Attendance --------------------
@api_view(["GET", "POST"])
def attendance_list_and_create(request):
    if request.method == "GET":
        # If employee id not provided, the query might be time consuming for big offsets through pagination
        # so, this can be kept for admin use only for now.
        qs = Attendance.objects.order_by("employee", "date")

        # Optional filters via query params
        employee_id = request.query_params.get("employee")
        if employee_id:
            qs = qs.filter(employee_id=employee_id)

        paginator = SmallResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = AttendanceSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == "POST":
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def attendance_details_and_modifications(request, pk: int):
    attd = get_object_or_404(Attendance, pk=pk)

    if request.method == "GET":
        return Response(AttendanceSerializer(attd).data)
    
    elif request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = AttendanceSerializer(attd, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        attd.delete()
        return Response(
            {"message": "Attendance record has been deleted successfully."},
            status=status.HTTP_200_OK
        )
        # return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


# -------------------- Performance --------------------
@api_view(["GET", "POST"])
def performance_list_and_create(request):
    if request.method == "GET":
        # If employee id not provided, the query might be time consuming for big offsets through pagination
        # so, this can be kept for admin use only for now.
        qs = Performance.objects.order_by("employee_id")

        # Optional filters via query params
        employee_id = request.query_params.get("employee")
        if employee_id:
            qs = qs.filter(employee_id=employee_id)

        paginator = SmallResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = PerformanceSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == "POST":
        serializer = PerformanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def performance_details_and_modifications(request, pk: int):
    pfmc = get_object_or_404(Performance, pk=pk)

    if request.method == "GET":
        return Response(PerformanceSerializer(pfmc).data)
    
    elif request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = PerformanceSerializer(pfmc, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        pfmc.delete()
        return Response(
            {"message": "Performance record has been deleted successfully."},
            status=status.HTTP_200_OK
        )
        # return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
