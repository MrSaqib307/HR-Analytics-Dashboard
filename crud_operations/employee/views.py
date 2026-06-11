from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee

def home(request):
    employees = Employee.objects.all()
    return render(request, "home.html", {'employees': employees})

def create_view(request):
    return render(request, "create.html")

def create_emp(request):
    if request.method == "POST":
        emp_id = request.POST.get('emp_id')
        emp_name = request.POST.get('emp_name')
        emp_dept = request.POST.get('emp_dept')
        emp_salary = request.POST.get('emp_salary')
        if emp_id and emp_name and emp_dept:
            Employee.objects.create(emp_id=emp_id, emp_name=emp_name, emp_dept=emp_dept, emp_salary=emp_salary)
            return redirect('/')
    return render(request, "create.html")

def update_view(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, "update.html", {"employee": employee})

def update_emp(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        employee.emp_id = request.POST.get("emp_id", employee.emp_id)
        employee.emp_name = request.POST.get("emp_name", employee.emp_name)
        employee.emp_dept = request.POST.get("emp_dept", employee.emp_dept)
        employee.emp_salary = request.POST.get("emp_salary", employee.emp_salary)
        employee.save()
        return redirect("/")
    return render(request, "update.html", {"employee": employee})

def delete(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect("/")