import fitz
import re
import os
from dataclasses import dataclass
from pathlib import Path

from typing import Tuple

PDF_SOURCE_DIR = "./examples/"

contents_entry = re.compile(r"^\d.*\d$")
toc_section = re.compile(r"^\d+(\.\d+)* .*")
non_bulletin_dot = re.compile(r"[^\n]+•.*")


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


# NOTE: returns None if the ToC does not exist
def get_toc(pdf_name: str) -> set[str]:
    doc = fitz.open(pdf_name)
    toc = doc.get_toc()

    if len(toc) == 0:
        return None

    res = set()
    for el in toc:
        res.add(el[1])
    return res


def get_blocks(pdf_name: str) -> [Block]:
    doc = fitz.open(pdf_name)

    ret = []

    for page_idx, page in enumerate(doc):
        if page_idx == 0:
            continue
        assert page.rect.x0 == 0
        assert page.rect.y0 == 0

        page_w = page.rect.x1
        page_h = page.rect.y1

        for x0, y0, x1, y1, text, _, block_type in page.get_text("blocks"):
            if block_type != 0:
                continue

            text = re.sub(r"\s+", " ", text).strip()
            text = re.sub("^•", "\n• ", text)
            # sometimes the section versions are together like: '3.1.CPU ...'
            # text = re.sub(r"(\d\.?)([A-Za-z])", r"\1 \2", text)

            block = Block(
                text=text,
                x0=x0 / page_w,
                y0=y0 / page_h,
                x1=x1 / page_w,
                y1=y1 / page_h,
                page=page_idx + 1,
            )

            ret.append(block)

    return ret


def is_paragraph(block: Block, toc: set[str], min_lowercase_coef=0.5) -> bool:
    if block.y0 < 0.1 or block.y1 > 0.9:
        return False
    if contents_entry.match(block.text):
        return False
    if non_bulletin_dot.match(block.text):
        return False
    if len(block.text.split()) < 2:
        return False

    if toc is not None:
        return lowercase_coef(block.text) > min_lowercase_coef or block.text in toc

    return lowercase_coef(block.text) > min_lowercase_coef


@dataclass
class Section:
    title: Block
    body: [Block]

    def __repr__(self) -> str:
        body_text = "\n".join(it.text for it in self.body)
        return f"{self.title.text}\n{body_text}\n\n"


def get_sections(pdf_name: str) -> [Section]:
    blocks = get_blocks(pdf_name)
    toc = get_toc(pdf_name)

    paragraphs = [b for b in blocks if is_paragraph(b, toc)]

    ret = []

    for paragraph in paragraphs:
        if paragraph.text in toc and toc_section.match(paragraph.text):
            ret.append(Section(title=paragraph, body=[]))
            continue

        if ret:
            ret[-1].body.append(paragraph)

    ret = [r for r in ret if r.body]

    return ret


if __name__ == "__main__":
    len_all = 0

    for file in Path(PDF_SOURCE_DIR).iterdir():
        sections = get_sections(file)
        len_all += len(sections)

        print(f"\nFile: {file}; sections: {len(sections)}")
        print(*[it.title.text for it in sections], sep="\n")
    print(f"Loaded {len_all} sections")
