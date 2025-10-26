# 05 - Conversational Multi-Agent System (MAS)
# In this setup, we have multiple Agents connected to a root Agent.  
# Each Agent has its own set of tools that it can use.  
# The `root_agent` is primarily responsible for steering to the other Agents, and then handling any failure cases that the other agents cannot.
# This is the most common multi-agent style setup when users refer to "Multi Agent Architectures".

import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

GEMINI_2_FLASH = "gemini-2.5-flash"
SAMPLE_CONTEXT = './05-mas/context.json'

import json
from datetime import datetime
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext

mock_flight_info = [
    {
        "ticket_no": "7240005432906569",
        "book_ref": "C46E9F",
        "flight_id": 19250,
        "flight_no": "LX0112",
        "departure_airport": "CDG",
        "arrival_airport": "BSL",
        "scheduled_departure": "2024-12-30 12:09:03.561731-04:00",
        "scheduled_arrival": "2024-12-30 13:39:03.561731-04:00",
        "seat_no": "18E",
        "fare_conditions": "Economy"
    }
]
mock_company_policy = {
    "baggage": "Each passenger is allowed one carry-on bag and one personal item.",
    "check_in": "Check-in is available online 24 hours prior to departure and at the airport 3 hours prior to departure.",
    "refunds": "Refunds are available for tickets canceled 24 hours prior to departure."
}
mock_available_flights = [
    {
        "flight_id": 20001,
        "flight_no": "LX0113",
        "departure_airport": "CDG",
        "arrival_airport": "JFK",
        "scheduled_departure": "2024-12-31 10:00:00-04:00",
        "scheduled_arrival": "2024-12-31 16:00:00-04:00",
        "price": 500
    },
    {
      "flight_id": 20002,
        "flight_no": "LX0114",
        "departure_airport": "JFK",
        "arrival_airport": "CDG",
        "scheduled_departure": "2024-12-31 18:00:00-04:00",
        "scheduled_arrival": "2025-01-01 06:00:00-04:00",
        "price": 600
    }
]
mock_hotel_info = [
    {
      "hotel_id": 30001,
      "hotel_name": "Luxury Hotel",
      "city": "Paris",
      "price": 300,
      "rating": 4
    },
    {
      "hotel_id": 30002,
      "hotel_name": "Budget Hotel",
      "city": "Paris",
      "price": 100,
      "rating": 2
    }
]


def list_customer_flights(customer_email: str) -> str:
    """Lists flights for a given customer email."""
    # print_tool(common.get_kwargs())
    return str(mock_flight_info)


def lookup_company_policy(policy_name: str) -> str:
    """Looks up a company policy."""
    # print_tool(common.get_kwargs())
    return str(mock_company_policy.get(policy_name, "Policy not found"))


def fetch_user_flight_information(customer_email: str) -> str:
    """Fetch user flight information."""
    # print_tool(common.get_kwargs())
    return str(mock_flight_info)


def search_flights(
    departure_airport: str, arrival_airport: str, departure_date: str
) -> str:
    """Searches for available flights."""
    # print_tool(common.get_kwargs())
    return str(mock_available_flights)


def update_ticket_to_new_flight(ticket_no: str, new_flight_id: str) -> str:
    """Updates a ticket to a new flight."""
    # print_tool(common.get_kwargs())
    return '{"status": "ok", "message": "ticket updated successfully"}'


def search_hotels(city: str, check_in_date: str, check_out_date: str) -> str:
    """Searches for available hotels."""
    # print_tool(common.get_kwargs())
    return str(mock_hotel_info)


def book_hotel(hotel_id: str, check_in_date: str, check_out_date: str) -> str:
    """Books a hotel."""
    # print_tool(common.get_kwargs())
    return '{"status": "ok", "message": "hotel booked successfully"}'

GLOBAL_PROMPT = """
The current datetime is: {current_datetime}

The profile of the current customer is: {customer_profile}
"""

flight_agent = Agent(
    name="flight_agent",
    instruction="""
    Use the provided tools to search for flights, company policies, and other information to assist the user's queries.
    When searching, be persistent. Expand your query bounds if the first search returns no results.
    If a search comes up empty, expand your search before giving up.
    """,
    tools=[list_customer_flights, fetch_user_flight_information, search_flights, update_ticket_to_new_flight]
)

hotel_agent = Agent(
    name="hotel_agent",
    instruction="""
    Use the provided tools to search for hotels, book a hotel, and other information to assist the user's queries.
    When searching, be persistent. Expand your query bounds if the first search returns no results.
    If a search comes up empty, expand your search before giving up.
    Make sure that you have all related information before using your tools to search and book hotels.
    """,
    tools=[search_hotels, book_hotel]
)



def load_context(callback_context: CallbackContext):
    
    data = {}
    with open(SAMPLE_CONTEXT, "r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")

    context = data["state"]
    callback_context.state["customer_profile"] = context["customer_profile"]
    callback_context.state["current_datetime"] = eval(context["current_datetime"]) # security risks: https://www.codiga.io/blog/python-eval/

root_agent = Agent(
    model=GEMINI_2_FLASH,
    name='swiss_airlines_steering',
    global_instruction=GLOBAL_PROMPT,
    instruction="""
        You are a helpful customer support assistant for Swiss Airlines.
        """,
    sub_agents=[flight_agent, hotel_agent],
    before_agent_callback=load_context
)



# from agents.sessions.in_memory_session_service import InMemorySessionService
# from agents.artifacts.in_memory_artifact_service import InMemoryArtifactService
# from google.genai import types

# APP_NAME = "04-multiagent-delegation"
# USER_ID = "rafa"

# session_service = InMemorySessionService()
# artifact_service = InMemoryArtifactService()
# runner = Runner(APP_NAME, root_agent, artifact_service, session_service)
# session = session_service.create(APP_NAME, USER_ID)
# session.state = context


# # colors: https://stackoverflow.com/questions/58030468/how-to-have-colors-in-terminal-with-python-in-vscode
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


# run_prompt("Hi, what time is my flight? you should have my info on file.")

# run_prompt("what is my arrival city and date?")

# # jumping to another agent
# run_prompt("can you help me find a hotel there?")

# # asking a question that causes escalation to root
# run_prompt("What's the company policy on bringing dogs on flights?")