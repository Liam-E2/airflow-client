from src.airflow_rest.base import create_session
from requests.adapters import HTTPAdapter


def test_create_session():
    tok = "test_token"
    base_url = "https://www.google.com"
    sess = create_session(tok, base_url)

    assert sess.cookies.get('session') == tok
    assert isinstance(sess.adapters[base_url], HTTPAdapter)

    assert sess.get("https://www.google.com/robots.txt", verify=False).status_code == 200
