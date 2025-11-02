# AI Agents labs

## Firebase Studio

We will use [Firebase Studio](https://firebase.blog/posts/2025/04/introducing-firebase-studio/), but these labs can run in any other environment, like local VS Code, [Cloud Workstations](https://cloud.google.com/workstations) or similar.

Firebase Studio provides [100 GiB total disk space for Nix packages and /tmp and 10 GiB for your /home directory](https://firebase.google.com/docs/studio/troubleshooting). It also provides templates to work with certain environments, like [this one for A2A](https://github.com/a2aproject/a2a-samples/pull/312).

You can check the status dashboard of Firebase products [here](https://status.firebase.google.com/).

Note Firebase Studio does not support upload from local, so the easiest way to work with files is through repositories. However, although you can not upload, you can download files by unzipping them using the contextual menu over a file or directory.

Steps to create the workspace for the labs in this repo:
1. Go to Firebase Studio at https://firebase.studio
2. Create a Flask app, and accept all installation suggestions. We are not going to use Flask, we are only interested in the basic package install.
3. Remove all the Flask app, including `*.dev` and `main.py`, since we will not need them.
4. Open a terminal and create virtual environment:
```sh
python -m venv myenv
source myenv/bin/activate
```
5. Replace `requirements.txt` with `google-adk` and `python-dotenv`, and install them with:
```sh
 pip3 install -r requirements.txt 
 ```
> Please, wait patiently, do NOT CTRL+C before the installation is finished.
6. You are ready to create a [Hello World basic agent](./adk/00-basic/) or any of the agents in the next section using ADK.


## ADK framework

> IMPORTANT: Before executing any of the agents, you must fill your credentials (`GOOGLE_API_KEY`) in an `.env` file.

The following samples provide ADK functionalities:

1. Tools
2. Sub-agents
3. Callbacks (HITL)
4. Artifacts
5. Short-term and long-term memory. 

> IMPORTANT: Lab 12 (long-term memory) will not work unless you provide  a valid Agent Engine id.

ADK includes tools like a command-line interface (CLI) and a Developer UI for running agents. Use `adk web` to run the UI or `adk run` for individual agents. Example for [00-basic](adk/00-basic):
```sh
echo "How were you built ?" | adk run 00-basic
```


## Finantial advisor agent

This agent is available in the [`adk-samples`](https://github.com/google/adk-samples) Google Cloud public repository. Follow the [README.md](https://github.com/google/adk-samples/blob/main/python/agents/financial-advisor/README.md) to make queries to the agent.

Make sure your .env file looks like this: 
```sh
USE_VERTEX_AI=False
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
```
While this agent can run locally with a `GOOGLE_API_KEY`, please note you can not deploy this to Agent Engine using the Gemini API key (you must use Vertex AI). 


## Data Science agent

This agent is available in the [`adk-samples`](https://github.com/google/adk-samples) Google Cloud public repository. Follow the [README.md](https://github.com/google/adk-samples/blob/main/python/agents/data-science/README.md) to make queries to the agent.

Make sure your .env file is inside `data_science` directory (not `data-science`) 


Dependencies:
```sh
pip3 install pandas immutabledict regex sqlglot db-dtypes absl-py
```

> **Note**: `pipx` vs `pip`: `pipx` is the new manager to install python apps in isolated environments. Ideal for tools like black, pipenv or poetry (`pipx install poetry`) that you want to use it globally without worrying on dependencies. So, while `pipx` is for tools you se from CLI, `pip` is to install packages(numpy, requests, django...)


## A2A protocol

1. Install A2A samples repo:
```sh
git clone https://github.com/a2aproject/a2a-samples.git
```
2. Install `uv` with `pip3 install uv`. Important: must be within your venv.
3. Launch `helloworld` sample. Note this sample does NOT provide any [mesop UI](https://mesop-dev.github.io/mesop/), only sends Message events. 
```sh
uv run .
# In another terminal launch the client
uv run test_client
```

4. A2A protocol includes a useful command-line interface to send Tasks and Messages. Launch a server (for example: adk_expense_reimbursement client) and a client. Make sure you add a `.env` file in both directories with the correct keys:
```sh
cd a2a-samples/samples/python/agents/adk_expense_reimbursement
uv run .
# In another terminal launch the client
cd a2a-samples/samples/python/hosts/cli
uv run . --agent http://localhost:10002
```

5. Finally, you can run a three-agent demo under `demo/ui` using a `mesop` interface. Make sure you use the modified `crewai` agent provided, and that you add a `.env` file in both directories with the correct keys.
```sh
# Launch server 1
cd a2a-samples/samples/python/agents/adk_expense_reimbursement
uv run .
# In another terminal launch the second server
cd ../crewai
uv run .
# In another terminal launch the third server
cd ../langgraph
uv run .
# In another terminal launch the client
cd a2a-samples/demo/ui
uv run main.py
```


## MCP protocol

This MCP sample deploys an MCP server with two available tools: `get_alerts` and `get_forecast`.

You can make a query like `"weather for SF, CA"`:

```sh
pip3 install mcp[cli] mcp --upgrade
python3 client.py  server.py
```


## Gemini CLI

Install in Firebase Studio with `npx https://github.com/google-gemini/gemini-cli`.

Note `.gemini/settings.jon` file that contains key configuration.

Shell commands:
```sh
gemini -p "your prompt here" # Direct prompt execution
gemini -i "your prompt" # Open gemini in interactive mode with that prompt
gemini -y  # Auto-confirm all prompts (YOLO mode)
gemini -m model # Use a spedific model
```

Gemini CLI commands:
```sh
/tools # Lists available tools and their descriptions.
/memory show # Displays the full, combined context currently being used by the AI.
/memory add # Add content to the memory
/extensions
@path    # Injects the content of the specified file or directory into the prompt.
!command # Executes the specified command directly in your system's shell.
```

Code examples:

* **1. Node.js app generation**: in a new directory, query in Spanish: _"Escribe una aplicacion en node.js que sea un servidor web y devuelva "hola, bbva". Debe usar el puerto 8080, y que tenga un dockerfile"_. You can then launch the app with `$ node index.js`.

* **2. Code analysis**: in a new directory, clone this same repo and run this query (Spanish): _"Analiza este repositorio y busca fallos de código"_.

Built-in tools examples (`/tools`):

* **3. Web fetch**: query in Spanish: _"Busca los 10 titulares de noticias noticias más importantes de las ultimas semanas sobre BBVA y guardalas en un archivo bbva.txt"_

* **4. Web fetch**: query in Spanish: _"Descarga las release notes solo de la ultima versión de Google Agent Development Kit de su feed rss y muestra las principales features en una lista bien formateada."_

Shell examples:

* **5. Equivalent of `$ find . --name hello --print`**: query in Spanish: _"Busca la palabra `hello` en el directorio actual"_. Also you can use `@`: _"@a2a/samples busca `hello` en este directorio"_.

Github MCP server examples (make sure you add your Github PAT on `.gemini/settings.json`):

* Who am I on github ? 
* Describe the `google/adk-samples` repository to me ?
* Clone that repo on my local machine.
* Describe `@adk-samples/python/agents/financial-advisor/` (can also be a directory `@<directory-name>/`)
* What are the different components of this repository?
* I have made necessary changes. Can you push the changes to Github and use the Github MCP Server tools to do that ?

You can also run [this codelab](https://codelabs.developers.google.com/gemini-cli-hands-on).


## Agent Engine

Samples from the official Google Cloud repo:

* [Debugging and Optimizing Agents: A Guide to Tracing in Agent Engine](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/agent-engine/tracing_agents_in_agent_engine.ipynb)
* [Building a Conversational Search Agent with Agent Engine and RAG on Vertex AI Search](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/agent-engine/tutorial_vertex_ai_search_rag_agent.ipynb)

Use an agent in another session:
```py
from vertexai import agent_engines
remote_agent = agent_engines.get("projects/989788194604/locations/us-central1/reasoningEngines/175860287793004544")
```

List agents per region:
```py
from vertexai import agent_engines
vertexai.init(location="us-centrla1")
print(list(agent_engines.list())) # only returns from one region
```


## `langchain-google-vertexai` package examples

Some examples of the [`langchain-google-vertexai` package](https://pypi.org/project/langchain-google-vertexai/), including the following classes:

* `langchain_google_vertexai.ChatVertexAI`
* `langchain_google_vertexai.VertexAIEmbeddings`
* `langchain_google_vertexai.VertexAIModelGarden`
* `langchain_google_vertexai.VertexAI`

```sh
pip install langchain-google-vertexai
```


## FAQ

### 1. Permission errors when running CrewAI agent in A2A

```sh 
$ uv run .
error: Failed to spawn: `.`
  Caused by: Permission denied (os error 13)
```
Solution: `uv run main.py`

### 2. Error with packages when running CrewAI agent in A2A

```sh
$ uv run .
ERROR:__main__:An error occurred during server startup: Packages `starlette` and `sse-starlette` are required to use the `JSONRPCApplication`. They can be added as a part of `a2a-sdk` optional dependencies, `a2a-sdk[http-server]`.
```

 Solution: `uv add a2a-sdk[http-server]` (do not use pip install)

### 3. A2A Demo UI stuck with no response (demo/ui)

* Reported [here](https://github.com/a2aproject/a2a-samples/issues/36) and [here](https://github.com/a2aproject/A2A/issues/96). Caused an UI error `argument of type 'NoneType' is not iterable` which ssometimes is not even shown in the logs.

Solution: use this `pyproject.toml` file.

```sh
[project]
name = "a2a-python-example-ui"
version = "0.1.0"
description = "Agent2Agent example UI"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "asyncio>=3.4.3",
    "httpx>=0.28.1",
    "httpx-sse>=0.4.0",
    "pydantic>=2.11.0",
    "fastapi>=0.115.0",
    "uvicorn>=0.34.0",
    "mesop>=1.0.0",
    "a2a-sdk==0.3.0",
    "pandas>=2.2.0",
    "google-genai==1.27.0",
    "google-adk[a2a]==1.10.0",
    "litellm",
    "a2a-sample-client-multiagent",
]

[tool.hatch.build.targets.wheel]
packages = ["a2a_ui"]

[tool.hatch.metadata]
allow-direct-references = true

[tool.uv.sources]
a2a_ui = { workspace = true }
a2a-sample-client-multiagent = { workspace = true }

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[dependency-groups]
dev = ["ruff>=0.11.2"]
```


### 4. Firebase Studio and Cloud Shell. 403 response when launching mesop (demo/ui)
```sh
$ uv run main.py
INFO:     127.0.0.1:34816 - "POST /__ui__ HTTP/1.1" 403 Forbidden
```

Solution: No solution so far for Firebase Studio. Use your local environment.


### 5. Agent Engine SDK error: 

* Agent Engine SDK error: failed to generate schema for stream_query: `stream_query` is not fully defined; you should define `ContentDict`, then call `stream_query.model_rebuild()`
Solution: https://b.corp.google.com/issues/416716891


### 6. ModuleNotFoundError: No module named 'data_science'

* Traceback (most recent call last):
  File "/Users/rafaelsanchez/git/genai-agents/data-science-agent/deployment/deploy.py", line 22, in <module>
    from data_science.agent import root_agent
ModuleNotFoundError: No module named 'data_science'
Solution
import sys
sys.path.append("./data_science-0.1.0-py3-none-any.whl")


### 7.

* https://b.corp.google.com/issues/412215081#comment16

pip3 install --upgrade --force-reinstall google-adk 'google-cloud-aiplatform[agent_engines]==1.90.0