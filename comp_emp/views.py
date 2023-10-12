import random
import json
from math import ceil

from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from faker import Faker
from .models import Employee, Company

fake = Faker()


class Reuse():
    '''
        Customised class. Contains redundant functions.
    '''
    mem_filepath = {}

    def return_records(self, filepath):
        '''
            This function uses the concept of memoization. For a given path,
            if required number of records are already present in the
            mem_filepath dictionary, then those are returned. Else the records
            are fetched from the file located at given filepath.
        '''

        if filepath in self.mem_filepath and ( 
            len(self.mem_filepath[filepath]) == 500000 or len(
                self.mem_filepath[filepath]) == 1000000):
            
            return self.mem_filepath[filepath]
        else:
            with open(filepath, 'r') as source_file:
                records_list = source_file.readlines()
                records = list(json.loads(employee)
                               for employee in records_list)
                self.mem_filepath[filepath] = records
                return records


class HomePage(generic.ListView):
    template_name = "home.html"

    def get_queryset(self):
        return []


class EmployeeList(generic.ListView):
    '''
        Class to generate and display list of employees.
    '''

    template_name = "employeeList.html"
    model = Employee
    paginate_by = 50
    context_object_name = "employees"
    filepath = "comp_emp/records/employee_records.txt"

    def get_context_data(self, **kwargs):
        '''
            This method adds extra context data to be used in the template.
            The data required for pagination is added to context in this
            function.
        '''

        # Get the default context data from the superclass method
        context = super().get_context_data(**kwargs)

        # Computing and adding custom data to context
        page_number = int(self.request.GET.get('page', 1))
        context['page_number'] = page_number
        records_per_page = self.paginate_by
        total_records = 1000000
        context['last'] = ceil(total_records / records_per_page)
        remaining_records = total_records - (
            (page_number - 1) * records_per_page)
        context['has_more_records'] = remaining_records > records_per_page
        return context

    def generate_data(self, size):
        '''
            This function generates data for employees
            i.e. creates list of employees.
        '''

        employees = []

        print("----- Generating employees' list -----")
        for _ in range(size):
            employee = Employee(id=_, emp_name=fake.name(), email=fake.email(),
                                phone=fake.phone_number())
            employees.append(employee)

        return employees

    def get_queryset(self):
        '''
            This function provides data to be processed to the html template.
        '''

        print("----- EmployeeList queryset -----")

        with open(self.filepath, 'r') as file:
            size = len(file.readlines())
        return self.process_data(size)

    def process_data(self, size):
        '''
            This function generates data if the number of records is less than
            the required (explicitly specified, number of employees = 1000000),
            and processes it to return a list of records.
        '''

        if size < 1000000:
            companies = self.generate_data(1000000)

            with open(self.filepath, 'w') as file:
                print("----- Writing employees' list in the file -----")

                for company in companies:
                    record = {
                        'id': company.id,
                        'emp_name': company.emp_name,
                        'email': company.email,
                        'phone': company.phone
                        }
                    file.write(json.dumps(record))
                    file.write('\n')

        employees = Reuse().return_records(self.filepath)
        return employees


class EmployeeDetails(generic.ListView):
    '''
        Class to produce details for each employee.
    '''

    template_name = "employeeDetails.html"
    model = Company
    paginate_by = 10
    context_object_name = "companies"
    total_records = random.randint(11, 25)
    filepath = "comp_emp/records/employee_details_records.txt"

    def get_queryset(self) -> QuerySet[Any]:
        '''
            This function provides data to be processed to the html template.
        '''

        print("----- EmployeeDetails queryset -----")

        with open(self.filepath, 'r') as file:
            size = len(file.readlines())

        companies = Reuse().return_records(
                "comp_emp/records/company_records.txt")

        # If there are no companies, generate the list of companies
        if companies == [] or len(companies) < 500000:
            print("----- No records for Companies. -----")
            companies = CompanyList().process_data(0)

        employees = Reuse().return_records(
            "comp_emp/records/employee_records.txt")

        # If there are no employees, generate the list of employees
        if employees == [] or len(employees) < 1000000:
            print("----- No records for Employees. -----")
            employees = EmployeeList().process_data(0)

        # If details are not present for all employees, add the details.
        if size < 1000000:
            self.process_data(companies)

        # Getting all records for details of each employee
        records = Reuse().return_records(self.filepath)

        # Fetching the id of the employee, whose details are to be displayed,
        # from the url
        path = self.request.path
        id = path[11:]

        # Fetching the list of companies for the given id of employee
        comp_list = []
        for record in records:
            if int(id) == int(record['id']):
                print("----- Success! -----")
                comp_list = record['comps']
                break

        return comp_list

    def process_data(self, companies):
        '''
            This function writes the details of each employee in the file.
        '''

        print("----- Writing employees' details in the file -----")
        with open(self.filepath, 'w') as dest_file:
            for id in range(0, 1000000):
                comps = random.sample(companies, self.total_records)

                record = {
                    'id': id,
                    'comps': comps
                }

                dest_file.write(json.dumps(record))
                dest_file.write('\n')

    def get_context_data(self, **kwargs):
        '''
            This method adds extra context data to be used in the template.
            The data required for pagination is added to context in this
            function.
        '''

        # Get the default context data from the superclass method
        context = super().get_context_data(**kwargs)

        # Computing and adding custom data to context
        page_number = int(self.request.GET.get('page', 1))
        context['page_number'] = page_number
        records_per_page = self.paginate_by
        total_records = self.total_records
        context['last'] = ceil(total_records / records_per_page)
        remaining_records = total_records - (
            (page_number - 1) * records_per_page)
        context['has_more_records'] = remaining_records > records_per_page

        return context


class CompanyList(generic.ListView):
    '''
        Class to generate and display list of companies.
    '''

    model = Company
    template_name = "companyList.html"
    paginate_by = 50
    context_object_name = "companies"
    filepath = "comp_emp/records/company_records.txt"

    def get_queryset(self) -> QuerySet[Any]:
        '''
            This function provides data to be processed to the html template.
        '''

        print("----- CompanyList queryset -----")
        file = open(self.filepath, 'r')
        size = len(file.readlines())
        return self.process_data(size)

    def process_data(self, size):
        '''
            This function generates data if the number of records is less than
            the required (explicitly specified, number of companies = 500000),
            and processes it to return a list of records.
        '''

        if size < 500000:
            companies = self.generate_data(500000)

            with open(self.filepath, 'w') as file:
                print("----- Writing companies' list in the file -----")

                for company in companies:
                    record = {
                        'id': company.id,
                        'comp_name': company.comp_name,
                        'domain': company.domain
                    }

                    file.write(json.dumps(record))
                    file.write('\n')

        companies = Reuse().return_records(self.filepath)
        return companies

    def get_context_data(self, **kwargs):
        '''
            This method adds extra context data to be used in the template.
            The data required for pagination is added to context in this
            function.
        '''

        # Get the default context data from the superclass method
        context = super().get_context_data(**kwargs)

        # Computing and adding custom data to context
        page_number = int(self.request.GET.get('page', 1))
        context['page_number'] = page_number
        records_per_page = self.paginate_by
        total_records = 500000
        context['last'] = ceil(total_records / records_per_page)
        remaining_records = total_records - (
            (page_number - 1) * records_per_page)
        context['has_more_records'] = remaining_records > records_per_page
        return context

    def generate_data(self, size):
        '''
            This function generates data for companies
            i.e. creates list of companies.
        '''

        print("----- Generating companies' list -----")

        companies = []

        for _ in range(size):
            company = Company(id=_, comp_name=fake.name(),
                              domain=fake.domain_name())
            companies.append(company)

        return companies


class CompanyDetails(generic.ListView):
    '''
        Class to produce details for each employee.
    '''

    template_name = "companyDetails.html"
    model = Employee
    paginate_by = 10
    context_object_name = "employees"
    filepath = "comp_emp/records/each_company_details.txt"
    total_records = random.randint(11, 25)

    def get_queryset(self) -> QuerySet[Any]:
        '''
            This function provides data to be processed to the html template.
        '''

        print("----- CompanyDetails queryset -----")

        file = open(self.filepath, 'r')
        size = len(file.readlines())

        companies = Reuse().return_records(
                "comp_emp/records/company_records.txt")

        # If there are no companies, generate the list of companies
        if companies == [] or len(companies) < 500000:
            print("----- No records for Companies. -----")
            companies = CompanyList().process_data(0)

        employees = Reuse().return_records(
                "comp_emp/records/employee_records.txt")

        # If there are no employees, generate the list of employees
        if employees == [] or len(employees) < 1000000:
            print("----- No records for Employees. -----")
            employees = EmployeeList().process_data(0)

        # If details are not present for all companies, add the details.
        if size < 500000:
            self.process_data(employees)

        # Getting all records for details of each company
        records = Reuse().return_records(self.filepath)

        # Fetching the id of the employee, whose details are to be displayed,
        # from the url
        path = self.request.path
        id = path[11:]

        # Fetching the list of companies for the given id of employee
        emp_list = []
        for record in records:
            if int(id) == int(record['id']):
                print("----- Success! -----")
                emp_list = record['emps']
                break

        return emp_list

    def process_data(self, employees):
        '''
            This function writes the details of each employee in the file.
        '''

        print("----- Writing companies' details in the file -----")
        with open(self.filepath, 'w') as dest_file:
            for id in range(0, 500000):
                if len(employees) < self.total_records:
                    print("id: ", id)
                    print("employees: ", len(employees))
                    print("total_records: ", self.total_records)
                emps = random.sample(employees, self.total_records)
                record = {
                    'id': id,
                    'emps': emps
                }

                dest_file.write(json.dumps(record))
                dest_file.write('\n')

    def get_context_data(self, **kwargs):
        '''
            This method adds extra context data to be used in the template.
            The data required for pagination is added to context in this
            function.
        '''

        # Get the default context data from the superclass method
        context = super().get_context_data(**kwargs)

        # Computing and adding custom data to context
        page_number = int(self.request.GET.get('page', 1))
        context['page_number'] = page_number
        records_per_page = self.paginate_by
        total_records = self.total_records
        context['last'] = ceil(total_records / records_per_page)
        remaining_records = total_records - (
            (page_number - 1) * records_per_page)
        context['has_more_records'] = remaining_records > records_per_page

        return context
