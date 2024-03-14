from sentence_transformers import SentenceTransformer, util
from pathlib import Path
import re

from pdf import get_paragraphs, PDF_SOURCE_DIR

model = SentenceTransformer("all-MiniLM-L6-v2")
#model = SentenceTransformer("all-mpnet-base-v2")

def get_sentences_from_paragraph(paragraph: str) -> [str]:
    sentence_border = re.compile('(\.\s+[A-Z])')

    split = sentence_border.split(paragraph)

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

if __name__ == '__main__':
    question = 'How are interrupts trigerred?'
    question_enc = model.encode(question)

    file = next(Path(PDF_SOURCE_DIR).iterdir())

    paragraphs = get_paragraphs(str(file))
    sentences_grouped_by_paragraphs = [get_sentences_from_paragraph(paragraph) for paragraph in paragraphs]

    paragraph_from_sentence = [par_idx for par_idx, sentences_in_paragraph in enumerate(sentences_grouped_by_paragraphs) for _ in sentences_in_paragraph]
    sentences = [sentence for sentences_in_paragraph in sentences_grouped_by_paragraphs for sentence in sentences_in_paragraph]

    encodings = model.encode(sentences)

    top = sorted([(it, i) for i, it in enumerate(util.cos_sim(encodings, question_enc))], reverse=True)[:10]

    print(f'Question is: {question}')

    print()

    print('Top 10 sentences:')
    for it, i in top:
        print(it, sentences[i])

    print()

    print('Best sentence paragraph:')
    print(paragraphs[paragraph_from_sentence[top[0][1]]])
