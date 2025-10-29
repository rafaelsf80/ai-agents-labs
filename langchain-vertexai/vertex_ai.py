## Class `langchain_google_vertexai.VertexAI`

from langchain_google_vertexai import VertexAI

model = VertexAI(model_name="gemini-2.5-flash")

message = "What are some of the pros and cons of Python as a programming language?"

response = model.invoke(message)
print(response)