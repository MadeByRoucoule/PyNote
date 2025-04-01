from customtkinter import *
from CTkListbox import *
import tkchart as tkc

class HomePage(CTk):
    def __init__(self, pronote_script, settings_script):
        super().__init__()

        self.title("Home Page")
        self.geometry("800x500")
        self.resizable(False, False)
        self.iconbitmap("src/assets/img/logo.ico")

        set_appearance_mode("system")
        set_default_color_theme("src/assets/json/themes/blue.json")

        self.pronote_script = pronote_script
        self.pronote_client = self.pronote_script.client_notes

        self.settings_script = settings_script

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

        self.account_name_label = CTkLabel(self.account_frame, text=self.pronote_script.client.info.name, font=("Arial", 12, "bold"))
        self.account_name_label.grid(row=0, column=0, sticky="ew")

        separator = CTkFrame(self.left_frame, height=2)
        separator.grid(row=1, column=0, padx=10, sticky="ew")

        self.tabs_frame = CTkFrame(self.left_frame, fg_color="transparent")
        self.tabs_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.tabs_frame.grid_columnconfigure(0, weight=1)
        self.tabs_frame.grid_rowconfigure(0, weight=1)
        self.tabs_frame.grid_rowconfigure(4, weight=1)

        self.notes_dashboard_tab_button = CTkButton(self.tabs_frame, 
                                          text="Notes Dashboard", 
                                          fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]),
                                          hover_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]),
                                          command=self.show_notes_dashboard_tab)
        self.notes_dashboard_tab_button.grid(row=1, column=0, pady=(10, 0), sticky="ew")

        self.notes_graph_tab_button = CTkButton(self.tabs_frame, 
                                          text="Notes Graph", 
                                          fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]),
                                          hover_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]),
                                          command=self.show_notes_graph_tab)
        self.notes_graph_tab_button.grid(row=2, column=0, pady=(10, 0), sticky="ew")

        self.incomming_tab_button = CTkButton(self.tabs_frame, text="In comming...", fg_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["top_fg_color"]),hover_color=self._apply_appearance_mode(ThemeManager.theme["CTkFrame"]["border_color"]))
        self.incomming_tab_button.grid(row=3, column=0, pady=10, sticky="ew")

        separator = CTkFrame(self.left_frame, height=2)
        separator.grid(row=3, column=0, padx=10, sticky="ew")

        self.disconect_button = CTkButton(self.left_frame, text="Disconnect", command=self.disconnect)
        self.disconect_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.show_notes_dashboard_tab()
    
    def disconnect(self):
        self.settings_script.reset_account()
        self.destroy()

    def show_notes_dashboard_tab(self):
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

        self.notes_general_average_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.notes_general_average_frame.grid(row=0, column=0, pady=(0,10), sticky="ew")
        
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

        self.notes_general_average_label = CTkLabel(self.notes_general_average_frame, height=25, text=f"General Average : {round(self.general_average, 2)}/20", anchor='w')
        self.notes_general_average_label.grid(row=0, column=0, sticky='ew', padx=10, pady=(10,0))
        self.notes_general_average_trim_1_label = CTkLabel(self.notes_general_average_frame, height=20, text=f"Trimestre 1 : {round(self.trim_1_average, 2)}/20", font=("Arial", 12, "italic"), text_color="gray", anchor='w')
        self.notes_general_average_trim_1_label.grid(row=1, column=0, sticky='ew', padx=20)
        self.notes_general_average_trim_2_label = CTkLabel(self.notes_general_average_frame, height=20, text=f"Trimestre 2 : {round(self.trim_2_average, 2)}/20", font=("Arial", 12, "italic"), text_color="gray", anchor='w')
        self.notes_general_average_trim_2_label.grid(row=2, column=0, sticky='ew', padx=20)
        self.notes_general_average_trim_3_label = CTkLabel(self.notes_general_average_frame, height=20, text=f"Trimestre 3 : {round(self.trim_3_average, 2)}/20", font=("Arial", 12, "italic"), text_color="gray", anchor='w')
        self.notes_general_average_trim_3_label.grid(row=3, column=0, sticky='ew', padx=20, pady=(0,10))

        self.notes_settings_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.notes_settings_frame.grid(row=1, column=0, rowspan=2, sticky="nsew")
        self.notes_settings_frame.grid_columnconfigure(0, weight=1)
        self.notes_settings_frame.grid_rowconfigure(0, weight=1)

        self.notes_subjects_listbox = CTkListbox(self.notes_settings_frame, corner_radius=6, command=self.notes_subjects_listbox_callback)
        self.notes_subjects_listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.period_option_menu = CTkOptionMenu(self.notes_settings_frame, values=self.periods_list, command=self.dashboard_period_option_menu_callback)
        self.period_option_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))

        self.subjects_list = list(set(grade["subject"] for grade in self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"]))
        for subject in self.subjects_list:
            self.notes_subjects_listbox.insert("end", subject)

        self.notes_list_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.notes_list_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(10,0))
        self.notes_list_frame.grid_columnconfigure(0, weight=1)
        self.notes_list_frame.grid_rowconfigure(0, weight=1)

        self.notes_list = CTkListbox(self.notes_list_frame, corner_radius=6, command=self.notes_listbox_callback)
        self.notes_list.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.notes_subjects_listbox_callback(self.notes_subjects_listbox.get(0))

        self.notes_list_info_frame = CTkFrame(self.notes_dashboard_tab_frame, corner_radius=6)
        self.notes_list_info_frame.grid(row=2, column=1, sticky="nsew", padx=(10,0), pady=(10,0))
        self.notes_list_info_frame.grid_columnconfigure(0, weight=1)
        self.notes_list_info_frame.grid_rowconfigure(0, weight=1)

        self.note_value_label = CTkLabel(self.notes_list_info_frame, height=20, text=f"Note : {20}", font=("Arial", 12), anchor='w')
        self.note_value_label.grid(row=0, column=0, sticky='ew', padx=20, pady=(10,0))

        self.note_subject_label = CTkLabel(self.notes_list_info_frame, height=20, text=f"Matière : {"Maths"}", font=("Arial", 12), anchor='w')
        self.note_subject_label.grid(row=1, column=0, sticky='ew', padx=20)
        
        self.note_date_label = CTkLabel(self.notes_list_info_frame, height=20, text=f"Date : {"01/01/2023"}", font=("Arial", 12), anchor='w')
        self.note_date_label.grid(row=2, column=0, sticky='ew', padx=20)

        self.note_period_label = CTkLabel(self.notes_list_info_frame, height=20, text=f"Period : Trimestre 1", font=("Arial", 12), anchor='w')
        self.note_period_label.grid(row=3, column=0, sticky='ew', padx=20, pady=(0,10))

    def dashboard_period_option_menu_callback(self, value):
        
        self.notes_subjects_listbox.delete(0, "end")
        self.subjects_list = list(set(grade["subject"] for grade in self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"]))

        for subject in self.subjects_list:
            self.notes_subjects_listbox.insert("end", subject)

        self.notes_subjects_listbox_callback(self.notes_subjects_listbox.get(0))

    def notes_subjects_listbox_callback(self, x):
        
        self.notes_list.delete(0, "end")

        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"])):
            if self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"] == x:
                self.notes_list.insert("end", f"{self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"]} : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["grade"]} / {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["out_of"]} | ({round(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"], 2)})")

    def notes_listbox_callback(self, x):
        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"])):
            if f"{self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"]} : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["grade"]} / {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["out_of"]} | ({round(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"], 2)})" == x:
                self.note_value_label.configure(text=f"Note : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["grade"]} / {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["out_of"]} | ({round(self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["value"], 2)})")
                self.note_subject_label.configure(text=f"Matière : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["subject"]}")
                self.note_date_label.configure(text=f"Date : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["grades"][i]["date"]}")
                self.note_period_label.configure(text=f"Period : {self.pronote_client["periods"][self.periods_list.index(self.period_option_menu.get())]["name"]}")

    def show_notes_graph_tab(self):
        try:
            self.notes_dashboard_tab_frame.grid_forget()
            self.notes_graph_tab_frame.grid_forget()
        except:
            pass

        self.notes_graph_tab_frame = CTkFrame(self, fg_color="transparent")
        self.notes_graph_tab_frame.grid(row=0, column=1, padx=(0,10), pady=10, sticky="nsew")
        self.notes_graph_tab_frame.grid_columnconfigure(0, weight=1)
        self.notes_graph_tab_frame.grid_rowconfigure(0, weight=1)

        self.notes_settings_frame = CTkFrame(self.notes_graph_tab_frame, corner_radius=6)
        self.notes_settings_frame.grid(row=1, column=0, sticky="ew")
        self.notes_settings_frame.grid_columnconfigure(0, weight=1)

        periods = [self.pronote_client["periods"][i]["name"] for i in range(len(self.pronote_client["periods"]))]
        subjects = list(set(grade["subject"] for grade in self.pronote_client["periods"][periods.index(self.period_option_menu.get())]["grades"]))

        self.subjects_option_menu = CTkOptionMenu(self.notes_settings_frame, values=subjects, command=self.update_graph)
        self.subjects_option_menu.grid(row=0, column=1, padx=5, pady=10)

        self.graph_period_option_menu = CTkOptionMenu(self.notes_settings_frame, values=periods, command=self.graph_period_option_menu_callback)
        self.graph_period_option_menu.grid(row=0, column=2, padx=(10,5), pady=10)

        self.update_graph()

    def update_graph(self, val=None):
        try: 
            self.notes_graph_frame.grid_forget()
        except : pass

        self.notes_graph_frame = CTkFrame(self.notes_graph_tab_frame, corner_radius=6)
        self.notes_graph_frame.grid(row=0, column=0, pady=(0,10), sticky="nsew")

        x_val = []
        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"])):
            if self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"][i]["subject"] == self.subjects_option_menu.get():
                x_val.append(self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"][i]["date"])

        self.notes_graph = tkc.LineChart(self.notes_graph_frame, width=701, height=515, 
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
        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"])):
            if self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"][i]["subject"] == self.subjects_option_menu.get():
                y += 1
                notes_graph_list.append(self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"][i]["value"])
                if y == 1:
                    notes_graph_list.append(self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"][i]["value"])

        notes_average_graph = []
        notes = 0
        coefs = 0
        for i in range(len(self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"])):
            if self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"][i]["subject"] == self.subjects_option_menu.get():
                notes += self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"][i]["value"] * self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"][i]["coefficient"]
                coefs += self.pronote_client["periods"][self.periods_list.index(self.graph_period_option_menu.get())]["grades"][i]["coefficient"]

        for i in range(len(notes_graph_list)):
            notes_average_graph.append(notes/coefs)

        self.notes_graph.show_data(self.note_average_line, notes_average_graph)
        self.notes_graph.show_data(self.note_line, notes_graph_list)


    def graph_period_option_menu_callback(self, value):
        periods = [self.pronote_client["periods"][i]["name"] for i in range(len(self.pronote_client["periods"]))]
        subjects = list(set(grade["subject"] for grade in self.pronote_client["periods"][periods.index(self.period_option_menu.get())]["grades"]))

        self.subjects_option_menu.configure(values=subjects)

        self.update_graph()