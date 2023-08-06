from time import sleep
from os import getenv
from importlib import import_module
from datetime import datetime, timedelta
from .util import Handler, ProcessManager
from multiprocessing import Process
import sys

PROC_MONITOR_CYCLE = 0.5

def _target(registry_str):
    sys.path.insert(0, "")
    handler = Handler()
    handler.setup()
    module, attr = registry_str.split(":")
    registry = import_module(module).__getattribute__(attr)
    while registry.consume() and handler.running:
        pass

def _mk_proc(registry_str):
    return Process(
        target = _target,
        args = (registry_str,)
    )

def handler(event, context):
    kwargs = event.get("kwargs", dict())
    time_now = datetime.utcnow()
    procs = [_mk_proc(kwargs["registry_str"]) for _ in range(int(kwargs.get("workers", 1)))]
    with ProcessManager(procs) as mgr:
        while mgr.all_running():
            if (datetime.utcnow() - time_now) > timedelta(seconds = int(kwargs["stop_after"])):
                break
            sleep(PROC_MONITOR_CYCLE)