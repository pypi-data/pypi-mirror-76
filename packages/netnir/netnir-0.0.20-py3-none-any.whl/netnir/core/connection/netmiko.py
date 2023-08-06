from typing import Any, Dict, Optional
from nornir.core.connections import ConnectionPlugin
from nornir.core.configuration import Config


class Netmiko(ConnectionPlugin):
    """
    This plugin connects to the device using the Netmiko driver and sets the
    relevant connection.
    Inventory:
        extras: maps to argument passed to ``ConnectHandler``.
    """

    def open(
        self,
        hostname: Optional[str],
        username: Optional[str],
        password: Optional[str],
        port: Optional[int],
        platform: Optional[str],
        extras: Optional[Dict[str, Any]] = None,
        configuration: Optional[Config] = None,
    ) -> None:
        from netnir.helpers import device_mapper
        from netmiko import ConnectHandler

        parameters = {
            "host": hostname,
            "username": username,
            "password": password,
            "port": port or 22,
        }

        try:
            parameters[
                "ssh_config_file"
            ] = configuration.ssh.config_file  # type: ignore
        except AttributeError:
            pass

        if platform is not None:
            platform = device_mapper(os_type=platform, proto="netmiko")
            parameters["device_type"] = platform

        extras = extras or {}
        parameters.update(extras)
        self.connection = ConnectHandler(**parameters)

    def close(self) -> None:
        self.connection.disconnect()
