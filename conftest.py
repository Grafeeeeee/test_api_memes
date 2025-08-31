import pytest
import requests
from api_memes.endpoints.meme_client import ToPostAPI, ToGetAPI, ToDeleteAPI, AuthToken, ToPutAPI


@pytest.fixture(scope="session")
def api_session():
    return requests.Session()


@pytest.fixture(scope="session")
def auth_token(api_session):
    payload = {"name": "artem"}
    auth = AuthToken(session=api_session)
    return auth.auth_token(payload)


@pytest.fixture()
def authorize_client(api_session):

    def _auth(payload):
        auth = AuthToken(session=api_session)
        return auth.auth_token(payload)
    return _auth


@pytest.fixture(scope="session")
def get_endpoint(api_session):
    return ToGetAPI(session=api_session)


@pytest.fixture()
def post_endpoint(api_session):
    return ToPostAPI(session=api_session)


@pytest.fixture()
def delete_endpoint(api_session):
    return ToDeleteAPI(session=api_session)


@pytest.fixture()
def put_endpoint(api_session):
    return ToPutAPI(session=api_session)
