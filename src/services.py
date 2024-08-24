import json
from datetime import datetime
import logging


serviceces_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/utils.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
serviceces_logger.addHandler(file_handler)
serviceces_logger.setLevel(logging.DEBUG)


def categories_cash_back(data: list[dict], year: int, month: int):
    serviceces_logger.info(f"cash_back за {month}, {year}")
    res = {}
    for operation in data:
        operation_date = datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if operation_date.year == year and operation_date.month == month:
            if operation["Категория"] in res:
                res[operation["Категория"]] += operation["Сумма платежа"] // (-100)
            else:
                res[operation["Категория"]] = operation["Сумма платежа"] // (-100)
            if operation.get("Кэшбэк") != "":
                res[operation["Категория"]] += operation["Кэшбэк"]
    return json.dumps(res, ensure_ascii=False, indent=2)