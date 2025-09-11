import pytest
import requests

from endpoints.meme_client import AuthToken, ToGetAPI, ToPostAPI, ToDeleteAPI, ToPutAPI


@pytest.fixture(scope="session")
def api_session():
    return requests.Session()


@pytest.fixture(scope="session")
def payload():
    return {"info": {"picture": "cat"}, "tags": ["dog", "god"], "text": "123",
                "url": "https://data.chpic.su/stickers/m/MemesAndPoops_stickers/MemesAndPoops_stickers_018.webp"}


@pytest.fixture(scope="session")
def auth_token(api_session):
    payload = {"name": "artem"}
    auth = AuthToken(session=api_session)
    return auth.auth_token(payload)


@pytest.fixture
def authorize_client(api_session):

    def _auth(payload):
        auth = AuthToken(session=api_session)
        return auth.auth_token(payload)
    return _auth


@pytest.fixture(scope="session")
def get_endpoint(api_session):
    return ToGetAPI(session=api_session)


@pytest.fixture
def post_endpoint(api_session):
    return ToPostAPI(session=api_session)


@pytest.fixture
def delete_endpoint(api_session):
    return ToDeleteAPI(session=api_session)


@pytest.fixture
def put_endpoint(api_session):
    return ToPutAPI(session=api_session)


@pytest.fixture
def fix(auth_token, api_session, payload, post_endpoint, delete_endpoint, get_endpoint):
    create_meme = post_endpoint.post_meme(payload, auth_token)
    assert create_meme.status_code == 200
    meme_json = create_meme.json()
    meme_id = meme_json['id']
    yield meme_json
    delete_endpoint.delete_meme(auth_token, meme_id)
    get_deleted_meme = get_endpoint.get_meme_by_id(meme_id, auth_token)
    assert get_deleted_meme.status_code == 404


@pytest.fixture()
def total_memes_to_db(api_session, auth_token, get_endpoint):
    get_all_memes = get_endpoint.get_memes(auth_token)
    total_memes = len(get_all_memes.json()['data'])
    return total_memes

