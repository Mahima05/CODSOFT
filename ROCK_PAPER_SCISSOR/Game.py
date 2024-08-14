import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import random
from PIL import Image, ImageTk


class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors - Game")
        self.root.geometry("600x600+475+100")

        # Game variables
        self.round = 1
        self.score = 0
        self.user_choice = None
        self.result = None
        self.difficulty = self.get_difficulty()
        self.rounds_to_win = self.calculate_wins()

        # Load images
        self.load_images()

        # Create widgets
        self.create_widgets()

    def get_difficulty(self):
        # Connect to the database and retrieve the last selected difficulty
        conn = sqlite3.connect('game_data.db')
        c = conn.cursor()
        c.execute("SELECT difficulty FROM players ORDER BY id DESC LIMIT 1")
        difficulty = c.fetchone()[0]
        conn.close()
        return difficulty

    def calculate_wins(self):
        if self.difficulty == "Normal":
            return 7
        elif self.difficulty == "Medium":
            return 5
        else:  # Hard
            return 3

    def load_images(self):
        # Resize images to 50x50 using the LANCZOS filter
        self.rock_img = ImageTk.PhotoImage(Image.open("rock.png").resize((75, 75), Image.LANCZOS))
        self.paper_img = ImageTk.PhotoImage(Image.open("paper.png").resize((75, 75), Image.LANCZOS))
        self.scissor_img = ImageTk.PhotoImage(Image.open("scissor.png").resize((75, 75), Image.LANCZOS))

    def create_widgets(self):
        # Display round and score
        self.round_label = tk.Label(self.root, text=f"Round: {self.round}", font=("Times New Roman", 20, "bold"))
        self.round_label.place(x=50, y=50)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Times New Roman", 20, "bold"))
        self.score_label.place(x=450, y=50)

        # Buttons for Rock, Paper, Scissors
        self.rock_button = tk.Button(self.root, image=self.rock_img, command=lambda: self.play_round("Rock"))
        self.rock_button.place(x=50, y=150)

        self.paper_button = tk.Button(self.root, image=self.paper_img, command=lambda: self.play_round("Paper"))
        self.paper_button.place(x=250, y=150)

        self.scissor_button = tk.Button(self.root, image=self.scissor_img, command=lambda: self.play_round("Scissor"))
        self.scissor_button.place(x=450, y=150)

        # Computer's choice label and image
        self.computer_choice_label = tk.Label(self.root, text="", font=("Times New Roman", 20, "bold"))
        self.computer_choice_label.place(x=150, y=275)

        self.computer_choice_img_label = tk.Label(self.root)
        self.computer_choice_img_label.place(x=250, y=325)

        # End Game button
        self.end_button = tk.Button(self.root, text="End Game", command=self.end_game)
        self.end_button.place(x=250, y=500, width=100, height=40)

        # Next Round button
        self.next_round_button = tk.Button(self.root, text="Next Round", command=self.start_next_round, state="disabled")
        self.next_round_button.place(x=250, y=425, width=100, height=40)

    def play_round(self, user_choice):
        self.user_choice = user_choice
        computer_choice = random.choice(["Rock", "Paper", "Scissor"])

        # Display computer's choice
        self.computer_choice_label.config(text=f"Computer chooses {computer_choice}")
        if computer_choice == "Rock":
            self.computer_choice_img_label.config(image=self.rock_img)
        elif computer_choice == "Paper":
            self.computer_choice_img_label.config(image=self.paper_img)
        else:
            self.computer_choice_img_label.config(image=self.scissor_img)

        self.determine_winner(computer_choice)
        self.update_score()

        # Disable buttons until the next round starts
        self.rock_button.config(state="disabled")
        self.paper_button.config(state="disabled")
        self.scissor_button.config(state="disabled")

        # Enable the Next Round button
        self.next_round_button.config(state="normal")

    def determine_winner(self, computer_choice):
        # Determine if the user wins, loses, or ties
        if self.user_choice == computer_choice:
            self.result = "Tie"
        elif (self.user_choice == "Rock" and computer_choice == "Scissor") or \
                (self.user_choice == "Paper" and computer_choice == "Rock") or \
                (self.user_choice == "Scissor" and computer_choice == "Paper"):
            self.result = "Win"
        else:
            self.result = "Lose"

        # Display the result
        messagebox.showinfo("Round Result", f"You {self.result} this round.")

    def update_score(self):
        if self.result == "Win":
            self.score += 5
        elif self.result == "Lose":
            self.score -= 2

        # Update score label
        self.score_label.config(text=f"Score: {self.score}")

    def start_next_round(self):
        # Prepare for the next round
        self.round += 1
        self.round_label.config(text=f"Round: {self.round}")

        # Enable buttons and disable the Next Round button
        self.rock_button.config(state="normal")
        self.paper_button.config(state="normal")
        self.scissor_button.config(state="normal")
        self.next_round_button.config(state="disabled")

        # Clear computer's choice display
        self.computer_choice_label.config(text="")
        self.computer_choice_img_label.config(image="")

    def end_game(self):
        # Store the final score in the database
        conn = sqlite3.connect('game_data.db')
        c = conn.cursor()
        c.execute("UPDATE players SET score = ? WHERE id = (SELECT MAX(id) FROM players)", (self.score,))
        conn.commit()
        conn.close()

        # Show final score
        messagebox.showinfo("Game Over", f"Final Score: {self.score}")

        # Return to the Dashboard
        self.root.destroy()
        os.system('python Dashboard.py')


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()
