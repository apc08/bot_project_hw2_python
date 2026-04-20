import pytest
from app.core.jwt import decode_and_validate
from app.core.exceptions import TokenExpiredError, TokenInvalidError


def test_decode_valid_token(mock_settings, valid_jwt_token):
    payload = decode_and_validate(valid_jwt_token)

    assert payload["sub"] == "123"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_expired_token(mock_settings, expired_jwt_token):
    with pytest.raises(TokenExpiredError) as exc_info:
        decode_and_validate(expired_jwt_token)

    assert "expired" in str(exc_info.value).lower()


def test_decode_invalid_token(mock_settings):
    invalid_token = "invalid.jwt.token"

    with pytest.raises(TokenInvalidError) as exc_info:
        decode_and_validate(invalid_token)

    assert "invalid" in str(exc_info.value).lower()


def test_decode_token_without_sub(mock_settings):
    from jose import jwt
    from datetime import datetime, timedelta, timezone

    now = datetime.now(timezone.utc)
    expire = now + timedelta(hours=1)

    # токен без sub
    payload = {
        "role": "user",
        "iat": now,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        mock_settings.jwt_secret,
        algorithm=mock_settings.jwt_alg
    )

    with pytest.raises(TokenInvalidError) as exc_info:
        decode_and_validate(token)

    assert "sub" in str(exc_info.value).lower()
