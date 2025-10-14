import copy
from dataclasses import replace, dataclass

@dataclass(frozen=True)
class CoreModel():
    

    def copy(self, **changes):
        """
        Create a copy of the instance with update value, suggest to only when
        the model is frozen
        """
        new_instance = copy.deepcopy(self)
        return replace(new_instance, **changes)


