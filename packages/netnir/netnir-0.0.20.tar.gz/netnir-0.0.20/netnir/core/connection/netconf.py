from typing import Any, Dict, Optional
from nornir.core.configuration import Config
from nornir.core.connections import ConnectionPlugin


class Netconf(ConnectionPlugin):
    """
    This plugin connects to the device via NETCONF using ncclient library.
    Inventory:
        extras: See
        `here <https://ncclient.readthedocs.io/en/latest/transport.html#ncclient.transport.SSHSession.connect>`_
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
        from ncclient import manager
        from pathlib import Path

        extras = extras or {
            "hostkey_verify": False,
            "allow_agent": False,
            "device_params": {"name": device_mapper(os_type=platform, proto="netconf")},
        }
        parameters: Dict[str, Any] = {
            "host": hostname,
            "username": username,
            "password": password,
            "port": port or 830,
        }

        if "ssh_config" not in extras:
            try:
                ssh_config_file = Path(configuration.ssh.config_file)
                if ssh_config_file.exists():
                    parameters["ssh_config"] = ssh_config_file
            except AttributeError:
                pass

        parameters.update(extras)

        connection = manager.connect(**parameters)
        self.connection = connection

    def close(self) -> None:
        self.connection.close_session()
