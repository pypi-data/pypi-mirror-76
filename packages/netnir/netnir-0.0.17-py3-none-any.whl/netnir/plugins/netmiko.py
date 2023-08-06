from nornir.core.task import Task, Result
from netmiko import ConnectHandler
from netnir.helpers import device_mapper


def netmiko_send_commands(task: Task, commands: list()) -> Result:
    """send show commands to a device via netmiko

    :param task: nornir Task object
    :param commands: a list of commands to execute

    :returns: nornir Result object
    """
    device_params = {
        "host": task.host.hostname,
        "device_type": device_mapper(os_type=task.host.platform, proto="netmiko"),
        "port": task.host.port,
        "username": task.host.username,
        "password": task.host.password,
        "secret": task.host.connection_options["netmiko"]["extras"].get("secret", None),
    }

    with ConnectHandler(**device_params) as conn:
        output = str()

        for command in commands:
            output += conn.send_command(command)

    return Result(host=task.host, result=output)


def netmiko_send_config(task: Task, commands: list()) -> Result:
    """execute configuration changes on a device via netmiko

    :param task: nornir Task object
    :param commands: a list of commands to execute

    :returns: nornir Result object
    """
    device_params = {
        "host": task.host.hostname,
        "device_type": device_mapper(os_type=task.host.platform, proto="netmiko"),
        "port": task.host.port,
        "username": task.host.username,
        "password": task.host.password,
        "secret": task.host.connection_options["netmiko"]["extras"].get("secret", None),
    }

    with ConnectHandler(**device_params) as conn:
        output = conn.send_config_set(commands)
        output += conn.save()

    return Result(task.host, result=output)
