from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny # IsAuthenticated
from django.utils.dateparse import parse_date
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth

from structures.models import Department, Employee
from structures.serializers import DepartmentSerializer, EmployeeSerializer
from common.helpers import SmallResultsSetPagination
from operations.models import Attendance

# -------------------- Department --------------------
@api_view(["GET", "POST"])
# @permission_classes([AllowAny]) # Default is restricted set up in settings.py. For explicit restriction, use: @permission_classes([AllowAny])
def department_list_and_create(request):
    """
    Query params:
      - page, page_size: pagination
    """
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

@api_view(["GET"])
@permission_classes([AllowAny])
def employees_per_department_chart(request):
    qs = Department.objects.annotate(emp_count=Count("employees")).order_by("name")
    
    labels = []
    data = []

    for d in qs:
        labels.append(d.name)
        data.append(d.emp_count)

    return render(
        request,
        "reports/employees_per_dept_chart.html",
        {"labels": labels, "data": data},
    )

# -------------------- Employee --------------------
@api_view(["GET", "POST"])
def employee_list_and_create(request):
    """
    Query params:
      - department:   int   (department id)
      - page, page_size: pagination
    """
    if request.method == "GET":
        # print(list(Employee.objects.select_related("department").all()))
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

@api_view(["GET"])
# @permission_classes([AllowAny])
def employees_query_filters(request):
    """
    Query params:
      - department:   int   (department id)
      - joined_on:    YYYY-MM-DD (exact match)
      - joined_from:  YYYY-MM-DD (inclusive lower bound)
      - joined_to:    YYYY-MM-DD (inclusive upper bound)
      - page, page_size: pagination
    """
    qs = Employee.objects.select_related("department")

    # filter by department (id)
    dept_id = request.query_params.get("department")
    if dept_id:
        qs = qs.filter(department_id=dept_id)

    # date filters (either exact or range)
    joined_on = request.query_params.get("joined_on")
    joined_from = request.query_params.get("joined_from")
    joined_to = request.query_params.get("joined_to")

    if joined_on:
        d = parse_date(joined_on)
        if not d:
            return Response({"detail": "Invalid 'joined_on' (use YYYY-MM-DD)."}, status=status.HTTP_400_BAD_REQUEST)
        qs = qs.filter(date_of_joining=d)
    else:
        if joined_from:
            d_from = parse_date(joined_from)
            if not d_from:
                return Response({"detail": "Invalid 'joined_from' (use YYYY-MM-DD)."}, status=status.HTTP_400_BAD_REQUEST)
            qs = qs.filter(date_of_joining__gte=d_from)
        if joined_to:
            d_to = parse_date(joined_to)
            if not d_to:
                return Response({"detail": "Invalid 'joined_to' (use YYYY-MM-DD)."}, status=status.HTTP_400_BAD_REQUEST)
            qs = qs.filter(date_of_joining__lte=d_to)

    # indexed ordering
    qs = qs.order_by("department_id", "name", "id")

    paginator = SmallResultsSetPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = EmployeeSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def employee_monthly_attendance(request, employee_id: int):
    """
    Bar chart of monthly attendance (Present/Absent/Late) for one employee.
    """
    employee = get_object_or_404(Employee, pk=employee_id)

    qs = Attendance.objects.filter(employee_id=employee_id).annotate(month=TruncMonth("date")).values("month").annotate(
            present=Count("id", filter=Q(status="P")),
            absent=Count("id", filter=Q(status="A")),
            late=Count("id", filter=Q(status="L")),
        ).order_by("month")

    labels = []
    present = []
    absent = []
    late = []
    for row in qs:
        labels.append(row["month"].strftime("%b %Y"))
        present.append(row["present"])
        absent.append(row["absent"])
        late.append(row["late"])

    return render(
        request,
        "reports/employee_monthly_attendance.html",
        {
            "employee": employee,
            "labels": labels,
            "present": present,
            "absent": absent,
            "late": late,
        },
    )