import pandas as pd
import pickle
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
        with open(path, "rb") as file:
            self.embeddings = pickle.load(file)

    def save_embeddings(self, path) -> None:
        with open(path, "wb") as file:
            pickle.dump(self.embeddings, file)

    def calc_embeddings(self, corpus: List[str]):
        corpus_embeddings = self.model.encode(corpus, convert_to_tensor=True)
        self.embeddings = corpus_embeddings

    def get_top_k(self, query: str, k=5) -> List[Dict]:
        """[summary]

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
        query_embedding = self.model.encode([query], convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, self.embeddings, top_k=k)
        hits = hits[0]  # Get the hits for the first query
        result = [
            {
                "ts": self.text_df[hit["corpus_id"]][0],
                "score": hit["score"],
                "text": self.text_df[hit["corpus_id"]][1],
            }
            for hit in hits
        ]
        return result


if __name__ == "__main__":
    df = pd.read_csv("./data/prepared/edu_courses.tsv", sep="\t")
    df.dropna(inplace=True)
    engine = SemanticEngine(text_df=df)
    # engine.calc_embeddings(df.text.tolist())
    # engine.save_embeddings("./data/embeddings/emb.pkl")
    engine.load_embeddings("./data/embeddings/emb.pkl")
    query = "посоветуйте каких-нибудь курсов по pytorch"
    result = engine.get_top_k(query, k=5)

    for res in result:
        print(res["ts"], res["text"], res["score"], sep="\n")
        print("---------------")

    import sentence_transformers

    print(
        sentence_transformers.__version__, pd.__version__, pickle.__version__,
    )

