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
