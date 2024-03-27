import pytest
from datetime import datetime, timedelta, timezone
from auth import utils

class MockUser:
    def __init__(self, is_active=True, role="user"):
        self.is_active = is_active
        self.role = role

class MockDB:
    def __init__(self, user=None):
        self.user = user

    def query(self, model):
        return self
    
    def filter(self, condition):
        return self
    
    def first(self):
        return self.user

@pytest.fixture
def mock_db():
    return MockDB()

def test_get_hashed_password():
    # Given
    test_password = "superSecret123"
    # When
    hashed_password = utils.get_hashed_password(test_password)
    # Then
    assert utils.password_context.verify(test_password, hashed_password)

def test_verify_password():
    # Given
    password = "correct_password"
    hashed_password = utils.get_hashed_password(password)
    # When & Then
    assert utils.verify_password(password, hashed_password)
    assert not utils.verify_password("incorrect_password", hashed_password)

def test_create_access_token():
    # Given
    subject = "test_subject"
    expires_delta = 3600  # 1 hour expiry
    # When
    token = utils.create_access_token(subject, expires_delta)
    decoded_token = utils.jwt.decode(token, utils.JWT_SECRET_KEY, algorithms=[utils.ALGORITHM])
    # Then
    assert decoded_token['sub'] == subject
    assert 'exp' in decoded_token
    assert datetime.utcfromtimestamp(decoded_token['exp']) - (datetime.now(timezone.utc) + timedelta(seconds=expires_delta)) < timedelta(seconds=5)

def test_create_refresh_token():
    # Given
    subject = "test_subject"
    expires_delta = 3600  # 1 hour expiry
    # When
    token = utils.create_refresh_token(subject, expires_delta)
    decoded_token = utils.jwt.decode(token, utils.JWT_REFRESH_SECRET_KEY, algorithms=[utils.ALGORITHM])
    # Then
    assert decoded_token['sub'] == subject
    assert 'exp' in decoded_token
    assert datetime.utcfromtimestamp(decoded_token['exp']) - (datetime.now(timezone.utc) + timedelta(seconds=expires_delta)) < timedelta(seconds=5)

@pytest.mark.asyncio
async def test_get_current_user_active():
    # Given
    active_user = MockUser()
    db = MockDB(active_user)
    # When
    result = await utils.get_current_user(MockDB(), db)
    # Then
    assert result == active_user

@pytest.mark.asyncio
async def test_get_current_user_inactive():
    # Given
    inactive_user = MockUser(is_active=False)
    db = MockDB(inactive_user)
    # When & Then
    with pytest.raises(utils.HTTPException) as exc_info:
        await utils.get_current_user(MockDB(), db)
    assert exc_info.value.status_code == utils.status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_get_current_active_user_active():
    # Given
    active_user = MockUser()
    # When
    result = await utils.get_current_active_user(active_user)
    # Then
    assert result == active_user

@pytest.mark.asyncio
async def test_get_current_active_user_inactive():
    # Given
    inactive_user = MockUser(is_active=False)
    # When & Then
    with pytest.raises(utils.HTTPException) as exc_info:
        await utils.get_current_active_user(inactive_user)
    assert exc_info.value.status_code == utils.status.HTTP_400_BAD_REQUEST

def test_role_checker():
    # Given
    allowed_roles = ["admin"]
    checker = utils.RoleChecker(allowed_roles)
    user = MockUser(role="admin")
    # When & Then
    assert checker(user)
    user = MockUser(role="user")
    with pytest.raises(utils.HTTPException) as exc_info:
        checker(user)
    assert exc_info.value.status_code == utils.status.HTTP_401_UNAUTHORIZED
