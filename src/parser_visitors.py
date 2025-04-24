from abc import ABC, abstractmethod
import sqlite3
import webbrowser

from src.csv_parser import Company, ProspectParser

unknown_company = Company(name='unknown', link='')

class PropectVisitor(ABC):
    @abstractmethod
    def visit(self, element: ProspectParser):
        pass


class SysoutVisitor(PropectVisitor):
    def visit(self, element: ProspectParser):
        companies = element.get_companies()
        employees = element.get_user_profiles()

        print("Companies:")
        for company in companies:
            print(f"Name: {company.name}, Link: {company.link}")

        print("\nEmployees:")
        for employee in employees:
            print(f"Link: {employee.link}, Company: {employee.company.name}")

class SQLLiteSaveVisitor(PropectVisitor):

    def __init__(self, db_path: str, has_been_added: bool):
        import sqlite3
        self.db_path = db_path
        self.has_been_added = has_been_added


    def visit(self, element: ProspectParser):
        # Implement the logic to save the parsed data to the database
        companies = element.get_companies() + [unknown_company]
        employees = element.get_user_profiles()

        con = sqlite3.connect(self.db_path, timeout=5.0)
        cur = con.cursor()

        try:
            # Batch company records insertion
            cur.executemany('''INSERT INTO company (company_name, company_link, is_added) VALUES (?, ?, ?) ON CONFLICT DO NOTHING''',
                                    [(company.name, company.link, self.has_been_added) for company in companies])

            # retrieve the company ids and company name
            lower_company_names = [employee.company.name.lower() for employee in employees]
            placeholders = ','.join(['?'] * len(lower_company_names))
            query = f'''SELECT rowid, company_name FROM company WHERE lower(company_name) IN ({placeholders})'''
            cur.execute(query, lower_company_names)

            company_ids = cur.fetchall()
            company_id_map = {name: rowid for rowid, name in company_ids}
#
            # Batch employee records insertion
            cur.executemany('''INSERT INTO employee (employee_link, company_id, is_added) VALUES (?, ?, ?) ON CONFLICT DO NOTHING''',
                                    [(employee.link, company_id_map.get(employee.company.name, None), self.has_been_added) for employee in employees])

            # Commit the changes
            con.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        finally:
            cur.close()
            con.close()



class OpenBrowserVisitor(PropectVisitor):

    def __init__(self, chunk_size: int = 5, delay: int = 15):
        self.chunk_size = chunk_size
        self.delay = delay

    def visit(self, element: ProspectParser):
        companies = element.get_companies()
        employees = element.get_user_profiles()

        all_links = [company.link for company in companies] + [employee.link for employee in employees]
        chunked_list = list(self.chunk_list(all_links, self.chunk_size))
        self.open_urls_in_browser(chunked_list, self.delay)

    def chunk_list(self, lst, size):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), size):
            yield lst[i:i + size]

    def open_urls_in_browser(chunks: list[list[str]], delay: int = 5):
        for chunk in chunks:
            for url in chunk:
                webbrowser.open(url)
            time.sleep(delay)

