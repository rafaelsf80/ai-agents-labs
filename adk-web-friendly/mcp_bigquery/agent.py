import os
import logging

from google.oauth2 import credentials, id_token
from google.auth.transport import requests as google_auth_requests

import google.auth

from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

from googleapiclient.discovery import build


def get_bigquery_mcp_toolset():   
        
    credentials, project_id = google.auth.default(
            scopes=["https://www.googleapis.com/auth/bigquery"]
    )

    credentials.refresh(google.auth.transport.requests.Request())
    oauth_token = credentials.token

    BIGQUERY_MCP_URL = "https://bigquery.googleapis.com/mcp"     
    HEADERS_WITH_OAUTH = {
        "Authorization": f"Bearer {oauth_token}",
        "x-goog-user-project": project_id
    }

    tools = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=BIGQUERY_MCP_URL,
            headers=HEADERS_WITH_OAUTH
        )
    )
    print("MCP Toolset configured for Streamable HTTP connection.")
    return tools

bigquery_toolset = get_bigquery_mcp_toolset()

root_agent = Agent(
    name="root_agent",
    model="gemini-3.5-flash",
    instruction="You are a helpful data analyst. You will use your tools to answer questions about BigQuery.",
    tools=[bigquery_toolset],
)