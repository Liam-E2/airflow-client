import argparse
from pprint import pprint

from .config import *
from . import airflow_rest


def parse_args():
    parser = argparse.ArgumentParser()
    parser.set_defaults(
        cmd=lambda args: print("No arguments supplied; pass -h/--help for available arguments"),
        conf=get_config()
        )
    subparsers = parser.add_subparsers()

    configure = subparsers.add_parser("configure", help="Opens config file in default text editor")
    configure.set_defaults(cmd=edit_config)

    list_objects = subparsers.add_parser("list", help="List objects; supported object types:")
    list_objects.add_argument("-d", "--dag", help="List DAGs", action="store_true")
    list_objects.add_argument("-f", "--filter", help="Regex pattern to match on dag_id", required=False)
    list_objects.add_argument("-l", "--limit", type=int, default=100)
    list_objects.add_argument("-o", "--offset", type=int, default=0)
    list_objects.add_argument("--active_only", action="store_true")

    def listfn(args: argparse.Namespace):
        sess = airflow_rest.create_session(
            args.conf.get('airflow_session_token'),
            args.conf.get('airflow_base_url')
        )
        pprint(
            airflow_rest.list_dags(
                sess,
                args.conf.get('airflow_base_url'),
                args.filter,
                args.limit,
                args.offset,
                args.active_only
            )
        )

    list_objects.set_defaults(
        cmd=listfn
    )

    trigger_dagrun = subparsers.add_parser("trigger")
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

    return parser.parse_args()