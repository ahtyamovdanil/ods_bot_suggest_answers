import pandas as pd
import pickle
import warnings
from sentence_transformers import SentenceTransformer, util
from typing import List, Dict


class SemanticEngine:
    def __init__(self, text_df: pd.DataFrame) -> None:
        """
        Args:
            text_df (pd.DataFrame): pandas dataframe with fields: ts, text
        """
        self.model = SentenceTransformer("paraphrase-distilroberta-base-v1")
        self.text_df = text_df.to_numpy()
        self.embeddings = None

    def load_embeddings(self, path) -> None:
        """ load embeddings from pickle file """
        with open(path, "rb") as file:
            self.embeddings = pickle.load(file)

    def save_embeddings(self, path) -> None:
        """ save embeddings to pickle file """
        with open(path, "wb") as file:
            pickle.dump(self.embeddings, file)

    def calc_embeddings(self, corpus: List[str]):
        """ calculate new embeddings """
        if len(corpus) == 0:
            raise ValueError("corpus is empty")

        corpus_embeddings = self.model.encode(
            corpus, convert_to_tensor=True, show_progress_bar=False
        )
        self.embeddings = corpus_embeddings

    def get_top_k(self, query: str, k=5) -> List[Dict]:
        r"""Get k most similar to query sentences
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
        Example 1: calculate embeddings, save them and get top 5 sentences :: 
            >>> df = pd.read_csv("data/prepared/edu_courses.tsv", sep="\t")
            >>> engine = SemanticEngine(text_df=df)
            >>> engine.calc_embeddings(df.text.tolist())
            >>> engine.save_embeddings("data/embeddings/edu_courses.pkl")
            >>> query = "посоветуйте каких-нибудь курсов по pytorch"
            >>> result = engine.get_top_k(query, k=5)
            >>> for res in result:
            ...     print(res["ts"], res["text"], res["score"], sep="\n")

        Example 2: load embeddings from file, and get top 5 sentences
            >>> df = pd.read_csv("data/prepared/edu_courses.tsv", sep="\t")
            >>> engine = SemanticEngine(text_df=df)
            >>> engine.load_embeddings("data/embeddings/edu_courses.pkl")
            >>> query = "посоветуйте каких-нибудь курсов по pytorch"
            >>> result = engine.get_top_k(query, k=5)
            >>> for res in result:
            ...     print(res["ts"], res["text"], res["score"], sep="\n")
        """
        if self.embeddings is None:
            raise ValueError(
                "embeddings are not initialized. Call `load_embeddings` or `calc_embeddings` first"
            )
        if k > len(self.embeddings):
            warnings.warn(
                f"""`k` with value of {k} is bigger then number of 
                sentences with value of {len(self.embeddings)}.
                Value of k is set to {len(self.embeddings)}
                """)
            k = len(self.embeddings)

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
        ]
        return result
