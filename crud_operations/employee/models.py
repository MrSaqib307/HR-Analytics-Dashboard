from django.db import models

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