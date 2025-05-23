import json
import os

class SettingsScript:
    def __init__(self, settings_path: str):
        self.settings_path = settings_path
        self.settings = self.load_settings()

    def load_settings(self):
        if not os.path.exists(self.settings_path) or os.path.getsize(self.settings_path) == 0:
            return {"default": True}
        try:
            with open(self.settings_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            print(f"Erreur lors du chargement du JSON: {e}")

    def get_setting_value(self, key):
        keys = key.split(".")
        ref = self.settings
        for k in keys:
            ref = ref.get(k)
            if ref is None:
                return None
        
        if isinstance(ref, dict):
            if set(ref.keys()) == {"state", "from", "to"}:
                return ref["state"]
            else:
                for option, value in ref.items():
                    if value == 1:
                        return option
                return list(ref.keys())[0] if ref else None
        else:
            return ref

    def save_settings(self):
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    def reset_account(self):
        self.settings["pronote_account"]["username"] = ""
        self.settings["pronote_account"]["password"] = ""
        self.settings["pronote_account"]["pronote_link"] = ""
        self.settings["pronote_account"]["ent_choice"] = ""
        self.settings["pronote_account"]["remember"] = 0
        self.save_settings()