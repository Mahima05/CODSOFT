import customtkinter as ctk
import sqlite3

class TrackApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()

        self.title("Track List")
        self.geometry("400x400+150+100")

        self.username = username

        # Combobox for selecting a list
        self.list_combobox_label = ctk.CTkLabel(self, text="Select List:")
        self.list_combobox_label.place(x=20, y=20)
        self.list_combobox = ctk.CTkComboBox(self, command=self.on_list_select)
        self.list_combobox.place(x=20, y=50)
        self.load_lists()

        # Textbox to display tasks and their status
        self.task_textbox = ctk.CTkTextbox(self)
        self.task_textbox.place(x=20, y=100)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.place(x=20, y=350)

    def load_lists(self):
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT list_name FROM tasks WHERE username=?", (self.username,))
        lists = cursor.fetchall()
        conn.close()

        # Populate the combobox with list names
        self.list_combobox.configure(values=[lst[0] for lst in lists])

    def on_list_select(self, selected_list):
        self.task_textbox.delete("1.0", ctk.END)  # Clear previous tasks
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute("SELECT task, status FROM tasks WHERE username=? AND list_name=?", (self.username, selected_list))
        tasks = cursor.fetchall()
        conn.close()

        # Display tasks and their status in the textbox
        for task, status in tasks:
            self.task_textbox.insert(ctk.END, f"{task}: {status}\n")

    def back(self):
        self.destroy()
        from Dashboard import DashboardApp
        DashboardApp().mainloop()

if __name__ == "__main__":
    app = TrackApp(username="current_user")
    app.mainloop()
