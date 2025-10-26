import json
import pprint
import vertexai
from vertexai import agent_engines

SAMPLE_CONTEXT = './context.json'
AGENT_ENGINE_ENDPOINT = "projects/989788194604/locations/europe-southwest1/reasoningEngines/2791967886179041280"

vertexai.init(project = "argolis-rafaelsanchez-ml-dev", location="europe-southwest1")

agent_engine = agent_engines.get( AGENT_ENGINE_ENDPOINT )

data = {}
with open(SAMPLE_CONTEXT, "r") as file:
   data = json.load(file)
   print(f"\nLoading Initial State: {data}\n")

initial_state = data["state"]
print(initial_state)
session = agent_engine.create_session(user_id="rafa07", state=initial_state )
print(session)

for event in agent_engine.stream_query(
   user_id="rafa07",  # Required
   session_id=session['id'],

   message="Hi what time is my flight ?"
):
   pprint.pprint(event)