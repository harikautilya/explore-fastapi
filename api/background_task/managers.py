from .task import Task
from .executors import Executor

from typing import List


class Manager:

    tasks: List[Task]
    exceutor: Executor

    def __init__(self, executor: Executor):
        self.exceutor = executor
        self.tasks = []

    def submit(self, task: Task):
        self.tasks.append(task)

    def start(self):
        self.exceutor.run(self.tasks)

    def stop(self):
        self.exceutor.stop()
