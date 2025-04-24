from src.db_prospection import ProspectionDB

if __name__ == '__main__':
    db = ProspectionDB('prospection_data.db')
    companies = db.get_all_companies_not_added()
    for company in companies:
        print(f"Company: {company.name}, Link: {company.link}")

    employees = db.get_all_employees_not_added()
    for employee in employees:
        print(f"Employee: {employee.link}, Company: {employee.company.name}, Company Link: {employee.company.link}")

    print(" ------------ ")
    print("Companies: " + str(len(companies)))
    print("Employees: " + str(len(employees)))

