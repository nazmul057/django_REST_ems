'''
# Basic
python manage.py seed_data --help

# Custom sizes
python manage.py seed_data --departments 5 --employees 50 --attendance-per-employee 30 --reviews-per-employee 10 --purge

# Wider date window for attendance
python manage.py seed_data --attendance-days-back 120

# Start fresh each time
python manage.py seed_data --purge

'''

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from faker import Faker
from faker.providers import DynamicProvider

from structures.models import Department, Employee
from operations.models import Attendance, Performance

'''
DEPT_CHOICES = ["Sales", "Finance", "Marketing", "Engineering", "Human Resources"]

fake = Faker()
department_provider = DynamicProvider(
    provider_name="department_name",
    elements=DEPT_CHOICES,
)
fake.add_provider(department_provider)
'''

DEPARTMENT_POOL = [
    "Sales", "Finance", "Marketing", "Engineering", "Human Resources",
    "IT", "Operations", "Customer Support", "Legal", "Product",
    "Research & Development", "Quality Assurance", "Procurement", "Logistics",
    "Business Development", "Data & Analytics", "Design / UX", "Administration",
    "Facilities", "Security", "Compliance", "Training", "Public Relations",
    "Accounting", "Manufacturing", "Field Service", "Strategy", "Investor Relations",
]

fake = Faker()
department_provider = DynamicProvider(
    provider_name="department_name",
    elements=DEPARTMENT_POOL,
)
fake.add_provider(department_provider)


class Command(BaseCommand):
    help = "Seed Departments, Employees, Attendance, and Performance with Faker data."

    def add_arguments(self, parser):
        parser.add_argument("--departments", type=int, default=6, help="Number of departments to create")
        parser.add_argument("--dept-seed", type=int, help="Seed for reproducible department selection")
        parser.add_argument("--employees", type=int, default=50, help="Number of employees to create")
        parser.add_argument("--attendance-per-employee", type=int, default=15,
                            help="Attendance rows per employee (unique by employee+date)")
        parser.add_argument("--reviews-per-employee", type=int, default=2,
                            help="Performance reviews per employee")
        parser.add_argument("--purge", action="store_true",
                            help="Delete existing rows before seeding")

    @transaction.atomic
    def handle(self, *args, **opts):
        fake = Faker()
        num_depts = opts["departments"]
        num_emps = opts["employees"]
        attd_per_emp = opts["attendance_per_employee"]
        perf_per_emp = opts["reviews_per_employee"]
        purge = opts["purge"]

        if purge:
            self.stdout.write(self.style.WARNING("Purging existing data..."))
            Attendance.objects.all().delete()
            Performance.objects.all().delete()
            Employee.objects.all().delete()
            Department.objects.all().delete()

        # -------------------- Departments --------------------
        '''
        self.stdout.write("Creating departments...")
        dept_names = set()
        while len(dept_names) < num_depts:
            # Ensure unique department names to satisfy Department.name unique=True
            dept_names.add(fake.unique.company())

        departments = [Department(name=name) for name in sorted(dept_names)]
        Department.objects.bulk_create(departments, ignore_conflicts=True)
        departments = list(Department.objects.all())
        if not departments:
            self.stdout.write(self.style.ERROR("No departments available; aborting."))
            return
        
        # -------------------- Departments (fixed set) --------------------
        self.stdout.write("Creating departments (fixed set)...")
        Department.objects.bulk_create(
            [Department(name=n) for n in DEPT_CHOICES],
            ignore_conflicts=True,   # safe on re-runs (name is unique)
        )
        departments = list(Department.objects.order_by("name"))
        if not departments:
            self.stdout.write(self.style.ERROR("No departments available; aborting."))
            return
        '''
        # -------------------- Departments (random unique selection) --------------------
        if opts.get("dept_seed") is not None:
            random.seed(opts["dept_seed"])

        requested = num_depts
        pool_size = len(DEPARTMENT_POOL)

        if requested > pool_size:
            self.stdout.write(self.style.WARNING(
                f"Requested {requested} departments, but pool has only {pool_size}. "
                f"Creating {pool_size}. Add more names to DEPARTMENT_POOL if you need more."
            ))
        k = min(requested, pool_size)

        chosen_names = random.sample(DEPARTMENT_POOL, k=k)

        self.stdout.write(f"Creating {k} department(s) from pool...")
        Department.objects.bulk_create(
            [Department(name=n) for n in chosen_names],
            ignore_conflicts=True,   # safe to re-run
        )
        departments = list(Department.objects.filter(name__in=chosen_names).order_by("name")) # this filtering only takes the depts from current run
        if not departments:
            self.stdout.write(self.style.ERROR("No departments available; aborting."))
            return



        # -------------------- Employees ----------------------
        self.stdout.write("Creating employees...")
        employees = []
        # Use Faker.unique for email to respect unique=True
        for _ in range(num_emps):
            name = fake.name()
            email = fake.unique.safe_email()
            phone = fake.phone_number()
            address = fake.address().replace("\n", ", ")
            doj = fake.date_between(start_date="-5y", end_date="today")
            dept = random.choice(departments)

            employees.append(Employee(
                name=name,
                email=email,
                phone_number=phone,
                address=address,
                date_of_joining=doj,
                department=dept,
            ))

        Employee.objects.bulk_create(employees, ignore_conflicts=True)
        employees = list(Employee.objects.select_related("department").all())
        if not employees:
            self.stdout.write(self.style.ERROR("No employees created; aborting."))
            return

        # -------------------- Attendance ---------------------
        self.stdout.write("Creating attendance...")
        today = timezone.now().date()
        attendance_rows = []

        STATUS_CHOICES = ["P", "A", "L"]
        # Skew realistic distribution (mostly Present)
        weights = [0.85, 0.10, 0.05]

        for emp in employees:
            for d in range(attd_per_emp, 0, -1):
                att_date = today - timedelta(days=d)
                status = random.choices(STATUS_CHOICES, weights=weights, k=1)[0]
                attendance_rows.append(Attendance(
                    employee=emp,
                    date=att_date,
                    status=status,
                ))

        # Use ignore_conflicts to skip any accidental duplicates (unique(employee, date))
        Attendance.objects.bulk_create(attendance_rows, ignore_conflicts=True)

        # -------------------- Performance --------------------
        self.stdout.write("Creating performance reviews...")
        performance_rows = []
        for emp in employees:
            for _ in range(perf_per_emp):
                rating = random.randint(1, 5)
                # Reviews spread across last 2 years
                review_date = fake.date_between(start_date="-2y", end_date="today")
                performance_rows.append(Performance(
                    employee=emp,
                    rating=rating,
                    review_date=review_date,
                ))

        Performance.objects.bulk_create(performance_rows, ignore_conflicts=True)

        # -------------------- Summary ------------------------
        self.stdout.write(self.style.SUCCESS("Seeding complete!"))
        self.stdout.write(f"Departments: {Department.objects.count()}")
        self.stdout.write(f"Employees:   {Employee.objects.count()}")
        self.stdout.write(f"Attendance:  {Attendance.objects.count()}")
        self.stdout.write(f"Performance: {Performance.objects.count()}")
