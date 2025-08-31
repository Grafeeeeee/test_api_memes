from pytest import mark


WRONG_DATA_OBJECT = [{"info": ["picture", "cat"], "tags": {"dog": "god"}, "text": 123,
                "url": "https://data.chpic.su/stickers/m/MemesAndPoops_stickers/MemesAndPoops_stickers_018.webp"}]
DATA_OBJECT = [{"info": {"picture": "cat"}, "tags": ["dog", "god"], "text": "123",
                "url": "https://data.chpic.su/stickers/m/MemesAndPoops_stickers/MemesAndPoops_stickers_018.webp"}]
DATA_OBJECT_TESTPOST = [{"info": {"color": "white"}, "tags": ["cat", "dark"], "text": "text for delete post",
                    "url": "https://data.chpic.su/stickers/m/MemesAndPoops_stickers/MemesAndPoops_stickers_031.webp"}]
WRONG_IDS = [-10, False, None, (), "", " ", [], {}]


@mark.parametrize("data", [{"name": "artem"}])
def test_auth_token_success(api_session, auth_token, data):
    resp = api_session.get(f"http://memesapi.course.qa-practice.com/authorize/{auth_token}")
    assert resp.status_code == 200


@mark.parametrize("data", WRONG_IDS)
def test_auth_wrong_token_success(api_session, authorize_client, data):
    resp = api_session.get(f"http://memesapi.course.qa-practice.com/authorize/{authorize_client}")
    assert resp.status_code == 404


@mark.get_success
def test_get_memes(get_endpoint, auth_token):
    get_endpoint.get_memes(auth_token)
    get_endpoint.check_response_status_is_200()


@mark.get_success
@mark.parametrize("data", [1, 1012, 101, 2929])
def test_get_meme_by_id(get_endpoint, data, auth_token):
    get_endpoint.get_meme_by_id(idx=data, token=auth_token)
    get_endpoint.check_response_status_is_200()


@mark.get_failed
@mark.parametrize("data", WRONG_IDS)
def test_get_meme_by_wrong_id(get_endpoint, data, auth_token):
    get_endpoint.get_meme_by_id(idx=data, token=auth_token)
    get_endpoint.check_response_status_is_404()


@mark.post_success
@mark.parametrize("data", DATA_OBJECT)
def test_post_meme_success(post_endpoint, auth_token, data):
    post_endpoint.post_meme(data, auth_token)
    post_endpoint.check_response_status_is_200()


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
@mark.parametrize("data", DATA_OBJECT_TESTPOST)
def test_delete_meme(post_endpoint, delete_endpoint, data, auth_token):
    resp = post_endpoint.post_meme(data, auth_token)
    meme_id = resp.json().get('id')
    delete_endpoint.delete_meme(idx=meme_id, token=auth_token)
    delete_endpoint.check_response_status_is_200()


@mark.delete_failed
@mark.parametrize("data", WRONG_IDS)
def test_delete_meme_failed(delete_endpoint, data, auth_token):
    delete_endpoint.delete_meme(idx=data, token=auth_token)
    resp_status = delete_endpoint.response.status_code
    assert resp_status in (403, 404)


@mark.put_success
@mark.parametrize("data", DATA_OBJECT_TESTPOST)
def test_put_meme(post_endpoint, put_endpoint, data, auth_token):
    resp = post_endpoint.post_meme(data, auth_token)
    meme_id = resp.json().get('id')
    payload = {"id": meme_id, "tags": ["text", "new"], "info": {"put": "method"}, "text": "sometext",
               "url": "https://data.chpic.su/stickers/m/MemesAndPoops_stickers/MemesAndPoops_stickers_031.webp"}
    put_endpoint.put_meme(idx=meme_id, payload=payload, token=auth_token)
    put_endpoint.check_response_status_is_200()


@mark.put_failed
@mark.parametrize("data", WRONG_IDS)
def test_put_meme_failed(post_endpoint, put_endpoint, data, auth_token):
    payload = {"id": WRONG_IDS, "tags": ["text", "new"], "info": {"put": "method"}, "text": "sometext",
               "url": "https://data.chpic.su/stickers/m/MemesAndPoops_stickers/MemesAndPoops_stickers_031.webp"}
    put_endpoint.put_meme(idx=WRONG_IDS, payload=payload, token=auth_token)
    resp_status = put_endpoint.response.status_code
    assert resp_status in (403, 404)
