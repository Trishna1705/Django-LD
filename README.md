Use Case Constraints:

1. The app comp_emp has two models named Employee and Company.
2. Each Employee can be a part of multiple Companies.
3. Each Company can have multiple Employees.
4. The data must not be stored in database. Instead it should be stored using file system.
5. There must be 1000000 records of Employees.
6. There must be 500000 records of Companies.



Additions:

1. Implemented pagination.
2. Used memoization concept.



To be noted:

1. The data generated will be stored in files in comp_emp/records folder.
2. Initially the files don't have any data. 
3. While first execution, the data needs to be generated hence the processing takes some time.
4. One can see the details of the execution on terminal.



Instructions to run the app:

1. Clone this repo on your system using the following command
    git clone https://github.com/Trishna1705/Django-LD

2. Create a virtual environment in your working directory and activate it.
    virtualenv -p python venv
    source venv/bin/activate

3. On the command line, while being in the same folder as that of the manage.py file, run the following commands to create migrations for the models.
    python manage.py makemigrations
    

4. If you get errors while running the above command, check for the below mentioned dependencies and install them. If there are no errors, you can directly skip to "Instruction 5"
    pip install django
    pip install faker

    Make sure that your are doing all the installations in your virtual environment.

5. Apply the migrations.
    python manage.py migrate

6. Run the server
    python manage.py runserver

    If you get an error like "Error: That port is already in use." , either close the operation running on port 8000 or change the port for this operation by using the following command.

    python manage.py runserver 8800

    Here, you can add any available port in the place of 8800.

7. The project will run on a server at http://127.0.0.1:8000/ . Navigate to this URL while your server is still running.

8. You will see two links : Employees and Companies . Click on any one of these to access the list of Employees and Companies respectively.

9. While on Employees page(http://127.0.0.1:8000/employees/), you can click on any one of employees' name to see the list of companies that employee is a part of.

10. While on Companies page(http://127.0.0.1:8000/companies/), you can click on any one of companies' name to see the list of employees in that company.

11. All these pages have Navigation links named first, previous, next, last to navigate to the first, previous, next, last page respectively.

12. You can stop the server by pressing Ctrl + C while on terminal(in Linux Machines.)