import pytest
from voiceflow.utils.validators import validate_phone_number, validate_api_key


def test_validate_phone_number_valid():
    assert validate_phone_number("+12345678901") is True
    assert validate_phone_number("+447911123456") is True


def test_validate_phone_number_invalid():
    assert validate_phone_number("123") is False
    assert validate_phone_number("invalid") is False
    assert validate_phone_number("") is False


def test_validate_api_key_valid():
    assert validate_api_key("sk-" + "x" * 30) is True


def test_validate_api_key_invalid():
    assert validate_api_key("short") is False
    assert validate_api_key("wrongprefix_longkey") is False
