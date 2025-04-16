import json

class LanguagesScript:
    def __init__(self):
        self.languages_path = "src/assets/json/languages.json"
        self.languages = self.load_languages()

    def load_languages(self):
        try:
            with open(self.languages_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            print(f"Erreur lors du chargement du JSON: {e}")
            return {}