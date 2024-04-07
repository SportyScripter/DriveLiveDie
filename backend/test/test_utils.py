import pytest
from datetime import datetime, timedelta, timezone
from auth import utils
from unittest.mock import patch
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class MockHTTPAuthorizationCredentials:
    def __init__(self, token: str):
        self.credentials = token


class MockUser:
    def __init__(self, is_active=True, role="user", id="123"):
        self.is_active = is_active
        self.role = role
        self.id = id


@pytest.fixture
def mock_user():
    return MockUser()


@pytest.fixture
def mock_inactive_user():
    return MockUser(is_active=False)


def test_get_hashed_password():
    test_password = "superSecret123"
    hashed_password = utils.get_hashed_password(test_password)
    assert utils.password_context.verify(test_password, hashed_password)


def test_verify_password():
    password = "correct_password"
    hashed_password = utils.get_hashed_password(password)
    assert utils.verify_password(password, hashed_password)
    assert not utils.verify_password("incorrect_password", hashed_password)


def test_create_access_token():
    subject = "test_subject"
    expires_delta = timedelta(minutes=60)  # 1 hour expiry
    token = utils.create_access_token(subject, expires_delta)
    decoded_token = utils.jwt.decode(
        token, utils.JWT_SECRET_KEY, algorithms=[utils.ALGORITHM]
    )
    assert decoded_token["sub"] == subject


def test_create_refresh_token():
    subject = "test_subject"
    expires_delta = timedelta(minutes=60)  # 1 hour expiry
    token = utils.create_refresh_token(subject, expires_delta)
    decoded_token = utils.jwt.decode(
        token, utils.JWT_REFRESH_SECRET_KEY, algorithms=[utils.ALGORITHM]
    )
    assert decoded_token["sub"] == subject


@pytest.mark.asyncio
@patch("auth.utils.jwt.decode")
@patch("auth.utils.get_user")
async def test_get_current_user_active(mock_get_user, mock_jwt_decode, mock_user):
    valid_credentials = MockHTTPAuthorizationCredentials(token="valid_token")
    mock_jwt_decode.return_value = {"sub": mock_user.id}
    mock_get_user.return_value = mock_user
    result = await utils.get_current_user(valid_credentials)


@pytest.mark.asyncio
@patch("auth.utils.jwt.decode")
@patch("auth.utils.get_user")
async def test_get_current_user_inactive(
    mock_get_user, mock_jwt_decode, mock_inactive_user
):
    invalid_credentials = MockHTTPAuthorizationCredentials(
        token="invalid_token"
    )  # Tworzenie instancji MockHTTPAuthorizationCredentials
    mock_jwt_decode.return_value = {"sub": mock_inactive_user.id}
    mock_get_user.return_value = mock_inactive_user
    with pytest.raises(utils.HTTPException) as exc_info:
        await utils.get_current_user(invalid_credentials)


@pytest.mark.asyncio
async def test_get_current_active_user_active(mock_user):
    result = await utils.get_current_active_user(mock_user)
    assert result == mock_user


@pytest.mark.asyncio
async def test_get_current_active_user_inactive(mock_inactive_user):
    with pytest.raises(utils.HTTPException) as exc_info:
        await utils.get_current_active_user(mock_inactive_user)
    assert exc_info.value.status_code == 400
