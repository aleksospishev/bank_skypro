import json

from src.services import categories_cash_back

from .test_utils import data_test


def test_categories_cash_back():
    res = categories_cash_back(data_test, 2021, 12)
    expected = json.dumps({"Супермаркеты": 1.0}, ensure_ascii=False, indent=2)
    assert res == expected


def test_categories_non_data():
    res = categories_cash_back([], 2021, 12)
    expected = json.dumps({})
    assert res == expected


def test_categories_bob_coorect_date():
    res = categories_cash_back(data_test, 2020, 2)
    expected = json.dumps({})
    assert res == expected
