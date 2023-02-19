from typing import List, Tuple
BACKGROUND_COLOR = "#B1B2DD"
import random
from tkinter import *
from tkinter import simpledialog
import fitz
from PyDictionary import PyDictionary
from pymongo import MongoClient
import PySimpleGUI as sg

client = MongoClient("mongodb+srv://anthonysharonov:awesome132@cluster0.kyrgb3n.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('vocabulary')
words = db.words

randEntry = {}
to_learn = {}
dictionary=PyDictionary()

def _parse_highlight(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
    points = annot.vertices
    quad_count = int(len(points) / 4)
    sentences = []
    for i in range(quad_count):
        r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect
        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        sentences.append(" ".join(w[4] for w in words))
    sentence = " ".join(sentences)
    return sentence

def handle_page(page):
    wordlist = page.get_text("words") 
    wordlist.sort(key=lambda w: (w[3], w[0]))  

    highlights = []
    annot = page.first_annot
    while annot:
        if annot.type[0] == 8:
            highlights.append(_parse_highlight(annot, wordlist))
        annot = annot.next
    return highlights

def main(filepath: str) -> List:
    doc = fitz.open(filepath)

    highlights = []
    for page in doc:
        highlights += handle_page(page)

    return highlights

def next_card():
    global flip_timer, randEntry
    window.after_cancel(flip_timer)
    count = words.count_documents({})
    randEntry = words.find()[random.randrange(count)]
    b = randEntry.get('word')
    canvas.itemconfig(card_title, text="Word", fill="black")
    canvas.itemconfig(card_word, text=b, fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    c = randEntry.get('meaning')
    canvas.itemconfig(card_title, text = "Meaning", fill = "white")
    canvas.itemconfig(card_word, text=c, fill = "white")
    canvas.itemconfig(card_background, image=card_back_img)

if __name__ == "__main__":
    
    highlights = main("text.pdf")
    
    for i in highlights:
        if words.find_one({'word':i}) is None:
            mean = dictionary.meaning(i)
            list2 = list(mean.values())[0]
            meaning = list2[0]
            to_learn[i] = meaning
            new_word = {
                'word':i,
                'meaning':meaning
            }
            words.insert_one(new_word)
            print("sent!")
        else:
            print('exists!')

    window = Tk()
    window.title("My Vocabulary")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
    flip_timer = window.after(3000, func=flip_card) #3 seconds

    canvas = Canvas(width=800, height=526)
    card_front_img = PhotoImage(file="./images/card_front.png")
    card_back_img = PhotoImage(file="./images/card_back.png")
    card_background = canvas.create_image(400, 263, image=card_front_img)
    card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
    canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
    card_word = canvas.create_text(400, 263, width = 500, text="Word", font=("Ariel",20,"bold"), tags="word")
    canvas.grid(row=0, column=0, columnspan=2)

    cross_image = PhotoImage(file="./images/next.png")
    unknown_button = Button(image=cross_image, command = next_card)
    unknown_button.grid(row=1, column=0, sticky="W")

    next_card()
    window.mainloop()
