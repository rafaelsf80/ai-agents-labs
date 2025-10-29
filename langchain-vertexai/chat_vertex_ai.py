## Class `langchain_google_vertexai.ChatVertexAI`

from langchain_google_vertexai import ChatVertexAI

llm = ChatVertexAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    max_retries=6,
    stop=None,
    # other params...
)

# Invocation
messages = [
    (
        "system",
        "You are a helpful assistant that translates English to Spanish. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
ai_msg
print(ai_msg.content)