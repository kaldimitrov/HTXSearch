import fitz
import re
from typing import Union
import os

PDF_SOURCE_DIR = './examples/'

invalid_chars = re.compile('.*[\x00-\x08\x0B-\x1F].*')

# the coefficient between lowercase characters and the total characters
def lowercase_coef(block: str) -> float:
    lowercase_count = sum([1 for ch in block if ch.islower()])
    return lowercase_count / len(block)

def get_paragraphs(pdf_name: str, min_lowercase_coef=0.5, paragraph_min_words=30) -> [str]:
    doc = fitz.open(pdf_name)

    result = []
    for idx, page in enumerate(doc):
        if idx == 0: continue
        blocks = page.get_text('blocks')

        # each block is a tuple with some metadata so we extract only the raw content
        blocks = [block[4] for block in blocks]

        # blocks may have invalid chars such as "^R"
        blocks = [block for block in blocks if not invalid_chars.match(block)]

        # a meaningful content block is one with at least some words
        blocks = [block for block in blocks if len(block.split(' ')) > paragraph_min_words]

        # a meaningful content block has a lot of lowercase letters
        blocks = [block for block in blocks if lowercase_coef(block) > min_lowercase_coef]

        blocks = [block.replace('\n', '') for block in blocks]

        # format the bulletins
        blocks = [re.sub('•', '\n• ', block) for block in blocks]

        if len(blocks) > 0:
            result.extend(blocks)

    return result


mode: Union['diff', 'show'] = 'show'

if __name__ == '__main__' and mode == 'show':
    len_all = 0

    for file in os.listdir(PDF_SOURCE_DIR):
        filename = os.path.join(PDF_SOURCE_DIR, file)
        paragraphs = get_paragraphs(filename)
        print(*paragraphs , sep='\n\n')
        len_all += len(paragraphs)

    print('all are', len_all)

if __name__ == '__main__' and mode == 'diff':
    len_all = 0

    for file in os.listdir(PDF_SOURCE_DIR):
        filename = os.path.join(PDF_SOURCE_DIR, file)
        paragraphs_low  = get_paragraphs(filename, min_lowercase_coef=0.50)
        paragraphs_high = get_paragraphs(filename, min_lowercase_coef=0.75)

        paragraphs = list(set(paragraphs_low) - set(paragraphs_high))

        print(*paragraphs , sep='\n\n')
        len_all += len(paragraphs)

    print(len_all, 'more')
