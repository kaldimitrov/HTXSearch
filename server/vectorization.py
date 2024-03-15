from typing import Tuple

from sentence_transformers import SentenceTransformer, util
from pathlib import Path
import re
import numpy as np

from pdf import get_sections, PDF_SOURCE_DIR, Section

model = SentenceTransformer("all-MiniLM-L6-v2")
#model = SentenceTransformer("all-mpnet-base-v2")

def split_sentences(text: str) -> [str]:
    sentence_border = re.compile('(\.\s+[A-Z])')

    split = sentence_border.split(text)

    for i in range(1, len(split)-1):
        if sentence_border.fullmatch(split[i]):
            split[i-1] = split[i-1] + split[i][0]
            split[i+1] = split[i][-1] + split[i+1]

    split = [it for it in split if not sentence_border.fullmatch(it)]

    sentences = []

    for it in split:
        if len(sentences) > 0 and sentences[-1].endswith(('e.g.', 'i.e.')):
            sentences[-1] += it
        else:
            sentences.append(it)

    return sentences


def vectorize_sections(sections: [Section]) -> Tuple[np.ndarray, np.ndarray]:
    # sections = sections[:40]

    sentences = []
    section_idxs = []

    for i, it in enumerate(sections):
        it_sentences = sum([split_sentences(jt.text) for jt in it.body], start=[])

        sentences.extend(it_sentences)
        section_idxs.extend([i] * len(it_sentences))

    encodings = model.encode(sentences)

    return encodings, np.array(section_idxs)


if __name__ == '__main__':
    file = next(Path(PDF_SOURCE_DIR).iterdir())

    sections = np.array(get_sections(file))

    encodings, section_idx = vectorize_sections(sections)

    while True:
        question = input("Question: ")
        question_enc = model.encode(question)

        similarity = util.cos_sim(encodings, question_enc).numpy().squeeze(axis=1)

        top = np.flip(np.argsort(similarity))[0]

        print(similarity[top], sections[section_idx[top]])

    print(encodings.shape, len(section_idx))

#util.cos_sim
