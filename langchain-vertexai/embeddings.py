## Class `langchain_google_vertexai.VertexAIEmbeddings`

from langchain_google_vertexai import VertexAIEmbeddings

embedding = VertexAIEmbeddings(model_name="gemini-embedding-001")

# Online
vector = embedding.embed_query("hello, world!")
print(vector[:5])
# Output:
# [0.051872074604034424, -0.03087949939072132, -0.030809178948402405, -0.028053300455212593, 0.018047483637928963]

# Batch
vectors = embedding.embed_documents([
        "Today is Monday",
        "Today is Tuesday",
        "Today is April Fools day"]
)
print(len(vectors), len(vectors[0]))
# Output:
# 3 768