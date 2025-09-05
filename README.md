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
6. You are ready to create a [Hello World basic agent](adk/00-basic/) using ADK.


## ADK framework

The following samples provide ADK functionalities:

1. Tools
2. Sub-agents
3. Callbacks (HITL)
4. Artifacts
5. Short-term and long-term memory. IMPORTANT: for lab 12 to work you need a valid Agent Engine id.

Steps tu run an agent. Xxample for [00-basic](adk/00-basic/]):
```sh
adk run 00-basic
adk web 
 ```


## A2A protocol

1. Install A2A samples repo with:
```sh
git clone https://github.com/a2aproject/a2a-samples.git
```
2. Install uv with `pip install uv`. Important: must be within your venv.
3. Launch `helloworld` sample. Note this sample does NOT provide any [mesop UI](https://mesop-dev.github.io/mesop/), only sends Message events. If you try to open a browser, you will get `GET / HTTP/1.1 405 Method Not Allowed`
```sh
uv run .
# In another terminal
uv run test_client
```
4. Launch the demo UI. Make sure you use the right dependencies as highlighted in Known errors below.
5. 


## MCP protocol

This MCP sample deploys an MCP server with two available tools: `get_alerts` and `get_forecast`.

You can make a query like `"weather for SF, CA"`:

```sh
pip3 install mcp[cli] mcp --upgrade
python3 client.py  server.py
```

## Known errors

### 1. Permission errors when running CrewAI agent in A2A

```sh 
$ uv run .
error: Failed to spawn: `.`
  Caused by: Permission denied (os error 13)
```
Solution: `uv run main.py`

### 2. Error with packages when running CrewAI agent

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


### 4. Firebase Studio and Cloud Shell. 403 response when launching mesop
```sh
$ uv run main.py
INFO:     127.0.0.1:34816 - "POST /__ui__ HTTP/1.1" 403 Forbidden
```

Solution: No solution so far.