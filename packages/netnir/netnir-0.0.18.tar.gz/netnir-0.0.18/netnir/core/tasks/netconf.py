from netnir.helpers.scaffold.command import CommandScaffold
from netnir.helpers.common.args import (
    netconf_config,
    netconf_filter,
    netconf_source,
    netconf_target,
    netconf_capabilities,
    config,
)


class NetConf(CommandScaffold):
    """netconf commands"""

    @staticmethod
    def parser(parser):
        CommandScaffold.parser(parser)
        netconf_config(parser)
        netconf_filter(parser)
        netconf_source(parser)
        netconf_target(parser)
        netconf_capabilities(parser)
        config(parser)

    def run(self):
        """execute netconf commands

        :returns: nornir Result object
        """
        from netnir.plugins.netconf import (
            netconf_get_config,
            netconf_edit_config,
            netconf_capabilities,
        )
        from nornir.plugins.functions.text import print_result

        self.nr = self._inventory()

        if self.args.capabilities:
            results = self.nr.run(
                task=netconf_capabilities, name="NETCONF SERVER CAPABILITIES",
            )
        elif self.args.config:
            results = self.nr.run(
                task=netconf_edit_config,
                name="NETCONF EDIT CONFIG",
                target=self.args.target,
                nc_config=self.args.nc_config,
            )
        else:
            results = self.nr.run(
                task=netconf_get_config,
                source=self.args.source,
                name="NETCONF GET FILTERED CONFIG",
                nc_filter_type=self.args.nc_filter,
                nc_filter=self.args.nc_config,
            )

        print_result(results)

        return results
