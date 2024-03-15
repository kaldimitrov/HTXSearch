from typing import Tuple

from sentence_transformers import SentenceTransformer, util
from pathlib import Path
import re
import numpy as np
from tqdm import tqdm

from pdf import get_sections, PDF_SOURCE_DIR, Section


def split_sentences(text: str) -> [str]:
    sentence_border = re.compile(r"(\.\s+[A-Z])")

    split = sentence_border.split(text)

    for i in range(1, len(split) - 1):
        if sentence_border.fullmatch(split[i]):
            split[i - 1] = split[i - 1] + split[i][0]
            split[i + 1] = split[i][-1] + split[i + 1]

    split = [it for it in split if not sentence_border.fullmatch(it)]

    sentences = []

    for it in split:
        if len(sentences) > 0 and sentences[-1].endswith(("e.g.", "i.e.")):
            sentences[-1] += it
        else:
            sentences.append(it)

    return sentences


def vectorize_sections(sections: [Section], model: SentenceTransformer) -> np.ndarray:
    encodings = []

    for i, it in enumerate(tqdm(sections)):
        it_sentences = sum([split_sentences(jt.text) for jt in it.body], start=[])
        if not it_sentences:
            it_sentences = ["AAAAAAAAAAAAAAAA"]
        encodings.append(np.mean(model.encode(it_sentences), axis=0))

    return np.array(encodings)


if __name__ == "__main__":
    file = next(Path(PDF_SOURCE_DIR).iterdir())

    sections = np.array(get_sections(file))

    encodings = vectorize_sections(sections)

    while True:
        question = input(f"[{file.stem}] Question: ")
        question_enc = model.encode(question)

        similarity = util.cos_sim(encodings, question_enc).numpy().squeeze(axis=1)

        top = np.flip(np.argsort(similarity))[0]

        if similarity[top] < 0.4:
            print("Could not find a relevant match in the text.")
        else:
            print(similarity[top], sections[top])
