
from glob import glob
import pdftotext
import re

def pdf_to_text(file):
    with open(file, "rb") as f:
        for page in pdftotext.PDF(f):
            yield page

def text_to_words(text):
    words = set()
    for line in text.split("\n"):
        line = clean_line(line.strip())
        #print(line)
        for word in line.split():
            words.add(word)
    return words

remove = [",",";",".",":","!","?","•","(",")","{","}","…",'"',"[","]","“","”","✔","●"]

def clean_line(line):
    for r in remove:
        line = line.replace(r," ")
    line = line.replace("’","'")
    while True:
        line2 = line.replace("  "," ")
        if len(line2)==len(line):
            break
        line = line2
    return line

training_data = set(line.strip().split()[0].lower() for line in open("training_data.txt", encoding="utf-8"))

lower_to_word = {}
for pdf_path in sorted(glob("pdf/*.pdf"), key=lambda x:(len(x),x)):
    print(pdf_path)

    text_pdf = pdf_to_text(pdf_path) # extract text of pdf

    words = set()
    for i,t in enumerate(text_pdf):
        words_i = text_to_words(t)
        for w in words_i:
            if w.lower() not in training_data and not any(n in w for n in "0123456789") and re.fullmatch(r"[a-zA-Z]+[a-zA-Z\-]?[a-zA-Z]+",w):
                if w.lower() in lower_to_word:
                    w = lower_to_word[w.lower()]
                words.add(w)
                lower_to_word[w.lower()] = w
    print(words)

    with open("wordfiles/"+pdf_path[len("pdf/"):-len("pdf")]+"words", "w", encoding="utf-8") as f:
        for w in sorted(words):
            f.write(w+"\n")

