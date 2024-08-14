import customtkinter as ctk
import random
import string
from PIL import Image, ImageTk

class PasswordGeneratorWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password generator")
        self.geometry("600x600+550+100")

        # Set dark mode (black-blue theme)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.label_1 = ctk.CTkLabel(self, text="Enter password length ", font=("Times New Roman", 26))
        self.label_1.place(x=200, y=40)

        self.password_length_entry = ctk.CTkEntry(self, width=200, height=30, border_width=1, corner_radius=10)
        self.password_length_entry.place(x=210, y=90)

        self.select_label = ctk.CTkLabel(self, text="Select the password strength ", font=("Times New Roman", 24))
        self.select_label.place(x=170, y=140)

        self.strength_var = ctk.StringVar()
        self.strength_var.set("Weak")

        self.weak_radio = ctk.CTkRadioButton(self, text="Weak", variable=self.strength_var, value="Weak", corner_radius=5)
        self.weak_radio.place(x=160, y=200)

        self.strong_radio = ctk.CTkRadioButton(self, text="Strong", variable=self.strength_var, value="Strong", corner_radius=5)
        self.strong_radio.place(x=260, y=200)

        self.very_strong_radio = ctk.CTkRadioButton(self, text="Very Strong", variable=self.strength_var, value="Very Strong", corner_radius=5)
        self.very_strong_radio.place(x=360, y=200)

        self.generate_password_button = ctk.CTkButton(self, text="Generate Password",font=("Times New Roman", 20),width=150, height=50, corner_radius=10, command=self.generate_password)
        self.generate_password_button.place(x=220, y=260)

        self.password_label = ctk.CTkLabel(self, text="", font=("Times New Roman", 22))
        self.password_label.place(x=200, y=350)

        self.copy_button = ctk.CTkButton(self, text="Copy",font=("Times New Roman", 18), width=100, height=40, corner_radius=10, command=self.copy_password)
        self.copy_button.place(x=255, y=410)

    def generate_password(self):
        try:
            password_length = int(self.password_length_entry.get())
            strength = self.strength_var.get()

            if strength == "Weak":
                characters_type = random.choice(['lowercase', 'uppercase', 'digits'])
                if characters_type == 'lowercase':
                    characters = string.ascii_lowercase
                elif characters_type == 'uppercase':
                    characters = string.ascii_uppercase
                else:
                    characters = string.digits
            elif strength == "Strong":
                characters = string.ascii_letters + string.digits
            elif strength == "Very Strong":
                characters = string.ascii_letters + string.digits + string.punctuation

            password = ''.join(random.choice(characters) for _ in range(password_length))
            self.password_label.configure(text=password)
        except ValueError:
            self.password_label.configure(text="Invalid input")

    def copy_password(self):
        password = self.password_label.cget("text")
        self.clipboard_clear()
        self.clipboard_append(password)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    window = PasswordGeneratorWindow()
    window.run()
