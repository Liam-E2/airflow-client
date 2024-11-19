from requests.sessions import Session


def get_dag_run(
        sess: Session,
        base_url: str,
        dag_id: str,
        dag_run_id: str
        ) -> dict:
    request_url = f"{base_url}/dags/{dag_id}/dagRuns/{dag_run_id}"
    resp = sess.get(request_url)
    return resp.json()


def set_run_state(
        sess: Session,
        base_url: str,
        dag_id: str,
        dag_run_id: str,
        state: str
        ) -> dict:
    request_url = f"{base_url}/dags/{dag_id}/dagRuns/{dag_run_id}"
    resp = sess.patch(request_url, json={"state": state})
    return resp.json()


def get_run_tasks(
        sess: Session,
        base_url: str,
        dag_id: str,
        dag_run_id: str,
        ) -> dict:
    request_url = f"{base_url}/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances"
    resp = sess.get(request_url)
    print(resp.content)
    return resp.json()
