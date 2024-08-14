import tkinter as tk
from tkinter import ttk  # Correctly import ttk
import sqlite3
import os

class Leaderboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors - Leaderboard")
        self.root.geometry("600x600+475+100")

        # Database setup
        self.conn = sqlite3.connect('game_data.db')
        self.c = self.conn.cursor()

        # Widgets
        self.create_widgets()

        # Load the leaderboard data
        self.load_leaderboard()

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self.root, text="Leaderboard", font=("Arial", 24))
        self.title_label.pack(pady=20)

        # Leaderboard Treeview
        self.tree = ttk.Treeview(self.root, columns=("Name", "Difficulty", "Score"), show='headings')
        self.tree.heading("Name", text="Name")
        self.tree.heading("Difficulty", text="Difficulty")
        self.tree.heading("Score", text="Score")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=20)

        # Back button
        self.back_button = tk.Button(self.root, text="Back to Dashboard", command=self.back_to_dashboard)
        self.back_button.pack(pady=20)

    def load_leaderboard(self):
        # Fetch data from the database and display it
        self.c.execute("SELECT name, difficulty, score FROM players ORDER BY score DESC")
        rows = self.c.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def back_to_dashboard(self):
        # Close the current window
        self.root.destroy()

        # Open the Dashboard.py file
        os.system('python Dashboard.py')

    def __del__(self):
        # Close the database connection when the object is deleted
        self.conn.close()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    leaderboard = Leaderboard(root)
    root.mainloop()
