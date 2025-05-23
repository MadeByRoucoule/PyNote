import customtkinter as ctk
from PIL import ImageTk, Image
from sys import platform
from login_page import LoginPage
from home_page import HomePage
from paths import *
from settings import SettingsScript
from languages import LanguagesScript
from pronote import PronoteScript

class Application(ctk.CTk):
    def __init__(self):
        # ---------------- variables
        self.settings_script = SettingsScript(settings_file_path)
        self.languages_script = LanguagesScript(langages_file_path)
        # ---------------- ctk config
        super().__init__()

        if platform == "win32":
            self.iconbitmap(app_icon_file_path)
        else:
            # unix (macOS and linux)
            self.icon = ImageTk.PhotoImage(Image.open(app_icon_file_path))
            self.iconphoto(True, self.icon)
            self.wm_iconbitmap()

        if not self.settings_script.settings["pronote_account"]["username"] or \
           not self.settings_script.settings["pronote_account"]["password"] or \
           not self.settings_script.settings["pronote_account"]["pronote_link"] or \
           not self.settings_script.settings["pronote_account"]["ent_choice"]:
            self.login_page = LoginPage(
                master=self,
                settings_script=self.settings_script,
                on_login_success=self.launch_home_page,
                fg_color="transparent"
            )
            self.login_page.pack(expand=True, fill="both")
        else:
            self.launch_home_page()

    def launch_home_page(self):
        if hasattr(self, "login_page"):
            self.login_page.destroy()
        self.pronote_script = PronoteScript(
            self.settings_script.settings["pronote_account"]["username"],
            self.settings_script.settings["pronote_account"]["password"],
            self.settings_script.settings["pronote_account"]["pronote_link"],
            self.settings_script.settings["pronote_account"]["ent_choice"],
            self.settings_script
        )
        home_page = HomePage(self, self.pronote_script, self.settings_script, self.languages_script, self.restart_app, fg_color="transparent")
        home_page.pack(expand=True, fill="both")
        if self.settings_script.settings["pronote_account"]["remember"] == 0:
            self.settings_script.reset_account()

    def restart_app(self):
        self.destroy()
        self.__init__()

if __name__ == "__main__":
    root = Application()

    ctk.set_appearance_mode(f"{root.settings_script.get_setting_value("appearance.theme").lower()}")
    ctk.set_default_color_theme(assets_theme_file_dir + root.settings_script.get_setting_value("appearance.color").lower() + ".json")

    root.mainloop()
    exit(0)