from nebari.hookspecs import hookimpl
from nebari_doctor.agent import run_agent

import typer


@hookimpl
def nebari_subcommand(cli):
    @cli.command()
    def doctor(
        prompt: str = typer.Option(
            "Nebari", help="Who to say hello to"
        )
    ):
        run_agent()
