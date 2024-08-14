import customtkinter as ctk
import sqlite3
from tkinter import messagebox

# Initialize the custom Tkinter theme
ctk.set_appearance_mode("dark")  # Modes: "system" (default), "light", "dark"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("400x300+150+100")

        # Username
        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.place(x=30, y=30)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.place(x=150, y=25)

        # Password
        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.place(x=30, y=80)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.place(x=150, y=75)

        # Show Password checkbox
        self.show_password_var = ctk.BooleanVar()
        self.show_password_checkbox = ctk.CTkCheckBox(self, text="Show Password", variable=self.show_password_var,
                                                    command=self.toggle_password)
        self.show_password_checkbox.place(x=150, y=120)

        # Login and Register buttons
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.place(x=75, y=160)

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.place(x=240, y=160)

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password")
            return

        # Check login credentials
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.destroy()
            from Dashboard import DashboardApp
            DashboardApp().mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        self.destroy()
        from Register import RegisterApp
        RegisterApp().mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
