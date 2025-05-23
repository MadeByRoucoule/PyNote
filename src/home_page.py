from customtkinter import *
import tkchart as tkc
import datetime
from PIL import Image, ImageDraw

from assets.widgets import CTkRadarChart
from paths import *

class HomePage(CTkFrame):
    def __init__(self, master, pronote_script, settings_script, languages_script, restart_app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.pronote_script = pronote_script
        self.pronote_client = self.pronote_script.client_notes
        self.settings_script = settings_script
        self.languages_script = languages_script
        self.languages = self.languages_script.languages
        self.restart_app = restart_app

        self.master.title(self.languages[self.settings_script.get_setting_value("general.language")][0])
        self.master.geometry("850x500")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.left_frame = CTkFrame(self, width=200, corner_radius=6)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.left_frame.grid_propagate(False)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)

        self.account_frame = CTkFrame(self.left_frame, height=28, fg_color="transparent")
        self.account_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.account_frame.grid_columnconfigure(0, weight=1)

        self.create_circular_image(profile_picture_file_path, round_profile_picture_file_path)

        self.account_img = Image.open(round_profile_picture_file_path)
        self.account_picture = CTkImage(light_image=self.account_img, dark_image=self.account_img, size=(28, 28))
        self.account_name_label = CTkLabel(
            self.account_frame,
            text=f"  {self.pronote_script.client.info.name}",
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12, "bold"),
            image=self.account_picture,
            compound="left",
            anchor="center"
        )
        self.account_name_label.grid(row=0, column=0, sticky="ew")

        separator = CTkFrame(self.left_frame, height=2)
        separator.grid(row=1, column=0, padx=10, sticky="ew")

        self.tabs_frame = CTkFrame(self.left_frame, fg_color="transparent")
        self.tabs_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.tabs_frame.grid_columnconfigure(0, weight=1)
        self.tabs_frame.grid_rowconfigure(0, weight=1)
        self.tabs_frame.grid_rowconfigure(4, weight=1)

        self.dashboard_tab_button = CTkButton(
            self.tabs_frame, 
            text=self.languages[self.settings_script.get_setting_value("general.language")][1], 
            fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]), 
            hover_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]),
            text_color=["black", "white"],
            command=self.show_dashboard_tab
        )
        self.dashboard_tab_button.grid(row=1, column=0, pady=(10, 0), sticky="ew")

        self.notes_tab_button = CTkButton(
            self.tabs_frame, 
            text=self.languages[self.settings_script.get_setting_value("general.language")][2], 
            fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]),
            hover_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]),
            text_color=["black", "white"],
            command=self.show_notes_tab
        )
        self.notes_tab_button.grid(row=2, column=0, pady=(10, 0), sticky="ew")

        self.settings_tab_button = CTkButton(
            self.tabs_frame, 
            text=self.languages[self.settings_script.get_setting_value("general.language")][3], 
            fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]),
            hover_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]), 
            text_color=["black", "white"],
            command=self.show_settings_tab
        )
        self.settings_tab_button.grid(row=3, column=0, pady=10, sticky="ew")

        separator = CTkFrame(self.left_frame, height=2)
        separator.grid(row=3, column=0, padx=10, sticky="ew")

        self.disconect_button = CTkButton(self.left_frame, text=self.languages[self.settings_script.get_setting_value("general.language")][4], command=self.disconnect)
        self.disconect_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.show_dashboard_tab()
    
    def create_circular_image(self, input_path, output_path):
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size
        side = min(width, height)
        left = (width - side) // 2 if width >= side else 0
        top = 0
        right = left + side
        bottom = top + side

        square_img = img.crop((left, top, right, bottom))
        mask = Image.new("L", (side, side), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, side, side), fill=255)
        square_img.putalpha(mask)
        square_img.save(output_path, format="PNG")
        return square_img

    def disconnect(self):
        self.settings_script.reset_account()
        self.destroy()

    def show_dashboard_tab(self):
        try:
            self.notes_dashboard_tab_frame.grid_forget()
            self.notes_graph_tab_frame.grid_forget()
            self.settings_tab_frame.grid_forget()
        except:
            pass

        self.dashboard_tab_frame = CTkFrame(self, fg_color="transparent")
        self.dashboard_tab_frame.grid(row=0, column=1, padx=(0,10), pady=10, sticky="nsew")
        self.dashboard_tab_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_tab_frame.grid_columnconfigure(1, weight=2)
        self.dashboard_tab_frame.grid_rowconfigure(0, weight=0)
        self.dashboard_tab_frame.grid_rowconfigure(1, weight=2)
        self.dashboard_tab_frame.grid_rowconfigure(2, weight=1)

        self.average_frame = CTkFrame(self.dashboard_tab_frame, corner_radius=6)
        self.average_frame.grid(row=0, column=0, padx=(0,10), pady=(0, 10), sticky="nsew")
        self.average_frame.grid_columnconfigure(0, weight=1)

        self.notes_general_average_label = CTkLabel(
            self.average_frame,
            height=25,
            text=f"{self.languages[self.settings_script.get_setting_value("general.language")][5]} {round(self.pronote_client['overall_average'], 2)}/20",
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 14),
            anchor='w'
        )
        self.notes_general_average_label.grid(row=0, column=0, sticky='ew', padx=15, pady=(10,0))
        self.notes_general_average_trim_1_label = CTkLabel(
            self.average_frame,
            height=20,
            text=f"{self.languages[self.settings_script.get_setting_value("general.language")][6]} {round(self.pronote_client['periods'][0]['average'], 2)}/20",
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 13),
            text_color="gray",
            anchor='w'
        )
        self.notes_general_average_trim_1_label.grid(row=1, column=0, sticky='ew', padx=20)
        self.notes_general_average_trim_2_label = CTkLabel(
            self.average_frame,
            height=20,
            text=f"{self.languages[self.settings_script.get_setting_value("general.language")][7]} {round(self.pronote_client['periods'][1]['average'], 2)}/20",
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 13),
            text_color="gray",
            anchor='w'
        )
        self.notes_general_average_trim_2_label.grid(row=2, column=0, sticky='ew', padx=20)
        self.notes_general_average_trim_3_label = CTkLabel(
            self.average_frame,
            height=20,
            text=f"{self.languages[self.settings_script.get_setting_value("general.language")][8]} {round(self.pronote_client['periods'][2]['average'], 2)}/20",
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 13),
            text_color="gray",
            anchor='w'
        )
        self.notes_general_average_trim_3_label.grid(row=3, column=0, sticky='ew', padx=20, pady=(0,10))

        self.lasts_notes_frame = CTkFrame(self.dashboard_tab_frame, corner_radius=6)
        self.lasts_notes_frame.grid(row=1, column=0, rowspan=2, padx=(0,10), sticky="nsew")
        self.lasts_notes_frame.grid_columnconfigure(0, weight=1)
        self.lasts_notes_frame.grid_rowconfigure(1, weight=1) 

        self.lasts_notes_label = CTkLabel(
            self.lasts_notes_frame,
            text=self.languages[self.settings_script.get_setting_value("general.language")][9],
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 14),
            anchor="w"
        )
        self.lasts_notes_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.lasts_notes_list = CTkScrollableFrame(self.lasts_notes_frame, fg_color="transparent")
        self.lasts_notes_list.grid(row=1, column=0, padx=(7,0), pady=(0,10), sticky="nsew")
        self.lasts_notes_list._scrollbar.grid_configure(padx=0)
        self.lasts_notes_list._scrollbar.configure(width=10)
        self.lasts_notes_list.grid_columnconfigure(0, weight=1)

        all_grades = []
        for period in self.pronote_client["periods"]:
            for grade in period["grades"]:
                try:
                    grade_date = datetime.datetime.strptime(grade["date"], "%d/%m/%Y")
                    grade["parsed_date"] = grade_date
                    all_grades.append(grade)
                except Exception:
                    continue

        all_grades.sort(key=lambda g: g["parsed_date"])
        last_10 = all_grades[-10:] if len(all_grades) >= 10 else all_grades
        last_10.reverse()
        for note in last_10:
            note_frame = CTkFrame(
                self.lasts_notes_list, 
                height=56, 
                corner_radius=6, 
                fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"])
            )
            note_frame.pack(fill="x", pady=(0,10))
            note_frame.grid_columnconfigure(0, weight=1)
            note_frame.grid_rowconfigure(0, weight=1)

            subject_label = CTkLabel(
                note_frame,
                text=note['subject'].split("<")[0].split(">")[0].strip(),
                font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                anchor="w"
            )
            subject_label.grid(row=0, column=0, padx=10, sticky="ew")

            date_label = CTkLabel(
                note_frame,
                text=note['date'],
                font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                anchor="w"
            )
            date_label.grid(row=1, column=0, padx=10, sticky="ew")

            if note['value'] <= 7:
                value_color = ["#c50606", "#f80a0a"]
            elif note['value'] <= 11:
                value_color = ["#998200", "#ffda01"]
            elif note['value'] <= 17:
                value_color = ["#379341", "#45b851"]
            else:
                value_color = ["#006600", "#008000"]

            value_frame = CTkFrame(note_frame, fg_color="transparent")
            value_frame.grid(row=0, column=1, rowspan=2, padx=(0,10), pady=10, sticky="nsew")
            value_frame.grid_columnconfigure(0, weight=1)
            value_frame.grid_rowconfigure(0, weight=1)
            value_label = CTkLabel(
                value_frame,
                text=f"{note['value']}/20",
                font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                anchor="w"
            )
            value_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
            value_color_frame = CTkFrame(value_frame, height=12, width=12, fg_color=value_color, corner_radius=6)
            value_color_frame.grid(row=0, column=1, sticky="ew")

        self.lasts_notes_list.grid_rowconfigure(0, weight=1)
        self.lasts_notes_list.grid_columnconfigure(0, weight=1)  

        self.radar_chart_frame = CTkFrame(self.dashboard_tab_frame, corner_radius=6)
        self.radar_chart_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.radar_chart_frame.grid_columnconfigure(0, weight=1)
        self.radar_chart_frame.grid_rowconfigure(0, weight=1)

        subject_grades = {}
        for period in self.pronote_client["periods"]:
            for grade in period["grades"]:
                subject = grade["subject"]
                try:
                    note_value = float(grade["value"])
                except:
                    continue
                if subject not in subject_grades:
                    subject_grades[subject] = []
                subject_grades[subject].append(note_value)

        subject_avg = {}
        for subject, values in subject_grades.items():
            if values:
                subject_avg[subject] = sum(values) / len(values)

        labels = list(subject_avg.keys())
        values = [subject_avg[label] for label in labels]

        self.radar_chart = CTkRadarChart(
            self.radar_chart_frame,
            labels=[label.split("<")[0].split(">")[0].strip() for label in labels],
            num_axes=len(labels)
        )
        self.radar_chart.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.radar_chart.add_data("A", values, color="#03CB5D", fill=True)

        self.average_per_subject_frame = CTkFrame(self.dashboard_tab_frame, corner_radius=6)
        self.average_per_subject_frame.grid(row=2, column=1, pady=(10,0), sticky="nsew")
        self.average_per_subject_frame.grid_columnconfigure(0, weight=1)
        self.average_per_subject_frame.grid_rowconfigure(1, weight=1)

        self.average_per_subject_label = CTkLabel(
            self.average_per_subject_frame,
            text=self.languages[self.settings_script.get_setting_value("general.language")][10],
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 14),
            anchor="w"
        )
        self.average_per_subject_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.average_per_subject_list = CTkScrollableFrame(self.average_per_subject_frame, fg_color="transparent")
        self.average_per_subject_list.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.average_per_subject_list._scrollbar.grid_configure(padx=0)
        self.average_per_subject_list._scrollbar.configure(width=10)
        self.average_per_subject_list.grid_columnconfigure(0, weight=1)

        for i in range(len(labels)):
            subject_frame = CTkFrame(
                self.average_per_subject_list,
                height=42,
                corner_radius=6,
                fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"])
            )
            subject_frame.pack(fill="x", pady=(0,10))
            subject_frame.grid_propagate(False)
            subject_frame.grid_columnconfigure(0, weight=1)
            subject_frame.grid_rowconfigure(0, weight=1)

            subject_label = CTkLabel(
                subject_frame,
                text=labels[i].split("<")[0].split(">")[0].strip(),
                font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                anchor="w"
            )
            subject_label.grid(row=0, column=0, padx=10, sticky="ew")

            if subject_avg[labels[i]] <= 7:
                value_color = ["#c50606", "#f80a0a"]
            elif subject_avg[labels[i]] <= 11:
                value_color = ["#998200", "#ffda01"]
            elif subject_avg[labels[i]] <= 17:
                value_color = ["#379341", "#45b851"]
            else:
                value_color = ["#006600", "#008000"]

            avg_frame = CTkFrame(subject_frame, fg_color="transparent")
            avg_frame.grid(row=0, column=1, padx=(0,10), sticky="nsew")
            avg_frame.grid_columnconfigure(0, weight=1)
            avg_frame.grid_rowconfigure(0, weight=1)
            avg_label = CTkLabel(
                avg_frame,
                text=f"{subject_avg[labels[i]]:.2f}/20",
                font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                anchor="w"
            )
            avg_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
            avg_color_frame = CTkFrame(avg_frame, height=12, width=12, fg_color=value_color, corner_radius=6)
            avg_color_frame.grid(row=0, column=1, sticky="ew")

    def show_notes_tab(self):
        try:
            self.notes_dashboard_tab_frame.grid_forget()
            self.notes_graph_tab_frame.grid_forget()
            self.settings_tab_frame.grid_forget()
        except:
            pass

        self.periods_list = [self.pronote_client["periods"][i]["name"] for i in range(len(self.pronote_client["periods"]))]

        self.notes_dashboard_tab_frame = CTkFrame(self, fg_color="transparent")
        self.notes_dashboard_tab_frame.grid(row=0, column=1, padx=(0,10), pady=10, sticky="nsew")
        self.notes_dashboard_tab_frame.grid_columnconfigure(1, weight=1)
        self.notes_dashboard_tab_frame.grid_rowconfigure(1, weight=1)

        self.notes_settings_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.notes_settings_frame.grid(row=0, column=0, sticky="nsew")
        self.notes_settings_frame.grid_columnconfigure(0, weight=1)
 
        self.period_option_menu = CTkOptionMenu(
            self.notes_settings_frame,
            values=self.periods_list,
            command=self.notes_period_option_menu_callback
        )
        self.period_option_menu.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.subjects_list = list(set(grade["subject"] for grade in self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"]))

        self.notes_subjects_option_menu = CTkOptionMenu(
            self.notes_settings_frame,
            values=[subject.split("<")[0].split(">")[0].strip() for subject in self.subjects_list],
            command=self.notes_subjects_listbox_callback
        )
        self.notes_subjects_option_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))

        self.notes_list_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.notes_list_frame.grid(row=1, column=0, sticky="nsew")
        self.notes_list_frame.grid_columnconfigure(0, weight=1)
        self.notes_list_frame.grid_rowconfigure(0, weight=1)

        self.notes_listbox = CTkScrollableFrame(self.notes_list_frame, fg_color="transparent")
        self.notes_listbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.notes_listbox._scrollbar.grid_configure(padx=0)
        self.notes_listbox._scrollbar.configure(width=10)
        self.notes_listbox.grid_columnconfigure(0, weight=1)

        self.subject_info_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.subject_info_frame.grid(row=2, column=0, sticky="nsew", pady=(10,0))
        self.subject_info_frame.grid_columnconfigure(0, weight=1)
        self.subject_info_frame.grid_rowconfigure(0, weight=1)

        self.subject_average_label = CTkLabel(
            self.subject_info_frame,
            height=20,
            text=f"{self.languages[self.settings_script.get_setting_value("general.language")][11]} : ",
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
            anchor='w'
        )
        self.subject_average_label.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        self.notes_graph_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.notes_graph_frame.grid(row=0, column=1, rowspan=2, padx=(10,0), sticky="nsew")
        self.notes_graph_frame.grid_columnconfigure(0, weight=1)
        self.notes_graph_frame.grid_rowconfigure(0, weight=1)

        self.notes_list_info_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.notes_list_info_frame.grid(row=2, column=1, sticky="nsew", padx=(10,0), pady=(10,0))
        self.notes_list_info_frame.grid_columnconfigure(0, weight=1)
        self.notes_list_info_frame.grid_rowconfigure(0, weight=1)

        self.notes_period_option_menu_callback(self.period_option_menu.get())
        self.notes_graph_frame.bind("<Configure>", lambda event: self.update_graph())

    def notes_period_option_menu_callback(self, value):
        self.subjects_list = list(set(grade["subject"] for grade in self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"]))
        current_value = self.notes_subjects_option_menu.get()
        new_values = [subject.split("<")[0].split(">")[0].strip() for subject in self.subjects_list]

        if current_value in new_values:
            self.notes_subjects_option_menu.configure(values=new_values)
            self.notes_subjects_option_menu.set(current_value)
            self.notes_subjects_listbox_callback(current_value)
        else:
            self.notes_subjects_option_menu.configure(values=new_values)
            self.notes_subjects_option_menu.set(self.notes_subjects_option_menu._values[0])
            self.notes_subjects_listbox_callback(self.notes_subjects_option_menu._values[0])

    def notes_subjects_listbox_callback(self, x):
        for child in self.notes_listbox.winfo_children():
            child.pack_forget()

        self.update_graph()
        self.subjects_list = list(set(grade["subject"] for grade in self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"]))

        self.subject_average_label.configure(
            text=f"{self.languages[self.settings_script.get_setting_value("general.language")][11]} {round(self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['subjects'][self.subjects_list[self.notes_subjects_option_menu._values.index(self.notes_subjects_option_menu.get())]], 2)}/20"
        )

        x = self.subjects_list[self.notes_subjects_option_menu._values.index(self.notes_subjects_option_menu.get())]

        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"])):
            if self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"] == x:
                subject_text = self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"].split("<")[0].split(">")[0].strip()
                note_frame = CTkFrame(
                    self.notes_listbox,
                    height=56,
                    corner_radius=6,
                    fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"])
                )
                note_frame.pack(fill="x", pady=(0,10))
                note_frame.grid_propagate(False)
                note_frame.grid_columnconfigure(0, weight=1)
                note_frame.grid_rowconfigure(0, weight=1)

                subject_label = CTkLabel(
                    note_frame,
                    text=subject_text,
                    font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                    anchor="w"
                )
                subject_label.grid(row=0, column=0, padx=10, sticky="ew")

                date_label = CTkLabel(
                    note_frame,
                    text=f"{self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['date']}",
                    font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                    anchor="w"
                )
                date_label.grid(row=1, column=0, padx=10, sticky="ew")

                if self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"] <= 7:
                    value_color = ["#c50606", "#f80a0a"]
                elif self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"] <= 11:
                    value_color = ["#998200", "#ffda01"]
                elif self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"] <= 17:
                    value_color = ["#379341", "#45b851"]
                else:
                    value_color = ["#006600", "#008000"]

                value_frame = CTkFrame(note_frame, fg_color="transparent")
                value_frame.grid(row=0, column=1, rowspan=2, padx=(0,10), pady=10, sticky="nsew")
                value_frame.grid_columnconfigure(0, weight=1)
                value_frame.grid_rowconfigure(0, weight=1)
                value_label = CTkLabel(
                    value_frame,
                    text=f"{self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['value']:.2f}/20",
                    font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                    anchor="w"
                )
                value_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
                value_color_frame = CTkFrame(value_frame, height=12, width=12, fg_color=value_color, corner_radius=6)
                value_color_frame.grid(row=0, column=1, sticky="ew")

                self.notes_listbox_callback(f"{self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['subject']} : {self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['grade']} / {self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['out_of']} | ({round(self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['value'], 2)})")
                note_frame.bind("<Enter>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"])))
                note_frame.bind("<Leave>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"])))
                note_frame.bind("<Button-1>", lambda event, x=f"{self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['subject']} : {self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['grade']} / {self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['out_of']} | ({round(self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['value'], 2)})": self.notes_listbox_callback(x))
                for child in note_frame.winfo_children():
                    child.bind("<Enter>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"])))
                    child.bind("<Leave>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"])))
                    child.bind("<Button-1>", lambda event, x=f"{self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['subject']} : {self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['grade']} / {self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['out_of']} | ({round(self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['value'], 2)})": self.notes_listbox_callback(x))
                    for child2 in child.winfo_children():
                        child2.bind("<Enter>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"])))
                        child2.bind("<Leave>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"])))
                        child2.bind("<Button-1>", lambda event, x=f"{self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['subject']} : {self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['grade']} / {self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['out_of']} | ({round(self.pronote_client['periods'][self.periods_list.index(self.period_option_menu.get())]['grades'][i]['value'], 2)})": self.notes_listbox_callback(x))

    def notes_listbox_callback(self, x):
        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"])):
            grade = self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]
            combo = f"{grade['subject']} : {grade['grade']} / {grade['out_of']} | ({round(grade['value'], 2)})"
            if combo == x:
                try:
                    self.note_comment_label.grid_forget()
                    self.note_value_label.grid_forget()
                    self.note_coefficient_label.grid_forget()
                    self.note_date_label.grid_forget()
                except:
                    pass
                self.note_comment_label = CTkLabel(
                    self.notes_list_info_frame,
                    height=20,
                    text=f"{grade['comment']}",
                    font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                    anchor='w'
                )
                self.note_value_label = CTkLabel(
                    self.notes_list_info_frame,
                    height=20,
                    text=f"Note : {grade['grade']} / {grade['out_of']} | ({round(grade['value'], 2)}/20)",
                    font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                    anchor='w'
                )
                self.note_coefficient_label = CTkLabel(
                    self.notes_list_info_frame,
                    height=20,
                    text=f"Coefficient : {grade['coefficient']}",
                    font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                    anchor='w'
                )
                self.note_date_label = CTkLabel(
                    self.notes_list_info_frame,
                    height=20,
                    text=f"Date : {grade['date']}",
                    font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
                    anchor='w'
                )
                if grade["comment"] != "":
                    self.note_comment_label.grid(row=0, column=0, sticky='ew', padx=20, pady=(10,0))
                    self.note_value_label.grid(row=1, column=0, sticky='ew', padx=20)
                    self.note_coefficient_label.grid(row=2, column=0, sticky='ew', padx=20)
                    self.note_date_label.grid(row=3, column=0, sticky='ew', padx=20, pady=(0,10))
                else:
                    self.note_value_label.grid(row=0, column=0, sticky='ew', padx=20, pady=(10,0))
                    self.note_coefficient_label.grid(row=1, column=0, sticky='ew', padx=20)
                    self.note_date_label.grid(row=2, column=0, sticky='ew', padx=20, pady=(0,10))

    def update_graph(self, val=None):
        try:
            self.notes_graph.grid_forget()
        except:
            pass
        
        x_val = []
        grades = self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"]
        subject = self.subjects_list[self.notes_subjects_option_menu._values.index(self.notes_subjects_option_menu.get())]
        for grade in grades:
            if grade["subject"] == subject:
                x_val.append(grade["date"])

        width, height = self.get_size()
        self.notes_graph = tkc.LineChart(
            self.notes_graph_frame,
            width=width,
            height=height-50,
            x_axis_values=tuple(x_val),
            y_axis_values=(0, 20),
            x_axis_section_count=5,
            y_axis_section_count=8,
            bg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["fg_color"]),
            fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["fg_color"]),
            x_axis_font_color=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["text_color"]),
            y_axis_font_color=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["text_color"]),
            axis_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]),
            x_axis_section_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]),
            y_axis_section_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"])
        )
        self.notes_graph.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.note_line = tkc.Line(
            self.notes_graph,
            size=3,
            point_highlight="enabled",
            color=self._apply_appearance_mode(ThemeManager.theme["CTkButton"]["fg_color"])
        )
        self.note_average_line = tkc.Line(
            self.notes_graph,
            size=2,
            style="dashed",
            color="#449944"
        )
        self.note_class_average_line = tkc.Line(
            self.notes_graph,
            size=2,
            point_highlight="enabled",
            color="#994444"
        )
        
        notes_graph_list = []
        y = 0
        for grade in grades:
            if grade["subject"] == subject:
                y += 1
                notes_graph_list.append(grade["value"])
                if y == 1:
                    notes_graph_list.append(grade["value"])
        
        notes_average_graph = []
        total_notes = 0
        total_coef = 0
        for grade in grades:
            if grade["subject"] == subject:
                total_notes += grade["value"] * grade["coefficient"]
                total_coef += grade["coefficient"]
        for i in range(len(notes_graph_list)):
            notes_average_graph.append(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["subjects"][subject])

        self.notes_graph.show_data(self.note_average_line, notes_average_graph)
        self.notes_graph.show_data(self.note_line, notes_graph_list)
        
    def get_size(self):
        return self.notes_graph_frame.winfo_width(), self.notes_graph_frame.winfo_height()
    
    def show_settings_tab(self):
        try:
            self.notes_dashboard_tab_frame.grid_forget()
            self.notes_graph_tab_frame.grid_forget()
            self.settings_tab_frame.grid_forget()
        except:
            pass

        self.settings_tab_frame = CTkFrame(self, fg_color="transparent")
        self.settings_tab_frame.grid(row=0, column=1, padx=(0,10), pady=10, sticky="nsew")
        self.settings_tab_frame.grid_columnconfigure(0, weight=1)
        self.settings_tab_frame.grid_columnconfigure(1, weight=1)
        self.settings_tab_frame.grid_rowconfigure(2, weight=1)

        self.account_info_frame = CTkFrame(self.settings_tab_frame, corner_radius=6)
        self.account_info_frame.grid(row=0, column=0, columnspan=2, sticky="new", pady=(0,10))
        self.account_info_frame.grid_columnconfigure(0, weight=1)
        self.account_info_frame.grid_rowconfigure(1, weight=1)
        self.account_info_frame.grid_rowconfigure(2, weight=1)
        self.account_info_frame.grid_rowconfigure(3, weight=1)


        self.account_info_label = CTkLabel(
            self.account_info_frame,
            text=self.languages[self.settings_script.get_setting_value("general.language")][12],
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 14, "bold"),
            anchor="w"
        )
        self.account_info_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,0))

        self.account_info_name_label = CTkLabel(
            self.account_info_frame,
            text=f"{self.languages[self.settings_script.get_setting_value("general.language")][13]} {self.pronote_client['client_info']['name']}",
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
            anchor="w"
        )
        self.account_info_name_label.grid(row=1, column=0, sticky="ew", padx=20)

        self.account_info_class_label = CTkLabel(
            self.account_info_frame,
            text=f"{self.languages[self.settings_script.get_setting_value("general.language")][14]} {self.pronote_client['client_info']['class']}",
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
            anchor="w"
        )        
        self.account_info_class_label.grid(row=2, column=0, sticky="ew", padx=20)

        self.account_info_school_label = CTkLabel(
            self.account_info_frame,
            text=f"{self.languages[self.settings_script.get_setting_value("general.language")][15]} {self.pronote_client['client_info']['school']}",
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
            anchor="w"
        )        
        self.account_info_school_label.grid(row=3, column=0, sticky="ew", padx=20, pady=(0,10))

        self.account_img_rect = Image.open("src/assets/img/profile_picture.png")
        picture_size = self.account_img_rect.size
        height = 100
        self.account_picture_rect = CTkImage(light_image=self.account_img_rect, dark_image=self.account_img_rect, size=(picture_size[0]*height/picture_size[1], height))
        self.account_picture_label = CTkLabel(
            self.account_info_frame,
            text="",
            image=self.account_picture_rect
        )
        self.account_picture_label.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=20)

        self.settings_general_frame = CTkFrame(self.settings_tab_frame, corner_radius=6)
        self.settings_general_frame.grid(row=1, column=0, sticky="new")
        self.settings_general_frame.grid_columnconfigure(0, weight=1)

        self.settings_general_label = CTkLabel(
            self.settings_general_frame,
            text=self.languages[self.settings_script.get_setting_value("general.language")][16],
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 14),
            anchor="w"
        )
        self.settings_general_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,0))

        self.language_label = CTkLabel(
            self.settings_general_frame,
            text=self.languages[self.settings_script.get_setting_value("general.language")][17],
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
            anchor="w"
        )
        self.language_label.grid(row=1, column=0, sticky="ew", padx=10, pady=(5,0))
        self.languages_list = [lang for lang in self.settings_script.settings["general"]["language"].keys()]
        self.language_option_menu = CTkOptionMenu(
            self.settings_general_frame,
            values=self.languages_list,
            command=self.change_language
        )
        self.language_option_menu.grid(row=2, column=0, sticky="ew", padx=10, pady=(0,10))
        self.language_option_menu.set(self.settings_script.get_setting_value("general.language"))

        self.settings_apparence_frame = CTkFrame(self.settings_tab_frame, corner_radius=6)
        self.settings_apparence_frame.grid(row=1, column=1, sticky="new", padx=(10,0))
        self.settings_apparence_frame.grid_columnconfigure(0, weight=1)

        self.settings_apparence_label = CTkLabel(
            self.settings_apparence_frame,
            text=self.languages[self.settings_script.get_setting_value("general.language")][18],
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 14),
            anchor="w"
        )
        self.settings_apparence_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10,0))

        self.theme_label = CTkLabel(
            self.settings_apparence_frame,
            text=self.languages[self.settings_script.get_setting_value("general.language")][19],
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
            anchor="w"
        )
        self.theme_label.grid(row=1, column=0, sticky="ew", padx=10, pady=(10,0))
        self.themes = [theme for theme in self.settings_script.settings["appearance"]["theme"].keys()]
        self.theme_option_menu = CTkOptionMenu(
            self.settings_apparence_frame,
            values=self.themes,
            command=self.change_theme
        )
        self.theme_option_menu.grid(row=2, column=0, sticky="ew", padx=10)
        self.theme_option_menu.set(self.settings_script.get_setting_value("appearance.theme"))

        self.color_label = CTkLabel(
            self.settings_apparence_frame,
            text=self.languages[self.settings_script.get_setting_value("general.language")][20],
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
            anchor="w"
        )
        self.color_label.grid(row=3, column=0, sticky="ew", padx=10, pady=(5,0))
        self.colors = [theme for theme in self.settings_script.settings["appearance"]["color"].keys()]
        self.color_option_menu = CTkOptionMenu(
            self.settings_apparence_frame,
            values=self.colors,
            command=self.change_color
        )
        self.color_option_menu.grid(row=4, column=0, sticky="ew", padx=10)
        self.color_option_menu.set(self.settings_script.get_setting_value("appearance.color"))

        self.font_label = CTkLabel(
            self.settings_apparence_frame,
            text=self.languages[self.settings_script.get_setting_value("general.language")][21],
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
            anchor="w"
        )
        self.font_label.grid(row=5, column=0, sticky="ew", padx=10, pady=(5,0))
        self.fonts = [font for font in self.settings_script.settings["appearance"]["font_family"].keys()]
        self.font_option_menu = CTkOptionMenu(
            self.settings_apparence_frame,
            values=self.fonts,
            command=self.change_font
        )
        self.font_option_menu.grid(row=6, column=0, sticky="ew", padx=10, pady=(0,10))
        self.font_option_menu.set(self.settings_script.get_setting_value("appearance.font_family"))

        self.apply_settings_button = CTkButton(
            self.settings_tab_frame,
            text=self.languages[self.settings_script.get_setting_value("general.language")][22],
            font=(self.settings_script.get_setting_value("appearance.font_family").lower(), 12),
            command=self.apply_settings
        )
        self.apply_settings_button.place(relx=0.99, rely=0.99, anchor="se")

    def apply_settings(self):
        self.settings_script.save_settings()
        self.restart_app()

    def change_language(self, value):
        self.settings_script.settings["general"]["language"][value] = 1
        for lang in self.settings_script.settings["general"]["language"].keys():
            if lang != value:
                self.settings_script.settings["general"]["language"][lang] = 0

    def change_theme(self, value):
        for param in self.settings_script.settings["appearance"]["theme"].keys():
            self.settings_script.settings["appearance"]["theme"][param] = 1 if param == value else 0

    def change_color(self, value):
        for param in self.settings_script.settings["appearance"]["color"].keys():
            self.settings_script.settings["appearance"]["color"][param] = 1 if param == value else 0

    def change_font(self, value):
        for param in self.settings_script.settings["appearance"]["font_family"].keys():
            self.settings_script.settings["appearance"]["font_family"][param] = 1 if param == value else 0
