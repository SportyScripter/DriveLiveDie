from auth import utils
import unittest


def test_get_hashed_password():
    test_password = "superSecret123"
    hashed_password = utils.get_hashed_password(test_password)
    assert utils.password_context.verify(test_password, hashed_password), "The hashed password does not match the original password."

