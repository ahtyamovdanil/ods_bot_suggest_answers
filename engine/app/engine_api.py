import flask
from flask import request, jsonify
from engine.app.semantic_engine import SemanticEngine
import pandas as pd
from typing import Union
import os


def create_app(data_path: Union[str, os.PathLike], embeddings_path: Union[str, os.PathLike]):
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True
    df = pd.read_csv(data_path, sep="\t", dtype=str)
    engine = SemanticEngine(text_df=df)
    engine.load_embeddings(embeddings_path)
    app.config["ENGINE"] = engine

    @app.route("/api/get_messages", methods=["GET", "POST"])
    def get_messages():
        """ get top `k` most similar messages and return json:
           List of { "ts": str,
                     "score": float,
                     "text": str }
        """
        content = request.json
        query = content["text"]
        top_k = content["top_k"]
        result = app.config["ENGINE"].get_top_k(query, k=top_k)
        return jsonify(result)

    return app


if __name__ == "__main__":

    app = create_app(
        data_path="data/prepared/edu_courses.tsv",
        embeddings_path="data/embeddings/edu_courses.pkl"
    )
    app.run(host="0.0.0.0")
