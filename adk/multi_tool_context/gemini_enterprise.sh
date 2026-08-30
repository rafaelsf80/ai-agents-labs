#!/bin/bash
# Must create a Gemini Enteprise app with a 30-day free trial
# Gemini Enterprise App and Agent Engine MUST be in same region
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -H "X-Goog-User-Project: 582095942167" \
"https://discoveryengine.googleapis.com/v1alpha/projects/582095942167/locations/global/collections/default_collection/engines/gemini-enterprise-17621096_1762109681291/assistants/default_assistant/agents" \
  -d '{
    "displayName": "airline_agent",
    "description": "Airline Agent",
    "icon": {
         "uri": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/corporate_fare/default/24px.svg"
     },
    "adkAgentDefinition": {
      "provisionedReasoningEngine": {
        "reasoningEngine": "projects/582095942167/locations/us-central1/reasoningEngines/5479460177486807040"
      }
    }
  }'