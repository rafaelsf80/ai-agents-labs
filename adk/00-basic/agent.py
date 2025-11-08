# 00 - Basic agent
# Reference: https://github.com/google/adk-python/issues/28

# NOTE: this script uses Runner and SessionService to emulate an agent runtime environment. It does not need "adk run"
# Output parsing with colors: https://stackoverflow.com/questions/58030468/how-to-have-colors-in-terminal-with-python-in-vscode

from google.adk.agents import Agent

GEMINI_2_FLASH = "gemini-2.5-flash"

root_agent = Agent(
    model=GEMINI_2_FLASH,
    name='root_agent',
    instruction='If they ask you where is the greatest Agents event, tell them its happening inow with BBVA.',
)


import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.runners import Runner
from google.genai import types

APP_NAME = "00-basic"
USER_ID = "rafa"

from dotenv import load_dotenv
load_dotenv()

# Set up Runner and Session service

session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

runner = Runner(agent=root_agent, app_name=APP_NAME, artifact_service=artifact_service, session_service=session_service)

# Agent Interaction (Since LLM calls and tool executions can take time, ADK's Runner operates asynchronously)
async def run_prompt(new_message: str):

    #Create the specific session where the conv ersation will happen
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID
    )  

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part.from_text(text=new_message)])

    #Key Concept: run_async executes the agent logic and yields Events.
    #We iterate through events to find the final answer.
    try:
        async for event in runner.run_async(
            user_id=session.user_id, session_id=session.id, new_message=content
        ):
            print(f"Event ID: {event.id}, Author: {event.author}, Session: {session.id}")

            if event.content:
                parts = event.content.model_dump(exclude_none=True).get("parts")
                for part in parts:
                    if part.get("text", None):
                        if event.content.role == "model":
                            print(f"\033[32m[Agent {event.author}]\033[0m")  # green
                            print(f"{part['text']}")
                        elif event.content.role == "user":
                            print("\033[31mUser\033[0m")
                            print("HI")
                            print(f"{part['text']}")

                    if part.get("function_call", None):
                        print("\033[34m[Tool]\033[0m") # blue
                        print(f"{part['function_call']}")

                    if part.get("function_response", None):
                        print("\033[33m[Tool result]\033[0m") # yellow
                        print(f"{part['function_response']}")
    except Exception as e:
        print(f"ERROR during agent run: {e}")
    print("-" * 30)

from importlib.metadata import version
print(f"google-adk {version('google-adk')}, google-cloud-aiplatform {version('google-cloud-aiplatform')}, google-genai {version('google-genai')}")

async def main():
    await run_prompt("how were you built?")

if __name__ == "__main__":
    asyncio.run(main())

# google-adk 1.12.0, google-cloud-aiplatform 1.110.0, google-genai 1.31.0
# Event ID: ced3f0dc-823f-4e58-aa50-1d7e358fc73f, Author: root_agent, Session: 26a02038-ef03-4df2-b041-7135f8b62d18
# [Agent root_agent]
# I was created with the greatest framework.