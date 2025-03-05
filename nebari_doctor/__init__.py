import pathlib
import textwrap
from nebari.hookspecs import hookimpl
from nebari_doctor.agent import USER_PROMPT, run_agent

import typer

user_issue = 'My user ad tried to shut down the My Panel App (Git) app started by Andy.  The Jupyterhub landing page said "Server stopped succesfully", bu tthe Status of the dashboard remained "Running".  What\'s going on?'

@hookimpl
def nebari_subcommand(cli):
    @cli.command()
    def doctor(
        prompt: str = typer.Option(
            user_issue,
            # '--prompt', '-p',  help="Describe your Nebari issue", prompt=USER_PROMPT
        ),
        config_filename: pathlib.Path = typer.Option(
            ...,
            "--config",
            "-c",
            help="nebari configuration yaml file path",
        ),
    ):
        
        result = run_agent(prompt, config_filename)
        print(result)
