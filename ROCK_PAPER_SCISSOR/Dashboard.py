import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors - Dashboard")
        self.root.geometry("600x600+475+100")

        # Database setup
        self.conn = sqlite3.connect('game_data.db')
        self.c = self.conn.cursor()

        # Alter the table to add the score column if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS players (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            difficulty TEXT NOT NULL,
                            score INTEGER DEFAULT 0
                        )''')
        self.conn.commit()

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Name label and entry
        self.name_label = tk.Label(self.root, text="Enter your name:", font=("Times New Roman", 20, "bold"))
        self.name_label.place(x=10, y=100)

        self.name_entry = tk.Entry(self.root)
        self.name_entry.place(x=235, y=108, width=300, height=30)

        # Difficulty label and combobox
        self.difficulty_label = tk.Label(self.root, text="Select Difficulty:", font=("Times New Roman", 20, "bold"))
        self.difficulty_label.place(x=10, y=160)

        self.difficulty_var = tk.StringVar(value="Normal")
        self.difficulty_menu = ttk.Combobox(self.root, textvariable=self.difficulty_var, state="readonly")
        self.difficulty_menu['values'] = ("Normal", "Medium", "Hard")
        self.difficulty_menu.place(x=235, y=168, width=300, height=30)

        # Start button
        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.place(x=100, y=250, width=150, height=40)

        # Leaderboard button
        self.leaderboard_button = tk.Button(self.root, text="Leaderboard", command=self.open_leaderboard)
        self.leaderboard_button.place(x=300, y=250, width=150, height=40)

    def start_game(self):
        name = self.name_entry.get()
        difficulty = self.difficulty_var.get()

        if not name:
            messagebox.showerror("Input Error", "Please enter your name.")
            return

        if difficulty not in ["Normal", "Medium", "Hard"]:
            messagebox.showerror("Input Error", "Please select a difficulty level.")
            return

        # Save the player data into the database
        self.c.execute("INSERT INTO players (name, difficulty, score) VALUES (?, ?, ?)", (name, difficulty, 0))
        self.conn.commit()

        # Close the current window
        self.root.destroy()

        # Open the Game.py file
        os.system('python Game.py')

    def open_leaderboard(self):
        # Close the current window
        self.root.destroy()

        # Open the Leaderboard.py file
        os.system('python Leaderboard.py')

    def __del__(self):
        # Close the database connection when the object is deleted
        self.conn.close()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    dashboard = Dashboard(root)
    root.mainloop()
