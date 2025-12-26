from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
import os

QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY', None)
COLLECTION = os.getenv('QDRANT_COLLECTION', 'pr_embeddings')

class Storage:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        # create collection if doesn't exist
        try:
            self.client.get_collection(COLLECTION)
        except Exception:
            self.client.recreate_collection(
                collection_name=COLLECTION,
                vectors_config=rest.VectorParams(size=1536, distance=rest.Distance.COSINE)
            )

    def upsert(self, points, ids=None):
        # points: list of vectors
        if ids is None:
            ids = list(range(len(points)))
        self.client.upsert(collection_name=COLLECTION, points=[(i, points[i]) for i in range(len(points))])

    def search(self, vector, top=5):
        hits = self.client.search(collection_name=COLLECTION, query_vector=vector, limit=top)
        return hits
