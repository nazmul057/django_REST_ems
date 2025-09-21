from django.db import models

class Department(models.Model):
    id = models.BigAutoField(primary_key=True)  # explicit PK
    name = models.CharField("Department Name", max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"id: {self.id}, name: {self.name}"


class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    date_of_joining = models.DateField()
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    class Meta:
        # ordering = ["name"]
        indexes = [
            models.Index(fields=["department", "name"]),
        ]

    def __str__(self) -> str:
        return f"id: {self.id}, name: {self.name}, department: ({self.department.name})"

