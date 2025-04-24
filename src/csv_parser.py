from abc import ABC, abstractmethod

import pandas as pd
from dataclasses import dataclass

@dataclass
class Company:
    name: str
    link: str

@dataclass
class Employee:
    link: str
    company: Company

unknown_company = Company(name='unknown', link='')

from enum import Enum
class ParserProviderType(Enum):
    MANTIKS = 'mantiks'
    BUILT_WITH = 'builtwith'

class ProspectParser(ABC):

    companies: list[Company] = []
    employees: list[Employee] = []

    def get_companies(self) -> list[Company]:
        return self.companies

    def get_user_profiles(self) ->list[Employee]:
        return self.employees

    def __init__(self,
                 path,
                 company_name_column: str,
                 company_link_column: str,
                 employee_link_column: str):
        self.path = path
        self.company_name_column = company_name_column.lower()
        self.company_link_column = company_link_column.lower()
        self.employee_link_column = employee_link_column.lower()

    def filter_df(self, df, column_name):
        if column_name not in df.columns:
            return pd.DataFrame(columns=[column_name])
        df_copy = df[df[column_name].notnull()]
        return df_copy.drop_duplicates(subset=[column_name])

    def open_as_df(self, file_path, parser_provider: ParserProviderType):
        if parser_provider == ParserProviderType.MANTIKS:
                return pd.read_csv(file_path, sep=',')
        elif parser_provider == ParserProviderType.BUILT_WITH:
                return pd.read_csv(file_path, sep=',', low_memory=False, skiprows=1)


    def parse(self, parser_provider: ParserProviderType):
        df = self.open_as_df(self.path, parser_provider)
        df.columns = map(str.lower, df.columns)

        df_companies = self.filter_df(df, self.company_link_column)
        df_employees = self.filter_df(df, self.employee_link_column)

        self.companies = [
            Company(row[self.company_name_column],
                    row[self.company_link_column]) if self.company_name_column in df.columns else None ## if no company name, set to None
            for row in df_companies.to_dict(orient='records')
        ]
        self.employees = [
            Employee(row[self.employee_link_column],
                     Company(row[self.company_name_column],
                            row[self.company_link_column]) if self.company_name_column in df.columns else unknown_company) ## if no company name, set to None
            for row in df_employees.to_dict(orient='records')
        ]

class MantiksCSVParser(ProspectParser):
    def __init__(self, path, company_name_column: str, company_link_column: str, employee_link_column: str):
        super().__init__(path, company_name_column, company_link_column, employee_link_column)
        self.parse(ParserProviderType.MANTIKS)


class BuiltwithCSVParser(ProspectParser):
    def __init__(self, path, company_name_column: str, company_link_column: str, employee_link_column: str):
        super().__init__(path, company_name_column, company_link_column, employee_link_column)
        self.parse(ParserProviderType.BUILT_WITH)
