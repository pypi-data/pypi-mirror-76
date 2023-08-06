from netnir.helpers.scaffold.command import CommandScaffold


class Inventory(CommandScaffold):
    """
    cli based inventory search
    """

    def run(self):
        from netnir.plugins.facts import inventory_facts
        from nornir.plugins.functions.text import print_result

        self.nr = self._inventory()
        results = self.nr.run(
            task=inventory_facts,
            name="INVENTORY FACTS",
            num_workers=self.args.workers,
            dry_run=self.args.X,
            severity_level=self._verbose()["level"],
            to_console=self._verbose()["to_console"],
        )

        print_result(result=results, severity_level=self._verbose()["level"])

        return results
