from signal import signal, SIG_IGN, SIGINT, SIGTERM

class Handler:
    def __init__(self):
        self.running = True

    def _handle(self, _sig, _frame):
        self.running = False

    def setup(self):
        signal(SIGINT, SIG_IGN)
        signal(SIGTERM, self._handle)

class ProcessManager:
    def __init__(self, procs):
        self._procs = procs

    def __enter__(self):
        for proc in self._procs:
            proc.start()
        return self

    def __exit__(self, type, value, traceback):
        for proc in self._procs:
            proc.terminate()
        for proc in self._procs:
            proc.join()

    def all_running(self):
        return all(proc.is_alive() for proc in self._procs)