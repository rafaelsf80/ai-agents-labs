# 10 - Image generation and artifacts
# Requires pip3 install pillow matplotlib
# TODO: check where image is stored

import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

IMAGE_MODEL = 'imagen-4.0-generate-001'

import io
from google.genai import Client
import google.genai.types as types
from google.adk.agents import Agent
from google.adk.tools import load_artifacts, ToolContext

from PIL import Image
import matplotlib.pyplot as plt

import os
from dotenv import load_dotenv
load_dotenv()

MODEL_GOOGLE = "gemini-2.5-flash"

# Only Vertex AI supports image generation for now.
client = Client()

def generate_image(prompt: str, tool_context: 'ToolContext'):
  """Generates an image based on the prompt."""
  response = client.models.generate_images(
      model=IMAGE_MODEL,
      prompt=prompt,
      config=types.GenerateImagesConfig(
        number_of_images= 4,
        personGeneration="allow_adult" # default
    )
  )
  if not response.generated_images:
    return {'status': 'failed'}
  image_bytes = response.generated_images[0].image.image_bytes
  
  # Save the image in the context, not in disk
  tool_context.save_artifact(
       './image.png',
       types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
   )

  # Save image in disk
  image = Image.open(io.BytesIO(image_bytes))
  plt.imshow(image)
  plt.show()

  tool_context.actions.skip_summarization = True # don't return image back to model for explanation

  return {'status': 'ok', 'filename': 'image.png'}

root_agent = Agent(
    model=MODEL_GOOGLE,
    name='root_agent',
    description="""An agent that generates images and answer questions about the images.""",
    instruction="""You are an agent whose job is to generate or edit an image based on the user's prompt.
    """,
    tools=[generate_image, load_artifacts],
)


# from agents.sessions.in_memory_session_service import InMemorySessionService
# from agents.artifacts.in_memory_artifact_service import InMemoryArtifactService
# from google.genai import types

# APP_NAME = "10-image-generation"
# USER_ID = "rafa"

# session_service = InMemorySessionService()
# artifact_service = InMemoryArtifactService()
# runner = Runner(APP_NAME, root_agent, artifact_service, session_service)
# session = session_service.create(APP_NAME, USER_ID)

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



# run_prompt("a dog riding a bike")

# # You need to close the image before continuing
# run_prompt("what kind of dog is that?")