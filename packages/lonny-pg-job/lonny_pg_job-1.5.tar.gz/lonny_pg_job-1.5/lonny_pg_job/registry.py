from lonny_pg_queue import Queue
from lonny_pg_cron import Scheduler
from .cfg import Configuration
from .logger import logger
from functools import wraps
from datetime import datetime, timedelta
from json import dumps

class Job:
    def __init__(self, queue, slug, fn):
        self._queue = queue
        self._fn = fn
        self.slug = slug

    def schedule(self, *args, **kwargs):
        logger.info(f"Scheduling job: {self.slug} with args: {dumps([args, kwargs])}.")
        self._queue.put([self.slug, args, kwargs])

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)

class Registry:
    def __init__(self, db, name = "_lonny_pg_job"):
        self._db = db
        self._queue = Queue(db, f"_lonny_pg_job::{name}")
        self._scheduler = Scheduler(db, f"_lonny_pg_job::{name}")
        self._data = dict()
        self._last_advance = None

    def job(self, slug, *, interval = None):
        def wrapper(fn):
            logger.info(f"Registering job: {slug}.")
            job = wraps(fn)(Job(self._queue, slug, fn))
            self._data[slug] = job
            if interval is not None:
                self._scheduler.schedule(slug, interval = interval)
            return job
        return wrapper

    def _advance_schedule(self):
        now_dt = datetime.utcnow()
        cutoff_dt = now_dt - timedelta(seconds = Configuration.schedle_advance_seconds)
        if self._last_advance is None or self._last_advance < cutoff_dt:
            self._last_advance = now_dt
            for slug in self._scheduler.get_pending():
                logger.info(f"Interval job: {slug} is due to be run.")
                self._data[slug].schedule()


    def on_error(self, slug, args, kwargs, err):
        logger.error(f"Job: {slug} failed to complete.")
        logger.exception(err)

    def consume(self):
        self._advance_schedule()
        msg = self._queue.get()
        if msg is None:
            return False
        try:
            slug, args, kwargs = msg.payload
            logger.info(f"Attempting to run job: {slug} with parameters: {dumps([args, kwargs])}.")
            if slug in self._data:
                self._data[slug](*args, **kwargs)
                logger.info(f"Job: {slug} completed successfully.")
            else:
                logger.error(f"Job: {slug} has no definition.")
            msg.consume()
        except Exception as err:
            self.on_error(slug, args, kwargs, err)
        return True

    @staticmethod
    def setup(db):
        Queue.setup(db)
        Scheduler.setup(db)