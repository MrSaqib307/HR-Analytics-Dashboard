import csv
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Employee

@login_required(login_url='/login/')
def home(request):
    query = request.GET.get('q', '')
    dept_filter = request.GET.get('dept', '')
    employees = Employee.objects.all()
    if query:
        employees = employees.filter(emp_name__icontains=query) | employees.filter(emp_dept__icontains=query)
    if dept_filter:
        employees = employees.filter(emp_dept=dept_filter)
    departments = Employee.objects.values_list('emp_dept', flat=True).distinct()
    paginator = Paginator(employees, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {'page_obj': page_obj, 'query': query, 'departments': departments, 'dept_filter': dept_filter})
def create_view(request):
    return render(request, "create.html")

def create_emp(request):
    if request.method == "POST":
        emp_id = request.POST.get('emp_id')
        emp_name = request.POST.get('emp_name')
        emp_dept = request.POST.get('emp_dept')
        emp_salary = request.POST.get('emp_salary')
        emp_email = request.POST.get('emp_email')
        emp_phone = request.POST.get('emp_phone')
        photo = request.FILES.get('photo')
        if emp_id and emp_name and emp_dept:
            Employee.objects.create(
                emp_id=emp_id,
                emp_name=emp_name,
                emp_dept=emp_dept,
                emp_salary=emp_salary,
                emp_email=emp_email,
                emp_phone=emp_phone,
                photo=photo
            )
            messages.success(request, "Employee added successfully!")
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
        employee.emp_email = request.POST.get("emp_email", employee.emp_email)
        employee.emp_phone = request.POST.get("emp_phone", employee.emp_phone)
        employee.save()
        messages.success(request, "Employee updated successfully!")
        return redirect("/")
    return render(request, "update.html", {"employee": employee})

def delete(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    messages.success(request, "Employee deleted successfully!")
    return redirect("/")

def dashboard(request):
    total_employees = Employee.objects.count()
    total_salary = Employee.objects.aggregate(Sum('emp_salary'))['emp_salary__sum'] or 0
    total_departments = Employee.objects.values('emp_dept').distinct().count()
    
    dept_data = Employee.objects.values('emp_dept').annotate(count=Count('emp_dept'), total_salary=Sum('emp_salary'))
    dept_labels = [d['emp_dept'] for d in dept_data]
    dept_counts = [d['count'] for d in dept_data]
    salary_data = [float(d['total_salary']) for d in dept_data]

    return render(request, "dashboard.html", {
        'total_employees': total_employees,
        'total_salary': total_salary,
        'total_departments': total_departments,
        'dept_labels': dept_labels,
        'dept_counts': dept_counts,
        'salary_data': salary_data,
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password!")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('/login/')
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Employee ID', 'Name', 'Department', 'Salary', 'Email', 'Phone', 'Date Joined'])
    employees = Employee.objects.all()
    for emp in employees:
        writer.writerow([emp.id, emp.emp_id, emp.emp_name, emp.emp_dept, emp.emp_salary, emp.emp_email, emp.emp_phone, emp.date_joined])
    return response
def employee_detail(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, "detail.html", {"employee": employee})