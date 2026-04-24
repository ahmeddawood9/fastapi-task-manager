import pytest
import jwt
from app.api.deps import get_current_user
from app.core import security
from fastapi import HTTPException

def test_get_current_user_invalid_token(session):
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(db=session, token="invalidtoken")
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"

def test_get_current_user_no_sub(session):
    payload = {"some": "data"}
    token = jwt.encode(payload, security.SECRET_KEY, algorithm=security.ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(db=session, token=token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"

def test_get_current_user_user_not_found(session):
    payload = {"sub": "9999"}
    token = jwt.encode(payload, security.SECRET_KEY, algorithm=security.ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(db=session, token=token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"
