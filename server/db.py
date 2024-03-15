import chromadb
from chromadb.utils import embedding_functions

from pdf import get_sections, Section, PDF_SOURCE_DIR
from pathlib import Path

from tqdm import tqdm

DB_PATH = "./var/htx-search/chroma"
N_RESULTS = 3

client = chromadb.PersistentClient(path=DB_PATH)

smart_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="multi-qa-distilbert-cos-v1"
)

collection = client.get_or_create_collection(name="global", embedding_function=smart_ef)


def get_body(s: Section) -> str:
    res = ""
    for b in s.body:
        res += b.text
    return res


def fmt_answers(db_resp) -> None:
    # print(db_resp)
    for i in range(N_RESULTS):
        distance = db_resp["distances"][0][i]
        title = db_resp["metadatas"][0][i]["title"]
        body = db_resp["documents"][0][i]
        file = db_resp["metadatas"][0][i]["file"]
        print(f"[{distance}] {title}\n")
        print(f"{body}")
        print(f"Source: {file}\n")


if __name__ == "__main__":
    id_counter = 0
    for file in tqdm(Path(PDF_SOURCE_DIR).iterdir()):
        sections = get_sections(file)
        bodies = [get_body(s) for s in sections]
        meta = [{"title": s.title.text, "file": str(file)} for s in sections]

        ids = [str(idx + id_counter) for idx, _ in enumerate(bodies)]
        id_counter += len(sections)

        collection.add(documents=bodies, metadatas=meta, ids=ids)

    while True:
        question = input(f"\033[92mQuestion\033[0m: ")

        fmt_answers(collection.query(query_texts=question, n_results=N_RESULTS))
