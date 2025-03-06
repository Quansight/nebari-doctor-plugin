import pathlib
from typing import Optional

import typer
from nebari.hookspecs import hookimpl

from nebari_doctor.agent import INITIAL_NEBARI_ISSUE, USER_PROMPT, run_agent  # noqa: F401

user_issue = 'My user ad tried to shut down the My Panel App (Git) app started by Andy.  The Jupyterhub landing page said "Server stopped successfully", but the Status of the dashboard remained "Running".  What\'s going on?'


@hookimpl
def nebari_subcommand(cli):
    doctor_app = typer.Typer(help="Diagnose and fix Nebari issues")
    
    @doctor_app.command()
    def diagnose(
        prompt: str = typer.Option(
            None,
            '--prompt', '-p',  help="Describe your Nebari issue", prompt=USER_PROMPT
        ),
        config_filename: pathlib.Path = typer.Option(
            ...,
            "--config",
            "-c",
            help="nebari configuration yaml file path",
        ),
    ):
        """Run the doctor with your own prompt and config file."""
        # Use provided prompt or get it interactively
        if prompt is None:
            prompt = typer.prompt(USER_PROMPT)

        result = run_agent(prompt, config_filename)
        print(result)
    
    @doctor_app.command()
    def demo():
        """Run the doctor in demo mode with a predefined prompt and config."""
        prompt = INITIAL_NEBARI_ISSUE
        config_filename = pathlib.Path("demo_config.yaml")
        
        result = run_agent(prompt, config_filename)
        print(result)
    
    cli.add_typer(doctor_app, name="doctor")
