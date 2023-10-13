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
4. One can see the details of the execution on console.
