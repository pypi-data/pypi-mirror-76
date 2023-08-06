from nornir.core.task import Task, Result
from typing import Any


def inventory_facts(task: Task, **kwargs: Any) -> Result:
    """gather inventory facts

    :params task: type object

    :returns: inventory host facts dictionary
    """
    return Result(
        host=task.host, result={"facts": task.host.data, "groups": task.host.groups},
    )
