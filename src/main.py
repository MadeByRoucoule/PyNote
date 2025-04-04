from customtkinter import *
from pages import *
from scripts import *

class App(CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("src/assets/img/logo.ico")
        
        set_appearance_mode("system")
        set_default_color_theme("src/assets/json/themes/green.json")
        
        self.settings_script = SettingsScript()

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
        home_page = HomePage(self, self.pronote_script, self.settings_script, fg_color="transparent")
        home_page.pack(expand=True, fill="both")
        if self.settings_script.settings["pronote_account"]["remember"] == 0:
            self.settings_script.reset_account()

if __name__ == "__main__":
    root = App()
    root.mainloop()
