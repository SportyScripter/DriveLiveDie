import pytest
import unittest
import jwt
import auth.utils as u
from datetime import datetime, timedelta, timezone
from typing import Union
from fastapi import HTTPException


ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def test_get_hashed_password():
    test_password = "superSecret123"
    hashed_password = u.get_hashed_password(test_password)
    assert password_context.verify(test_password, hashed_password), "The hashed password does not match the original password."

class MockPasswordContext:
    @staticmethod
    def verify(password, hashed_password):
        return password == hashed_password

class MockUser:
    def __init__(self, is_active):
        self.is_active = is_active

class TestVerifyPassword(unittest.TestCase):
    def setUp(self):
        # Replace the actual password_context with the mock
        self.original_password_context = password_context
        global password_context
        password_context = MockPasswordContext

    def tearDown(self):
        # Restore the original password_context after each test
        global password_context
        password_context = self.original_password_context

    def test_correct_password(self):
        # Given
        password = "correct_password"
        hashed_password = "correct_password"
        # When
        result = u.verify_password(password, hashed_password)
        # Then
        self.assertTrue(result)

    def test_incorrect_password(self):
        # Given
        password = "incorrect_password"
        hashed_password = "correct_password"
        # When
        result = u.verify_password(password, hashed_password)
        # Then
        self.assertFalse(result)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    return jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)

class TestCreateAccessToken(unittest.TestCase):
    def test_create_token_with_custom_expiry(self):
        # Given
        subject = "test_subject"
        expires_delta = 3600  # 1 hour expiry
        # When
        token = create_access_token(subject, expires_delta)
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        # Then
        self.assertEqual(decoded_token['sub'], subject)
        self.assertIn('exp', decoded_token)
        self.assertAlmostEqual(
            datetime.utcfromtimestamp(decoded_token['exp']),
            datetime.now(timezone.utc) + timedelta(seconds=expires_delta),
            delta=timedelta(seconds=5)
        )

    def test_create_token_with_default_expiry(self):
        # Given
        subject = "test_subject"
        # When
        token = create_access_token(subject)
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        # Then
        self.assertEqual(decoded_token['sub'], subject)
        self.assertIn('exp', decoded_token)
        self.assertAlmostEqual(
            datetime.utcfromtimestamp(decoded_token['exp']),
            datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            delta=timedelta(seconds=5)
        )

@pytest.mark.asyncio
async def test_get_current_active_user_active_user():
    # Given
    active_user = MockUser(is_active=True)
    
    # When
    result = await u.get_current_active_user(active_user)
    
    # Then
    assert result == active_user

@pytest.mark.asyncio
async def test_get_current_active_user_inactive_user():
    # Given
    inactive_user = MockUser(is_active=False)
    
    # When & Then
    with pytest.raises(HTTPException) as exc_info:
        # When
        await u.get_current_active_user(inactive_user)
    
    # Then
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Inactive user"
