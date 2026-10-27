# pip install -r requirements.txt, then: python main.py
# Runs a tiny OpenAI Agents SDK agent (scripted model, no API key needed)
# and prints an AER-1 receipt for the whole run.
import asyncio
from agents import Agent, Runner, function_tool
from agents.testing.model import ScriptedModel, assistant_message, function_call
from aer1_openai_agents import install

@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"Sunny in {city}"

async def main():
    processor = install(goal="Check the weather")
    scripted = ScriptedModel(steps=[
        [function_call("get_weather", {"city": "Austin"}, call_id="call_1")],
        [assistant_message("It is sunny in Austin.")],
    ])
    agent = Agent(name="weather", instructions="Answer briefly.",
                  tools=[get_weather])
    agent.model = scripted  # swap for your real model in production

    result = await Runner.run(agent, "What is the weather in Austin?")
    receipt = processor.finalize(final_answer=result.final_output)
    problems = processor.verify(receipt)
    assert problems == [], problems
    processor.save("receipt.json", receipt)
    print("final answer:", result.final_output)
    print("receipt id:", receipt.get("receipt_id") or receipt.get("id"))
    print("verified by the built-in AER-1 verifier: no problems")
    print("independent check: aer1-verify receipt.json")
    print("want this on your own ai: https://zambo.dev/add/?ref=zambo-template-openai-agents")

asyncio.run(main())
