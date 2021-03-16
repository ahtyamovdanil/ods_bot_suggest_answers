import engine_api as api
import sys
from os import path

datapath = path.join(sys.path[0], "data")
my_app = api.create_app(
    data_path=path.join(datapath, "prepared/edu_courses.tsv"),
    embeddings_path=path.join(datapath, "embeddings/edu_courses.pkl")
)

my_app.run(host="0.0.0.0")
