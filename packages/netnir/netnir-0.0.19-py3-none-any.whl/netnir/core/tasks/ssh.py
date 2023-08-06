from netnir.helpers.scaffold.command import CommandScaffold
from netnir.plugins.netmiko import netmiko_send_commands, netmiko_send_config
from netnir.helpers import output_writer
from netnir.helpers.common.args import (
    output,
    commands,
    config,
)
from nornir.plugins.functions.text import print_result


class Ssh(CommandScaffold):
    """
    cli command to execute show and config commands via SSH
    """

    @staticmethod
    def parser(parser):
        """
        cli command parser
        """
        CommandScaffold.parser(parser)
        output(parser)
        commands(parser)
        config(parser)

    def run(self):
        """
        cli command execution
        """

        self.nr = self._inventory()

        if self.args.config:
            results = self.nr.run(
                task=netmiko_send_config,
                commands=self.args.commands,
                name="SSH CONFIG EXECUTION",
                num_workers=self.args.workers,
                dry_run=self.args.X,
                severity_level=self._verbose()["level"],
                to_console=self._verbose()["to_console"],
            )
        else:
            results = self.nr.run(
                task=netmiko_send_commands,
                commands=self.args.commands,
                name="SSH COMMAND EXECUTION",
                num_workers=self.args.workers,
                dry_run=self.args.X,
                severity_level=self._verbose()["level"],
                to_console=self._verbose()["to_console"],
            )

        if self.args.output:
            output_writer(nornir_results=results, output_file=self.args.output)

        print_result(result=results, severity_level=self._verbose()["level"])

        return results
