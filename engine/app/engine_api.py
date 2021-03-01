import flask
from flask import request, jsonify
from semantic_engine import SemanticEngine
import pandas as pd


def create_app():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True
    df = pd.read_csv("data/prepared/edu_courses.tsv", sep="\t", dtype=str)
    engine = SemanticEngine(text_df=df)
    engine.load_embeddings("data/embeddings/edu_courses.pkl")
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
    app = create_app()
    app.run(host="0.0.0.0")
