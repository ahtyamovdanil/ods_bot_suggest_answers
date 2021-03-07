import flask
import pandas as pd
import os
from flask import request, jsonify
from app.semantic_engine import SemanticEngine
from typing import Union


def create_app(data_path: Union[str, os.PathLike], embeddings_path: Union[str, os.PathLike]):
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True
    df = pd.read_csv(data_path, sep="\t", dtype=str)
    engine = SemanticEngine(df)
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
    
    @app.route("/api/ready", methods=["GET"])
    def ready():
        return 'OK', 200
  
    return app
