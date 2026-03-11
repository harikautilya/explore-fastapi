from typing import Any
from abc import ABC, abstractmethod

class Task(ABC):

    is_success = False

    def __init__(self, *args, **kwargs):
        # keep raw inputs in case callers need them
        self.args = args
        self.kwargs = kwargs
        # merged dictionary of args and kwargs
        self.args_dict: dict[str, Any] = self.prepare_args()

    def prepare_args(self) -> dict[str, Any]:
        merged: dict[str, Any] = {f"arg{i}": v for i, v in enumerate(self.args)}
        # kwargs override positional entries if keys collide
        merged.update(self.kwargs)
        return merged

    @abstractmethod
    def prepare(self):
        pass
    
    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        """Make Task instances callable, forwarding to run()."""
        return self.run(*args, **kwargs)
