from argparse import ArgumentParser
from .runner import MigrationRunner
from importlib import import_module
from os import getenv
from logging import StreamHandler, Formatter, INFO, getLogger
import sys

parser = ArgumentParser()
parser.add_argument("runner")
parser.add_argument("-d", "--drop", action="store_true")

def init_logger():
    hdlr = StreamHandler()
    hdlr.setFormatter(Formatter("[%(levelname)s] %(asctime)s - %(message)s"))
    log_level = getenv("LOG_LEVEL", INFO)
    logger = getLogger()
    logger.setLevel(log_level)
    logger.addHandler(hdlr)

def run():
    init_logger()
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