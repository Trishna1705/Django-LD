from django.urls import path
from .views import EmployeeList, EmployeeDetails, CompanyDetails, CompanyList, HomePage


app_name = "comp_emp"
urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("employees/", EmployeeList.as_view(), name="emp_list"),
    path("employees/<int:id>", EmployeeDetails.as_view(),
         name="emp_details"),
    path("companies/", CompanyList.as_view(), name="comp_list"),
    path("companies/<int:id>", CompanyDetails.as_view(),
         name="comp_details"),
]
