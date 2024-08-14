import customtkinter as ctk
import sqlite3
from tkinter import messagebox, END
from tkinter.ttk import Combobox

class ModifyApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()

        self.title("Modify Existing List")
        self.geometry("600x500+150+100")

        self.username = username

        # Initialize database connection
        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()

        # List selection
        self.list_label = ctk.CTkLabel(self, text="Select List:", font = ("Times New Roman", 20, "bold"))
        self.list_label.place(x=25, y=20)
        self.list_combobox = Combobox(self, state="readonly")
        self.list_combobox.place(x=170, y=35)
        self.load_lists()
        self.list_combobox.bind('<<ComboboxSelected>>', self.on_list_select)

        # Task selection
        self.task_label = ctk.CTkLabel(self, text="Select Task:", font = ("Times New Roman", 20, "bold"))
        self.task_label.place(x=275, y=20)
        self.task_combobox = Combobox(self, state="readonly")
        self.task_combobox.place(x=500, y=35)

        self.new_task_label = ctk.CTkLabel(self, text="New Task:", font = ("Times New Roman", 20, "bold"))
        self.new_task_label.place(x=25, y=75)
        self.new_task_entry = ctk.CTkEntry(self)
        self.new_task_entry.place(x=130, y=75)

        self.add_task_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_task_button.place(x=300, y=75)

        # Display tasks in the selected list
        self.tasks_textbox = ctk.CTkTextbox(self, font = ("Times New Roman", 20, "bold"), width = 475)
        self.tasks_textbox.place(x=25, y=125)

        # Modify task status
        self.status_label = ctk.CTkLabel(self, text="Modify Task Status:", font = ("Times New Roman", 20, "bold"))
        self.status_label.place(x=25, y=350)
        self.status_combobox = Combobox(self, values=["Ongoing", "Completed", "Terminated"], state="readonly")
        self.status_combobox.place(x=275, y=445)

        self.modify_status_button = ctk.CTkButton(self, text="Modify Status", command=self.modify_status)
        self.modify_status_button.place(x=25, y=400)

        # Delete task button
        self.delete_task_button = ctk.CTkButton(self, text="Delete Task", command=self.delete_task)
        self.delete_task_button.place(x=200, y=400)

        # Delete list button
        self.delete_list_button = ctk.CTkButton(self, text="Delete List", command=self.delete_list)
        self.delete_list_button.place(x=25, y=450)

        # Back button
        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.place(x=200, y=450)

    def load_lists(self):
        try:
            self.cursor.execute("SELECT DISTINCT list_name FROM tasks WHERE username=?", (self.username,))
            lists = self.cursor.fetchall()

            list_names = [lst[0] for lst in lists]
            self.list_combobox['values'] = list_names
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def on_list_select(self, event):
        selected_list = self.list_combobox.get()
        if selected_list:
            self.load_tasks(selected_list)
        else:
            messagebox.showwarning("Input Error", "Please select a list")

    def load_tasks(self, list_name):
        try:
            self.task_combobox.set('')
            self.task_combobox['values'] = []
            self.tasks_textbox.delete(1.0, END)

            self.cursor.execute("SELECT task, status FROM tasks WHERE username=? AND list_name=?",
                                (self.username, list_name))
            tasks = self.cursor.fetchall()

            task_names = []
            for task, status in tasks:
                self.tasks_textbox.insert(END, f"{task} ({status})\n")
                task_names.append(task)

            self.task_combobox['values'] = task_names
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def modify_status(self):
        selected_task = self.task_combobox.get()
        new_status = self.status_combobox.get().strip()

        list_name = self.list_combobox.get()

        if selected_task and new_status:
            try:
                self.cursor.execute("UPDATE tasks SET status=? WHERE username=? AND list_name=? AND task=?",
                                    (new_status, self.username, list_name, selected_task))
                self.conn.commit()
                messagebox.showinfo("Success", "Task status updated successfully")
                self.load_tasks(list_name)
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please select a task and enter a new status")

    def delete_task(self):
        selected_task = self.task_combobox.get()
        list_name = self.list_combobox.get()

        if selected_task and list_name:
            try:
                self.cursor.execute("DELETE FROM tasks WHERE username=? AND list_name=? AND task=?",
                                    (self.username, list_name, selected_task))
                self.conn.commit()
                messagebox.showinfo("Success", "Task deleted successfully")
                self.load_tasks(list_name)
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please select a task to delete")

    def delete_list(self):
        list_name = self.list_combobox.get()

        if list_name:
            try:
                self.cursor.execute("DELETE FROM tasks WHERE username=? AND list_name=?", (self.username, list_name))
                self.conn.commit()
                self.load_lists()
                self.tasks_textbox.delete(1.0, END)
                self.task_combobox.set('')
                messagebox.showinfo("Success", "List deleted successfully")
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please select a list to delete")

    def add_task(self):
        list_name = self.list_combobox.get()
        new_task = self.new_task_entry.get().strip()

        if list_name and new_task:
            try:
                self.cursor.execute("INSERT INTO tasks (username, list_name, task, status) VALUES (?, ?, ?, 'Ongoing')",
                                    (self.username, list_name, new_task))
                self.conn.commit()
                messagebox.showinfo("Success", "Task added successfully")
                self.new_task_entry.delete(0, END)  # Clear the entry after adding
                self.load_tasks(list_name)
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please select a list and enter a new task")

    def back(self):
        self.conn.close()  # Close the database connection
        self.destroy()
        from Dashboard import DashboardApp
        DashboardApp().mainloop()

if __name__ == "__main__":
    username = "current_user"  # This should be dynamically set based on the logged-in user
    app = ModifyApp(username)
    app.mainloop()
