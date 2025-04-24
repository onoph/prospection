from db_prospection import ProspectionDB
import time
import webbrowser

# more than this number can lead to not loaded pages
def add_company_with_validation(nb_open_companies_at_once: int = 8):
    prospection_db = ProspectionDB('prospection_data.db')
    all_companies = prospection_db.get_all_companies_not_added()
    print('Total nb companies not added : ' + str(len(all_companies)))

    counter = 0
    companies_to_open = []

    def update_companies_status():
        for c in companies_to_open:
            prospection_db.updateAddedCompany(c)

    while(True):
        update_companies_status()

        if counter >= len(all_companies):
            print('No more employee to open')
            break

        user_input = input("Press 'Y' to continue...")
        if user_input in ['y', 'Y']:
            # open new companies in browser
            companies_to_open = all_companies[counter:counter + nb_open_companies_at_once]
            for company in companies_to_open:
                link =  company.link if company.link.startswith('http') else 'http://' + company.link
                webbrowser.open(link)
                print('Opening company : ' + company.name + " - " + company.link)
                time.sleep(1)
            counter += nb_open_companies_at_once
        else:
            break

# uses plugin to open browser and update status in DB
def auto_add_companies(nb_companies_to_add: int):
    prospection_db = ProspectionDB('prospection_data.db')
    companies_to_add = prospection_db.get_all_companies_not_added()[:nb_companies_to_add]

    print('Total nb companies not added : ' + str(len(companies_to_add)))
    for company in companies_to_add:
        link =  company.link if company.link.startswith('http') else 'http://' + company.link
        webbrowser.open(link)
        print('Opening company : ' + str(company.name) + " - " + company.link)
        prospection_db.updateAddedCompany(company)
        time.sleep(1)

if __name__ == '__main__':
    print("Hello")

    # uncomment to choose which way you prefer. Best way is to install the plugin and use auto mode.Everything is easy :)

    #auto_add_companies(20)
    #add_company_with_validation(8)