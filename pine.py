from pinecone import Pinecone

# Initialize Pinecone client with your API key
pc = Pinecone(api_key="c97864e5-bd79-4736-88d9-2c852cc89159")

# Target the existing Pinecone index
index_name = "pdf"
index = pc.Index(index_name)

# Define vectors to be inserted
vectors_to_insert = [
    {"id": "vec1", "values": [0.1, 0.2, 0.3]},
    {"id": "vec2", "values": [0.4, 0.5, 0.6]},
    {"id": "vec3", "values": [0.7, 0.8, 0.9]}
]

# Upsert vectors into the index
index.upsert(vectors=vectors_to_insert, namespace="ns1")

# Define query vector
