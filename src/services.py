import json
from datetime import datetime


def categories_cash_back(data: list[dict], year: int, month: int):
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
