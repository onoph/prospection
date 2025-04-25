from IPython.utils.openpy import source_to_unicode

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

def auto_add_companies_with_batch_delay(nb_companies: int, avg_batch_delay: int, max_iter=6):
    import random
    can_add_companies = True
    current_iter = 0
    while(can_add_companies and current_iter < max_iter):
        can_add_companies = auto_add_companies(nb_companies)
        current_iter += 1
        if can_add_companies:
            batch_delay_variation = avg_batch_delay + random.randint(-10, 10)
            print("Batch delay variation : " + str(batch_delay_variation))
            time.sleep(batch_delay_variation)


# uses plugin to open browser and update status in DB
def auto_add_companies(max_nb_companies_to_add: int) -> bool:
    import random
    prospection_db = ProspectionDB('prospection_data.db')
    max_nb_companies_to_add = random.randint(int(max_nb_companies_to_add / 2), max_nb_companies_to_add)
    print('Random number of companies to add : ' + str(max_nb_companies_to_add))

    companies_to_add = prospection_db.get_all_companies_not_added()[:max_nb_companies_to_add]


    print('Total nb companies not added : ' + str(len(companies_to_add)))
    for company in companies_to_add:
        link =  company.link if company.link.startswith('http') else 'http://' + company.link
        webbrowser.open(link)
        print('Opening company : ' + str(company.name) + " - " + company.link)
        prospection_db.updateAddedCompany(company)
        time.sleep(1)
    return len(companies_to_add) > 0

if __name__ == '__main__':
    print("Hello")

    # uncomment to choose which way you prefer. Best way is to install the plugin and use auto mode.Everything is easy :)
    auto_add_companies_with_batch_delay(10, 60, 5)
    #add_company_with_validation(8)