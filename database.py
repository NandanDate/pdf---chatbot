import os
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import pinecone

load_dotenv()

from langchain_pinecone import Pinecone

def setup_pinecone(api_key, index_name):
    pc = Pinecone()
    pc.init(api_key=api_key, environment="us-east-1-aws")
    return pc.index(index_name)


def retrieve_query(query, index, model):
    query_embedding = model.encode(query, convert_to_tensor=True)
    matching_results = index.query(queries=[query_embedding], top_k=2)
    return matching_results

def retrieve_answers(query, index, chain, model):
    doc_search = retrieve_query(query, index, model)
    response = chain.run(input_documents=doc_search, question=query)
    return response

api_key = 'c97864e5-bd79-4736-88d9-2c852cc89159'
index_name = 'pdf'

if api_key is None:
    print("Pinecone API key not found. Exiting...")
    exit()

index = setup_pinecone(api_key, index_name)
print(f"Using Pinecone index: {index_name}")

model = SentenceTransformer('all-MiniLM-L6-v2')
llm = OpenAI(model_name='text-davinci-003', temperature=0.5)
chain = load_qa_chain(llm, chain_type='stuff')

our_query = 'what fuel can cause?'
answer = retrieve_answers(our_query, index, chain, model)
print(answer)
