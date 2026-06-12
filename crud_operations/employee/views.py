import csv
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Employee, Department, Attendance, Payroll

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

def toggle_employee_of_month(request, id):
    employee = get_object_or_404(Employee, id=id)
    Employee.objects.all().update(is_employee_of_month=False)
    employee.is_employee_of_month = True
    employee.save()
    messages.success(request, f"{employee.emp_name} is now Employee of the Month! 🏆")
    return redirect('/')

def department_list(request):
    departments = Department.objects.all()
    return render(request, "departments.html", {'departments': departments})

def department_create(request):
    if request.method == "POST":
        dept_name = request.POST.get('dept_name')
        dept_head = request.POST.get('dept_head')
        dept_description = request.POST.get('dept_description')
        if dept_name:
            Department.objects.create(dept_name=dept_name, dept_head=dept_head, dept_description=dept_description)
            messages.success(request, "Department added successfully!")
            return redirect('/departments/')
    return render(request, "department_create.html")

def department_delete(request, id):
    dept = get_object_or_404(Department, id=id)
    dept.delete()
    messages.success(request, "Department deleted successfully!")
    return redirect('/departments/')

def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-date')
    employees = Employee.objects.all()
    return render(request, "attendance.html", {'attendances': attendances, 'employees': employees})

def mark_attendance(request):
    if request.method == "POST":
        emp_id = request.POST.get('employee')
        date = request.POST.get('date')
        status = request.POST.get('status')
        employee = get_object_or_404(Employee, id=emp_id)
        Attendance.objects.create(employee=employee, date=date, status=status)
        messages.success(request, "Attendance marked successfully!")
        return redirect('/attendance/')
    employees = Employee.objects.all()
    return render(request, "mark_attendance.html", {'employees': employees})

def delete_attendance(request, id):
    attendance = get_object_or_404(Attendance, id=id)
    attendance.delete()
    messages.success(request, "Attendance deleted successfully!")
    return redirect('/attendance/')

def attendance_report(request):
    query = request.GET.get('q', '')
    employees = Employee.objects.all()
    if query:
        employees = employees.filter(emp_name__icontains=query)
    report = []
    for emp in employees:
        total = Attendance.objects.filter(employee=emp).count()
        present = Attendance.objects.filter(employee=emp, status='Present').count()
        absent = Attendance.objects.filter(employee=emp, status='Absent').count()
        leave = Attendance.objects.filter(employee=emp, status='Leave').count()
        if total > 0:
            percentage = round((present / total) * 100, 1)
        else:
            percentage = 0
        report.append({
            'employee': emp,
            'total': total,
            'present': present,
            'absent': absent,
            'leave': leave,
            'percentage': percentage,
        })
    return render(request, "attendance_report.html", {'report': report, 'query': query})

def payroll_list(request):
    query = request.GET.get('q', '')
    payrolls = Payroll.objects.all().order_by('-year', '-month')
    if query:
        payrolls = payrolls.filter(employee__emp_name__icontains=query)
    return render(request, "payroll.html", {'payrolls': payrolls, 'query': query})

def payroll_create(request):
    employees = Employee.objects.all()
    if request.method == "POST":
        emp_id = request.POST.get('employee')
        employee = get_object_or_404(Employee, id=emp_id)
        month = request.POST.get('month')
        year = request.POST.get('year')
        basic_salary = float(request.POST.get('basic_salary', 0))
        bonus_type = request.POST.get('bonus_type', 'amount')
        bonus_value = float(request.POST.get('bonus_value', 0))
        if bonus_type == 'percentage':
            bonus = (basic_salary * bonus_value) / 100
        else:
            bonus = bonus_value
        salary_increase_percent = float(request.POST.get('salary_increase_percent', 0))
        salary_increase_amount = (basic_salary * salary_increase_percent) / 100
        new_basic_salary = basic_salary + salary_increase_amount
        leave_deduction_per_day = float(request.POST.get('leave_deduction_per_day', 0))
        late_deduction = float(request.POST.get('late_deduction', 0))
        leaves_taken = int(request.POST.get('leaves_taken', 0))
        notes = request.POST.get('notes', '')
        total_deduction = (leave_deduction_per_day * leaves_taken) + late_deduction
        net_salary = new_basic_salary + bonus - total_deduction
        Payroll.objects.create(
            employee=employee,
            month=month,
            year=year,
            basic_salary=new_basic_salary,
            bonus=bonus,
            leave_deduction_per_day=leave_deduction_per_day,
            late_deduction=late_deduction,
            leaves_taken=leaves_taken,
            total_deduction=total_deduction,
            net_salary=net_salary,
            notes=notes,
        )
        messages.success(request, f"{employee.emp_name} ki payroll ban gayi!")
        return redirect('/payroll/')
    return render(request, "payroll_create.html", {'employees': employees})

def payroll_detail(request, id):
    payroll = get_object_or_404(Payroll, id=id)
    return render(request, "payroll_detail.html", {'payroll': payroll})

def payroll_delete(request, id):
    payroll = get_object_or_404(Payroll, id=id)
    payroll.delete()
    messages.success(request, "Payroll deleted successfully!")
    return redirect('/payroll/')