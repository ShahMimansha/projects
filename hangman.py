from tkinter import *
from tkinter import messagebox
import random

# Initialize main window
root = Tk()
root.title('HANG MAN')
root.geometry('800x600')
root.resizable(False, False)
root.configure(bg="#E7FFFF")

# Load images for hangman stages
hangman_images = ['h1.png', 'h2.png', 'h3.png', 'h4.png', 'h5.png', 'h6.png', 'h7.png']
hangman_pics = [PhotoImage(file=img) for img in hangman_images]
hangman_label = Label(root, bg="#E7FFFF", image=hangman_pics[0])
hangman_label.place(x=300, y=-50)

# Word selection
words = ["apple", "banana", "grape", "mango", "orange"]
selected_word = random.choice(words)

# UI for word blanks
win_count = 0
d = []
for i in range(len(selected_word)):
    d.append(Label(root, text="_", font=("Arial", 20)))
    d[i].place(x=200 + (i * 40), y=300)

# Variables
count = 0
score = 0
run = True
guessed_letters = set()

# Function to update hangman image on wrong guesses
def update_hangman():
    if count < len(hangman_pics):
        hangman_label.config(image=hangman_pics[count])

# Check function for button clicks
def check(letter, button):
    global count, win_count, run, score
    button.destroy()  # Remove button after clicking
    guessed_letters.add(letter)

    if letter in selected_word:
        for i in range(len(selected_word)):
            if selected_word[i] == letter:
                win_count += 1
                d[i].config(text=letter.upper())

        if win_count == len(selected_word):
            score += 1
            answer = messagebox.askyesno('GAME OVER', 'YOU WON!\nWANT TO PLAY AGAIN?')
            if answer:
                run = True
                root.destroy()
            else:
                run = False
                root.destroy()
    else:
        count += 1
        update_hangman()  # Update image on wrong guess

        if count == 6:
            answer = messagebox.askyesno('GAME OVER', 'YOU LOST!\nWANT TO PLAY AGAIN?')
            if answer:
                run = True
                score = 0
                root.destroy()
            else:
                run = False
                root.destroy()

# AI Agent with dynamic difficulty selection
difficulty = StringVar(value="Medium")  # Default is Medium

def set_difficulty(level):
    difficulty.set(level)
    difficulty_label.config(text=f"Difficulty: {level}")

def ai_guess():
    available_letters = [l for l in "abcdefghijklmnopqrstuvwxyz" if l not in guessed_letters]

    if not available_letters:
        messagebox.showinfo("AI Guess", "No more letters left to guess!")
        return

    level = difficulty.get()
    
    if level == "Easy":
        best_guess = random.choice(available_letters)  # AI picks randomly
    elif level == "Medium":
        best_guess = max(available_letters, key=lambda x: selected_word.count(x))  # AI picks based on frequency
    elif level == "Hard":
        # AI tries to predict using known word structure
        revealed = "".join([l if l in guessed_letters else "_" for l in selected_word])
        possible_guesses = [l for l in available_letters if l in selected_word]
        best_guess = random.choice(possible_guesses) if possible_guesses else random.choice(available_letters)

    guessed_letters.add(best_guess)

    # Find and simulate clicking the correct button
    for btn in buttons:
        if btn.cget("text").lower() == best_guess:
            check(best_guess, btn)
            break

# Create letter buttons
buttons = []
letters = "abcdefghijklmnopqrstuvwxyz"
x_pos, y_pos = 0, 520  # Adjusted position for visibility

for i, letter in enumerate(letters):
    if i == 13:  # Move to the next row after 13 letters
        x_pos = 0
        y_pos = 570

    btn = Button(root, text=letter.upper(), command=lambda l=letter: check(l, btn), font=("Arial", 12), bg="red", fg="white")
    btn.place(x=x_pos, y=y_pos, width=50, height=50)
    buttons.append(btn)

    x_pos += 60  # Spacing between buttons

# AI Guess Button
ai_button = Button(root, text="AI Guess", command=ai_guess, font=("Arial", 12), bg="gray", fg="white")
ai_button.place(x=350, y=470, width=100, height=40)

# Difficulty Selection UI
difficulty_label = Label(root, text="Difficulty: Medium", font=("Arial", 12), bg="#E7FFFF")
difficulty_label.place(x=620, y=10)

easy_button = Button(root, text="Easy", command=lambda: set_difficulty("Easy"), font=("Arial", 10), bg="lightgreen")
easy_button.place(x=620, y=40, width=60, height=30)

medium_button = Button(root, text="Medium", command=lambda: set_difficulty("Medium"), font=("Arial", 10), bg="yellow")
medium_button.place(x=690, y=40, width=60, height=30)

hard_button = Button(root, text="Hard", command=lambda: set_difficulty("Hard"), font=("Arial", 10), bg="red", fg="white")
hard_button.place(x=760, y=40, width=60, height=30)

# Run the application
root.mainloop()
