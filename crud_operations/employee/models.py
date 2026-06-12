from django.db import models

class Department(models.Model):
    dept_name = models.CharField(max_length=50)
    dept_head = models.CharField(max_length=50, blank=True, default='')
    dept_description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.dept_name

class Employee(models.Model):
    emp_id = models.IntegerField()
    emp_name = models.CharField(max_length=50)
    emp_dept = models.CharField(max_length=50)
    emp_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    emp_email = models.EmailField(max_length=100, blank=True, default='')
    emp_phone = models.CharField(max_length=15, blank=True, default='')
    date_joined = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    is_employee_of_month = models.BooleanField(default=False)

    def __str__(self):
        return self.emp_name

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')

    def __str__(self):
        return f"{self.employee.emp_name} - {self.date} - {self.status}"

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leave_deduction_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    late_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leaves_taken = models.IntegerField(default=0)
    total_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.emp_name} - {self.month} {self.year}"