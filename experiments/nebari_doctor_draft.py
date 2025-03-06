import asyncio
from typing import Union

from pydantic import BaseModel, Field
from pydantic_ai import Agent


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


# get nebari config with descriptions
def get_nebari_config():
    pass


# getting relevant pod logs/status (maybe make an agent that summarizes anything it sees that could be related to the issue and the main agent just gets that summary)
def get_pod_names():
    return ["nebari-1", "nebari-2", "nebari-3"]


def get_pod_logs(pod_names, level="W", since_minutes: int = 10):
    pass


# getting relevant docs
def nebari_docs_rag():
    pass


def nebari_docs_outline():
    pass


# getting relevant nebari code base (at first), jupyter code base, argo code base, etc.


# getting relevant github issues/discussions on nebari repo (at first), jupyter repo, argo repo, etc.


def open_github_issue():
    # make sure user doesn't have confidential information in the github issue.
    pass


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
