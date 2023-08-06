from nornir.core.task import Task, Result
from netnir.helpers import device_mapper
from ncclient import manager
from typing import Any


def netconf_capabilities(task: Task, **kwargs: Any) -> Result:
    """nornir get netconf capabilities

    :params task: type object
    :returns: nornir result object
    """
    device_params = {
        "host": task.host.hostname,
        "port": task.host.port or 830,
        "username": task.host.username,
        "password": task.host.password,
        "hostkey_verify": False,
        "device_params": {
            "name": device_mapper(os_type=task.host.data["os"], proto="netconf")
        },
    }

    with manager.connect(**device_params) as conn:
        results = [capability for capability in conn.server_capabilities]

    return Result(host=task.host, result=results)


def netconf_get_config(
    task: Task,
    source: str = "running",
    nc_filter: str = None,
    nc_filter_type: str = None,
    **kwargs: Any
) -> Result:
    """nornir netconf get config task

    :params task: type object
    :params source: type str - configuration source
    :params nc_filter: type str - netconf filter
    :params nc_filter_type: type str
    :returns: nornir result object
    """
    device_params = {
        "host": task.host.hostname,
        "port": task.host.port or 830,
        "username": task.host.username,
        "password": task.host.password,
        "hostkey_verify": False,
        "device_params": {
            "name": device_mapper(os_type=task.host.data["os"], proto="netconf")
        },
    }

    with manager.connect(**device_params) as conn:
        if nc_filter and nc_filter_type:
            with open(nc_filter) as xml:
                nc_filter = xml.read()

            result = conn.get_config(source=source, filter=(nc_filter_type, nc_filter))
        else:
            result = conn.get_config(source=source)

    return Result(result=result, host=task.host)


def netconf_edit_config(
    task: Task, target: str = "running", nc_config: str = None
) -> Result:
    """nornir netconf edit config task

    :params task: type object
    :params target: type str - configuration target
    :params nc_config: type str - yang config model
    :returns: nornir result object
    """
    device_params = {
        "host": task.host.hostname,
        "port": task.host.port or 830,
        "username": task.host.username,
        "password": task.host.password,
        "hostkey_verify": False,
        "device_params": {
            "name": device_mapper(os_type=task.host.data["os"], proto="netconf")
        },
    }

    with manager.connect(**device_params) as conn:
        with open(nc_config) as xml:
            nc_config = xml.read()

        config_response = conn.edit_config(target=target, config=nc_config)
        config_validate = conn.validate(source=target)

        if config_response.ok and config_validate.ok:
            result = {
                "config_response": config_response.ok,
                "config_validate": config_validate.ok,
            }
            failed = False
            conn.commit()
        else:
            result = {
                "config_response": config_response.error,
                "config_validate": config_validate.error,
            }
            failed = True
            conn.discard_changes()

    return Result(result=result, host=task.host, failed=failed)
