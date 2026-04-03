from sentence_transformers import SentenceTransformer

class EmbeddingClient:
    def __init__(self):
        self.transformer = SentenceTransformer('all-MiniLM-L6-v2')

    def embed(self, sentence: str) -> list[float]:
        return self.transformer.encode(sentence).tolist()