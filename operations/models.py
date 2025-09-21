from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from structures.models import Employee

class Attendance(models.Model):
    STATUS_CHOICES = [
        ("P", "Present"),
        ("A", "Absent"),
        ("L", "Late"),
    ]

    id = models.BigAutoField(primary_key=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")

    class Meta:
        # ordering = ["-date", "employee__name"]
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["employee", "date"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["employee", "date"], name="uniq_attendance_per_employee_per_date"),
        ]

    def __str__(self):
        return f"id: {self.id}, employee: {self.employee}, date: {self.date}, status: {self.get_status_display()}"

class Performance(models.Model):
    id = models.BigAutoField(primary_key=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="performance_reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_date = models.DateField()

    class Meta:
        '''
        # ordering = ["-review_date"]
        indexes = [
            models.Index(fields=["employee", "-review_date"]),
        ]
        '''
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1, rating__lte=5),
                name="performance_rating_between_1_and_5",
            ),
        ]

    def __str__(self) -> str:
        return f"id: {self.id}, employee: {self.employee.name}, review_date: {self.review_date}, rating: {self.rating}"

