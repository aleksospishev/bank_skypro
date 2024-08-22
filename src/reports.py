from datetime import datetime, timedelta

import pandas as pd


def log(file_name: str = "./logs/results.txt") -> None:
    """Декоратор для логирования вызовов функции.

    Параметры:
    file_name (str): Название файла для записи результата.
    Если не указан, результат пишеться в файл "logs/decorator.txt" .
    """

    def decorator(func) -> None:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file_name, "a") as file:
                file.write(str(result))
            return result

        return wrapper

    return decorator


@log()
def spending_by_category(transactions: pd.DataFrame, category: str, date=None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    if date is None:
        parsed_date = datetime.now()
    else:
        parsed_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    transactions = transactions[transactions["Сумма операции"] < 0]
    transactions = transactions[transactions["Категория"] == category]

    end_data = parsed_date - timedelta(days=90)

    transactions = transactions[pd.to_datetime(transactions["Дата операции"], dayfirst=True) <= parsed_date]

    transactions = transactions[pd.to_datetime(transactions["Дата операции"], dayfirst=True) > end_data]
    return pd.DataFrame(transactions)
