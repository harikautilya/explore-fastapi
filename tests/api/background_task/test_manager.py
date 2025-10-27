from api.background_task.managers import Manager
from api.background_task.executors import ConcurrentExecutor, SequentailExecutor, ParrallelExecutor
from api.background_task.task import Task
import time


class Sample(Task):
    work = {}

    def prepare(self):
        return super().prepare()

    def destroy(self):
        return super().destroy()

    def run(self, run_number):
        time.sleep(0.2)


def test_concurrent():
    from concurrent.futures import ThreadPoolExecutor

    thread_pool = ThreadPoolExecutor(max_workers=5)
    exec = ConcurrentExecutor(threadPoolExecutor=thread_pool)
    manager = Manager(executor=exec)

    for i in range(0, 10):
        manager.submit(Sample(run_number=i))

    t_start = time.time()
    manager.start()
    manager.stop()
    t_stop = time.time()

    execution_time = t_stop - t_start

    assert execution_time < 10 * 0.2

def test_seqentail():
    exec = SequentailExecutor()
    manager = Manager(executor=exec)
    for i in range(0, 10):
        manager.submit(Sample(run_number=i))
    t_start = time.time()
    manager.start()
    manager.stop()
    t_stop = time.time()

    execution_time = t_stop - t_start

    assert execution_time >= 10 * 0.2


def test_parrellel():
    from multiprocessing import Pool

    thread_pool = Pool(processes=5)
    exec = ParrallelExecutor(pool=thread_pool)
    manager = Manager(executor=exec)

    for i in range(0, 10):
        manager.submit(Sample(run_number=i))

    t_start = time.time()
    manager.start()
    manager.stop()
    t_stop = time.time()

    execution_time = t_stop - t_start

    assert execution_time < 10 * 0.2


def test_append_concurrent():
    from concurrent.futures import ThreadPoolExecutor

    thread_pool = ThreadPoolExecutor(max_workers=5)
    exec = ConcurrentExecutor(threadPoolExecutor=thread_pool)
    manager = Manager(executor=exec)

    for i in range(0, 10):
        manager.submit(Sample(run_number=i))

    t_start = time.time()
    manager.start()
    # append some more tasks
    for i in range(0, 10):
        manager.submit(Sample(run_number=i))
    manager.start()
    manager.stop()
    t_stop = time.time()

    execution_time = t_stop - t_start

    assert execution_time < 10 * 0.2