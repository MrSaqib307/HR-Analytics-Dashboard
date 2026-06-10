from django.db import models

class Employee(models.Model):
    emp_id = models.IntegerField()
    emp_name = models.CharField(max_length=50)
    emp_dept = models.CharField(max_length=50)