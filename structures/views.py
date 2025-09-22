from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny # IsAuthenticated

from structures.models import Department, Employee
from structures.serializers import DepartmentSerializer, EmployeeSerializer
from common.helpers import SmallResultsSetPagination

# -------------------- Department --------------------
@api_view(["GET", "POST"])
# @permission_classes([AllowAny]) # Default is restricted set up in settings.py. For explicit restriction, use: @permission_classes([AllowAny])
def department_list_and_create(request):
    if request.method == "GET":
        qs = Department.objects.all().order_by("id")  # stable order for pagination
        paginator = SmallResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = DepartmentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == "POST":
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def department_details_and_modifications(request, pk: int):
    dept = get_object_or_404(Department, pk=pk)

    if request.method == "GET":
        return Response(DepartmentSerializer(dept).data)

    elif request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = DepartmentSerializer(dept, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        dept.delete()
        return Response(
            {"message": "Department has been deleted successfully."},
            status=status.HTTP_200_OK
        )
        # return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


# -------------------- Employee --------------------
@api_view(["GET", "POST"])
def employee_list_and_create(request):
    if request.method == "GET":
        print(list(Employee.objects.select_related("department").all()))
        qs = Employee.objects.all().order_by("id")

        # Optional filters via query params
        dept_id = request.query_params.get("department")
        if dept_id:
            qs = qs.filter(department_id=dept_id)

        paginator = SmallResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = EmployeeSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == "POST":
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def employee_details_and_modifications(request, pk: int):
    emp = get_object_or_404(Employee, pk=pk)

    if request.method == "GET":
        return Response(EmployeeSerializer(emp).data)
    
    elif request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"
        serializer = EmployeeSerializer(emp, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        emp.delete()
        return Response(
            {"message": "Employee has been deleted successfully."},
            status=status.HTTP_200_OK
        )
        # return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)