import json
import glob


def get_channel_messages(channel: str):
    """
    read all json files from  ./data/raw/{channel}/
    and write recevied messages to ./data/prepared/{channel}.tcv
    """

    files = list(glob.iglob(f"./data/raw/{channel}/*.json"))

    with open(f"./data/prepared/{channel}.tsv", "w") as file:
        file.write("ts\ttext\n")

    for name in files:

        with open(name) as msgs_file:
            messages = json.load(msgs_file)

        with open(f"./data/prepared/{channel}.tsv", "a") as file:
            for msg in messages:
                if (
                    ("user" not in msg)
                    or ("thread_ts" not in msg)
                    or (msg["user"] == "USLACKBOT")
                    or ("reply_users_count" not in msg)
                ):
                    continue

                msg["text"] = msg["text"].replace("\t", " ").replace("\n", " ")
                file.writelines([msg["ts"], "\t", '"' + msg["text"] + '"' + "\n"])


if __name__ == "__main__":
    get_channel_messages("edu_courses")