import re

from requests.sessions import Session
from requests import Response


def list_dags(sess: Session, 
              base_url: str, 
              filter_pattern: str = None, 
              limit: int = 100,
              offset: int = 0,
              active_only: bool = False,
              tags: 'list[str]' = None
              ) -> list:
    """
    Send a request to the list dags endpoint, return a list of DAG objects returned from API.
    Optional: if filter_pattern passed, return filtered list of DAg objects where dag id matches provided regex pattern.
    """
    request_url = f"{base_url}/dags?limit={limit}&offset={offset}"
    if filter_pattern is not None:
        request_url += f"&dag_id_pattern={filter_pattern}"
    if active_only is not None:
        request_url += f"&only_active=true"

    resp = sess.get(request_url)
    return resp.json().get('dags', [])

