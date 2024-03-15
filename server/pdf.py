import fitz
import re
import os
from dataclasses import dataclass

PDF_SOURCE_DIR = "./examples/"


# the coefficient between lowercase characters and the total characters
def lowercase_coef(block: str) -> float:
    lowercase_count = sum([1 for ch in block if ch.islower()])
    return lowercase_count / len(block)


@dataclass
class Block:
    text: str
    x0: float
    y0: float
    x1: float
    y1: float
    page: int


def get_blocks(pdf_name: str) -> [Block]:
    doc = fitz.open(pdf_name)

    ret = []

    for page_idx, page in enumerate(doc):
        assert(page.rect.x0 == 0)
        assert(page.rect.y0 == 0)

        page_w = page.rect.x1
        page_h = page.rect.y1

        for x0, y0, x1, y1, text, _, type in page.get_text("blocks"):
            if type != 0:
                continue

            text = text.replace("\n", "")
            re.sub("^•", "• ", text)

            block=Block(
                text=text,
                x0=x0/page_w,
                y0=y0/page_h,
                x1=x1/page_w,
                y1=y1/page_h,
                page=page_idx+1,
            )

            ret.append(block)

    return ret


def is_paragraph(block: Block, min_lowercase_coef=0.5, paragraph_min_words=30) -> bool:
    return len(block.text.split(" ")) > paragraph_min_words and lowercase_coef(block.text) > min_lowercase_coef

if __name__ == "__main__":
    len_all = 0

    for file in os.listdir(PDF_SOURCE_DIR):
        filename = os.path.join(PDF_SOURCE_DIR, file)
        paragraphs = [block for block in get_blocks(filename) if is_paragraph(block)]
        # print(*paragraphs, sep="\n\n")
        len_all += len(paragraphs)

    print("all are", len_all)
