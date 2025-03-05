import pathlib
import textwrap
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent
import questionary
import rich
from rich.prompt import Prompt
from nebari_doctor.tools.get_nebari_config import make_get_nebari_config_tool
from nebari_doctor.tools.get_pod_logs import get_nebari_pod_logs_tool, make_get_nebari_pod_names_tool, get_nebari_pod_logs_tool
from nebari_doctor.prompts import LLM_PROMPT

MODEL_CONTEXT_LIMIT = {
    # Not in pydantic-ai somewhere
    'openai:gpt-4o': 128_000,
    'google-gla:gemini-2.0-flash-exp': 1_000_000,
}


# def directory_structure():
#     """ Returns directory structure (recursively) + number of tokens in each document"""
#     pass

def message_user(message: str) -> str:
    """
    Send a message to the user.  This tool is used to update the user on the status of trying to fix their problem or to ask the user for additional information, or any other message that the agent wants to send to the user.
    
    Args:
        message (str): message to display to user
        
    Returns:
        str: user's response to the message
    """
    rich.print(f'Agent: [bright_yellow]{message}[/bright_yellow]\n')
    user_input = Prompt.ask('User',)
    # print(question)
    # user_input = input("User: ")
    return user_input


USER_PROMPT = textwrap.dedent("""
    I am an AI Agent designed to help users with their Nebari issues.  Tell me the issue you're seeing.  I'll look at pod logs, the nebari config file, and the nebari code and docs to help you resolve your issue.""")

# INITIAL_NEBARI_ISSUE = textwrap.dedent("""
#     My user "ad" tried to shGetting podsut down the My Panel App (Git) app started by Andy.  The Jupyterhub landing page said "Server stopped succesfully", but the Status of the dashboard remained "Running".  What\'s going on?""".strip())

INITIAL_NEBARI_ISSUE = textwrap.dedent("""
    Does anything look wrong with my nebari config?""".strip())


class ChatResponse(BaseModel):
    message: str = Field(description="The message to display to the user.")


def run_agent(prompt: str, nebari_config_path: pathlib.Path) -> str:
    """
    Run the agent with a simple prompt.
    """
    try:
        agent = Agent(
            # 'google-gla:gemini-2.0-flash',
            'openai:gpt-4o',
            system_prompt=LLM_PROMPT,
            result_type=ChatResponse,
            tools=[
                message_user,
                make_get_nebari_config_tool(nebari_config_path),
                make_get_nebari_pod_names_tool(nebari_config_path),
                get_nebari_pod_logs_tool,
            ],
        )

        latest_result  = ChatResponse(message=USER_PROMPT)
        i = 0
        message_history = []
        user_input = INITIAL_NEBARI_ISSUE
        rich.print(f'User: [cyan]{user_input}[/cyan]', end='\n\n')            
        while True:
            result = agent.run_sync(user_input)#, message_history=message_history)
            latest_result = result.data
            message_user(latest_result.message)
    except KeyboardInterrupt:
        print('Exiting...')
    except Exception as e:
        print('An error occurred.  Now Exiting...')
        print(e)
    
    