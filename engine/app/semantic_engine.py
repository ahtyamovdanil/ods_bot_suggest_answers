import pandas as pd
import pickle
from sentence_transformers import SentenceTransformer, util
from typing import List, Dict


class SemanticEngine:
    def __init__(self, text_df: pd.DataFrame, model=None) -> None:
        """
        Args:
            text_df (pd.DataFrame): pandas dataframe with fields: ts, text
        """
        self.model = SentenceTransformer(model)
        self.text_df = text_df.to_numpy()
        self.embeddings = None

    def load_embeddings(self, path) -> None:
        with open(path, "rb") as file:
            self.embeddings = pickle.load(file)

    def save_embeddings(self, path) -> None:
        with open(path, "wb") as file:
            pickle.dump(self.embeddings, file)

    def calc_embeddings(self, corpus: List[str]):
        corpus_embeddings = self.model.encode(
            corpus, convert_to_tensor=True, show_progress_bar=False
        )
        self.embeddings = corpus_embeddings

    def get_top_k(self, query: str, k=5) -> List[Dict]:
        """Get k most similar to query sentences
        You need to call load_embeddings or calc_embeddings first to use this method
        Args:
            query (str): text for which you want to find similar sentences
            k (int, optional): number of sentences to find. Defaults to 5.

        Returns:
            List[Dict[float, str, float]]: List with dictionaries of the following structure:
            {
                ts: timestamp of message,
                score: cosin similarity score
                text: message text
            }
        """
        if self.embeddings is None:
            raise ValueError(
                "embeddings are not initialized. Call load_embeddings or calc_embeddings first"
            )
        query_embedding = self.model.encode(
            [query], convert_to_tensor=True, show_progress_bar=False
        )
        hits = util.semantic_search(query_embedding, self.embeddings, top_k=k)
        hits = hits[0]
        result = [
            {
                "ts": str(self.text_df[hit["corpus_id"]][0]),
                "score": str(hit["score"]),
                "text": self.text_df[hit["corpus_id"]][1],
            }
            for hit in hits
            if hit["score"] != 1
        ]
        return result


if __name__ == "__main__":
    """Usage example"""
    df = pd.read_csv("./data/prepared/edu_courses.tsv", sep="\t")
    df.dropna(inplace=True)
    engine = SemanticEngine(text_df=df)
    engine.calc_embeddings(df.text.tolist())
    engine.save_embeddings("./data/embeddings/edu_courses.pkl")
    engine.load_embeddings("./data/embeddings/edu_courses.pkl")
    query = "посоветуйте каких-нибудь курсов по pytorch"
    result = engine.get_top_k(query, k=5)

    for res in result:
        print(res["ts"], res["text"], res["score"], sep="\n")
        print("---------------")