import inspect
import pathlib
import textwrap
from typing import Optional, Callable, List, Dict, Any
from pydantic import BaseModel, Field
from pydantic_ai import Agent
import questionary
import rich
from rich.prompt import Prompt
from rich.panel import Panel
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


def display_tool_info(tools: List[Callable]) -> None:
    """
    Display information about available tools using questionary.
    
    Args:
        tools: List of tool functions
    """
    tool_names = [tool.__name__ for tool in tools]
    
    while True:
        choice = questionary.select(
            "Select a tool to see its documentation (or 'Exit' to continue):",
            choices=tool_names + ["Exit"]
        ).ask()
        
        if choice == "Exit":
            break
        
        # Find the selected tool and display its docstring
        for tool in tools:
            if tool.__name__ == choice:
                docstring = inspect.getdoc(tool) or "No documentation available"
                rich.print(Panel(docstring, title=f"[bold green]{choice}[/bold green]"))
                break


def get_tools_description(tools: List[Callable]) -> str:
    """
    Generate a description of available tools for the LLM prompt.
    
    Args:
        tools: List of tool functions
        
    Returns:
        str: Description of tools
    """
    tool_descriptions = []
    for tool in tools:
        name = tool.__name__
        doc = inspect.getdoc(tool)
        if doc:
            # Get the first line of the docstring as a brief description
            brief = doc.split('\n')[0].strip()
        else:
            brief = "No description available"
        tool_descriptions.append(f"- {name}: {brief}")
    
    return "\n".join(tool_descriptions)


USER_PROMPT = textwrap.dedent("""
    I am an AI Agent designed to help users with their Nebari issues. Tell me the issue you're seeing. I'll look at pod logs, the nebari config file, and the nebari code and docs to help you resolve your issue.
    
    Would you like to see information about the tools I have available?""")

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
        # Define tools
        tools = [
            message_user,
            make_get_nebari_config_tool(nebari_config_path),
            make_get_nebari_pod_names_tool(nebari_config_path),
            get_nebari_pod_logs_tool,
        ]
        
        # Ask if user wants to see tool information
        rich.print(USER_PROMPT)
        show_tools = questionary.confirm("Would you like to see information about available tools?").ask()
        
        if show_tools:
            display_tool_info(tools)
        
        # Create tool description for LLM prompt
        tools_description = get_tools_description(tools)
        enhanced_prompt = f"{LLM_PROMPT}\n\nAvailable tools:\n{tools_description}"
        
        agent = Agent(
            # 'google-gla:gemini-2.0-flash',
            'openai:gpt-4o',
            system_prompt=enhanced_prompt,
            result_type=ChatResponse,
            tools=tools,
        )

        latest_result = ChatResponse(message=USER_PROMPT)
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
    
    
