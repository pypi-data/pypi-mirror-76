#!/usr/bin/env python3
import click
from godale import Executor
from memory_profiler import profile
from sys import getsizeof
import time

import worker_func


@click.command()
@click.option('--executor', '-e', default="multiprocessing")
@click.option('--start_method', '-s', default="fork")
def run_tests(executor, start_method):
    _run_tests(executor, start_method)


@profile
def _run_tests(executor, start_method):
    data = worker_func.SomeDataClass()
    start = time.time()
    for task in Executor(executor=executor, start_method=start_method).as_completed(
        func=worker_func.worker_func,
        iterable=range(1000),
        fargs=(10, ),
        # fkwargs={"data": data},
        chunksize=1
    ):
        # print(task)
        pass
    end = time.time()
    click.echo(
        "%s %s executed in %ss" % (
            executor, start_method, round(end - start, 3)
        )
    )
    getsizeof(data)

if __name__ == '__main__':
    run_tests()
