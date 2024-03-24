from backend.auth.utils import (
get_hashed_password,
password_context)
import unittest


def test_get_hashed_password():
    test_password = "superSecret123"
    hashed_password = get_hashed_password(test_password)
    assert password_context.verify(test_password, hashed_password), "The hashed password does not match the original password."

