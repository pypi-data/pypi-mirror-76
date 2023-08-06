# remoteit

Super basic multiprocessing/multithreading with a `concurrent.futures` type interface.

## Install

```bash
pip install remoteit
```

## Usage

```python
import time
import remoteit

@remoteit.remote
def do_something(x):
    time.sleep(1)
    return x * 2

@remoteit.threaded
def do_something_else(x):
    time.sleep(1)
    return x * 2


# simple - just call and get results

future = do_something(5)
future2 = do_something_else(6)

assert future.result() == 10
assert future2.result() == 12

# concurrent processes - run multiple together

# get results in order
futures = [do_something(i) for i in range(4)]
assert list(remoteit.results(futures)) == [0, 2, 4, 6]

# get results as soon as they finish
futures = [do_something(i) for i in range(4)]
assert set(remoteit.as_completed(futures)) == {0, 2, 4, 6}

```

## Description & Motivation

The difference between this and `concurrent.futures` is that:
 - it's a single worker process
 - it forks a new process every time.

The reason that I made this and didn't just use `concurrent.futures` is because I was getting an error when trying to submit a job that referenced a Queue object about how certain objects can only be shared through inheritance.

So I was back to using `multiprocessing.Process`, but passing and raising remote exceptions is a total pain and is something that I find myself solving and resolving. So I decided that this would be the last time that I wanted to think about how that messaging needs to happen.

This package is basically a thin wrapper around `multiprocessing.Process` and `threading.Thread` that will send the result back and raise any exceptions from the remote worker. Super simple!

## Notes & Caveats
##### `Future` objects should only be used by a single process.
 - currently, I handle multiple concurrent futures+results by generating a random id and having the id returned along side the result.
 - then if another future pulls a result off that doesn't match its result_id, it will put it in a results dictionary which is checked by other futures for their result_ids.
 - but the problem is that dictionaries aren't shared between processes so if you're reading items from the result queue in 2 different processes, then it'll cause a deadlock because one process may pop another processes result from the queue and the future will never see its result.
 - if anyone has any ideas on ways to fix this without too much overhead, post an issue!!

## Missing Interface
 - `fut.cancel()` - cancelling a task. we don't handle a cancelled result
 - `fut.result(timeout)` - we don't have result timeout atm.
 - `fut.add_done_callback()` - we don't have a monitoring thread that will run the result. better off just calling `future.result()` for now
