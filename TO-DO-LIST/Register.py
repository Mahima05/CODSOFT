import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class RegisterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Register")
        self.geometry("400x500+150+100")

        # Name
        self.name_label = ctk.CTkLabel(self, text="Name:")
        self.name_label.place(x=30, y=30)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.place(x=150, y=25)

        # Age
        self.age_label = ctk.CTkLabel(self, text="Age:")
        self.age_label.place(x=30, y=80)
        self.age_entry = ctk.CTkEntry(self)
        self.age_entry.place(x=150, y=75)

        # Current Role
        self.role_label = ctk.CTkLabel(self, text="Current Role:")
        self.role_label.place(x=30, y=130)
        self.role_entry = ctk.CTkEntry(self)
        self.role_entry.place(x=150, y=125)

        # Mobile Number
        self.mobile_label = ctk.CTkLabel(self, text="Mobile Number:")
        self.mobile_label.place(x=30, y=180)
        self.mobile_entry = ctk.CTkEntry(self)
        self.mobile_entry.place(x=150, y=175)

        # Password
        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.place(x=30, y=230)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.place(x=150, y=225)

        # Confirm Password
        self.confirm_password_label = ctk.CTkLabel(self, text="Confirm Password:")
        self.confirm_password_label.place(x=30, y=280)
        self.confirm_password_entry = ctk.CTkEntry(self, show="*")
        self.confirm_password_entry.place(x=150, y=275)

        # Show Password checkbox
        self.show_password_var = ctk.BooleanVar()
        self.show_password_checkbox = ctk.CTkCheckBox(self, text="Show Password", variable=self.show_password_var, command=self.toggle_password)
        self.show_password_checkbox.place(x=150, y=320)

        # Register and Back buttons
        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.place(x=150, y=370)

        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.place(x=150, y=430)

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")
            self.confirm_password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
            self.confirm_password_entry.configure(show="*")

    def register(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        role = self.role_entry.get()
        mobile = self.mobile_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not name or not age or not role or not mobile or not password or not confirm_password:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            conn = sqlite3.connect('todo.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (name, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration Successful")
            self.back()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def back(self):
        self.destroy()
        from Login import LoginApp
        LoginApp().mainloop()

if __name__ == "__main__":
    app = RegisterApp()
    app.mainloop()
