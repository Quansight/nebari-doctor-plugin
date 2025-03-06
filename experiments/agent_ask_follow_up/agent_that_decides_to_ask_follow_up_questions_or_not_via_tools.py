import asyncio
from typing import Union

from pydantic import BaseModel, Field
from pydantic_ai import Agent

# from pydantic_ai.messages import (
#     ModelMessage,
#     ModelMessagesTypeAdapter,
#     ModelRequest,
#     ModelResponse,
#     TextPart,
#     UserPromptPart,
# )

# class GiveUp(BaseModel):
#     """Response when not enough information is available"""
#     message: str = Field(description="Message to the user explaining that more information is needed")


class Solution(BaseModel):
    """Response when enough information is available"""

    answer: str = Field(description="Solution to the user's problem")
    reasoning: str = Field(description="Explanation of how the solution was determined")


Response = Union[Solution]


def ask_user_for_more_info(question: str) -> str:
    """
    Prompt the user for additional information based on a follow-up question.

    Args:
        question (str): The follow-up question to display to the user

    Returns:
        str: The user's response to the follow-up question
    """
    print(question)
    user_input = input("User: ")
    return user_input


agent = Agent(
    "google-gla:gemini-2.0-flash",
    # 'anthropic:claude-3-5-sonnet-latest',
    result_type=Response,
    system_prompt="""You are a helpful assistant that either provides a solution or uses a tool to obtain more information.
    """,
    tools=[ask_user_for_more_info],
)


async def chat_with_agent():
    user_input = input("Please describe your problem: ")
    message_history = []

    while True:
        result = await agent.run(user_input, message_history=message_history)

        message_history.extend(result.new_messages())

        print(f"\nSolution: {result.data.answer}")
        print(f"Reasoning: {result.data.reasoning}")
        user_input = input("User: ")


if __name__ == "__main__":
    asyncio.run(chat_with_agent())
