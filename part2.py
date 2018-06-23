# these should be the only imports you need
import sys
import sqlite3

sqlite_file = 'Northwind_small.sqlite'
customer = 'Customer'
employee = 'Employee'
orders = "\"Order\""

# write your code here
# usage should be
#  python3 part2.py customers
#  python3 part2.py employees
#  python3 part2.py orders cust=<customer id>
#  python3 part2.py orders emp=<employee last name>

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

def customerList():
    c.execute('SELECT Id, CompanyName FROM {tn}'.\
            format(tn=customer))
    all_rows = c.fetchall()
    print ("ID     Customer Name")
    for person in all_rows:
        print (person[0] + "  "+ person[1])

def employeeList():
    c.execute('SELECT Id, FirstName, LastName FROM {tn}'.\
            format(tn=employee))
    all_rows = c.fetchall()
    print ("ID   Employee Name")
    for person in all_rows:
        print (str(person[0]) + "    "+ person[1]+ "  "+ person[2])

def orderDates(custID):
    c.execute('SELECT OrderDate FROM {tn} WHERE {cn}="{cust_id}"'.\
            format(tn=orders, cn='CustomerID', cust_id=custID))
    all_rows = c.fetchall()
    print ("Order dates")
    for date in all_rows:
        print (date[0])

def orderEmp(name):
    c.execute('SELECT OrderDate FROM "Order" AS Ord INNER JOIN Employee ON Ord.EmployeeId=Employee.Id WHERE LastName="{last_name}"'.\
            format(last_name=name))
    all_rows = c.fetchall()
    print ("Order dates")
    for date in all_rows:
        print (date[0])

#customerList()
#employeeList()
#orderDates("WOLZA");
#orderEmp("King");
if sys.argv[1] == 'customers':
    customerList()
if sys.argv[1] == 'employees':
    employeeList()
if sys.argv[1] == 'orders' and sys.argv[2].startswith("cust"):
    orderDates(sys.argv[2].split('=')[1]);
if sys.argv[1] == 'orders' and sys.argv[2].startswith("emp"):
    orderEmp(sys.argv[2].split('=')[1]);

conn.close()
