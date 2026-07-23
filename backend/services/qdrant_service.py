import os
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))
qdrant = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

COLLECTION = "log_incidents"

def init_collection():
    if COLLECTION not in [c.name for c in qdrant.get_collections().collections]:
        qdrant.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )

def _embed(text: str):
    resp = co.embed(texts=[text], model="embed-english-v3.0", input_type="search_document")
    return resp.embeddings[0]

def upsert_incident(incident_id: str, text: str, metadata: dict):
    init_collection()
    vector = _embed(text)
    qdrant.upsert(
        collection_name=COLLECTION,
        points=[PointStruct(id=incident_id, vector=vector, payload=metadata)],
    )

def search_similar(text: str, top_k: int = 5):
    init_collection()
    query_vector = co.embed(texts=[text], model="embed-english-v3.0", input_type="search_query").embeddings[0]
    hits = qdrant.search(collection_name=COLLECTION, query_vector=query_vector, limit=top_k)
    return [{"score": h.score, **h.payload} for h in hits]