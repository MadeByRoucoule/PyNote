from customtkinter import *
from pages import *
from scripts import *

class App():
    def __init__(self):
        
        self.root = CTk()
        self.root.iconbitmap("src/assets/img/logo.ico")
        
        self.settings_script = SettingsScript()
        self.languages_script = LanguagesScript()

        set_appearance_mode(f"{self.settings_script.get_setting_value("appearance.theme").lower()}")
        set_default_color_theme(f"src/assets/json/themes/{self.settings_script.get_setting_value("appearance.color").lower()}.json")

        if not self.settings_script.settings["pronote_account"]["username"] or \
           not self.settings_script.settings["pronote_account"]["password"] or \
           not self.settings_script.settings["pronote_account"]["pronote_link"] or \
           not self.settings_script.settings["pronote_account"]["ent_choice"]:
            self.login_page = LoginPage(
                master=self.root, 
                settings_script=self.settings_script,
                on_login_success=self.launch_home_page,
                fg_color="transparent"
            )
            self.login_page.pack(expand=True, fill="both")
        else:
            self.launch_home_page()

        self.root.mainloop()

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
        home_page = HomePage(self.root, self.pronote_script, self.settings_script, self.languages_script, self.restart_app, fg_color="transparent")
        home_page.pack(expand=True, fill="both")
        if self.settings_script.settings["pronote_account"]["remember"] == 0:
            self.settings_script.reset_account()

    def restart_app(self):
        self.root.destroy()
        self.__init__()

if __name__ == "__main__":
    root = App()
