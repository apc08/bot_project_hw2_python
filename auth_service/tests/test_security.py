import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)
from app.core.config import settings


def test_hash_password():
    password = "test_password_123"
    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$2b$")  # bcrypt


def test_verify_password_correct():
    password = "correct_password"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    hashed = hash_password("correct_password")
    assert verify_password("wrong_password", hashed) is False


def test_create_access_token():
    token = create_access_token(sub=123, role="user")

    assert token
    assert len(token.split(".")) == 3

    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_alg],
    )

    assert payload["sub"] == "123"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_token_valid():
    token = create_access_token(sub=456, role="admin")
    payload = decode_token(token)

    assert payload["sub"] == "456"
    assert payload["role"] == "admin"


def test_decode_token_invalid_signature():
    fake_token = jwt.encode(
        {"sub": "123", "role": "user"},
        "wrong_secret",
        algorithm="HS256"
    )

    with pytest.raises(JWTError):
        decode_token(fake_token)


def test_decode_token_expired():
    now = datetime.now(timezone.utc)
    expired_time = now - timedelta(hours=1)

    payload = {
        "sub": "123",
        "role": "user",
        "iat": now - timedelta(hours=2),
        "exp": expired_time,
    }

    expired_token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg
    )

    with pytest.raises(JWTError):
        decode_token(expired_token)


def test_password_hash_is_unique():
    password = "same_password"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    # разные хеши из-за соли
    assert hash1 != hash2
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)
