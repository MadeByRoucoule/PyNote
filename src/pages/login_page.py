from customtkinter import *
import pronotepy.ent
from PIL import Image

class LoginPage(CTk):
    def __init__(self, settings_script):
        super().__init__()

        self.settings_script = settings_script

        self.title("Login Page")
        self.geometry("600x400")
        self.resizable(False, False)
        self.iconbitmap("src/assets/img/logo.ico")

        self.config(background="#62B1FC")
        set_appearance_mode("system")
        set_default_color_theme("src/assets/json/themes/blue.json")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        bg_image = Image.open("src/assets/img/login_bg.jpg").resize((800, 450))
        image = CTkImage(light_image=bg_image, dark_image=bg_image, size=(800, 450))

        self.bg_label = CTkLabel(self, text="", image=image)
        self.bg_label.grid(row=0, column=0, sticky="nsew")

        self.login_frame = CTkFrame(self.bg_label, width=250, corner_radius=0)
        self.login_frame.grid(row=0, column=0, padx=10, pady=0, sticky="ns")
        self.login_frame.grid_propagate(False)
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(1, weight=1)

        self.login_label = CTkLabel(self.login_frame, text="Login", font=("Arial", 24, "bold"), anchor="w")
        self.login_label.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        self.entry_frame = CTkFrame(self.login_frame, corner_radius=0, fg_color="transparent")
        self.entry_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=20)
        self.entry_frame.grid_columnconfigure(0, weight=1)

        self.username_entry = CTkEntry(self.entry_frame, placeholder_text="Username")
        self.username_entry.grid(row=0, column=0, sticky="ew", pady=5)

        self.password_entry = CTkEntry(self.entry_frame, placeholder_text="Password", show="*")
        self.password_entry.grid(row=1, column=0, sticky="ew", pady=5)

        self.link_entry = CTkEntry(self.entry_frame, placeholder_text="Pronote link")
        self.link_entry.grid(row=2, column=0, sticky="ew", pady=5)

        self.ent_optionmenu = CTkOptionMenu(self.entry_frame, values=[attr for attr in dir(pronotepy.ent) if not attr.startswith("__")])
        self.ent_optionmenu.grid(row=3, column=0, sticky="ew", pady=5)

        self.remember_checkbox = CTkCheckBox(self.entry_frame, text="Remember me")
        self.remember_checkbox.grid(row=4, column=0, pady=5, sticky="w")

        self.login_button = CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, sticky="ew", padx=20, pady=15)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        pronote_link = self.link_entry.get()
        ent_choice = self.ent_optionmenu.get()
        remember = self.remember_checkbox.get()
        
        if username and password and pronote_link and ent_choice:
            self.settings_script.settings["pronote_account"]["username"] = username
            self.settings_script.settings["pronote_account"]["password"] = password
            self.settings_script.settings["pronote_account"]["pronote_link"] = pronote_link
            self.settings_script.settings["pronote_account"]["ent_choice"] = ent_choice
            self.settings_script.settings["pronote_account"]["remember"] = remember
            self.settings_script.save_settings()
            self.destroy()
        else:
            if not username:
                self.username_entry.configure(border_color="red")
            else:
                self.username_entry.configure(border_color=self._apply_appearance_mode(ThemeManager.theme["CTkEntry"]["border_color"]))
            if not password:
                self.password_entry.configure(border_color="red")
            else:
                self.password_entry.configure(border_color=self._apply_appearance_mode(ThemeManager.theme["CTkEntry"]["border_color"]))
            if not pronote_link:
                self.link_entry.configure(border_color="red")
            else:
                self.link_entry.configure(border_color=self._apply_appearance_mode(ThemeManager.theme["CTkEntry"]["border_color"]))

