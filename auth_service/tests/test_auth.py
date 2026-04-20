import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, test_user_data):
    response = await client.post("/auth/register", json=test_user_data)

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["email"] == test_user_data["email"]
    assert data["role"] == "user"
    assert "created_at" in data
    assert "password_hash" not in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, test_user_data):
    await client.post("/auth/register", json=test_user_data)
    response = await client.post("/auth/register", json=test_user_data)

    assert response.status_code == 409
    detail = response.json()["detail"].lower()
    assert "already" in detail and ("exists" in detail or "registered" in detail)


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user_data):
    await client.post("/auth/register", json=test_user_data)

    response = await client.post(
        "/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"].split(".")) == 3


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user_data):
    await client.post("/auth/register", json=test_user_data)

    response = await client.post(
        "/auth/login",
        data={
            "username": test_user_data["email"],
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post(
        "/auth/login",
        data={
            "username": "nonexistent@email.com",
            "password": "anypassword"
        }
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_with_valid_token(client: AsyncClient, test_user_data):
    await client.post("/auth/register", json=test_user_data)
    login_response = await client.post(
        "/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]

    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["role"] == "user"
    assert "id" in data
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_get_me_without_token(client: AsyncClient):
    response = await client.get("/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_with_invalid_token(client: AsyncClient):
    response = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "password": "testpass123"
        }
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_full_auth_flow(client: AsyncClient):
    email = "fullflow@email.com"
    password = "securepass456"

    # регистрация
    reg_response = await client.post(
        "/auth/register",
        json={"email": email, "password": password}
    )
    assert reg_response.status_code == 201
    user_id = reg_response.json()["id"]

    # логин
    login_response = await client.post(
        "/auth/login",
        data={"username": email, "password": password}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # профиль
    me_response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    profile = me_response.json()

    assert profile["id"] == user_id
    assert profile["email"] == email
