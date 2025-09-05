# 02 - Conversational Agent - Single Agent, Multi-Tool Use
# Single agent structure with Multiple Tools with context.   

import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

GEMINI_2_FLASH = "gemini-2.0-flash"
SAMPLE_CONTEXT = './02-multi_tool_context/context.json'

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



def load_context(callback_context: CallbackContext):
    
    data = {}
    with open(SAMPLE_CONTEXT, "r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")

    context = data["state"]
    callback_context.state["user_info"] = context["user_info"]
    callback_context.state["time"] = eval(context["time"]) # security risks: https://www.codiga.io/blog/python-eval/

root_agent = Agent(
        model=GEMINI_2_FLASH,
        name='airline_agent',
        instruction="""
            You are a helpful customer support assistant for Swiss Airlines.
            Use the provided tools to search for flights, company policies, and other information to assist the user's queries.
            When searching, be persistent. Expand your query bounds if the first search returns no results.
            If a search comes up empty, expand your search before giving up.

            Current user:
            <User>
            {user_info}
            </User>
            Current time: {time}.
            """,
        tools=[
            list_customer_flights,
            lookup_company_policy,
            fetch_user_flight_information,
            search_flights,
            update_ticket_to_new_flight,
            search_hotels,
            book_hotel
            ],
        before_agent_callback=load_context
        )



# from agents.sessions.in_memory_session_service import InMemorySessionService
# from agents.artifacts.in_memory_artifact_service import InMemoryArtifactService
# from google.genai import types

# APP_NAME = "02-conversational-single-multitool"
# USER_ID = "rafa"

# session_service = InMemorySessionService()
# artifact_service = InMemoryArtifactService()
# runner = Runner(APP_NAME, flight_agent, artifact_service, session_service)
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


# run_prompt("Hi what time is my flight?")