from dataclasses import dataclass

@dataclass
class CompanyDB:
    id: int
    name: str
    link: str

@dataclass
class EmployeeDB:
    id: int
    link: str
    company: CompanyDB

import sqlite3
class ProspectionDB:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def init_db(self, drop_existing: bool = False):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        # Create table
        if drop_existing:
            cur.execute('''DROP TABLE IF EXISTS company''')

        cur.execute('''CREATE TABLE IF NOT EXISTS company
                       (company_name TEXT, company_link TEXT UNIQUE, is_added BOOLEAN)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS employee
                    (employee_link TEXT, company_id INTEGER, is_added BOOLEAN,
                    FOREIGN KEY (company_id) REFERENCES company (rowid))''')

    def show_all_companies(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # select all companies
        cur.execute('SELECT * FROM company')
        rows = cur.fetchall()
        print("Companies:")
        for row in rows:
            print(row)
        cur.close()
        con.close()

    def show_all_employees(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # select all employees
        cur.execute('SELECT * FROM employee')
        rows = cur.fetchall()
        print("Employees:")
        for row in rows:
            print(row)
        cur.close()
        con.close()

    def get_all_companies_not_added(self) -> list[CompanyDB]:
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # select all companies
        cur.execute('SELECT rowid, company_name, company_link FROM company WHERE is_added = 0')
        rows = cur.fetchall()
        companies = [CompanyDB(row[0], row[1], row[2]) for row in rows]
        cur.close()
        con.close()
        return companies

    def get_all_employees_not_added(self) -> list[EmployeeDB]:
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # select all employees
        cur.execute('SELECT e.rowid, e.employee_link,'
                     'c.rowid, c.company_name, c.company_link'
                    ' FROM employee e LEFT JOIN company c on c.rowid = e.company_id WHERE e.is_added = 0')
        rows = cur.fetchall()
        employees = [EmployeeDB(row[0], row[1], CompanyDB(row[2], row[3], row[4])) for row in rows]
        cur.close()
        con.close()
        return employees

    def updateAddedEmployee(self, employee: EmployeeDB):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # update employee
        cur.execute('UPDATE employee SET is_added = 1 WHERE rowid = ?', (employee.id,))
        con.commit()
        cur.close()
        con.close()

    def updateAddedCompany(self, company: CompanyDB):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        # update company
        cur.execute('UPDATE company SET is_added = 1 WHERE rowid = ?', (company.id,))
        con.commit()
        cur.close()
        con.close()
