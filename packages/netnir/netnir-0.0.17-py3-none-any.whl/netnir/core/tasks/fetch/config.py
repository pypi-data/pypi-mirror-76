from netnir.helpers.scaffold.command import CommandScaffold
from netnir.helpers.common.args import num_workers
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
        num_workers(parser)

    def run(self):
        """execute the cli task

        :return: nornir results
        """

        self.nr = self._inventory()
        results = self.nr.run(task=netmiko_send_commands, commands="show running")
        output_writer(nornir_results=results, output_file="running.conf")

        return print_result(results)
