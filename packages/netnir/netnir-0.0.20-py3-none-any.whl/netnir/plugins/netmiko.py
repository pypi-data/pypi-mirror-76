from nornir.core.task import Task, Result
from typing import Any


def netmiko_send_commands(task: Task, commands: list(), **kwargs: Any) -> Result:
    """send show commands to a device via netmiko

    :param task: nornir Task object
    :param commands: a list of commands to execute

    :returns: nornir Result object
    """
    output = str()
    conn = task.host.get_connection(
        connection="netmiko", configuration=task.nornir.config
    )

    if isinstance(commands, str):
        commands = [commands]

    for command in commands:
        output += conn.send_command(command)

    return Result(host=task.host, result=output)


def netmiko_send_config(task: Task, commands: list(), **kwargs: Any) -> Result:
    """execute configuration changes on a device via netmiko

    :param task: nornir Task object
    :param commands: a list of commands to execute

    :returns: nornir Result object
    """
    output = str()
    conn = task.host.get_connection(
        connection="netmiko", configuration=task.nornir.config
    )
    output = conn.send_config_set(commands)
    output += conn.save()

    return Result(task.host, result=output)
