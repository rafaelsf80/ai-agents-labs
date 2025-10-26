# 03 - Non-conversational multiagent
# This is a multi agent system that uses `sequential` flow setup.
# (Root) -> (A) -> (B) -> (C) -> [END]

import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

GEMINI_2_FLASH = "gemini-2.5-flash"
SAMPLE_CONTEXT = './03-workflow_agent_sequential/context.json'


import json
from datetime import datetime
from google.adk.agents import Agent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
     
developer = Agent(
    model=GEMINI_2_FLASH,
    name="developer",
    instruction="""
	 You are a software engineer at a leading tech company.
	 Your expertise in programming in python. and do your best to produce perfect code.
        You will create a game using python, these are the instructions:

        Game: {game}

        Your Final answer must be the full python code,
        only the python code and nothing else."""
)

reviewer = Agent(
    model=GEMINI_2_FLASH,
    name="reviewer",
    instruction="""
      You are a software engineer that specializes in checking code for errors. You have an eye for detail and a knack for finding hidden bugs.

      You are reviewing a game developed using python, these are the instructions:

      Game: {game}

      Using the code you got, check for errors. Check for logic errors, syntax errors, missing imports, variable declarations, mismatched brackets, and security vulnerabilities.
      Your Final answer is a bullet list of errors you found or suggestions to improve the code.
      You are not asked to run the code. You just need to provide feedback."""
)

team_lead = Agent(
    model=GEMINI_2_FLASH,
    name="team_lead",
    instruction="""
      You are a senior software engineer TL at a leading tech company.
      You are helping a junior software engineer improve their code.
      Their code creates a game using python, these are the instructions:

      Game: {game}

      Based on the code the developer_agent wrote, and the feedback from the reviewer_agent,
      you will improve the code.

      Your final answer must be the full python code, only the python code and nothing else."""
)


def load_context(callback_context: CallbackContext):
    
    data = {}
    with open(SAMPLE_CONTEXT, "r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")

    context = data["state"]
    callback_context.state["game"] = context["game"]
    callback_context.state["time"] = eval(context["time"]) # security risks: https://www.codiga.io/blog/python-eval/

root_agent = SequentialAgent(
    name="game_builder",
    sub_agents=[developer, reviewer, team_lead],
    before_agent_callback=load_context
)

context = {
    "game" : """ 
        The game will genearate a random number between 1 and 100. The user will guess the number. If the user guesses
        the number, the game will end. If the user guesses a number that is too high, the game will tell the user that
        the number is too high. If the user guesses a number that is too low, the game will tell the user that the
        number is too low. The game will continue until the user guesses the number.
        """
}



# from agents.sessions.in_memory_session_service import InMemorySessionService
# from agents.artifacts.in_memory_artifact_service import InMemoryArtifactService
# from google.genai import types

# APP_NAME = "01-non-conversational-multiagent"
# USER_ID = "rafa"

# session_service = InMemorySessionService()
# artifact_service = InMemoryArtifactService()
# runner = Runner(APP_NAME, root_agent, artifact_service, session_service)
# session = session_service.create(APP_NAME, USER_ID, state=context)
# #session.state = context

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


# run_prompt("I want to play a game ! ")