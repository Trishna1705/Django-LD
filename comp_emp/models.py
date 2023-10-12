from django.db import models


class Employee(models.Model):
    emp_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.emp_name


class Company(models.Model):
    comp_name = models.CharField(max_length=100)
    domain = models.CharField(max_length=10)

    def __str__(self):
        return self.comp_name
