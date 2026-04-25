import pytest
from httpx import AsyncClient
from fastapi import status

from core.main import app


@pytest.fixture
async def client():
    """Create async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration."""
    user_data = {
        "email": "test@example.com",
        "password": "SecurePass123!"
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "role" in data
    assert "subscription_tier" in data
    assert "password_hash" not in data  # Password should not be in response


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Test registration with duplicate email fails."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "SecurePass123!"
    }
    
    # First registration should succeed
    response1 = await client.post("/api/v1/auth/register", json=user_data)
    assert response1.status_code == status.HTTP_201_CREATED
    
    # Second registration with same email should fail
    response2 = await client.post("/api/v1/auth/register", json=user_data)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response2.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test successful login."""
    user_data = {
        "email": "login@example.com",
        "password": "SecurePass123!"
    }
    
    # Register user first
    await client.post("/api/v1/auth/register", json=user_data)
    
    # Login
    response = await client.post("/api/v1/auth/login", json=user_data)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Test login with wrong password fails."""
    user_data = {
        "email": "wrongpass@example.com",
        "password": "SecurePass123!"
    }
    
    # Register user first
    await client.post("/api/v1/auth/register", json=user_data)
    
    # Try to login with wrong password
    wrong_data = {
        "email": "wrongpass@example.com",
        "password": "WrongPassword123!"
    }
    
    response = await client.post("/api/v1/auth/login", json=wrong_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect email or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_current_user_profile(client: AsyncClient):
    """Test getting current user profile with valid token."""
    user_data = {
        "email": "profile@example.com",
        "password": "SecurePass123!"
    }
    
    # Register and login
    await client.post("/api/v1/auth/register", json=user_data)
    login_response = await client.post("/api/v1/auth/login", json=user_data)
    token = login_response.json()["access_token"]
    
    # Get profile
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_profile_without_token(client: AsyncClient):
    """Test getting profile without token fails."""
    response = await client.get("/api/v1/auth/me")
    
    # Should fail with 403 or 401 (depends on FastAPI security handling)
    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
