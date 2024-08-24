import json
import logging
import os
from typing import Any

from dotenv import load_dotenv

from src.utils import (cards_info, currency_rate_api, greeting, read_file_xlsx, stock_prices_api,
                       top_transactions_dict, user_settings_to_dict)

views_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/views.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
views_logger.addHandler(file_handler)
views_logger.setLevel(logging.DEBUG)


load_dotenv()

PATH_FILE = os.getenv("PATH_TO_FILE_OPERATIONS")
PATH_TO_FILE_USER_SETTING = os.getenv("PATH_TO_FILE_USER_SETTING")

transactions = read_file_xlsx(PATH_FILE)


def main_page(date: str) -> Any:
    greeting_message = greeting(date)
    cards = cards_info(transactions)
    top_transaction = top_transactions_dict(transactions)
    user_currencies, user_stocks = user_settings_to_dict(PATH_TO_FILE_USER_SETTING)
    currency_rate = currency_rate_api(user_currencies)
    stock_prices = stock_prices_api(user_stocks)
    data = {
        "greeting": greeting_message,
        "cards": cards,
        "top_transactions": top_transaction,
        "currency_rates": currency_rate,
        "stock_prices": stock_prices,
    }
    return json.dumps(data, ensure_ascii=False, indent=2)
