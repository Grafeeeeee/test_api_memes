import requests
from pytest import mark


WRONG_DATA_OBJECT = [{"info": ["picture", "cat"], "tags": {"dog": "god"}, "text": 123,
                "url": "https://data.chpic.su/stickers/m/MemesAndPoops_stickers/MemesAndPoops_stickers_018.webp"}]
DATA_OBJECT = [{"info": {"picture": "catadog"}, "tags": ["dog", "god"], "text": "test",
                "url": "URLA_NAVEKA.com"}]
DATA_OBJECT_TESTPOST = [{"info": {"color": "white"}, "tags": ["cat", "dark"], "text": "text for delete post",
                    "url": "https://data.chpic.su/stickers/m/MemesAndPoops_stickers/MemesAndPoops_stickers_031.webp"}]
WRONG_IDS = [-10, False, None, (), "", " ", [], {}]


@mark.parametrize("data", [{"name": "artem"}])
def test_auth_token_success(data):
    response = requests.post('http://memesapi.course.qa-practice.com/authorize', json=data)
    assert response.status_code == 200
    data_json = response.json()
    token = data_json.get('token')
    assert token is not None
    headers = {"Authorization": token}
    resp = requests.get('http://memesapi.course.qa-practice.com/meme', headers=headers)
    assert resp.status_code == 200


@mark.parametrize("data", WRONG_IDS)
def test_auth_wrong_token_success(api_session, authorize_client, data):
    resp = api_session.get(f"http://memesapi.course.qa-practice.com/authorize/{authorize_client}")
    assert resp.status_code == 404


@mark.get_success
def test_get_memes(get_endpoint, auth_token):
    response = get_endpoint.get_memes(auth_token)
    memes = response.json()
    assert len(memes['data']) > 100


@mark.get_success
def test_get_meme_by_id(fix, get_endpoint, auth_token):
    created_id = fix['id']
    get_meme_id = get_endpoint.get_meme_by_id(created_id, auth_token)
    data_meme = get_meme_id.json()
    assert 'id' in data_meme
    assert created_id == fix['id']
    assert data_meme['text'] == fix['text']


@mark.get_failed
@mark.parametrize("data", WRONG_IDS)
def test_get_meme_by_wrong_id(get_endpoint, data, auth_token):
    get_endpoint.get_meme_by_id(idx=data, token=auth_token)
    get_endpoint.check_response_status_is_404()


@mark.post_success
@mark.parametrize("data", DATA_OBJECT)
def test_post_meme_success(post_endpoint, auth_token, data):
    create_meme = post_endpoint.post_meme(data, auth_token)
    create_meme_json = create_meme.json()
    assert 'id' in create_meme_json
    for key, value in data.items():
        assert create_meme_json[key] == value


@mark.post_failed
@mark.parametrize("key,wrong_value", [
    ("text", v) for v in WRONG_IDS] + [("tags", v) for v in WRONG_IDS] + [("info", v) for v in WRONG_IDS] + [
    ("url", v) for v in WRONG_IDS]
)
def test_post_create_meme_failed(post_endpoint, auth_token, key, wrong_value):
    payload = {"text": "example", "tags": {'1': 2}, "info": [1, 2], "url": 'www.google.com'}
    payload[key] = wrong_value
    post_endpoint.post_meme(payload=payload, token=auth_token)
    post_endpoint.check_response_status_is_400()


@mark.delete_success
def test_delete_meme(fix, delete_endpoint, auth_token, get_endpoint):
    created_post_meme = fix
    delete_endpoint.delete_meme(auth_token, created_post_meme['id'])
    deleted_meme = get_endpoint.get_meme_by_id(created_post_meme['id'], auth_token)
    assert deleted_meme.status_code == 404, 'meme is still alive'


@mark.delete_failed
@mark.parametrize("data", WRONG_IDS)
def test_delete_meme_failed(delete_endpoint, data, auth_token):
    delete_endpoint.delete_meme(idx=data, token=auth_token)
    resp_status = delete_endpoint.response.status_code
    assert resp_status in (403, 404)


@mark.put_success
@mark.parametrize("data", DATA_OBJECT_TESTPOST)
def test_put_meme(fix, put_endpoint, data, auth_token):
    created_post_meme = fix
    payload = {"id": created_post_meme['id'], "tags": ["text", "new"], "info": {"put": "method"}, "text": "sometext",
               "url": "https://data.chpic.su/stickers/m/MemesAndPoops_stickers/MemesAndPoops_stickers_031.webp"}
    changed_meme = put_endpoint.put_meme(auth_token, payload, created_post_meme['id'])
    changed_meme_json = changed_meme.json()
    for key, value in changed_meme_json.items():
        if key in payload:
            assert str(payload[key]) == str(value)


@mark.put_failed
@mark.parametrize("data", WRONG_IDS)
def test_put_meme_failed(fix, put_endpoint, data, auth_token):
    created_post_meme = fix
    payload = {"id": data, "tags": ["text", "new"], "info": {"put": "method"}, "text": "sometext",
               "url": "https://data.chpic.su/stickers/m/MemesAndPoops_stickers/MemesAndPoops_stickers_031.webp"}
    changed_meme = put_endpoint.put_meme(auth_token, payload, created_post_meme['id'])
    assert changed_meme.status_code == 400
