from customtkinter import *
import pronotepy.ent
from PIL import Image

class LoginPage(CTkFrame):
    def __init__(self, master, settings_script, on_login_success, *args, **kwargs):
        self.on_login_success = on_login_success
        self.settings_script = settings_script
        if "on_login_success" in kwargs:
            del kwargs["on_login_success"]
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.settings_script = settings_script

        self.master.title("Login Page")
        self.master.geometry("439x452")

        set_appearance_mode("system")
        set_default_color_theme("src/assets/json/themes/green.json")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.login_frame = CTkFrame(self)
        self.login_frame.grid(row=0, column=0, padx=10, pady=0)
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(1, weight=1)

        self.label_frame = CTkFrame(self.login_frame, corner_radius=0, fg_color="transparent")
        self.label_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.label_frame.grid_columnconfigure(0, weight=1)

        self.logo_image = CTkImage(Image.open("src/assets/img/logo.ico").resize((40, 40)), size=(40, 40))
        self.logo_label = CTkLabel(self.label_frame, text="", image=self.logo_image, anchor="center")
        self.logo_label.grid(row=0, column=0, sticky="ew", pady=(5, 15))

        self.login_label = CTkLabel(self.label_frame, text="Login", font=("Arial", 24, "bold"), anchor="center")
        self.login_label.grid(row=1, column=0, sticky="ew")

        self.entry_frame = CTkFrame(self.login_frame, corner_radius=0, fg_color="transparent")
        self.entry_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=0)
        self.entry_frame.grid_columnconfigure(0, weight=1)

        self.username_entry = CTkEntry(self.entry_frame, placeholder_text="Username", width=250)
        self.username_entry.grid(row=0, column=0, sticky="ew", pady=5)

        self.password_entry = CTkEntry(self.entry_frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.grid(row=1, column=0, sticky="ew", pady=5)

        self.link_entry = CTkEntry(self.entry_frame, placeholder_text="Pronote link", width=250)
        self.link_entry.grid(row=2, column=0, sticky="ew", pady=5)

        self.ent_optionmenu = CTkOptionMenu(self.entry_frame, values=[attr for attr in dir(pronotepy.ent) if not attr.startswith("__")], fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]), button_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]), button_hover_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]), width=250)
        self.ent_optionmenu.grid(row=3, column=0, sticky="ew", pady=5)

        self.remember_checkbox = CTkCheckBox(self.entry_frame, text="Remember me")
        self.remember_checkbox.grid(row=4, column=0, pady=5, sticky="w")

        self.login_button = CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

    def login(self):
        
        print(self.master.winfo_width(), self.master.winfo_height())
        print(self.login_frame.winfo_width(), self.login_frame.winfo_height())

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
            self.on_login_success()
        else:
            if not username:
                self.username_entry.configure(border_color="#cc1111")
            else:
                self.username_entry.configure(border_color=self._apply_appearance_mode(ThemeManager.theme["CTkEntry"]["border_color"]))
            if not password:
                self.password_entry.configure(border_color="#cc1111")
            else:
                self.password_entry.configure(border_color=self._apply_appearance_mode(ThemeManager.theme["CTkEntry"]["border_color"]))
            if not pronote_link:
                self.link_entry.configure(border_color="#cc1111")
            else:
                self.link_entry.configure(border_color=self._apply_appearance_mode(ThemeManager.theme["CTkEntry"]["border_color"]))
