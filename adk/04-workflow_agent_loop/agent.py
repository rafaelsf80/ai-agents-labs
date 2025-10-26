# 04 - Loop Agent
# This is a multi agent system that uses `loop` flow setup.

import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

GEMINI_2_FLASH = "gemini-2.5-flash"
SAMPLE_CONTEXT = './04-workflow_agent_loop/context.json'

import json
from datetime import datetime
from google.adk.agents import Agent, LoopAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext


def debate_status(callback_context: CallbackContext):
    current_round = callback_context.state.get("current_round_number", 0)
    num_rounds = callback_context.state.get("num_debate_rounds", 0)
    print(f"END ROUND: {current_round}")
    callback_context.state["current_round_number"] = current_round + 1

def stop(reason: str, tool_context: ToolContext):
    """Indicate that the debate is over."""
    tool_context.actions.skip_summarization = True
    tool_context.actions.escalate = True

    return reason


def load_context(callback_context: CallbackContext):
    
    data = {}
    with open(SAMPLE_CONTEXT, "r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")

    context = data["state"]
    callback_context.state["topic"] = context["topic"]
    callback_context.state["num_debate_rounds"] = context["num_debate_rounds"]
    callback_context.state["current_round_number"] = context["current_round_number"]


affirmative_agent = Agent(
    model=GEMINI_2_FLASH,
    name='affirmative_agent',
    instruction="""
      You are the first speaker from the affirmative team in a debate.
      You are supportive to the topic.
      You will be given a topic to debate.
      Your job is to make a speech supporting the affirmative position.
      Your speech must be concise, less than 50 words.
      In addition to your statement, you can also ask a question to the other team.
      If there's a question to you, you will answer it.

      The topic is: {topic}""",)

opposition_agent = Agent(
    model=GEMINI_2_FLASH,
    name='opposition_agent',
    instruction="""
      You are the first speaker from the opposition team in a debate.
      You are against to the topic.
      You will be given a topic to debate.
      Your job is to make a speech supporting the opposition position.
      Your speech must be concise, less than 50 words.
      In addition to your statement, you can also ask a question to the other team.
      If there's a question to you, you will answer it.

      The topic is: {topic}""",)

judge_agent = Agent(
    model=GEMINI_2_FLASH,
    name='judge_agent',
    instruction="""
    You serve as the judge of a debate.
    Your job is to moderate the debate, ensuring that both sides have a fair
    chance to present their arguments.
    If any of the participants are rude or offensive, you reply with
    [warning], followed by a warning message.
    If you think the outcome of the debate is clear, you reply with [exit],
    followed by the winner and the reason.
    If there's nothing perticular, you reply with [continue] to let the debate
    continue.""",
    tools=[stop])

judge_agent.after_agent_callback = debate_status


root_agent = LoopAgent(
    name='debate_team',
    sub_agents=[affirmative_agent, opposition_agent, judge_agent],
    before_agent_callback=load_context
    )


# from agents.sessions.in_memory_session_service import InMemorySessionService
# from agents.artifacts.in_memory_artifact_service import InMemoryArtifactService
# from google.genai import types

# APP_NAME = "07-loops"
# USER_ID = "rafa"

# session_service = InMemorySessionService()
# artifact_service = InMemoryArtifactService()
# runner = Runner(root_agent, artifact_service, session_service)
# session = session_service.create(APP_NAME, USER_ID)

# def run_prompt(new_message: str):
#   content = types.Content(role='user', parts=[types.Part.from_text(text=new_message)])
#   for event in runner.run(
#       session=session,
#       new_message=content,
#   ):
#     if event.content:
#       parts = event.content.model_dump(exclude_none=True).get("parts")
#       for part in parts:
#           if part.get("text", None):
#               if event.content.role == "model":
#                   print(f"\033[32m[Agent {event.author}]\033[0m")  # green
#                   print(f"{part['text']}")
#               elif event.content.role == "user":
#                   print("\033[31mUser\033[0m")
#                   print(f"{part['text']}")

#           if part.get("function_call", None):
#               print("\033[34m[Tool]\033[0m") # blue
#               print(f"{part['function_call']}")

#           if part.get("function_response", None):
#               print("\033[33m[Tool result]\033[0m") # yellow
#               print(f"{part['function_response']}")


# run_prompt("Let's begin the debate!")