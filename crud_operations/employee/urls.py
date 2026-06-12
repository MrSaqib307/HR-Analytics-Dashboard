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
]