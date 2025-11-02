import vertexai
from vertexai import agent_engines


AGENT_ENGINE_ENDPOINT = "projects/989788194604/locations/europe-southwest1/reasoningEngines/4804373232171876352"

vertexai.init(project = "argolis-rafaelsanchez-ml-dev", location="europe-southwest1")

agent_engine = agent_engines.get( AGENT_ENGINE_ENDPOINT )

import pprint
#pprint.pprint(agent_engine.operation_schemas())
#print("-" * 30)
#pprint.pprint(agent_engine.list_sessions(user_id="rafa07"))
#print("-" * 30)

# Query 
session = agent_engine.create_session(user_id="rafa07")

for event in agent_engine.stream_query(
   user_id="rafa07",  # Required
   message="roll a 9-sided die and check if it's prime",
):
   pprint.pprint(event)