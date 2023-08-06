from netnir.helpers.scaffold.command import CommandScaffold
from netnir.helpers import output_writer
from netnir.plugins.netmiko import netmiko_send_commands
from nornir.plugins.functions.text import print_result


class FetchConfig(CommandScaffold):
    """
    cli command to fetch remote device configs via nornir's netmiko_show_command plugin
    """

    @staticmethod
    def parser(parser):
        """cli command parser

        :param parser: type obj
        """
        CommandScaffold.parser(parser)

    def run(self):
        """execute the cli task

        :return: nornir results
        """

        self.nr = self._inventory()
        results = self.nr.run(
            task=netmiko_send_commands,
            commands="show running",
            num_workers=self.args.workers,
            dry_run=self.args.X,
            severity_level=self._verbose()["level"],
            to_console=self._verbose()["to_console"],
            name="FETCH RUNNING CONFIG",
        )
        output_writer(nornir_results=results, output_file="running.conf")

        print_result(result=results, severity_level=self._verbose()["level"])

        return results
