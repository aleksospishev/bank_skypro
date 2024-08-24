from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import cards_info, greeting, read_file_xlsx, top_transactions_dict, user_settings_to_dict

data_test = [
    {
        "Дата операции": "31.12.2021 16:44:00",
        "Дата платежа": "31.12.2021",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -160.89,
        "Валюта операции": "RUB",
        "Сумма платежа": -160.89,
        "Валюта платежа": "RUB",
        "Кэшбэк": "",
        "Категория": "Супермаркеты",
        "MCC": 5411,
        "Описание": "Колхоз",
        "Бонусы (включая кэшбэк)": 3,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 160.89,
    },
    {
        "Дата операции": "31.12.2021 16:42:04",
        "Дата платежа": "31.12.2021",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -64.0,
        "Валюта операции": "RUB",
        "Сумма платежа": -64.0,
        "Валюта платежа": "RUB",
        "Кэшбэк": "",
        "Категория": "Супермаркеты",
        "MCC": 5411,
        "Описание": "Колхоз",
        "Бонусы (включая кэшбэк)": 1,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 64.0,
    },
]


@pytest.fixture
def test_df() -> pd.DataFrame:
    """Тестовый Frame для проверки работтоспособности функции"""
    return pd.DataFrame(data_test)


@patch("src.utils.pd.read_excel")
def test_read_file_xls(mock_read_xls: Any, test_df: Any) -> None:
    """Тест чтение из файла xls."""
    mock_read_xls.return_value = test_df
    res = read_file_xlsx("./data_test/test.xlsx")
    expected = test_df.to_dict(orient="records")
    assert res == expected
    mock_read_xls.assert_called_once_with("./data_test/test.xlsx")


def test_read_file_not_file() -> None:
    """Тест несуществующий файл."""
    res = read_file_xlsx("./data_test/not_file.xlsx")
    assert res == "Файл не найден"


@pytest.mark.parametrize(
    "my_date, expected",
    [
        ("2021-12-13 00:13:15", "Доброй ночи"),
        ("2021-12-13 06:13:15", "Доброе утро"),
        ("2021-12-13 14:13:15", "Добрый день"),
        ("2021-12-13 20:13:15", "Добрый вечер"),
    ],
)
def test_greeting(my_date: str, expected: str) -> None:
    """Тест функции Greeting."""
    assert greeting(my_date) == expected


def test_cards_info() -> None:
    """Тест cards_info."""
    res = cards_info(data_test)
    expected = [{"last_digits": "7197", "total_spent": 224.89, "cashback": 3.0}]
    assert res == expected


def test_cards_info_len_zero() -> None:
    """Тест cards_info с пустым списком"""
    assert cards_info([]) == []


def test_top_transactions_dict() -> None:
    """Тест top_transaction_dict."""
    res = top_transactions_dict(data_test)
    expected = [
        {"date": "31.12.2021", "amount": -64.0, "category": "Супермаркеты", "description": "Колхоз"},
        {"date": "31.12.2021", "amount": -160.89, "category": "Супермаркеты", "description": "Колхоз"},
    ]
    assert res == expected


def test_top_trans_len_list() -> None:
    """Тест top_transacton_dict с пустым списком"""
    assert top_transactions_dict([]) == []


data_test_json = {"user_currencies": ["test", "test_1"], "user_stocks": ["AB", "CD", "DG"]}


@patch("src.utils.json.load")
def test_user_settings_to_dict(mock_json_load: Any) -> None:
    mock_json_load.return_value = data_test_json
    res = user_settings_to_dict("./data_test/test.json")
    expected = (["test", "test_1"], ["AB", "CD", "DG"])
    assert res == expected


data_test_json_not_full = {"user_currencies": ["test", "test_1"]}


@patch("src.utils.json.load")
def test_user_settings_to_dict_not_full(mock_json_load: Any) -> None:
    mock_json_load.return_value = data_test_json_not_full
    res = user_settings_to_dict("./data_test/test.json")
    expected = (["test", "test_1"], None)
    assert res == expected


def test_user_settings_to_dict_len_list() -> None:
    res = user_settings_to_dict("./data_test/non_file.json")
    assert res == (None, None)
