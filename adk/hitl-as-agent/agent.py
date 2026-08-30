# 06 - HITL as agent
# The main differences between this and "HITL as tool" are:
# * No Tool calling
# * Using Callbacks to allow human interjection
# This means we have swapped Tool Call <> Callbacks.  
# In practical terms, this could mean less infrastructure overhead (no tools) and using the native callbacks + model to do the tasks.   
# Also, because we're using Callbacks, we can do additional modification of the human user response.
# In practical terms, the outputs of both 5 and 6 are identical.
 
import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

GEMINI_2_FLASH = "gemini-2.5-flash"

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext 
from google.adk.sessions import Session

manager_human_agent = Agent(
    model=GEMINI_2_FLASH,
    name="manager_human_agent",
    instruction="""You are a manager in a travel company.
    You are only been called when the user demand to talk to the manager.""",
    )

root_agent = Agent(
    model=GEMINI_2_FLASH,
    name="info_agent",
    instruction="""You are an agent in a travel company that answers users' questions.
      You want to answer the user's questions as best as you can.
      Only if they demand to talk to the manager, you will call the manager_human_agent.""",
    sub_agents=[manager_human_agent])

def before_agent_call(callback_context: CallbackContext):
    user_message = Session.get_last_user_message(callback_context)

    prompt = str.encode(user_message + '\n')
    response = input(prompt)

    return Session.build_content(response)

manager_human_agent.before_agent_callback = before_agent_call


# from agents.sessions.in_memory_session_service import InMemorySessionService
# from agents.artifacts.in_memory_artifact_service import InMemoryArtifactService
# from google.genai import types

# APP_NAME = "06-hitl-as-agent"
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


# run_prompt("How far is Hawaii from San Jose?")
