from typing import Any


class Task:
    """Base background task.

    This class collects positional and keyword arguments passed to the
    constructor and normalizes them into a single dictionary available as
    ``self.args_dict``. Positional args are stored with keys ``arg0``,
    ``arg1``, ...; keyword args are merged and will override any positional
    keys if the same key is used.
    """

    is_success = False

    def __init__(self, *args, **kwargs):
        # keep raw inputs in case callers need them
        self.args = args
        self.kwargs = kwargs
        # merged dictionary of args and kwargs
        self.args_dict: dict[str, Any] = self.prepare_args()

    def prepare_args(self) -> dict[str, Any]:
        """Convert positional ``args`` and ``kwargs`` into a single dict.

        Positional arguments become keys ``arg0``, ``arg1``, etc. Keyword
        arguments are merged into the same dict and will override positional
        entries when keys collide.

        Returns:
            A dict containing all provided arguments.
        """
        merged: dict[str, Any] = {f"arg{i}": v for i, v in enumerate(self.args)}
        # kwargs override positional entries if keys collide
        merged.update(self.kwargs)
        return merged

    def prepare(self):
        pass

    def destroy(self):
        pass

    def run(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        """Make Task instances callable, forwarding to run()."""
        return self.run(*args, **kwargs)
