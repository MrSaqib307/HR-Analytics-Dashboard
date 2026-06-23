from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create/', views.create_view, name="create"),
    path('create_emp/', views.create_emp, name="create_emp"),
    path('update/', views.update_view, name="update"),
    path('update/update_emp/<int:id>/', views.update_emp, name="update_emp"),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('export-csv/', views.export_csv, name="export_csv"),
    path('detail/<int:id>/', views.employee_detail, name="detail"),
    path('employee-of-month/<int:id>/', views.toggle_employee_of_month, name="employee_of_month"),
    path('departments/', views.department_list, name="departments"),
    path('departments/create/', views.department_create, name="department_create"),
    path('departments/delete/<int:id>/', views.department_delete, name="department_delete"),
    path('attendance/', views.attendance_list, name="attendance"),
    path('attendance/mark/', views.mark_attendance, name="mark_attendance"),
    path('attendance/delete/<int:id>/', views.delete_attendance, name="delete_attendance"),
    path('attendance/report/', views.attendance_report, name="attendance_report"),
    path('payroll/', views.payroll_list, name="payroll"),
    path('payroll/create/', views.payroll_create, name="payroll_create"),
    path('payroll/detail/<int:id>/', views.payroll_detail, name="payroll_detail"),
    path('payroll/delete/<int:id>/', views.payroll_delete, name="payroll_delete"),
    path('profile/', views.profile, name="profile"),
    path('register/', views.register, name="register"),

]