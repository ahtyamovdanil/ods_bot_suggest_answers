import flask
from flask import request, jsonify
from semantic_engine import SemanticEngine
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True

df = pd.read_csv("./data/prepared/edu_courses.tsv", sep="\t", dtype=str)
df.dropna(inplace=True)
engine = SemanticEngine(text_df=df, model = "distiluse-base-multilingual-cased-v2")
engine.load_embeddings("./data/embeddings/edu_courses.pkl")

@app.route("/api/get_messages", methods=["GET", "POST"])
def get_messages():
    content = request.json
    query = content["text"]
    top_k = content["top_k"]
    result = engine.get_top_k(query, k=top_k)
    return jsonify(result)

@app.route("/api/ready", methods=["GET"])
def ready():
    return 'OK', 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
