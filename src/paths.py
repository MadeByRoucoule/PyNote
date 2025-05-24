import os
import sys

# ------------------------ create file's paths
assets_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(sys.argv[0]))), "assets")

app_icon_file_path = os.path.join(assets_dir, "img", "logo.png")
# profile pictures
profile_picture_file_path = os.path.join(assets_dir, "img", "profile_picture.png")
round_profile_picture_file_path = os.path.join(assets_dir, "img", "round_profile_picture.png")

assets_theme_file_dir = os.path.join(assets_dir, "json", "themes/")
settings_file_path = os.path.join(assets_dir, "json", "settings.json")
pronote_data_file_path = os.path.join(assets_dir, "json", "pronote_data.json")
langages_file_path = os.path.join(assets_dir, "json", "languages.json")