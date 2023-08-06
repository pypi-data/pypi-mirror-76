import billiard
import concurrent.futures
from functools import partial
from itertools import chain
import logging
import multiprocessing
import os
import sys


logger = logging.getLogger(__name__)


class Executor():
    """Executor factory for different parallelization implementations."""

    def __init__(
        self,
        executor="concurrent_processes",
        start_method="fork",
        max_workers=None
    ):
        """
        Create an Executor.

        Parameters
        ==========
        executor : str
            One of "concurrent_processes", "concurrent_threads", "billiard" or
            "multiprocessing". (default: "concurrent_processes)
        start_method : str
            One of "fork" or "spawn"
        max_workers : int
            Number of parallel workers. (default: number of CPU cores)
        """
        self.executor = executor
        self.start_method = start_method
        self.max_workers = max_workers or os.cpu_count()
        logger.debug(
            "init Executor %s with start_method %s and %s workers",
            self.executor, self.start_method, self.max_workers
        )

    def as_completed(
        self,
        func=None,
        iterable=None,
        fargs=None,
        fkwargs=None,
        chunksize=1
    ):
        """
        Run function on items and yield results as soon as they are ready.

        Parameters
        ==========
        func : function
            Function to be applied to iterable items. Note that the iterable items
            will be passed on to the first item of the function.
        iterable : iterable
            Items to be processed.
        fargs : list
            List of function arguments.
        fkwargs : dict
            Dictionary of function keyword arguments.

        Yields
        ======
        godale.FinishedTask items
        """
        fargs = fargs or []
        fkwargs = fkwargs or {}
        for i in _mode[self.executor](
            mode="as_completed",
            func=func,
            iterable=iterable,
            fargs=fargs,
            fkwargs=fkwargs,
            max_workers=self.max_workers,
            start_method=self.start_method,
            chunksize=chunksize
        ):
            yield i

    def map(
        self,
        func=None,
        iterable=None,
        fargs=None,
        fkwargs=None,
        chunksize=1
    ):
        """
        Run function on items and yield in the same order as the input iterable items.

        Parameters
        ==========
        func : function
            Function to be applied to iterable items. Note that the iterable items
            will be passed on to the first item of the function.
        iterable : iterable
            Items to be processed.
        fargs : list
            List of function arguments.
        fkwargs : dict
            Dictionary of function keyword arguments.

        Yields
        ======
        godale.FinishedTask items.
        """
        fargs = fargs or []
        fkwargs = fkwargs or {}
        for i in _mode[self.executor](
            mode="map",
            func=func,
            iterable=iterable,
            fargs=fargs,
            fkwargs=fkwargs,
            max_workers=self.max_workers,
            start_method=self.start_method,
            chunksize=chunksize
        ):
            yield i


class FinishedTask():
    """Wrapper around function result and exeption."""

    def __init__(self, func, fargs=None, fkwargs=None):
        """
        Run function and store result or exception.

        Parameters
        ==========
        func : function
            Function to be run.
        fargs : list
            List of function arguments.
        fkwargs : dict
            Dictionary of function keyword arguments.

        """
        fargs = fargs or []
        fkwargs = fkwargs or {}
        try:
            self._result = func(*fargs, **fkwargs)
            self._exception = None
        except Exception as e:
            self._result = None
            self._exception = e

    def result(self):
        """Return func result or raise Exception."""
        if self._exception:
            raise self._exception
        else:
            return self._result

    def exception(self):
        """Return Exception."""
        return self._exception

    def __repr__(self):
        return "FinishedTask(result=%s, exception=%s)" % (self._result, self._exception)


def _worker_func(func, fargs, fkwargs, i):
    return FinishedTask(func, list(chain([i], fargs)), fkwargs)


def _billiard(
    mode=None,
    func=None,
    iterable=None,
    fargs=None,
    fkwargs=None,
    max_workers=None,
    start_method="fork",
    chunksize=None,
    **kwargs
):
    logger.debug("open billiard.Pool and %s %s workers", start_method, max_workers)
    iterable = list(iterable)
    with billiard.get_context(start_method).Pool(max_workers) as pool:
        if mode == "as_completed":
            logger.debug(
                "submit %s tasks to billiard.Pool.imap_unordered()", len(iterable)
            )
            mode_func = pool.imap_unordered
        elif mode == "map":
            logger.debug(
                "submit %s tasks to billiard.Pool.map()", len(iterable)
            )
            mode_func = pool.map
        for i, finished_task in enumerate(mode_func(
            partial(_worker_func, func, fargs, fkwargs),
            iterable,
            chunksize=chunksize
        )):
            yield finished_task
            logger.debug("task %s/%s finished", i + 1, len(iterable))
    logger.debug("billiard.Pool closed")


def _multiprocessing(
    mode=None,
    func=None,
    iterable=None,
    fargs=None,
    fkwargs=None,
    max_workers=None,
    start_method="fork",
    chunksize=None,
    **kwargs
):
    logger.debug("open multiprocessing.Pool and %s %s workers", start_method, max_workers)
    iterable = list(iterable)
    with multiprocessing.get_context(start_method).Pool(max_workers) as pool:
        if mode == "as_completed":
            logger.debug(
                "submit %s tasks to multiprocessing.Pool.imap_unordered()", len(iterable)
            )
            mode_func = pool.imap_unordered
        elif mode == "map":
            logger.debug(
                "submit %s tasks to multiprocessing.Pool.map()", len(iterable)
            )
            mode_func = pool.map
        for i, finished_task in enumerate(mode_func(
            partial(_worker_func, func, fargs, fkwargs),
            iterable,
            chunksize=chunksize
        )):
            yield finished_task
            logger.debug("task %s/%s finished", i + 1, len(iterable))
    logger.debug("multiprocessing.Pool closed")


def _concurrent_processes(
    mode=None,
    func=None,
    iterable=None,
    fargs=None,
    fkwargs=None,
    max_workers=None,
    start_method="fork",
    **kwargs
):
    logger.debug("open concurrent.futures.ProcessPoolExecutor")
    for i in _execute_concurrent_futures(
        concurrent.futures.ProcessPoolExecutor,
        mode=mode,
        func=func,
        iterable=iterable,
        fargs=fargs,
        fkwargs=fkwargs,
        max_workers=max_workers,
        start_method=start_method
    ):
        yield FinishedTask(i.result)


def _concurrent_threads(
    mode=None,
    func=None,
    iterable=None,
    fargs=None,
    fkwargs=None,
    max_workers=None,
    start_method="fork",
    **kwargs
):
    logger.debug("open concurrent.futures.ThreadPoolExecutor")
    for i in _execute_concurrent_futures(
        concurrent.futures.ThreadPoolExecutor,
        mode=mode,
        func=func,
        iterable=iterable,
        fargs=fargs,
        fkwargs=fkwargs,
        max_workers=max_workers
    ):
        yield FinishedTask(i.result)


def _execute_concurrent_futures(
    executor, mode=None, func=None, iterable=None, fargs=None, fkwargs=None,
    max_workers=None, start_method=None
):
    if sys.version_info.minor < 7:
        if start_method in ["fork", None]:
            executor_kwargs = {}
        else:
            raise RuntimeError("in Python <3.7 only 'fork' is allowed as start_method")
    else:
        executor_kwargs = {
            "mp_context": multiprocessing.get_context(start_method)
        } if start_method else {}
    with executor(max_workers=max_workers, **executor_kwargs) as executor:
        if mode == "as_completed":
            for task in concurrent.futures.as_completed(
                (
                    executor.submit(func, *chain([item], fargs), **fkwargs)
                    for item in iterable
                )
            ):
                yield task
        elif mode == "map":
            for task in executor.map(
                partial(_worker_func, func, fargs, fkwargs), iterable
            ):
                yield task


_mode = {
    "concurrent_processes": _concurrent_processes,
    "concurrent_threads": _concurrent_threads,
    "billiard": _billiard,
    "multiprocessing": _multiprocessing
}
