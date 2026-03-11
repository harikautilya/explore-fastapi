from typing import Any, List


def compare(listA: List[Any], listB: List[Any]):
    set_a = {frozenset(d.items()) for d in listA}
    set_b = {frozenset(d.items()) for d in listB}
    return set_a == set_b
