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
                                   default="pl", choises=["pl", "eng"])
    dispatcher_parser.add_argument("--location-id", type=str,
                                   default=274723)

    subparsers.add_parser("worker")
    subparsers.add_parser("collector")

    return parser.parse_args()


def main():
    args = get_args()

    domain = {
        "pl": "https://pl.tripadvisor.com",
        "eng": "https://www.tripadvisor.com"
        }

    opt = {
        "dispatcher": lambda: Dispatcher(args.location_id),
        "worker": lambda: Worker(domain[args.domain]),
        "collector": lambda: Collector()
        }
    opt[args.type]()


if __name__ == "__main__":
    main()
