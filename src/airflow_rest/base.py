import requests
import requests.adapters
from requests.cookies import cookiejar_from_dict


def create_session(
        session_token: str,
        base_url: str
        ) -> requests.Session:
    """
    Returns a requests.Session object with an HTTP adapter mounted for the base URL
    and a session cookie set equal to session_token
    """
    jar = cookiejar_from_dict({
        "session": session_token
    })
    adapter = requests.adapters.HTTPAdapter()
    sess = requests.Session()

    sess.cookies = jar
    sess.mount(base_url, adapter)
    
    return sess
