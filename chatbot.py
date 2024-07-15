import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

class PineconeIndex:
    def __init__(self, pinecone_index_name, api_key):
        self.pinecone_client = Pinecone(api_key=api_key)
        self.index = self.pinecone_client.Index(pinecone_index_name)

    def query_similar(self, query_embedding, top_k=5):
        # Perform similarity search in the Pinecone index
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_values=True,
            include_metadata=True  # Include metadata to fetch text content
        )
        return results

# Step 2: Embed Text using Sentence Transformer
def embed_text(text):
    # Load a pre-trained SentenceTransformer model for sentence embeddings
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(text)  # Note: No wrapping list around text
    return embeddings

# Main Process
def main(pinecone_index_name, api_key, user_question):
    # Step 3: Pinecone Integration
    pc_index = PineconeIndex(pinecone_index_name, api_key)

    # Retrieve embeddings of user's question
    user_embedding = embed_text(user_question).tolist()

    # Query similar questions in the Pinecone index
    similar_questions = pc_index.query_similar(user_embedding)

    # Summarize similar questions
    summarized_content = summarize_questions(similar_questions)

    # Print the summarized response
    print(summarized_content)

def summarize_questions(similar_questions):
    # Check if there are any matches
    if not similar_questions.get('matches'):
        return "No similar questions found."

    # Summarize the content of similar questions
    summarized_content = "Top similar questions:\n"
    for match in similar_questions['matches']:
        question_text = match['metadata'].get('text', 'No text found')
        summarized_content += f"ID: {match['id']}, Score: {match['score']:.4f}, Text: {question_text}\n"
    return summarized_content

if __name__ == "__main__":
    main("pdf", "c97864e5-bd79-4736-88d9-2c852cc89159", "modifications to your hyundai")
