import fitz
import re
import os

PARAGRAPH_MIN_WORDS = 30
PDF_SOURCE_DIR = './examples/'

invalid_chars = re.compile('.*[\x00-\x08\x0B-\x1F].*')

def is_content_entry(block: str) -> bool:
    prev_is_ascii = False
    
    for char in block:
        if char.isalpha():
            prev_is_ascii = True

        if char == '.' and not prev_is_ascii:
            return True 

        if char == '.':
            prev_is_ascii = False

    return False 
            
class Paragraph:
    title: str
    content: str

    def __init__(self, title: str, content: str) -> None:
        self.title = title 
        self.content = content

# the coefficient between uppercase characters and the total characters 
def uppercase_coef(block: str) -> float:
    uppercase_count = sum([1 for ch in block if ch.isupper()])
    return uppercase_count / len(block)

# the coefficient of non-readable to total characters 
def non_alphanum_coef(block: str) -> float:
    non_ascii_count = sum([1 for ch in block if not ch.isalnum()])
    return non_ascii_count / len(block)

def get_paragraphs(pdf_name: str) -> [Paragraph]:
    doc = fitz.open(pdf_name)
    
    result = []
    for idx, page in enumerate(doc):
        if idx == 0: continue
        text_blocks_raw = page.get_text('blocks')

        # each block is a tuple with some metadata so we extract only the raw content
        text_blocks = list(map(lambda block: block[4], text_blocks_raw))

        # each block could be a non-readable contents entry, which carries no meaningful data
        readable_blocks = list( \
                filter(lambda block: \
                    not is_content_entry(block) or 
                        invalid_chars.match(block), \
                text_blocks))

        # a meaningful content block is one with at least 15 words and 2 lines
        content_blocks = list( \
                filter(lambda block: \
                    len(block.split('\n')) >= 2 \
                        and len(block.split(' ')) > PARAGRAPH_MIN_WORDS \
                        and uppercase_coef(block) < 0.20 \
                        and non_alphanum_coef(block) < 0.35, \
                readable_blocks))

        content_blocks = list(map(lambda block: block.replace('\n', ''), content_blocks))

        # format the bulletins
        content_blocks = [re.sub('•', '\n• ', block) for block in content_blocks]
        
        if len(content_blocks) > 0:
            result.extend(content_blocks)

    return result


if __name__ == '__main__':
    for file in os.listdir(PDF_SOURCE_DIR):
        filename = os.path.join(PDF_SOURCE_DIR, file)
        print(*get_paragraphs(filename), sep='\n\n')
