import json

class LanguagesScript:
    def __init__(self, languages_path: str):
        self.languages_path = languages_path
        self.languages = self.load_languages()

    def load_languages(self):
        try:
            with open(self.languages_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            print(f"Erreur lors du chargement du JSON: {e}")
            return {}