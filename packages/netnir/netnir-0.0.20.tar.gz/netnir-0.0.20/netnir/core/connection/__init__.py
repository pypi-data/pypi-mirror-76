def register_connections():
    """
    register nornir connection plugins
    """
    from nornir.core.connections import Connections
    from netnir.core.connection.netmiko import Netmiko
    from netnir.core.connection.netconf import Netconf

    Connections.deregister_all()
    Connections.register(name="netconf", plugin=Netconf)
    Connections.register(name="netmiko", plugin=Netmiko)
