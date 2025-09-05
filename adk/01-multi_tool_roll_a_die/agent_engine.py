import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

GEMINI_2_FLASH = "gemini-2.0-flash"

import random
from google.adk.agents import Agent
import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp

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
    tools=[
        roll_die,
        check_prime,
    ]
)


# Test locally

app = AdkApp(agent=root_agent)
session = app.create_session(user_id="u_123")
for event in app.stream_query(
    user_id="u_123",
    session_id=session.id,
    message="whats the weather in new york",
):
  print(event)

# Deploy to Vertex AI Agent Engine
# https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview#supported-regions

vertexai.init(
    project="argolis-rafaelsanchez-ml-dev",
    location="us-central1",
    staging_bucket="gs://argolis-rafaelsanchez-ml-dev-agent-engine",
    )


remote_agent = agent_engines.create(
    agent_engine=app,
    display_name = "01-multi-tool-roll-a-die-agent",
    description = "Agente con juego de tirar un dado con dos tools",
    requirements=["google-cloud-aiplatform[agent_engines,adk]"]
)

# run_prompt("roll a 2 sided die")

# #run_prompt('roll a 9 sided die and check if its prime')

# #run_prompt("What were the previous rolls?")