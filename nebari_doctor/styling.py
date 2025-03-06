"""
Styling utilities for Nebari Doctor CLI interface.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.table import Table
from rich.theme import Theme

# Define a custom theme with consistent colors
NEBARI_THEME = Theme(
    {
        # Main conversation colors
        "agent": "bold bright_blue",
        "user": "bold bright_cyan",
        "tool_name": "bold green",
        "tool_output": "dim white",
        "error": "bold red",
        "warning": "yellow",
        "success": "green",
        # UI elements
        "header": "bold bright_magenta",
        "border": "bright_blue",
        "prompt": "bold bright_white",
        "info": "italic bright_black",
    }
)

# Create a console with our theme
console = Console(theme=NEBARI_THEME)


class MessageType(Enum):
    AGENT = "agent"
    USER = "user"
    TOOL = "tool"
    SYSTEM = "system"
    ERROR = "error"


def format_code(code: str, language: str = "yaml") -> Syntax:
    """Format code with syntax highlighting"""
    return Syntax(code, language, theme="monokai", line_numbers=True, word_wrap=True)


def display_message(
    message: str, message_type: MessageType, title: Optional[str] = None
) -> None:
    """Display a formatted message in the appropriate style"""
    if message_type == MessageType.AGENT:
        panel = Panel(
            Markdown(message),
            title=title or "🤖 Nebari Doctor",
            title_align="left",
            border_style="agent",
            padding=(1, 2),
            expand=False,
        )
        console.print(panel)

    elif message_type == MessageType.USER:
        panel = Panel(
            message,
            title=title or "👤 User",
            title_align="left",
            border_style="user",
            padding=(1, 2),
            expand=False,
        )
        console.print(panel)

    elif message_type == MessageType.TOOL:
        panel = Panel(
            message,
            title=title or "🔧 Tool Output",
            title_align="left",
            border_style="tool_name",
            style="tool_output",
            padding=(1, 2),
            expand=False,
        )
        console.print(panel)

    elif message_type == MessageType.SYSTEM:
        console.print(f"[info]{message}[/info]")

    elif message_type == MessageType.ERROR:
        panel = Panel(
            message,
            title="❌ Error",
            title_align="left",
            border_style="error",
            padding=(1, 2),
            expand=False,
        )
        console.print(panel)


def get_user_input(prompt_text: str = "What would you like to know?") -> str:
    """Get input from the user with styled prompt"""
    return Prompt.ask(f"[prompt]{prompt_text}[/prompt]")


def display_header(title: str) -> None:
    """Display a header with the Nebari Doctor title"""
    console.print()
    console.rule(f"[header]{title}[/header]")
    console.print()


def display_tool_list(tools: List[Dict[str, Any]]) -> None:
    """Display a formatted list of available tools"""
    table = Table(title="Available Tools", expand=True)
    table.add_column("Tool", style="tool_name")
    table.add_column("Description", style="info")

    for tool in tools:
        table.add_row(tool["name"], tool["description"])

    console.print(table)
    console.print()
