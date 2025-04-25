from src.db_prospection import ProspectionDB

prospection_db_name = 'prospection_data.db'

def update_companies_allready_added(nb_companies: int):
    db = ProspectionDB(prospection_db_name)
    companies = db.get_all_companies_not_added()[:nb_companies]
    for company in companies:
        print(f"Company: {company.name}, Link: {company.link}")
        #db.updateAddedCompany(company)

def display_current_state():
    db = ProspectionDB(prospection_db_name)
    index = 30
    companies = db.get_all_companies_not_added()[index:index + 10]
    for company in companies:
        print(f"Company: {company.name}, Link: {company.link}")

    employees = db.get_all_employees_not_added()[:5]
    for employee in employees:
        print(f"Employee: {employee.link}, Company: {employee.company.name}, Company Link: {employee.company.link}")

    print(" ------------ ")
    print("Companies: " + str(len(companies)))
    print("Employees: " + str(len(employees)))

if __name__ == '__main__':
    update_companies_allready_added(2)

