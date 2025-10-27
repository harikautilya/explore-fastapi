from concurrent.futures import ThreadPoolExecutor
from .task import Task
from typing import List
from multiprocessing.pool import Pool as PoolType

class Executor:
    def run(self, tasks: List[Task]):
        pass

    def stop(self):
        pass


class ConcurrentExecutor(Executor):
    threadPoolExecutor: ThreadPoolExecutor

    def __init__(self, threadPoolExecutor: ThreadPoolExecutor):
        super().__init__()
        self.threadPoolExecutor = threadPoolExecutor

    def run(self, tasks: List[Task]):
        futures = [
            self.threadPoolExecutor.submit(task.run, **task.prepare_args())
            for task in tasks
        ]

    def stop(self):
        self.threadPoolExecutor.shutdown(wait=True)


class SequentailExecutor(Executor):
    threadPoolExecutor: ThreadPoolExecutor

    def __init__(self):
        super().__init__()
        self.threadPoolExecutor = ThreadPoolExecutor(max_workers=1)

    def run(self, tasks: List[Task]):

        for task in tasks:
            try:
                future = self.threadPoolExecutor.submit(task.run, **task.prepare_args())
                future.result()
            except:
                pass

    def stop(self):
        self.threadPoolExecutor.shutdown(wait=True)

class ParrallelExecutor(Executor):
    pool: PoolType

    def __init__(self, pool: PoolType):
        super().__init__()
        self.pool = pool

    def run(self, tasks):
        for task in tasks:
            self.pool.apply_async(task.run, kwds=task.prepare_args())

    def stop(self):
        self.pool.close()
        self.pool.join()