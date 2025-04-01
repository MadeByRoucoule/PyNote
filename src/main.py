from pages import *
from scripts import *

class App:
    def __init__(self):

        self.settings_script = SettingsScript()

        if not self.settings_script.settings["pronote_account"]["username"] or not self.settings_script.settings["pronote_account"]["password"] or not self.settings_script.settings["pronote_account"]["pronote_link"] or not self.settings_script.settings["pronote_account"]["ent_choice"]:
            login_page = LoginPage(self.settings_script)
            login_page.mainloop()

        self.pronote_script = PronoteScript(
            self.settings_script.settings["pronote_account"]["username"],
            self.settings_script.settings["pronote_account"]["password"],
            self.settings_script.settings["pronote_account"]["pronote_link"],
            self.settings_script.settings["pronote_account"]["ent_choice"],
            self.settings_script
            )
        
        home_page = HomePage(self.pronote_script, self.settings_script)
        home_page.mainloop()

        if self.settings_script.settings["pronote_account"]["remember"] == 0:
            self.settings_script.reset_account()

if __name__ == "__main__":
    App()