import argparse
from pprint import pprint

from .config import *
from .utils import pprint_table
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
    trigger_dagrun.add_argument("-i", "--dag_id", help="DAG id", type=str)
    trigger_dagrun.add_argument("-r", "--run_id", help="(optional) DAG Run ID", required=False, default=None)
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


    return parser.parse_args()
