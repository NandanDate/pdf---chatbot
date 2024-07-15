from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import PyPDF2
import re


# Step 1: Extract Text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted_text = page.extract_text()
            # Preprocessing to remove noise
            cleaned_text = preprocess_text(extracted_text)
            text += cleaned_text
    return text

def preprocess_text(text):
    # Define regular expressions to identify and remove noise patterns
    header_pattern = r'^[A-Z\s]+\n'  # Match uppercase text followed by newline
    footer_pattern = r'\n\d+\n*$'     # Match digits followed by newline, possibly followed by trailing newlines
    noise_patterns = [header_pattern, footer_pattern]

    # Apply noise removal
    for pattern in noise_patterns:
        text = re.sub(pattern, '', text, flags=re.MULTILINE)
    
    return text

# Step 2: Embed Text using BERT
def embed_text(text):
    # Load a pre-trained BERT model for sentence embeddings
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode([text])
    return embeddings

# Main Process
def main(pdf_path, pinecone_index_name, api_key):
    # Step 1: Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Embed text using BERT
    text_embedding = embed_text(pdf_text)
    
    # Step 3: Pinecone Integration
    pc = Pinecone(api_key=api_key)

# Target the existing Pinecone index
    index_name = pinecone_index_name
    pinecone_index = pc.Index(index_name)
    items_to_insert = [{'id': str(i), 'values': vector.tolist()} for i, vector in enumerate(text_embedding)]
    #pinecone_index = PineconeIndex(pinecone_index_name, api_key)
    #pinecone_index.upsert_embeddings(text_embedding, namespace="ns1")
    pinecone_index.upsert(vectors=items_to_insert, namespace="ns1")
    # For query similarity, you might need to embed the relationships separately if they are not part of the PDF text
    # Then, perform similarity search on the existing Pinecone index

if __name__ == "__main__":
    main("c://Users//Nandan//Downloads//exter.pdf", "pdf", "c97864e5-bd79-4736-88d9-2c852cc89159")
