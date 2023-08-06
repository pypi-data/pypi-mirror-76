from argparse import ArgumentParser
from time import sleep
from os import getenv
from importlib import import_module
from multiprocessing import Process
from .util import Handler, ProcessManager
from logging import getLogger, StreamHandler
import sys

JOB_POLL_CYCLE = 2
PROC_MONITOR_CYCLE = 0.5

parser = ArgumentParser()
parser.add_argument("registry_str")
parser.add_argument("-w", "--workers", type = int, default = 1)

def _target(registry_str):
    sys.path.insert(0, "")
    handler = Handler()
    handler.setup()
    module, attr = registry_str.split(":")
    registry = import_module(module).__getattribute__(attr)
    while True:
        while registry.consume() and handler.running:
            pass
        if not handler.running:
            break
        sleep(JOB_POLL_CYCLE)

def _mk_proc(registry_str):
    return Process(
        target = _target,
        args = (registry_str,)
    )

def run():
    logger = getLogger()
    logger.addHandler(StreamHandler())
    logger.setLevel(getenv("LOG_LEVEL", "INFO"))
    
    args = parser.parse_args()
    procs = [_mk_proc(args.registry_str) for _ in range(args.workers)]
    with ProcessManager(procs) as mgr:
        while True:
            if not mgr.all_running():
                raise RuntimeError("Worker Failed!")
            sleep(PROC_MONITOR_CYCLE)

if __name__ == "__main__":
    run()