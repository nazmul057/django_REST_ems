from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from structures.models import Employee
from operations.models import Attendance, Performance


class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Attendance
        fields = ["id", "employee", "date", "status"]
        validators = [
            UniqueTogetherValidator(
                queryset=Attendance.objects.all(),
                fields=("employee", "date"),
                message="An attendance record for this employee on this date already exists.",
            )
        ]


class PerformanceSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Performance
        fields = ["id", "employee", "rating", "review_date"]