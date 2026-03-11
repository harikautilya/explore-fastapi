import copy
from dataclasses import replace, dataclass, fields, is_dataclass
from typing import get_origin, get_args


@dataclass(frozen=True)
class CoreModel():

    def __post_init__(self):
        """
        Convert nested dicts into dataclass instances for annotated fields.
        """
        # Only operate if this object is a dataclass (subclasses will be)
        if not is_dataclass(self):
            return

        for f in fields(self):
            val = getattr(self, f.name)
            # if the value is a dict and the annotation is a dataclass type,
            # construct the nested dataclass instance
            if isinstance(val, dict):
                ann = f.type
                # Handle Optional/Union annotations by extracting args
                origin = get_origin(ann)
                if origin is None:
                    target = ann
                else:
                    args = get_args(ann)
                    # pick the first dataclass arg if present
                    target = None
                    for a in args:
                        if is_dataclass(a):
                            target = a
                            break

                if target and is_dataclass(target):
                    try:
                        inst = target(**val)
                        object.__setattr__(self, f.name, inst)
                    except Exception:
                        # If instantiation fails, leave the original dict
                        pass

    def copy(self, **changes):
        """
        Create a copy of the instance with update value, suggest to only when
        the model is frozen
        """
        new_instance = copy.deepcopy(self)
        return replace(new_instance, **changes)


