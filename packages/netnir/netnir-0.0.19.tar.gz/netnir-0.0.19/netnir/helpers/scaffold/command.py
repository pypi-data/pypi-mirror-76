class CommandScaffold:
    """ scaffold class """

    def __init__(self, args):
        """initialize the class

        :params args: type object
        """
        from netnir.constants import NR
        import logging

        self.args = args
        self.logging = logging.getLogger("nornir")
        self.nr = NR

    @staticmethod
    def parser(parser):
        """command parser function

        :params parser: type object
        """
        from netnir.helpers.common.args import (
            filter_host,
            filter_hosts,
            filter_group,
            num_workers,
            make_changes,
            verbose,
        )

        filter_host(parser)
        filter_hosts(parser)
        filter_group(parser)
        num_workers(parser)
        make_changes(parser)
        verbose(parser)

    def run(self):
        """things to do"""
        return "things to do"

    def _verbose(self):
        self.logging.setLevel(self.args.verbose)
        to_console = True if self.args.verbose == "DEBUG" else False

        return {"level": self.logging.level, "to_console": to_console}

    def _inventory(self):
        """filter inventory

        :returns: filtered nornir inventory object
        """
        from netnir.helpers import inventory_filter, filter_type

        devices_filter = filter_type(
            host=self.args.host, filter=self.args.filter, group=self.args.group
        )
        self.nr = inventory_filter(
            nr=self.nr,
            device_filter=devices_filter["data"],
            type=devices_filter["type"],
        )

        return self.nr
