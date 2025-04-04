from customtkinter import *
from CTkListbox import *
import tkchart as tkc
import datetime
from PIL import Image, ImageDraw

from assets.widgets import CTkRadarChart

class HomePage(CTkFrame):
    def __init__(self, master, pronote_script, settings_script, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.pronote_script = pronote_script
        self.pronote_client = self.pronote_script.client_notes
        self.settings_script = settings_script

        self.master.title("Home Page")
        self.master.geometry("800x500")

        set_appearance_mode("system")
        set_default_color_theme("src/assets/json/themes/green.json")

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

        self.create_circular_image("src/assets/img/profile_picture.png", "src/assets/img/round_profile_picture.png")

        self.account_img = Image.open("src/assets/img/round_profile_picture.png")
        self.account_picture = CTkImage(light_image=self.account_img, dark_image=self.account_img, size=(28, 28))
        self.account_name_label = CTkLabel(self.account_frame, text=f"  {self.pronote_script.client.info.name}", font=("Arial", 12, "bold"), image=self.account_picture, compound="left", anchor="center")
        self.account_name_label.grid(row=0, column=0, sticky="ew")

        separator = CTkFrame(self.left_frame, height=2)
        separator.grid(row=1, column=0, padx=10, sticky="ew")

        self.tabs_frame = CTkFrame(self.left_frame, fg_color="transparent")
        self.tabs_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.tabs_frame.grid_columnconfigure(0, weight=1)
        self.tabs_frame.grid_rowconfigure(0, weight=1)
        self.tabs_frame.grid_rowconfigure(4, weight=1)

        self.dashboard_tab_button = CTkButton(self.tabs_frame, 
                                              text="Dashboard", 
                                              fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]), 
                                              hover_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]),
                                              command=self.show_dashboard_tab)
        self.dashboard_tab_button.grid(row=1, column=0, pady=(10, 0), sticky="ew")

        self.notes_tab_button = CTkButton(self.tabs_frame, 
                                          text="Notes", 
                                          fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]),
                                          hover_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]),
                                          command=self.show_notes_tab)
        self.notes_tab_button.grid(row=2, column=0, pady=(10, 0), sticky="ew")

        self.incomming_tab_button = CTkButton(self.tabs_frame, text="In comming...", fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]),hover_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]))
        self.incomming_tab_button.grid(row=3, column=0, pady=10, sticky="ew")

        separator = CTkFrame(self.left_frame, height=2)
        separator.grid(row=3, column=0, padx=10, sticky="ew")

        self.disconect_button = CTkButton(self.left_frame, text="Disconnect", command=self.disconnect)
        self.disconect_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.show_dashboard_tab()
    
    def create_circular_image(self, input_path, output_path):
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size

        side = min(width, height)

        if width >= side:
            left = (width - side) // 2
        else:
            left = 0
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
        except:
            pass

        self.dashboard_tab_frame = CTkFrame(self, fg_color="transparent")
        self.dashboard_tab_frame.grid(row=0, column=1, padx=(0,10), pady=10, sticky="nsew")
        self.dashboard_tab_frame.grid_columnconfigure(1, weight=1)
        self.dashboard_tab_frame.grid_rowconfigure(0, weight=0)
        self.dashboard_tab_frame.grid_rowconfigure(1, weight=2)
        self.dashboard_tab_frame.grid_rowconfigure(2, weight=1)

        self.average_frame = CTkFrame(self.dashboard_tab_frame, corner_radius=6)
        self.average_frame.grid(row=0, column=0, padx=(0,10), pady=(0, 10), sticky="nsew")
        self.average_frame.grid_columnconfigure(0, weight=1)
        self.average_frame.grid_rowconfigure(1, weight=1)        

        notes = 0
        coefs = 0
        for p in range(len(list(self.pronote_client["periods"]))):
            for i in range(len(self.pronote_client["periods"][p]["grades"])):
                notes += self.pronote_client["periods"][p]["grades"][i]["value"] * self.pronote_client["periods"][p]["grades"][i]["coefficient"]
                coefs += self.pronote_client["periods"][p]["grades"][i]["coefficient"]
        self.general_average = notes/coefs

        trim_1_notes = 0
        trim_1_coefs = 0
        for i in range(len(self.pronote_client["periods"][0]["grades"])):
            trim_1_notes += self.pronote_client["periods"][0]["grades"][i]["value"] * self.pronote_client["periods"][0]["grades"][i]["coefficient"]
            trim_1_coefs += self.pronote_client["periods"][0]["grades"][i]["coefficient"]
        self.trim_1_average = trim_1_notes/trim_1_coefs

        trim_2_notes = 0
        trim_2_coefs = 0
        for i in range(len(self.pronote_client["periods"][1]["grades"])):
            trim_2_notes += self.pronote_client["periods"][1]["grades"][i]["value"] * self.pronote_client["periods"][1]["grades"][i]["coefficient"]
            trim_2_coefs += self.pronote_client["periods"][1]["grades"][i]["coefficient"]
        self.trim_2_average = trim_2_notes/trim_2_coefs

        trim_3_notes = 0
        trim_3_coefs = 0
        for i in range(len(self.pronote_client["periods"][2]["grades"])):
            trim_3_notes += self.pronote_client["periods"][2]["grades"][i]["value"] * self.pronote_client["periods"][2]["grades"][i]["coefficient"]
            trim_3_coefs += self.pronote_client["periods"][2]["grades"][i]["coefficient"]
        self.trim_3_average = trim_3_notes/trim_3_coefs

        self.notes_general_average_label = CTkLabel(self.average_frame, height=25, text=f"General Average : {round(self.general_average, 2)}/20", font=("Arial", 14), anchor='w')
        self.notes_general_average_label.grid(row=0, column=0, sticky='ew', padx=15, pady=(10,0))
        self.notes_general_average_trim_1_label = CTkLabel(self.average_frame, height=20, text=f"Trimestre 1 : {round(self.trim_1_average, 2)}/20", font=("Arial", 13, "italic"), text_color="gray", anchor='w')
        self.notes_general_average_trim_1_label.grid(row=1, column=0, sticky='ew', padx=20)
        self.notes_general_average_trim_2_label = CTkLabel(self.average_frame, height=20, text=f"Trimestre 2 : {round(self.trim_2_average, 2)}/20", font=("Arial", 13, "italic"), text_color="gray", anchor='w')
        self.notes_general_average_trim_2_label.grid(row=2, column=0, sticky='ew', padx=20)
        self.notes_general_average_trim_3_label = CTkLabel(self.average_frame, height=20, text=f"Trimestre 3 : {round(self.trim_3_average, 2)}/20", font=("Arial", 13, "italic"), text_color="gray", anchor='w')
        self.notes_general_average_trim_3_label.grid(row=3, column=0, sticky='ew', padx=20, pady=(0,10))

        self.lasts_notes_frame = CTkFrame(self.dashboard_tab_frame, corner_radius=6)
        self.lasts_notes_frame.grid(row=1, column=0, rowspan=2, padx=(0,10), sticky="nsew")
        self.lasts_notes_frame.grid_columnconfigure(0, weight=1)
        self.lasts_notes_frame.grid_rowconfigure(1, weight=1)        

        self.lasts_notes_label = CTkLabel(self.lasts_notes_frame, text="Lasts notes", font=("Arial", 14), anchor="w")
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
            note_frame.grid_propagate(False)
            note_frame.grid_columnconfigure(0, weight=1)
            note_frame.grid_rowconfigure(0, weight=1)

            subject_label = CTkLabel(note_frame, text=note['subject'], font=("Arial", 12), anchor="w")
            subject_label.grid(row=0, column=0, padx=10, sticky="ew")

            date_label = CTkLabel(note_frame, text=note['date'], font=("Arial", 12), anchor="w")
            date_label.grid(row=1, column=0, padx=10, sticky="ew")

            value_color = None
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
            value_label = CTkLabel(value_frame, text=f"{note['value']}/20", font=("Arial", 12), anchor="w")
            value_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
            value_color_frame = CTkFrame(value_frame, height=12, width=12,fg_color=value_color, corner_radius=6)
            value_color_frame.grid(row=0, column=1, sticky="ew")

        self.lasts_notes_list.grid_rowconfigure(0, weight=1)
        self.lasts_notes_list.grid_columnconfigure(0, weight=1)  

        self.radar_chart_frame = CTkFrame(self.dashboard_tab_frame, corner_radius=6)
        self.radar_chart_frame.grid(row=0, column=1, rowspan=2, padx=(0,10), sticky="nsew")
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

        self.radar_chart = CTkRadarChart(self.radar_chart_frame, labels=[label.split("<")[0].split(">")[0].strip() for label in labels], num_axes=len(labels))
        self.radar_chart.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.radar_chart.add_data("A", values, color="#03CB5D", fill=True)

        self.average_per_subject_frame = CTkFrame(self.dashboard_tab_frame, corner_radius=6)
        self.average_per_subject_frame.grid(row=2, column=1, padx=(0,10), pady=(10,0), sticky="nsew")
        self.average_per_subject_frame.grid_columnconfigure(0, weight=1)
        self.average_per_subject_frame.grid_rowconfigure(1, weight=1)

        self.average_per_subject_label = CTkLabel(self.average_per_subject_frame, text="Average per subject", font=("Arial", 14), anchor="w")
        self.average_per_subject_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.average_per_subject_list = CTkScrollableFrame(self.average_per_subject_frame, fg_color="transparent")
        self.average_per_subject_list.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.average_per_subject_list._scrollbar.grid_configure(padx=0)
        self.average_per_subject_list._scrollbar.configure(width=10)
        self.average_per_subject_list.grid_columnconfigure(0, weight=1)

        for i in range(len(labels)):
            subject_frame = CTkFrame(self.average_per_subject_list, height=42, corner_radius=6, fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]))
            subject_frame.pack(fill="x", pady=(0,10))
            subject_frame.grid_propagate(False)
            subject_frame.grid_columnconfigure(0, weight=1)
            subject_frame.grid_rowconfigure(0, weight=1)

            subject_label = CTkLabel(subject_frame, text=labels[i], font=("Arial", 12), anchor="w")
            subject_label.grid(row=0, column=0, padx=10, sticky="ew")

            value_color = None
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
            avg_label = CTkLabel(avg_frame, text=f"{subject_avg[labels[i]]:.2f}/20", font=("Arial", 12), anchor="w")
            avg_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
            avg_color_frame = CTkFrame(avg_frame, height=12, width=12,fg_color=value_color, corner_radius=6)
            avg_color_frame.grid(row=0, column=1, sticky="ew")

    def show_notes_tab(self):
        try:
            self.notes_dashboard_tab_frame.grid_forget()
            self.notes_graph_tab_frame.grid_forget()
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
 
        self.period_option_menu = CTkOptionMenu(self.notes_settings_frame, values=self.periods_list, command=self.notes_period_option_menu_callback)
        self.period_option_menu.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.subjects_list = list(set(grade["subject"] for grade in self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"]))

        self.notes_subjects_option_menu = CTkOptionMenu(self.notes_settings_frame, values=[subject.split("<")[0].split(">")[0].strip() for subject in self.subjects_list], command=self.notes_subjects_listbox_callback)
        self.notes_subjects_option_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))

        self.notes_list_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.notes_list_frame.grid(row=1, column=0, rowspan=2, sticky="nsew", pady=(10,0))
        self.notes_list_frame.grid_columnconfigure(0, weight=1)
        self.notes_list_frame.grid_rowconfigure(0, weight=1)

        self.notes_listbox = CTkScrollableFrame(self.notes_list_frame, fg_color="transparent")
        self.notes_listbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.notes_listbox._scrollbar.grid_configure(padx=0)
        self.notes_listbox._scrollbar.configure(width=10)
        self.notes_listbox.grid_columnconfigure(0, weight=1)

        self.notes_graph_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.notes_graph_frame.grid(row=0, column=1, rowspan=2, padx=(10,0), sticky="nsew")
        self.notes_graph_frame.grid_columnconfigure(0, weight=1)
        self.notes_graph_frame.grid_rowconfigure(0, weight=1)

        self.notes_list_info_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.notes_list_info_frame.grid(row=2, column=1, sticky="nsew", padx=(10,0), pady=(10,0))
        self.notes_list_info_frame.grid_columnconfigure(0, weight=1)
        self.notes_list_info_frame.grid_rowconfigure(0, weight=1)

        self.note_value_label = CTkLabel(self.notes_list_info_frame, height=20, text=f"", font=("Arial", 12), anchor='w')
        self.note_value_label.grid(row=0, column=0, sticky='ew', padx=20, pady=(10,0))

        self.note_subject_label = CTkLabel(self.notes_list_info_frame, height=20, text=f"", font=("Arial", 12), anchor='w')
        self.note_subject_label.grid(row=1, column=0, sticky='ew', padx=20)
        
        self.note_date_label = CTkLabel(self.notes_list_info_frame, height=20, text=f"", font=("Arial", 12), anchor='w')
        self.note_date_label.grid(row=2, column=0, sticky='ew', padx=20)

        self.note_period_label = CTkLabel(self.notes_list_info_frame, height=20, text=f"", font=("Arial", 12), anchor='w')
        self.note_period_label.grid(row=3, column=0, sticky='ew', padx=20, pady=(0,10))

        self.notes_period_option_menu_callback(self.period_option_menu.get())
        self.notes_graph_frame.bind("<Configure>", lambda event: self.update_graph())

    def notes_period_option_menu_callback(self, value):

        self.subjects_list = list(set(grade["subject"] for grade in self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"]))
        self.notes_subjects_option_menu.configure(values=[subject.split("<")[0].split(">")[0].strip() for subject in self.subjects_list])

        self.notes_subjects_option_menu.set(self.notes_subjects_option_menu._values[0])
        self.notes_subjects_listbox_callback(self.notes_subjects_option_menu._values[0])

    def notes_subjects_listbox_callback(self, x):
        
        for child in self.notes_listbox.winfo_children():
            child.pack_forget()

        self.update_graph()

        self.subjects_list = list(set(grade["subject"] for grade in self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"]))

        x = self.subjects_list[self.notes_subjects_option_menu._values.index(x)]

        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"])):
            if self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"] == x:
                subject_text = self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"].split("<")[0].split(">")[0].strip()
                note_frame = CTkFrame(self.notes_listbox, height=56, corner_radius=6, fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]))
                note_frame.pack(fill="x", pady=(0,10))
                note_frame.grid_propagate(False)
                note_frame.grid_columnconfigure(0, weight=1)
                note_frame.grid_rowconfigure(0, weight=1)

                subject_label = CTkLabel(note_frame, text=subject_text, font=("Arial", 12), anchor="w")
                subject_label.grid(row=0, column=0, padx=10, sticky="ew")

                date_label = CTkLabel(note_frame, text=f"{self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["date"]}", font=("Arial", 12), anchor="w")
                date_label.grid(row=1, column=0, padx=10, sticky="ew")

                value_color = None
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
                value_label = CTkLabel(value_frame, text=f"{self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"]:.2f}/20", font=("Arial", 12), anchor="w")
                value_label.grid(row=0, column=0, padx=(0, 10), sticky="ew")
                value_color_frame = CTkFrame(value_frame, height=12, width=12,fg_color=value_color, corner_radius=6)
                value_color_frame.grid(row=0, column=1, sticky="ew")

                note_frame.bind("<Enter>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"])))
                note_frame.bind("<Leave>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"])))
                note_frame.bind("<Button-1>", lambda event, x=f"{self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"]} : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["grade"]} / {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["out_of"]} | ({round(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"], 2)})": self.notes_listbox_callback(x))
                for child in note_frame.winfo_children():
                    child.bind("<Enter>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"])))
                    child.bind("<Leave>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"])))
                    child.bind("<Button-1>", lambda event, x=f"{self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"]} : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["grade"]} / {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["out_of"]} | ({round(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"], 2)})": self.notes_listbox_callback(x))
                    for child2 in child.winfo_children():
                        child2.bind("<Enter>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"])))
                        child2.bind("<Leave>", lambda event, note_frame=note_frame: note_frame.configure(fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"])))
                        child2.bind("<Button-1>", lambda event, x=f"{self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"]} : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["grade"]} / {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["out_of"]} | ({round(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"], 2)})": self.notes_listbox_callback(x))

    def notes_listbox_callback(self, x):
        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"])):
            if f"{self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"]} : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["grade"]} / {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["out_of"]} | ({round(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"], 2)})" == x:
                self.note_value_label.configure(text=f"Note : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["grade"]} / {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["out_of"]} | ({round(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"], 2)}/20)")
                self.note_subject_label.configure(text=f"Coefficient : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["coefficient"]}")
                self.note_date_label.configure(text=f"Date : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["date"]}")
                self.note_period_label.configure(text=f"Period : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["name"]}")

    def update_graph(self, val=None):
        try:
            self.notes_graph.grid_forget()
        except:
            pass
        
        x_val = []
        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"])):
            if self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"] == self.subjects_list[self.notes_subjects_option_menu._values.index(self.notes_subjects_option_menu.get())]:
                x_val.append(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["date"])

        width, height = self.get_size()

        self.notes_graph = tkc.LineChart(self.notes_graph_frame, width=width, height=height-50,
                                         x_axis_values=tuple(x_val), y_axis_values=(0, 20),
                                         x_axis_section_count=5, y_axis_section_count=8,
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
        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"])):
            if self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"] == self.subjects_list[self.notes_subjects_option_menu._values.index(self.notes_subjects_option_menu.get())]:
                y += 1
                notes_graph_list.append(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"])
                if y == 1:
                    notes_graph_list.append(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"])

        notes_average_graph = []
        notes = 0
        coefs = 0
        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"])):
            if self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"] == self.subjects_list[self.notes_subjects_option_menu._values.index(self.notes_subjects_option_menu.get())]:
                notes += self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"] * self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["coefficient"]
                coefs += self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["coefficient"]

        for i in range(len(notes_graph_list)):
            notes_average_graph.append(notes/coefs)

        self.notes_graph.show_data(self.note_average_line, notes_average_graph)
        self.notes_graph.show_data(self.note_line, notes_graph_list)
        

    def get_size(self):
        return self.notes_graph_frame.winfo_width(), self.notes_graph_frame.winfo_height()