import chromadb

from pdf import get_sections, Section, PDF_SOURCE_DIR
from pathlib import Path

DB_PATH = "./var/htx-search/chroma"
N_RESULTS = 3

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(name="global")


def get_body(s: Section) -> str:
    res = ""
    for b in s.body:
        res += b.text
    return res


def fmt_answers(db_resp) -> None:
    for i in range(N_RESULTS):
        distance = db_resp.distances[0][i]
        title = db_resp.titles[0][i]
        body = db_resp.documents[0][i]
        print(f"[{distance}] {title}\n")
        print(f"{body}")


if __name__ == "__main__":
    file = "./examples/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf"

    # file = next(Path(PDF_SOURCE_DIR).iterdir())

    id_counter = 0
    for file in Path(PDF_SOURCE_DIR).iterdir():
        sections = get_sections(file)
        bodies = [get_body(s) for s in sections]
        titles = [{"title": s.title.text} for s in sections]

        ids = [str(idx + id_counter) for idx, _ in enumerate(bodies)]
        id_counter += len(sections)

        collection.add(documents=bodies, metadatas=titles, ids=ids)

    while True:
        question = input(f"Question: ")

        print(collection.query(query_texts=question, n_results=N_RESULTS))
