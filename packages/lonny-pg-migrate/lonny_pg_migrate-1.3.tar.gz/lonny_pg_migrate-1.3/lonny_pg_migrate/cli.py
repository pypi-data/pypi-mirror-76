from argparse import ArgumentParser
from .runner import MigrationRunner
from importlib import import_module
from os import getenv
from logging import StreamHandler, Formatter, getLogger
import sys

parser = ArgumentParser()
parser.add_argument("runner")
parser.add_argument("-d", "--drop", action="store_true")

def run():
    logger = getLogger()
    logger.addHandler(StreamHandler())
    logger.setLevel(getenv("LOG_LEVEL", "INFO"))

    sys.path.insert(0,"")
    args = parser.parse_args()
    module, runner_ref = args.runner.split(":")
    runner = import_module(module).__getattribute__(runner_ref)
    if args.drop:
        runner.drop()
        return
    runner.migrate()

if __name__ == "__main__":
    run()