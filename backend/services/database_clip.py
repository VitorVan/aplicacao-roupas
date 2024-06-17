from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv, find_dotenv



_ = load_dotenv(find_dotenv())  # read local .env file
api_key = os.getenv('PINECONE_KEY')
pc = Pinecone(api_key=api_key)

index_name = "clothes-clip-index"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=512, 
        metric="cosine", 
        spec=ServerlessSpec(
            cloud="aws", 
            region="us-east-1"
        ) 
    ) 

def add_clothes_to_clip_index(data):
    index = pc.Index(index_name)
    index.upsert(vectors=data)

def get_similar_clip_clothes(vector):
    index = pc.Index(index_name)
    results = index.query(vector=vector, top_k=6, include_metadata=True)

    print(results)
    return results.matches

print('teste')