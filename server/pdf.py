import fitz
import re
from typing import Union
import os

PDF_SOURCE_DIR = "./examples/"

contents_entry = re.compile(r"^\d.*\d$")
section_title = re.compile(r"^\d(\.(\d|[a-z])+)* ")
section_title_version = re.compile(r"^(\d+(\.(\d|[a-z])+)*) ")


class Version:
    # '2.4.3' or '1.4.a'
    raw: str

    def __init__(self, raw: str) -> None:
        self.raw = raw

    def increment(self) -> "Version":
        versions = self.raw.split(".")[::-1]
        if versions[0].isalpha():
            versions[0] = chr(ord(versions[0]) + 1)
        else:
            versions[0] = str(int(versions[0]) + 1)
        self.raw = ".".join(versions[::-1])
        return self

    def __repr__(self) -> str:
        return self.raw

    # returns whether other is a proper successor to the current version
    def compare(self, other: str) -> bool:
        left = self.raw.split(".")
        right = other.split(".")

        for idx in range(min(len(left), len(right))):
            l = left[idx]
            r = right[idx]

            if l.isalpha() and r.isalpha():
                diff = ord(r) - ord(l)
                if diff < -1 or diff > 2:
                    return False
                continue

            if l.isdigit() and r.isdigit():
                diff = int(r) - int(l)
                if diff < -1 or diff > 2:
                    return False
                continue

            return False

        return True


# the coefficient between lowercase characters and the total characters
def lowercase_coef(block: str) -> float:
    lowercase_count = sum([1 for ch in block if ch.islower()])
    return lowercase_count / len(block)


def get_paragraphs(
    pdf_name: str, min_lowercase_coef=0.50, paragraph_min_words=30
) -> [str]:
    doc = fitz.open(pdf_name)

    # NOTE: here we assume the pdf's pages are equal in size
    _dict = doc.load_page(0).get_text("dict")
    width = _dict["width"]
    # height = _dict["height"]

    # width low bound
    wlb = width * 0.10
    # width high bound
    whb = width * 0.90

    result = []
    for idx, page in enumerate(doc):
        if idx == 0:
            continue

        blocks = page.get_text("blocks")

        # each block is a tuple with some metadata so we extract only the raw content
        blocks = [block[4] for block in blocks if block[1] > wlb and block[1] < whb]

        # a meaningful content block is one with at least some words
        # blocks = [
        #     block for block in blocks if len(block.split(" ")) > paragraph_min_words
        # ]

        # a meaningful content block has a lot of lowercase letters
        blocks = [
            block
            for block in blocks
            if lowercase_coef(block) > min_lowercase_coef or section_title.match(block)
        ]

        blocks = [block.replace("\n", "") for block in blocks]

        # blocks may have invalid chars such as "^R"
        blocks = [block for block in blocks if not contents_entry.match(block)]

        # format the bulletins
        blocks = [re.sub("•", "\n• ", block) for block in blocks]

        if len(blocks) > 1:
            result.extend(blocks)

    return result


class Section:
    title: str
    body: str

    def __init__(self, title: str, body: str) -> None:
        self.title = title
        self.body = body

    def __repr__(self) -> str:
        return f"{self.title}\n{self.body}\n\n"


def get_sections(pdf_name: str) -> [Section]:
    paragraphs = get_paragraphs(pdf_name)

    # used buffers
    buf_title = ""
    buf_body = ""

    result = []
    version = Version("1")

    paragraph_min_words = 35

    for paragraph in paragraphs:
        title = re.findall(section_title_version, paragraph)

        if len(title) > 0 and version.compare(title[0][0]):
            version = Version(title[0][0])
            if buf_title != "" and len(buf_body.split(" ")) > paragraph_min_words:
                result.append(Section(buf_title, buf_body))
            buf_title = paragraph
            buf_body = ""
        else:
            buf_body += paragraph

    if buf_title != "" and buf_body != "":
        result.append(Section(buf_title, buf_body))

    return result


mode: Union["diff", "show"] = "show"

if __name__ == "__main__" and mode == "show":
    len_all = 0

    for file in os.listdir(PDF_SOURCE_DIR)[1:]:
        print(f"\nFile: {file}")
        filename = os.path.join(PDF_SOURCE_DIR, file)
        sections = get_sections(filename)
        print(*sections, sep="\n\n")
        len_all += len(sections)

    # sections = get_sections("./examples/STM32F103_Datasheet.pdf")
    # print(*sections, sep="\n\n")
    # print("all are", len(sections))

if __name__ == "__main__" and mode == "diff":
    len_all = 0

    for file in os.listdir(PDF_SOURCE_DIR)[1:]:
        filename = os.path.join(PDF_SOURCE_DIR, file)
        paragraphs_low = get_paragraphs(filename, min_lowercase_coef=0.50)
        paragraphs_high = get_paragraphs(filename, min_lowercase_coef=0.75)

        paragraphs = list(set(paragraphs_low) - set(paragraphs_high))

        print(*paragraphs, sep="\n\n")
        len_all += len(paragraphs)

    print(len_all, "more")

ver = Version("2.a")
ver.increment()
print(ver.compare("2.c"))
print(ver.compare("2.2"))

print(re.findall(section_title_version, "2ajajajaj"))
