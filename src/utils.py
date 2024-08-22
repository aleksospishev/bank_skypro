import json
import logging
import os
from datetime import datetime
from typing import Any, Hashable

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY_API_LAYER = os.getenv("API_KEY_API_LAYER")
API_KEY_ALPHA = os.getenv("API_KEY_ALPHA")

URL_CURRENCY = "https://api.apilayer.com/exchangerates_data/convert"
HEADERS = {"apikey": API_KEY_API_LAYER}

utils_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/utils.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)
utils_logger.setLevel(logging.DEBUG)


def greeting(time_date: str) -> str:
    """Приветсвие.

    Функция приветсвия пользователя в зависимости от времени суток на вход функции передается строка с датой в
    формате ГГГГ-ММ-ДД ЧЧ-ММ-СС.
    """
    time = datetime.strptime(time_date, "%Y-%m-%d %H:%M:%S")
    if time.hour < 6:
        message = "Доброй ночи"
    elif time.hour < 12:
        message = "Доброе утро"
    elif time.hour < 18:
        message = "Добрый день"
    else:
        message = "Добрый вечер"
    utils_logger.info(f"Приветсвие пользовотеля {message}")
    return message


def read_file_xlsx(path_file: str) -> list[dict[Hashable, Any]] | str:
    """Считывание списка транзакций из файла.

    Функция считывает список транзакций из файла с разрешением .xlsx,
    на вход функции передается строка путь файла.
    """
    utils_logger.info(f"Считываем данные из {path_file}")
    try:
        df = pd.read_excel(path_file)
        df = df.fillna("")
        return df.to_dict(orient="records")
    except FileNotFoundError as e:
        utils_logger.warning(e)
        return "Файл не найден"


def cards_info(operations_list: list[dict]) -> list[dict[Hashable, Any]]:
    """Функция возвращает по каждой транзакции номер карты, сумму платежа, и кэшбэк 1 рубль с каждых 100 рублей."""
    utils_logger.info("Обработка списка операций ")
    cards: dict[str, Any] = dict()
    for operation in operations_list:
        number_card = operation.get("Номер карты")[-4:]
        if number_card in cards:
            cards[number_card] += operation["Сумма платежа"]
        else:
            cards[number_card] = operation["Сумма платежа"]
    cards_res = []
    for key, value in cards.items():
        temp = {}
        if len(key) == 4:
            temp["last_digits"] = key
        temp["total_spent"] = round(value, 2) * -1
        temp["cashback"] = round(value // 100, 2) * -1
        cards_res.append(temp)
    return cards_res


def top_transactions_dict(operations_list: list[dict]) -> list[dict[str, Any]]:
    """Функция возвращает 5 транзакций с максимальной суммой транзакций."""
    utils_logger.info(f"Топ 5 транзакций из {operations_list}")
    transaction_sort = sorted(
        operations_list, key=lambda operations_list: operations_list.get("Сумма платежа"), reverse=True
    )[:5]
    top_transactions = list()
    for transaction in transaction_sort:
        temp = dict()
        temp["date"] = transaction["Дата операции"][:10]
        temp["amount"] = transaction["Сумма платежа"]
        temp["category"] = transaction["Категория"]
        temp["description"] = transaction["Описание"]
        top_transactions.append(temp)
    return top_transactions


def user_settings_to_dict(path_file: str) -> tuple():
    """Функция чтения данных из json файлов, для считывания пользовательских настроек."""
    utils_logger.info(f"считываем данные из {path_file}")
    try:
        with open(path_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("user_currencies"), data.get("user_stocks")
    except json.decoder.JSONDecodeError as e:
        utils_logger.warning(e)
        return None, None
    except FileNotFoundError as e:
        utils_logger.warning(f"{e} Файла{path_file} не существует")
        return None, None


def currency_rate_api(user_currencies: list) -> list:
    """Функция обращается к API"apilayer" для получения актуального курса валют из списка пользовательских настроек."""
    res = []
    if user_currencies is None:
        return []
    for code_currency in user_currencies:
        temp = {}
        params = {"to": "RUB", "from": code_currency, "amount": 1}
        response = requests.get(URL_CURRENCY, headers=HEADERS, params=params).json()
        temp["currency"] = code_currency
        temp["rate"] = round(response["info"]["rate"], 2)
        res.append(temp)
    return res


def stock_prices_api(user_stocks: list) -> list:
    """Функция обращается к API alphavantage для получения актуальной стоимости акций из списка настроек."""
    res = []
    if user_stocks is None:
        return []
    for symbol in user_stocks:
        temp = {}
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY_ALPHA}"
        response = requests.get(url)
        data = response.json()
        temp["stock"] = symbol
        if data.get("Global Quote"):
            temp["price"] = round(float(data["Global Quote"]["05. price"]), 2)
        else:
            temp["price"] = "Данные временно не доступны"
        res.append(temp)
    return res
