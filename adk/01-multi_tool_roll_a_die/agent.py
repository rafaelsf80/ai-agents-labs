import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

GEMINI_2_FLASH = "gemini-2.5-flash"

import random
from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types

def roll_die(sides: int) -> int:
  """Roll a die and return the rolled result.

  Args:
    sides: The integer number of sides the die has.

  Returns:
    An integer of the result of rolling the die.
  """
  return random.randint(1, sides)


def check_prime(nums: list[int]) -> list[str]:
  """Check if a given list of numbers are prime.

  Args:
    nums: The list of numbers to check.

  Returns:
    A str indicating which number is prime.
  """
  primes = set()
  for number in nums:
    number = int(number)
    if number <= 1:
      continue
    is_prime = True
    for i in range(2, int(number**0.5) + 1):
      if number % i == 0:
        is_prime = False
        break
    if is_prime:
      primes.add(number)
  return (
      'No prime numbers found.'
      if not primes
      else f"{', '.join(str(num) for num in primes)} are prime numbers."
  )


root_agent = Agent(
    model=GEMINI_2_FLASH,
    name='roll_dice_agent',
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
      You can roll dice of different sizes.
      You can use multiple tools in parallel by calling functions in parallel(in one request and in one round).
      The only things you do are roll dice for the user and discuss the outcomes.
      It is ok to discuss previous dice roles, and comment on the dice rolls.
      When you are asked to roll a die, you must call the roll_die tool with the number of sides. Be sure to pass in an integer. Do not pass in a string.
      You should never roll a die on your own.
      When checking prime numbers, call the check_prime tool with a list of integers. Be sure to pass in a list of integers. You should never pass in a string.
      You should not check prime numbers before calling the tool.
      When you are asked to roll a die and check prime numbers, you should always make the following two function calls:
      1. You should first call the roll_die tool to get a roll. Wait for the function response before calling the check_prime tool.
      2. After you get the function response from roll_die tool, you should call the check_prime tool with the roll_die result.
        2.1 If user asks you to check primes based on previous rolls, make sure you include the previous rolls in the list.
      3. When you respond, you must include the roll_die result from step 1.
      You should always perform the previous 3 steps when asking for a roll and checking prime numbers.
      You should not rely on the previous history on prime results.
    """,
    planner = BuiltInPlanner(thinking_config=types.ThinkingConfig(thinking_budget= 0)),
    tools=[
        roll_die,
        check_prime,
    ]
)

# import asyncio
# from google.adk.sessions import InMemorySessionService
# from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
# from google.adk.runners import Runner
# from google.genai import types

# APP_NAME = "01-roll-a-die"
# USER_ID = "rafa"

# from dotenv import load_dotenv
# load_dotenv()

# # Session and Runner
# session_service = InMemorySessionService()
# artifact_service = InMemoryArtifactService()

# runner = Runner(agent=root_agent, app_name=APP_NAME, artifact_service=artifact_service, session_service=session_service)

# # Agent Interaction (Async)
# async def run_prompt(new_message: str):

#     session = await session_service.create_session(
#         app_name=APP_NAME, user_id=USER_ID
#     )
 
#     content = types.Content(role='user', parts=[types.Part.from_text(text=new_message)])

#     try:
#         async for event in runner.run_async(
#             user_id=session.user_id, session_id=session.id, new_message=content
#         ):
#             #print(f"Event ID: {event.id}, Author: {event.author}, Session: {session.id}")

#             if event.content:
#                 parts = event.content.model_dump(exclude_none=True).get("parts")
#                 for part in parts:
#                     if part.get("text", None):
#                         if event.content.role == "model":
#                             print(f"\033[32m[Agent {event.author}]\033[0m")  # green
#                             print(f"{part['text']}")
#                         elif event.content.role == "user":
#                             print("\033[31mUser\033[0m")
#                             print(f"{part['text']}")

#                     if part.get("function_call", None):
#                         print("\033[34m[Tool]\033[0m") # blue
#                         print(f"{part['function_call']}")

#                     if part.get("function_response", None):
#                         print("\033[33m[Tool result]\033[0m") # yellow
#                         print(f"{part['function_response']}")
#     except Exception as e:
#         print(f"ERROR during agent run: {e}")
#     print("-" * 30)

# from importlib.metadata import version
# print(f"google-adk {version('google-adk')}, google-cloud-aiplatform {version('google-cloud-aiplatform')}, google-genai {version('google-genai')}")

# asyncio.run(run_prompt("roll a 2 sided die"))

#run_prompt('roll a 9 sided die and check if its prime')
#run_prompt("What were the previous rolls?")

# google-adk 1.2.1, google-cloud-aiplatform 1.96.0, google-genai 1.19.0
# Event ID: kc6avkCe, Author: root_agent, Session: 4e0ba366-37f2-41c3-957d-0ae36daec6a1
# [Agent root_agent]
# I was created with the greatest framework.