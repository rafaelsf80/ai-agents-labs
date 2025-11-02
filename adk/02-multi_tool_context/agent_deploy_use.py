import json
import pprint
import vertexai
from vertexai import agent_engines

SAMPLE_CONTEXT = './context.json'
USER_ID="rafa07"
AGENT_ENGINE_ENDPOINT = "projects/989788194604/locations/europe-southwest1/reasoningEngines/2791967886179041280"

vertexai.init(project = "argolis-rafaelsanchez-ml-dev", location="europe-southwest1")

agent_engine = agent_engines.get( AGENT_ENGINE_ENDPOINT )

data = {}
with open(SAMPLE_CONTEXT, "r") as file:
   data = json.load(file)
   print(f"\nLoading Initial State: {data}\n")

initial_state = data["state"]
print(initial_state)
session = agent_engine.create_session(user_id=USER_ID, state=initial_state )
print(session)

# for event in agent_engine.stream_query(
#    user_id=USER_ID,  # Required
#    session_id=session['id'],

#    message="Hi what time is my flight ?"
# ):
#    pprint.pprint(event)

while True:
    user_input = input("Input: ")
    if user_input == "quit":
      break

    for event in agent_engine.stream_query(
            user_id=USER_ID, session_id=session["id"], message=user_input
        ):
            if "content" in event:
                if "parts" in event["content"]:
                    parts = event["content"]["parts"]
                    for part in parts:
                        if "text" in part:
                            text_part = part["text"]
                            print(f"Response: {text_part}")