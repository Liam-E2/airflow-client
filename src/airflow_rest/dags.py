import datetime

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


def trigger_dag(
        sess: Session, 
        base_url: str, 
        dag_id: str,
        dag_run_id: str = None,
        conf: dict = dict(),
        note: str = ""
        ):
    """
    Trigger a new DAG run for the specified dag_id.
    If no run_id passed, generates a run id of the form
        "cli_trigger_datetime.now().isoformat()"
    """
    ISO = datetime.datetime.now().isoformat()
    request_url = f"{base_url}/dags/{dag_id}/dagRuns"
    if dag_run_id is None:
        dag_run_id = f"cli_trigger_{ISO}"
    
    body = {
        "conf": conf,
        "dag_run_id": dag_run_id,
        "logical_date": ISO[0:-3]+"Z",
        "note": note
    }

    return sess.post(request_url, json=body).json()


def list_dag_runs(
        sess: Session, 
        base_url: str, 
        dag_id: str,
        limit: int = 100,
        offset: int = 0,
        order_by: str = 'start_date'
        ) -> 'list[dict]':
    
    request_url = f"{base_url}/dags/{dag_id}/dagRuns?limit={limit}&offset={offset}&order_by={order_by}"
    return sess.get(request_url).json()


def pause_dag(
        sess: Session,
        base_url: str,
        dag_id: str,
        pause_status: bool = True
    ) -> bool:
    """
    Set DAG pause status to pause_status
    """
    request_url = f"{base_url}/dags/{dag_id}?update_mask=is_paused"
    return sess.patch(request_url, json={"is_paused": pause_status}).json()
