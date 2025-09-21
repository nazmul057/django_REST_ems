from rest_framework import serializers
from structures.models import Department, Employee

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    # Use PK for write operations; swap to a nested serializer if you want read-nested (see below).
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "email",
            "phone_number",
            "address",
            "date_of_joining",
            "department",
        ]
