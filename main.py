from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#2A36FF"

# Load the data using pandas
# to a csv file that orients by records,
# Load from words to learn or original file using exception handling

try:
    data = pandas.read_csv("data/Unlearned_words.csv")
except FileNotFoundError:
    use_original = pandas.read_csv("data/french_words.csv")
    dictionary_file = use_original.to_dict(orient="records")
else:
    dictionary_file = data.to_dict(orient="records")
finally:
    present_card = {}


def next_card():
    global present_card, flip
    window.after_cancel(flip)
    # cancel timer so as tto wait on new card before timing
    present_card = random.choice(dictionary_file)
    # make a random data be present from loaded csv file
    canvas.itemconfig(card_background, image=get_card_front_image)
    canvas.itemconfig(title_text, text="French word", fill="black")
    canvas.itemconfig(word_text, text=present_card["French"], fill="black")
    # Update user interface upon new cards
    flip = window.after(3000, func=flip_em_cards)
    # resume and resets timer on evey new card shown


def flip_em_cards():
    # A function that updates UI and reveals back card
    canvas.itemconfig(card_background, image=get_card_back_image)
    canvas.itemconfig(title_text, text="English word", fill="blue")
    canvas.itemconfig(word_text, text=present_card["English"], fill="blue")


def already_learned_card():
    dictionary_file.remove(present_card)
    remaining_words = pandas.DataFrame(dictionary_file)
    remaining_words.to_csv("data/Unlearned_words.csv", index=False)
    next_card()


# -----------------------------------------------------------------------------
# -------------------------- UI SECTION -------------------------------------

window = Tk()
window.title("Flash card app")
window.config(padx=30, pady=50, bg=BACKGROUND_COLOR)
flip = window.after(3000, func=flip_em_cards)

canvas = Canvas(width=400, height=226)
get_card_front_image = PhotoImage(file="images/card_front.png")
get_card_back_image = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(200, 133, image=get_card_front_image)
title_text = canvas.create_text(200, 60, text="", font=("Ariel", 20, "italic"))
word_text = canvas.create_text(200, 120, text="", font=("sans", 35, "bold"))


canvas.config(highlightthickness=0, background=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)

cancel_image = PhotoImage(file="images/wrong.png")
cancel_button = Button(image=cancel_image, highlightthickness=0, command=next_card)
cancel_button.grid(column=0, row=2)

space_text = Label(text="", bg=BACKGROUND_COLOR)
space_text.grid(column=0, row=1)
space_text_2 = Label(text="", bg=BACKGROUND_COLOR)
space_text_2.grid(column=1, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0,  command=already_learned_card)
right_button.grid(column=1, row=2)
next_card()

window.mainloop()
