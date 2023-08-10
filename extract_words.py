
from glob import glob
from PyPDF2 import PdfReader

import fitz # PyMuPDF
from PIL import Image
import pytesseract

from tqdm import tqdm

def pdf_to_text(file):
    with open(file, "rb") as f:
        for page in PdfReader(f).pages:
            yield page.extract_text()

def pdf_to_text_ocr(file):
    pdf_document = fitz.open(pdf_path)
    for page_number in tqdm(range(pdf_document.page_count)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(4,4))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save("tmp.png", "PNG")
        yield pytesseract.image_to_string("tmp.png")
    pdf_document.close()

def extract_text_from_image(image_path):
    # This function is optional. Use it if you want to extract text from images.
    return pytesseract.image_to_string(image_path)

def text_to_words(text):
    words = set()
    for line in text.split("\n"):
        line = clean_line(line.strip())
        for word in line.split():
            words.add(word)
    return words

remove = [",",";",".",":","!","?","\"","•","(",")","[","]","✔","✗","…","“","”","‘","’","-","●","=>","/","—","}","{","˜","¨"]

def clean_line(line):
    for r in remove:
        line = line.replace(r," ")
    while True:
        line2 = line.replace("  "," ")
        if len(line2)==len(line):
            break
        line = line2
    return line

training_data = set(line.strip().split()[0].lower() for line in open("training_data.txt", encoding="utf-8"))

for pdf_path in glob("pdf/*.pdf"):
    print(pdf_path)

    text_pdf = pdf_to_text(pdf_path) # extract text of pdf
    text_orc = pdf_to_text_ocr(pdf_path) # extract text of pdf by OCR
    words = set()
    for i,(t,t2) in enumerate(zip(text_pdf,text_orc)):
        words_i = text_to_words(t)
        words2_i = text_to_words(t2)
        w_rem = []
        w_add = []
        for w in words_i:
            if any(w2 in w and w!=w2 for w2 in words2_i): # OCR detected word which is subword of pdf text -> removing this error
                w_rem.append(w)
                for w2 in words2_i:
                    if w2 in w and w!=w2:
                        w_add.append(w2)
        for w in w_add:
            words2_i.add(w)
        for w in w_rem:
            words_i.remove(w)
            
        for w in words_i:
            if w.isalpha() and w.isascii() and w.lower() not in training_data:
                words.add(w)
    print(words)

    with open("wordfiles/"+pdf_path[:-len("pdf")]+"words", "w") as f:
        for w in words:
            f.write(w+"\n")

