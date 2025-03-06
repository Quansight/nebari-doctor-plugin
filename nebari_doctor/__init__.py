import pathlib
from typing import Optional

import typer
from nebari.hookspecs import hookimpl

from nebari_doctor.agent import INITIAL_NEBARI_ISSUE, USER_PROMPT, run_agent  # noqa: F401

user_issue = 'My user ad tried to shut down the My Panel App (Git) app started by Andy.  The Jupyterhub landing page said "Server stopped successfully", but the Status of the dashboard remained "Running".  What\'s going on?'


@hookimpl
def nebari_subcommand(cli):
    @cli.command()
    def doctor(
        prompt: str = typer.Option(
            None,
            '--prompt', '-p',  help="Describe your Nebari issue", prompt=USER_PROMPT
        ),
        config_filename: Optional[pathlib.Path] = typer.Option(
            None,
            "--config",
            "-c",
            help="nebari configuration yaml file path",
        ),
        demo: bool = typer.Option(
            False,
            "--demo",
            help="Run in demo mode with sample config and predefined prompt",
        ),
    ):
        # In demo mode, use predefined prompt and don't require config file
        if demo:
            prompt = INITIAL_NEBARI_ISSUE
            # Use a dummy config path if none provided in demo mode
            if config_filename is None:
                config_filename = pathlib.Path("demo_config.yaml")
        # In normal mode, config file is required
        elif config_filename is None:
            typer.echo("Error: --config option is required when not in demo mode")
            raise typer.Exit(1)
        
        # Use provided prompt or get it interactively if not in demo mode
        if prompt is None and not demo:
            prompt = typer.prompt(USER_PROMPT)

        result = run_agent(prompt, config_filename)
        print(result)
