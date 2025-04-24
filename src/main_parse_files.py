from csv_parser import BuiltwithCSVParser, MantiksCSVParser
from parser_visitors import SQLLiteSaveVisitor
from src.db_prospection import ProspectionDB


def load_builtwith_files():
    # requires unzipped files
    builtwith_dir = '<your_full_path_to_mantiks_directory>'
    bfile1 = builtwith_dir + '/' + 'Angular-JS-websites-in-France.csv'
    bfile2 = builtwith_dir + '/' + 'Angular-JS-websites-in-UAE.csv'
    bfile3 = builtwith_dir + '/' + 'Angular-Material-websites-in-France.csv'
    bfile4 = builtwith_dir + '/' + 'Angular-websites-in-France.csv'
    bfile5 = builtwith_dir + '/' + 'Angular-websites-in-Luxembourg.csv'
    bfile6 = builtwith_dir + '/' + 'Angular-websites-in-the-United-Kingdom.csv'

    # sysoutVisitor is only useful for debug
    #sysout_visitor = SysoutVisitor()
    sqlite_visitor = SQLLiteSaveVisitor('prospection_data.db', False)
    bfiles = [bfile1, bfile2, bfile3, bfile4, bfile5, bfile6]
    for bfile in bfiles:
        parsed_file = BuiltwithCSVParser(bfile, 'Company', 'Linkedin', '')
        sqlite_visitor.visit(parsed_file)


def load_mantiks_files():
    dir = '<your_full_path_to_mantiks_directory>'
    file1 = dir + '/' + 'Angular à partir du 18_02_2025 - 6 mois.csv'
    file2 = dir + '/' + 'Développeur Java Freelance Moins De 1000 Salariés.csv'
    file3 = dir + '/' + 'Développeur Angular Entreprise De Moins De 1000 Salariés Qui Bossent En Télétravail Avec Des CDIs.csv'
    file4 = dir + '/' + 'Développeur Java Freelance Moins De 1000 Salariés.csv'

    sqlite_visitor = SQLLiteSaveVisitor('prospection_data.db', False)
    mantiks_file_1 = MantiksCSVParser(file1, 'Nom de l\'entreprise', 'LinkedIn Entreprise', '')
    mantiks_file_2 = MantiksCSVParser(file2, 'Company name', 'Company LinkedIn', 'LinkedIn profil')
    mantiks_file_3 = MantiksCSVParser(file3, 'Company name', 'Company LinkedIn', 'Company LinkedIn Employees')
    mantiks_file_4 = MantiksCSVParser(file4, 'Company name', 'Company LinkedIn', 'Company LinkedIn Employees')

    sqlite_visitor.visit(mantiks_file_1)
    sqlite_visitor.visit(mantiks_file_2)
    sqlite_visitor.visit(mantiks_file_3)
    sqlite_visitor.visit(mantiks_file_4)


if __name__ == '__main__':
    db = ProspectionDB('prospection_data.db') # it will create a "prospection_data.db" in this current folder
    db.init_db(drop_existing=False)
    load_builtwith_files()
    load_mantiks_files()


