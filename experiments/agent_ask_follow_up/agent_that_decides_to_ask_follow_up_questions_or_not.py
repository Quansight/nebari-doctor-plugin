import asyncio
from typing import Union

from pydantic import BaseModel, Field
from pydantic_ai import Agent


class FollowUpQuestion(BaseModel):
    """Response when more information is needed"""

    question: str = Field(description="Follow-up question to ask the user")
    explanation: str = Field(description="Why this information is needed")


class Solution(BaseModel):
    """Response when enough information is available"""

    answer: str = Field(description="Solution to the user's problem")
    reasoning: str = Field(description="Explanation of how the solution was determined")


Response = Union[FollowUpQuestion, Solution]

agent = Agent(
    "google-gla:gemini-2.0-flash",
    # 'anthropic:claude-3-5-sonnet-latest',
    result_type=Response,
    system_prompt="""You are a helpful assistant that either:
    1. Asks for more information if the user's problem description is unclear
    2. Provides a solution if enough information is available

    Return a FollowUpQuestion if you need more details.
    Return a Solution if you have enough information.
    """,
)


async def chat_with_agent():
    user_input = input("Please describe your problem: ")
    message_history = []

    while True:
        result = await agent.run(user_input, message_history=message_history)

        message_history.extend(result.new_messages())

        if isinstance(result.data, Solution):
            print(f"\nSolution: {result.data.answer}")
            print(f"Reasoning: {result.data.reasoning}")
            break
        else:
            print(f"\nNeed more information: {result.data.explanation}")
            print(f"Question: {result.data.question}")

            user_input = input("\nYour response: ")


if __name__ == "__main__":
    asyncio.run(chat_with_agent())
