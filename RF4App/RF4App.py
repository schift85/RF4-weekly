import customtkinter
from PIL import Image
import os
import tkinter as tk
from tkinter import ttk
import json
import sys
import subprocess
from datetime import datetime

class RF4App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.clr1 = '#292929'
        self.clr2 = '#323332'
        self.data_all = []
        # File path
        exe_path = os.path.abspath(sys.argv[0])
        self.dir_path = os.path.dirname(exe_path)
        self.geometry('1700x900')
        self.title('RF4 Weekly Records v1.01')
        self.resizable(width=False, height=False)
        customtkinter.set_appearance_mode('dark')

        self.regions_list = [('Internacional','GL'),
                             ('Other','EN'),
                             ('Germany','DE'),
                             ('USA','US'),
                             ('France','FR'),
                             ('China','CN'),
                             ('Poland','PL'),
                             ('Korea','KR'),
                             ('Russia','RU'),
                             ('Japan','JP'),
                             ('Spain','ES'),
                             ('Italy','IT')
                             ]

        self.sel_region = tk.StringVar()  # Add this line to define sel_region
        self.sel_region.set(self.regions_list[0][1])

        self.rod_types = ['records', 'ultralight', 'telestick']
        self.sel_rod_type = tk.StringVar()
        self.sel_rod_type.set(self.rod_types[0])

        self.rod_type_buttons = []

        self.last_modified_date = None

        self.create_widgets()
############ tohle je v nejakym divnym cyklu a uklada to buh vi kam ???? opravit scrapper !!!!!!!!
        self.check_files()

    def check_files(self):
        for reg_file in self.regions_list:
            for rod_type in self.rod_types:
                self.file_name_json = f'/data/d_{rod_type}_{reg_file[1]}.json'
                #self.ger_curr_file = os.path.join(self.dir_path, self.file_name_json)
                self.ger_curr_file = self.dir_path + f'/data/d_{rod_type}_{reg_file[1]}.json'
                if not os.path.exists(self.ger_curr_file):
                    self.reload_data()

    def setup_maps(self):
        self.map_list = ['Select Map', 'Mosquito Lake', 'Winding Rivulet', 'Old Burg Lake', 'Belaya River',
                         'Kuori Lake', 'Bear Lake', 'Volkhov River', 'Seversky Donnets River', 'Sura River',
                         'Ladoga Lake', 'The Amber Lake', 'Ladoga archipelago', 'Akhtuba River',
                         'Lower Tunguska River', 'Yama River', 'Norwegian Sea']
        self.map_dict = {}

        for map_name in self.map_list:
            self.map_dict[map_name] = customtkinter.CTkImage(Image.open(self.dir_path + f'/data/maps/{map_name}.png'), size=(450, 450))

    
    
    
    def reload_data(self):
        self.reload_app = self.dir_path + '/data/RF4Scraper.py'
        try:
            subprocess.call(['python', self.reload_app])
            self.get_last_modified_date()
            self.last_update_date.configure(text='Last update: ' + self.last_modified_date)
        except subprocess.CalledProcessError as e:
            print(f'Error: {e}')

    
    ''' def reload_data(self):
        self.reload_app = self.dir_path + '/data/RF4Scraper.exe'
        try:
            subprocess.run([self.reload_app], check=True)
            self.get_last_modified_date()
            self.last_update_date.configure(text='Last update: ' + self.last_modified_date)
        except subprocess.CalledProcessError as e:
            print(f'Error: {e}') '''





    def get_last_modified_date(self):
        try:
            last_modified_timestamp = os.path.getmtime(self.dir_path + f'/data/d_{self.sel_rod_type.get()}_{self.sel_region.get()}.json')
            self.last_modified_date = datetime.fromtimestamp(last_modified_timestamp)
            self.last_modified_date = self.last_modified_date.strftime('%d.%m.%Y %H:%M')
        except FileNotFoundError:
            print(f'The file {self.dir_path}/data/d_{self.sel_rod_type.get()}_{self.sel_region.get()}.json does not exist.')

        return self.last_modified_date

    def create_widgets(self):
        self.configure(bg=self.clr2)
        self.setup_maps()
        self.get_last_modified_date()

        self.sel_map = customtkinter.StringVar()
        self.sel_map.set(self.map_list[0])
        self.sel_url = customtkinter.StringVar()

        self.top_frame = customtkinter.CTkFrame(master=self, fg_color=self.clr1, height=80)
        self.top_frame.pack(padx=30, pady=(30, 15), side='top', fill='x')


        self.reload_btn = customtkinter.CTkButton(master=self.top_frame, text='Refresh data', command=self.reload_data)
        self.reload_btn.pack(padx=10, pady=10, side='right')
        self.last_update_date = customtkinter.CTkLabel(master=self.top_frame, text='Last database update: ' + self.last_modified_date, font=('Roboto', 16, 'bold'))
        self.last_update_date.pack(padx=10, pady=10, side='right')
        self.text_label = customtkinter.CTkLabel(master=self.top_frame, text='RF4 Weekly records', font=('Roboto', 24, 'bold'), anchor='center')
        self.text_label.pack(padx=10, pady=10,side='left', fill='x')

        self.left_frame = customtkinter.CTkFrame(master=self, fg_color=self.clr1, width=550)
        self.left_frame.pack(padx=(30, 15), pady=(0, 30), side='left', fill='y')
        self.left_frame.pack_propagate(0)

        # OptionMenu for selecting Map
        
        self.rods_frame = customtkinter.CTkFrame(master=self.left_frame )
        self.rods_frame.pack(side='top')

        for rod_type in self.rod_types:
            rod_button = customtkinter.CTkButton(master=self.rods_frame, text=rod_type, command=lambda r_type=rod_type: self.rod_type_selected(r_type))
            self.rod_type_buttons.append(rod_button)
            rod_button.pack(padx=10, pady=10, side='left')
        
        
        self.dropdown = customtkinter.CTkOptionMenu(master=self.left_frame, width=250, height=50, font=('Roboto', 16, 'bold'), anchor='center', values=self.map_list, variable=self.sel_map, command=self.map_selected)
        self.dropdown.pack(pady=(20, 50))
        self.map_image = customtkinter.CTkLabel(master=self.left_frame, text='')
        self.map_image.pack()
        self.logo = customtkinter.CTkLabel(master=self.left_frame, image=customtkinter.CTkImage(Image.open(self.dir_path + '/data/my_logo.png'), size=(100, 100)), text='')
        self.logo.pack(padx=15, pady=(15, 15), anchor='w', side='bottom')

        # Frame for URL buttons
        url_buttons_frame = customtkinter.CTkFrame(master=self, fg_color=self.clr1)
        url_buttons_frame.pack(padx=(15, 30), pady=(5, 20), side='top', fill='x')

        # Buttons for selecting URL
        url_buttons = []
        for file_name in ['Internacional', 'Russia', 'Germany', 'USA', 'France', 'China', 'Poland', 'Korea', 'Japan', 'Spain', 'Italy', 'Other Countries']:
            url_button = customtkinter.CTkButton(master=url_buttons_frame, text=file_name, command=lambda name=file_name: self.region_selected(name), width= 96)
            url_buttons.append(url_button)

        # Center the buttons horizontally
        for button in url_buttons:
            button.pack(side='left', padx=5, pady=10, fill='x')

        self.url_buttons = url_buttons

        self.right_frame = customtkinter.CTkFrame(master=self, fg_color=self.clr1)
        self.right_frame.pack(padx=(15, 30), pady=(0, 30), side='top', fill='both', expand=True)

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview.Heading', font=('Roboto', 16, 'bold'))
        self.style.configure('Treeview', background=self.clr1, fieldbackground=self.clr1, foreground='white', font=('Roboto', 12, 'bold'))

        self.scroll_bar = ttk.Scrollbar(self.right_frame)
        self.scroll_bar.pack(pady=(3, 3), side='right', fill='y')

        self.table = ttk.Treeview(self.right_frame, columns=('Fish_h', 'Weight_h', 'Location_h', 'Bait_h1', 'Bait_h2'), show='headings', yscrollcommand=self.scroll_bar.set)
        self.table.heading('Fish_h', text='Fish')
        self.table.heading('Weight_h', text='Weight')
        self.table.heading('Location_h', text='Location')
        self.table.heading('Bait_h1', text='Bait 1')
        self.table.heading('Bait_h2', text='Bait 2')
        self.table.pack(pady=(3, 3), fill='both', expand=True)
        for column in self.table["columns"]:
            self.table.column(column, anchor='w')
        self.scroll_bar.configure(command=self.table.yview)

        # Default file
        self.current_file = self.dir_path + '/data/d_records_GL.json'
        self.get_source_data(self.current_file)
        self.sort_data()

    def sort_data(self):
        self.data_all.sort(key=lambda x: (x[0], x[1]), reverse=True)
        data_rows = len(self.data_all)
        for j in range(0, data_rows):
            self.table.insert(parent='', index=0, values=self.data_all[j])

    def rod_type_selected(self, rod_type):
        self.sel_rod_type.set(rod_type)
        self.current_file = self.dir_path + f'/data/d_{rod_type}_{self.sel_region.get()}.json'
        self.refresh_data()

    def map_selected(self, e):
        map_name = self.sel_map.get()
        self.map_image.configure(image=self.map_dict[map_name])
        self.refresh_data()

    def filter_data(self, *args):
        selected_option = self.sel_map.get()
        if selected_option == self.map_list[0]:
            data_rows = len(self.data_all)
            for j in range(0, data_rows):
                self.table.insert(parent='', index=0, values=self.data_all[j])
        else:
            filtered_data = [item for item in self.data_all if selected_option.lower() in item[2].lower()]

            for row in self.table.get_children():
                self.table.delete(row)
            filtered_data.sort(key=lambda x: x[0], reverse=False)
            
            for item in filtered_data:
                self.table.insert('', 'end', values=item)

    def region_selected(self, file_name):
        for reg_sel in self.regions_list:
            if reg_sel[0] in file_name:
                selected_region = reg_sel[1]
                self.sel_region.set(selected_region)
                self.current_file = self.dir_path + f'/data/d_{self.sel_rod_type.get()}_{reg_sel[1]}.json'
        self.refresh_data()

    def get_source_data(self, file):
        try:
            json_file_path = file
            #print(f"Loading data from file: {json_file_path}")
            with open(json_file_path, 'r', encoding='utf-8') as file:
                self.data_all = json.load(file)
        except Exception as e:
            print(f"Error loading data: {e}")

    def refresh_data(self):
        self.data_all.clear()
        self.table.delete(*self.table.get_children())
        self.get_source_data(self.current_file)

        self.sort_data()

        data_rows = len(self.data_all)
        for j in range(0, data_rows):
            self.table.insert(parent='', index=0, values=self.data_all[j])

        self.filter_data()

if __name__ == "__main__":
    app = RF4App()
    app.mainloop()