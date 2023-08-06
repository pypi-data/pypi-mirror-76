import time
import random
import traceback
import threading
import multiprocessing as mp
from .queue import DictQueue


MIN_SLEEP = 1e-6


def remote(__func__=None, *a, **kw):
    def inner(func):
        return RemoteFunction(func, *a, **kw)
    return inner(__func__) if callable(__func__) else inner


def threaded(*a, **kw):
    return remote(*a, threaded=True, **kw)


def results(futures):
    yield from (f.result() for f in futures)


def as_completed(futures):
    futures = {f.result_id: f for f in futures}
    ids = list(futures)  # because RuntimeError: dictionary changed size during iteration
    while futures:
        for i in ids:
            if i in futures and futures[i].done():
                f = futures.pop(futures[i].result_id)
                yield f.result()
        time.sleep(MIN_SLEEP)



class RemoteFunction:
    def __init__(self, func, threaded=False):
        self.func = func
        self._result_queue = DictQueue()
        self._cls = threading.Thread if threaded else mp.Process

    def __call__(self, *a, **kw):
        result_id = random.randint(0, 1000000000)
        worker = self._cls(
            target=self._remote_run,
            args=(result_id, self.func) + a,
            kwargs=kw)
        future = Future(result_id, worker, self._result_queue)
        worker.start()
        return future

    def call(self, *a, **kw):
        return self.func(*a, **kw)

    def _remote_run(self, remote_id, func, *a, **kw):
        res, exc = None, None
        try:
            res = func(*a, **kw)
        except BaseException as e:
            exc = _ExceptionWithTraceback(e)
        finally:
            self._result_queue.put((res, exc), id=remote_id)


class Future:
    def __init__(self, result_id, worker, q):
        self.result_id = result_id
        self.worker = worker
        self.queue = q
        self._result = ...

    def done(self):
        self._pull_result(block=False)
        return self._result is not ...

    def exception(self):
        return self.done() and self._result[1]

    def __str__(self):
        return f'<Future {self.result_id} completed={self.done()} error={self.exception()}>'

    def _pull_result(self, block=False):
        if self._result is ...:
            self._result = self.queue.get(self.result_id, block=block) or ...
        return self._result is not ...

    def join(self):
        self.worker.join()
        self._pull_result(block=True)

    def result(self):
        self.join()
        res, exc = self._result
        if exc is not None:
            raise exc
        return res


class _RemoteTraceback(Exception):
    def __init__(self, tb):
        self.tb = tb

    def __str__(self):
        return self.tb

class _ExceptionWithTraceback:
    def __init__(self, exc):
        tb = ''.join(traceback.format_exception(
            type(exc), exc, exc.__traceback__))
        self.exc = exc
        self.tb = f"\n'''\n{tb}'''"

    def __reduce__(self):
        return _rebuild_exc, (self.exc, self.tb)

def _rebuild_exc(exc, tb):
    exc.__cause__ = _RemoteTraceback(tb)
    return exc
