import logging
import os

from sentence_transformers import SentenceTransformer

os.environ["TOKENIZERS_PARALLELISM"] = "false"
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub.utils._auth").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

class EmbeddingClient:
    def __init__(self):
        self.transformer = SentenceTransformer('all-MiniLM-L6-v2')

    def embed(self, sentence: str) -> list[float]:
        return self.transformer.encode(sentence).tolist()