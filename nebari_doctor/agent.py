import textwrap
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent
import questionary
import rich
from nebari_doctor.prompts import LLM_PROMPT

MODEL_CONTEXT_LIMIT = {
    # May be in pydantic-ai somewhere
    'openai:gpt-4o': 128_000,
    'google-gla:gemini-2.0-flash-exp': 1_000_000,
}


def directory_structure():
    """ Returns directory structure (recursively) + number of tokens in each document"""
    pass

def get_pod_summary():
    """
    Get the logs from the nebari pod.
    """
    return 'logs'

def get_pod_logs():
    """
    Get the logs for the last 5 minutes from the pods.
    """
    # ~15_000_000 tokens for all logs
    print('Getting last 5 minutes of pod logs...', end='\n\n')
    from nebari_doctor.pod_logs import POD_LOGS
    return POD_LOGS

# def get_nebari_docs():
#     """
#     Get the nebari docs.
#     """
#     # ~138_000 tokens
#     return 'docs'

# def get_nebari_code():
#     """
#     Get the nebari code.
#     """
#     # ~350_000 tokens
#     return 'code'

def get_nebari_config():
    """
    Get the nebari config.
    """
    return 'config'

USER_PROMPT = textwrap.dedent("""
    I am an AI Agent designed to help users with their Nebari issues.  Tell me the issue you're seeing.  I'll look at pod logs, the nebari config file, and the nebari code and docs to help you resolve your issue.""")

INITIAL_NEBARI_ISSUE = textwrap.dedent("""
    My user "ad" tried to shut down the My Panel App (Git) app started by Andy.  The Jupyterhub landing page said "Server stopped succesfully", but the Status of the dashboard remained "Running".  What\'s going on?""".strip())

class ChatResponse(BaseModel):
    message: str = Field(description="The message to display to the user.")


def run_agent(prompt: str = None) -> str:
    """
    Run the agent with a simple prompt.
    """
    try:
        agent = Agent(
            'google-gla:gemini-2.0-flash',
            # 'openai:gpt-4o',
            system_prompt=LLM_PROMPT,
            result_type=ChatResponse,
            tools=[get_pod_logs],
        )

        latest_result  = ChatResponse(message=USER_PROMPT)
        i = 0
        message_history = []
        user_input = INITIAL_NEBARI_ISSUE
        rich.print(f'User: [cyan]{user_input}[/cyan]', end='\n\n')            
        while True:
            result = agent.run_sync(user_input)#, message_history=message_history)
            latest_result = result.data
            rich.print(f'Agent: [bright_yellow]{latest_result.message}[/bright_yellow]\n')
            user_input = rich.prompt.Prompt.ask('User',)
    except KeyboardInterrupt:
        print('Exiting...')
    except Exception as e:
        print('An error occurred.  Now Exiting...')
        print(e)
    
    