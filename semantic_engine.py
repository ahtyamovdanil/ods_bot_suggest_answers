import torch
import pandas as pd

from sentence_transformers import SentenceTransformer, util


class SemanticEngine:

    def __init__(self, embeddings_path, corpus_path):
        self.model = SentenceTransformer('paraphrase-distilroberta-base-v1')
        # FIXME: не держать в памяти весь корпус с его эмбеддингами, может
        # быть вынести в базу данных.
        self.embeddings = torch.load(embeddings_path)
        self.corpus_df = pd.read_pickle(corpus_path)

    def get_top_k(self, query, top_k):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(
            query_embeddings=query_embedding,
            corpus_embeddings=self.embeddings,
            top_k=top_k
        )

        if not hits:
            return []

        result = []
        for hit in hits[0]:
            item = self.corpus_df.iloc[hit['corpus_id']]
            result.append({
                'ts': item['ts'],
                'text': item['text'],
                'score': hit['score'],
            })

        return result
