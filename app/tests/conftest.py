import pytest
from fastapi.testclient import TestClient

# Import after app is fully initialized
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def settings():
    from app.config import get_settings
    return get_settings()