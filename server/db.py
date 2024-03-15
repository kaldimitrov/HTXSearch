import chromadb
from chromadb.utils import embedding_functions

from pathlib import Path
from tqdm import tqdm

import os

from pdf import get_sections, Section, PDF_SOURCE_DIR
from vectorization import vectorize_sections

DB_PATH = "./chroma"
CHROMA_COLLECTION = "htx-search"
SENTENCE_MODEL = "multi-qa-MiniLM-L6-cos-v1"
DISTANCE_THRESHOLD = 1.0

N_RESULTS = 3


class ChromaDbInstance:
    collection: chromadb.Collection
    embed_fn: embedding_functions.SentenceTransformerEmbeddingFunction
    id_counter: int

    def __init__(self) -> None:
        client = chromadb.PersistentClient(path=DB_PATH)

        self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=SENTENCE_MODEL
        )

        try:
            self.collection = client.get_collection(
                name=CHROMA_COLLECTION, embedding_function=self.embed_fn
            )
            self.id_counter = self.collection.count()

        except:
            self.collection = client.create_collection(
                name=CHROMA_COLLECTION, embedding_function=self.embed_fn
            )
            self.id_counter = 0
            self.__populate__()

    def __populate__(self) -> None:
        for file in Path(PDF_SOURCE_DIR).iterdir():
            sections = get_sections(file)
            bodies = [get_body(s) for s in sections]
            meta = [{"title": s.title.text, "file": file.name} for s in sections]

            ids = [str(idx + self.id_counter) for idx, _ in enumerate(bodies)]
            self.id_counter += len(sections)

            embeddings = vectorize_sections(sections, file, self.embed_fn._model)

            self.collection.add(
                documents=bodies, embeddings=embeddings, metadatas=meta, ids=ids
            )

    def query(self, query: str) -> dict[str]:
        response = self.collection.query(query_texts=query, n_results=N_RESULTS)

        result = {"count": 0, "distances": [], "metadatas": [], "documents": []}
        for i in range(N_RESULTS):
            if response["distances"][0][i] > DISTANCE_THRESHOLD:
                continue

            result["distances"].append(response["distances"][0][i])
            result["metadatas"].append(
                {
                    "title": response["metadatas"][0][i]["title"],
                    "file": response["metadatas"][0][i]["file"],
                }
            )
            result["documents"].append(response["documents"][0][i])
            result["count"] += 1

        return result


def get_body(s: Section) -> str:
    res = ""
    for b in s.body:
        res += b.text + "\n"
    return res


def fmt_answers(db_resp) -> None:
    for i in range(db_resp["count"]):
        distance = db_resp["distances"][i]
        title = db_resp["metadatas"][i]["title"]
        body = db_resp["documents"][i]
        file = db_resp["metadatas"][i]["file"]
        print(f"[{distance}] {title}\n")
        print(f"{body}")
        print(f"Source: {file}\n")


if __name__ == "__main__":
    chroma = ChromaDbInstance()

    while True:
        question = input(f"\033[92mQuestion\033[0m: ")
        fmt_answers(chroma.query(question))
