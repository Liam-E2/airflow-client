import argparse
from pprint import pprint

from .config import *
from .utils import pprint_table
from.id_cache import *
from . import airflow_rest


def dag(subs: argparse._SubParsersAction):
    """
    Create the dag subcommands:
      - list
      - trigger
    """

    dag: argparse.ArgumentParser = subs.add_parser("dag", help="DAG commands")
    dag_subs = dag.add_subparsers()

    dag_list = dag_subs.add_parser("list", help="List DAGs")
    dag_list.add_argument("-f", "--filter", help="Regex pattern to match on dag_id", required=False)
    dag_list.add_argument("-l", "--limit", type=int, default=100)
    dag_list.add_argument("-o", "--offset", type=int, default=0)
    dag_list.add_argument("--active_only", action="store_true")
    dag_list.add_argument("--raw", action="store_true", help="PPrint raw JSON")

    def listfn(args: argparse.Namespace):
        sess = airflow_rest.create_session(
            args.conf.get('airflow_session_token'),
            args.conf.get('airflow_base_url')
        )

        dag_results = airflow_rest.list_dags(
                sess,
                args.conf.get('airflow_base_url'),
                args.filter,
                args.limit,
                args.offset,
                args.active_only
            )
        if args.raw:
            pprint(dag_results)
            return
        
        pprint_table(
            [
                {k: d[k] for k in d.keys() if k in args.conf.get('dag_list_cols')} for d in dag_results
            ]
        )
    
    dag_list.set_defaults(cmd=listfn)


    trigger_dagrun = dag_subs.add_parser("trigger", help="Trigger a DAG run given DAG ID/run ID")
    trigger_dagrun.add_argument("dag_id", help="DAG id", type=str, default=load_cache().get('dag_id'), nargs='?')
    trigger_dagrun.add_argument("-r", "--run_id", help="(optional) DAG Run ID", required=False, default=load_cache().get('run_id'), nargs='?')
    trigger_dagrun.add_argument("-c", "--run_conf", help="(optional) JSON-formatted dag run conf", type=lambda v: json.loads(v), required=False, default=dict())
    trigger_dagrun.add_argument("-n", "--note", help="(optional) DAG Run Note", required=False)
    def triggerfn(args: argparse.Namespace):
        # TODO: refactor out the session logic
        sess = airflow_rest.create_session(
            args.conf.get('airflow_session_token'),
            args.conf.get('airflow_base_url')
        )

        pprint(
            airflow_rest.trigger_dag(
                sess,
                args.conf.get('airflow_base_url'),
                args.dag_id,
                args.run_id,
                args.run_conf,
                args.note
            )
            )

    trigger_dagrun.set_defaults(
        cmd=triggerfn
    )

    list_dagruns = dag_subs.add_parser("runs", help="List DAG runs given DAG ID")
    list_dagruns.add_argument("dag_id", help="DAG id", type=str, default=load_cache().get('dag_id'), nargs='?')
    list_dagruns.add_argument("-l", "--limit", type=int, default=10)
    list_dagruns.add_argument("-o", "--offset", type=int, default=0)
    list_dagruns.add_argument("-ob", "--order_by", type=str, help="Field to order by, prefix with - for reverse", default="-start_date")
    list_dagruns.add_argument('--raw', action="store_true")

    def list_runsfn(args: argparse.Namespace):
        sess = airflow_rest.create_session(
            args.conf.get('airflow_session_token'),
            args.conf.get('airflow_base_url')
        )

        dag_run_results = airflow_rest.list_dag_runs(
                sess,
                args.conf.get('airflow_base_url'),
                args.dag_id,
                args.limit,
                args.offset,
                args.order_by
            )
        
        if args.raw:
            pprint(dag_run_results)
            return
        
        dag_run_data = dag_run_results.get('dag_runs', [])
        pprint_table([
                {k: d[k] for k in d.keys() if k in args.conf.get('dag_run_list_cols')} for d in dag_run_data
            ])
    
    list_dagruns.set_defaults(cmd=list_runsfn)

    pause_dag = dag_subs.add_parser("pause")
    pause_dag.add_argument("dag_id", help="DAG ID", type=str, default=load_cache().get('dag_id'), nargs='?')
    pause_dag.add_argument('--unpause', action="store_false")


    def pausefn(args):
        sess = airflow_rest.create_session(
            args.conf.get('airflow_session_token'),
            args.conf.get('airflow_base_url')
        )

        pause_result = airflow_rest.pause_dag(
                sess,
                args.conf.get('airflow_base_url'),
                args.dag_id,
                args.unpause
            )
        
        pprint_table([
                {k: d[k] for k in d.keys() if k in args.conf.get('dag_list_cols')} for d in [pause_result]
            ])


    pause_dag.set_defaults(cmd=pausefn)


def run(subs: argparse._SubParsersAction):
    _run: argparse.ArgumentParser = subs.add_parser('run')
    run_subs = _run.add_subparsers()

    # Get dag run
    get = run_subs.add_parser('get')
    get.add_argument('-d','--dag_id', type=str, help="Dag ID", default=load_cache().get('dag_id'), nargs='?')
    get.add_argument('-r', '--run_id', type=str, help="DagRun ID", default=load_cache().get('run_id'), nargs='?')

    def getfn(args):
        sess = airflow_rest.create_session(
            args.conf.get('airflow_session_token'),
            args.conf.get('airflow_base_url')
        )
        get_result = airflow_rest.get_dag_run(
                sess,
                args.conf.get('airflow_base_url'),
                args.dag_id,
                args.run_id
            )

        pprint_table([
                {k: d[k] for k in d.keys() if k in args.conf.get('dag_run_list_cols')} for d in [get_result]
            ])
    
    get.set_defaults(cmd=getfn)

    # Set run state
    state = run_subs.add_parser("state")
    state.add_argument('-d', '--dag_id', help='dag_id', default=load_cache().get('dag_id'), nargs='?')
    state.add_argument('-r', '--run_id', help='dag run id', default=load_cache().get('run_id'), nargs='?')

    states = state.add_mutually_exclusive_group(required=True)
    states.add_argument('--success', action='store_true', help='Set state to success')
    states.add_argument('--failed', action='store_true', help='Set state to failed')

    def statefn(args):
        sess = airflow_rest.create_session(
            args.conf.get('airflow_session_token'),
            args.conf.get('airflow_base_url')
        )

        state_result = airflow_rest.set_run_state(
                sess,
                args.conf.get('airflow_base_url'),
                args.dag_id,
                args.run_id,
                'success' if args.success else 'failed'
            )
        pprint_table([
            {k: d[k] for k in d.keys() if k in args.conf.get('dag_run_list_cols')} for d in [state_result]
        ])


    states.set_defaults(cmd=statefn)


    # Get run tasks
    tasks = run_subs.add_parser('tasks')
    tasks.add_argument('-d', '--dag_id', help='DAG id', default=load_cache().get('dag_id'), nargs='?')
    tasks.add_argument('-r', '--run_id', help='Dag run id', default=load_cache().get('run_id'), nargs='?')

    def tasksfn(args):
        sess = airflow_rest.create_session(
            args.conf.get('airflow_session_token'),
            args.conf.get('airflow_base_url')
        )

        task_result = airflow_rest.get_run_tasks(
                sess,
                args.conf.get('airflow_base_url'),
                args.dag_id,
                args.run_id
            )
        pprint_table([
            {k: d[k] for k in d.keys() if k in args.conf.get('task_list_cols')} for d in task_result.get('task_instances', [])
        ])

    tasks.set_defaults(cmd=tasksfn)

def parse_args():

    parser = argparse.ArgumentParser()
    parser.set_defaults(
        cmd=lambda args: print("No arguments supplied; pass -h/--help for available arguments"),
        conf=get_config()
        )
    subparsers = parser.add_subparsers()

    configure = subparsers.add_parser("configure", help="Opens config file in default text editor")
    configure.set_defaults(cmd=edit_config)

    dag(subparsers) # Add dag + subcommands
    run(subparsers)

    args = parser.parse_args()
    if hasattr(args, "dag_id"):
        update_cache("dag_id", args.dag_id)
    if hasattr(args, "run_id"):
        update_cache("run_id", args.run_id)

    return parser.parse_args()
