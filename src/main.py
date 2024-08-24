import os

import pandas as pd
from dotenv import load_dotenv

from src.reports import spending_by_category
from src.services import categories_cash_back
from src.utils import read_file_xlsx
from src.views import main_page, transactions

load_dotenv()
PATH_FILE = os.getenv("PATH_TO_FILE_OPERATIONS")


transactions_data = read_file_xlsx("./data/operations.xlsx")
transactions_pd = pd.DataFrame(transactions_data)


if __name__ == "__main__":
    # print(main_page("2023-12-21 12:23:45"))
    # print(categories_cash_back(transactions, 2018, 12))
    print(spending_by_category(transactions_pd, "Аптеки", "31.12.2021 16:42:04"))
