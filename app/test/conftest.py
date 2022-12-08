from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient

# from sqlalchemy.orm import Session
from db.session import DbConnexionHandler

from core.config import settings
from main import app
# from app.tests.utils.user import authentication_token_from_email
# from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session")
def db() -> Generator:
    d=DbConnexionHandler()
    d.connect()
    yield d


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


# @pytest.fixture(scope="module")
# def superuser_token_headers(client: TestClient) -> Dict[str, str]:
#     return get_superuser_token_headers(client)


# @pytest.fixture(scope="module")
# def normal_user_token_headers(client: TestClient, db: DbConnexionHandler) -> Dict[str, str]:
#     return authentication_token_from_email(
#         client=client, email=settings.EMAIL_TEST_USER, db=db
#     )
