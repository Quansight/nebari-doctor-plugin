from pydantic_ai import Agent

def run_agent(prompt: str) -> str:
    """
    Run the agent with a simple prompt.
    """
    agent = Agent(
        'google-gla:gemini-1.5-flash',
        system_prompt=prompt or 'Be concise, reply with one sentence.',
    )

    result = agent.run_sync('Where does "hello world" come from?')
    return result.data
    