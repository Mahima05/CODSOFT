import customtkinter as ctk

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard")
        self.geometry("400x300+150+100")

        # Create New List button
        self.create_list_button = ctk.CTkButton(self, text="Create New List", command=self.open_create)
        self.create_list_button.place(x=125, y=50)

        # Modify Existing List button
        self.modify_list_button = ctk.CTkButton(self, text="Modify Existing List", command=self.open_modify)
        self.modify_list_button.place(x=125, y=100)

        # Track List button
        self.track_list_button = ctk.CTkButton(self, text="Track List", command=self.track_list)
        self.track_list_button.place(x=125, y=150)

        # Back button
        self.back_button = ctk.CTkButton(self, text="Back", command=self.back)
        self.back_button.place(x=125, y=200)

    def open_create(self):
        self.destroy()
        from Create import CreateApp
        CreateApp().mainloop()

    def open_modify(self):
        self.destroy()
        from Modify import ModifyApp
        ModifyApp(username="current_user").mainloop()

    def track_list(self):
        self.destroy()
        from Track import TrackApp
        TrackApp(username="current_user").mainloop()

    def back(self):
        self.destroy()
        from Login import LoginApp
        LoginApp().mainloop()

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
