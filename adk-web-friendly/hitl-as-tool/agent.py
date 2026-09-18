# 06 - HITL as tool
# Sometimes we need a human to make an approval in an Agentic workflow.  

import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

GEMINI_2_FLASH = "gemini-2.0-flash"

from google.adk.agents import Agent


def reimburse(purpose: str, amount: float) -> str:
  """Reimburse the amount of money to the employee."""
  return '{"status": "ok"}'

def ask_for_approval(purpose: str, amount: float) -> str:
    """Ask for approval for the reimbursement."""
    prompt = f'An employee wants to reimburse {purpose}, it was ${amount}. Do you want to approve?'

    response = input(prompt)

    return response

root_agent = Agent(
    model=GEMINI_2_FLASH,
    name='reimbursement_agent',
    instruction="""
        You are an agent whose job is to handle the reimbursement process for
        the employees. If the amount is less than $100, you will automatically
        approve the reimbursement.

        If the amount is greater than $100, you will
        ask for approval from the manager. If the manager approves, you will
        reimburse the amount to the employee. If the manager rejects, you will
        inform the employee of the rejection.
        """,
    tools=[reimburse, ask_for_approval,]
    )

# from agents.sessions.in_memory_session_service import InMemorySessionService
# from agents.artifacts.in_memory_artifact_service import InMemoryArtifactService
# from google.genai import types

# APP_NAME = "06-hitl-as-tool"
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


# run_prompt("I want to buy this $80 pair of headphones")

# run_prompt("I also need this new computer chair for $500")