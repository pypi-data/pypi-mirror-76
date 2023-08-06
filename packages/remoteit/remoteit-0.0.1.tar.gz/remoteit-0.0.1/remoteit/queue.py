import time
import multiprocessing as mp
import multiprocessing.queues


class DictQueue(mp.queues.SimpleQueue):
    _delay = 1e-6
    def __init__(self, *a, ctx=None, **kw):
        self._results = {}
        super().__init__(*a, ctx=ctx or mp.get_context(), **kw)

    def get(self, result_id=..., block=True):
        return (
            self._get_result(result_id, block=block) if result_id is not ...
            else super().get())

    def empty(self, result_id=...):
        return result_id not in self._results and super().empty()

    def _get_result(self, result_id, block=True):
        '''Get the result from the queue. If there are overlapping calls, and
        if you pull the result meant for a different thread, save it to
        the results dictionary and keep pulling results until you get
        your result id.
        '''
        # NOTE: ripped from reip/util/remote.py
        while result_id not in self._results:
            if not super().empty():
                out_id, x = super().get()
                if out_id == result_id:
                    return x
                self._results[out_id] = x
            if not block:
                break
            time.sleep(self._delay)

        return self._results.pop(result_id, None)

    def put(self, x, id=None, **kw):
        return super().put((id, x), **kw)
