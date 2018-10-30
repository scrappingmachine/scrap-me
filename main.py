import argparse
from src.nodes.dispatcher import Dispatcher
from src.nodes.worker import Worker
from src.nodes.collector import Collector


def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="type")
    subparsers.required = True

    dispatcher_parser = subparsers.add_parser("dispatcher")
    dispatcher_parser.add_argument("--domain", type=str,
                                   default="pl")
    dispatcher_parser.add_argument("--location-id", type=str,
                                   required=True)

    subparsers.add_parser("worker")
    subparsers.add_parser("collector")

    return parser.parse_args()


def main():
    args = get_args()

    opt = {
        "dispatcher": Dispatcher,
        "worker": Worker,
        "collector": Collector
        }
    opt[args.type]()


if __name__ == "__main__":
    main()
