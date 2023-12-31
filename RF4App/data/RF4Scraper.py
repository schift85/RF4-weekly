import os
from bs4 import BeautifulSoup
import requests
import json
import threading
from queue import Queue, Empty
import customtkinter
import sys

class RF4ScraperApp:
    def __init__(self, master, width=600, height=200):
        self.master = master
        self.width = width
        self.height = height
        
        # File path
        if getattr(sys, 'frozen', False):
            self.dir_path = os.path.dirname(sys.executable)
        elif __file__:
            self.dir_path = os.path.dirname(os.path.realpath(__file__))
        
        self.dots_count = 0

        # List of regions
        self.regs = [
            ('Internacional', 'GL/'), 
            ('Russia', 'RU/'), 
            ('Germany', 'DE/'), 
            ('USA', 'US/'), 
            ('France', 'FR/'), 
            ('China', 'CN/'), 
            ('Poland', 'PL/'), 
            ('Korea', 'KR/'), 
            ('Japan', 'JP/'), 
            ('Spain', 'ES/'), 
            ('Italy', 'IT/'), 
            ('Other', 'EN/'), 
        ]
        # List of rod type
        self.list_type_rod = ['records', 'ultralight', 'telestick']

        # GUI Setup
        self.setup_gui()
        
        # Start the dot animation
        self.animate_dots()

        # After 2 seconds, start the scraping loop in the background
        self.master.after(2000, self.scrape_in_background, Queue())

    # GUI
    def setup_gui(self):
        self.master.geometry(f'{self.width}x{self.height}')
        self.master.title('RF4 : Weekly Records')
        self.master.resizable(width=False, height=False)
        customtkinter.set_appearance_mode('dark')

        self.top_frame = customtkinter.CTkFrame(master=self.master, fg_color='#292929', height=180, width=480)
        self.top_frame.pack(padx=20, pady=20, fill='both')

        self.text_label1 = customtkinter.CTkLabel(master=self.top_frame, text='Downloading data', font=('Roboto', 24, 'bold'))
        self.text_label1.pack(padx=20, pady=(20, 10), fill='x')
        self.text_label2 = customtkinter.CTkLabel(master=self.top_frame, text='Please wait', font=('Roboto', 24, 'bold'))
        self.text_label2.pack(padx=20, pady=(10, 10), fill='x')
        self.text_label3 = customtkinter.CTkLabel(master=self.top_frame, text='......', font=('Roboto', 24, 'bold'))
        self.text_label3.pack(padx=20, pady=(10, 20), fill='x')
    # dots animation
    def animate_dots(self):
        self.dots_count = (self.dots_count + 1) % 20
        self.text_label3.configure(text=f'{"." * self.dots_count}')
        self.master.after(500, self.animate_dots)

    # scraping part
    def scrape_and_close(self, queue):
        for rod_type in self.list_type_rod:
            self.url_g = f'https://rf4game.com/{rod_type}/weekly/region/'
            for i in range(len(self.regs)):
                region = self.regs[i][1]
                url = self.url_g + region
                result = requests.get(url)
                doc = BeautifulSoup(result.text, 'html.parser')
                records = doc.find_all('div', 'rows')
                data_all = []
                for record in records:
                    radek = record.find_all('div', class_='records_subtable flex_table')
                    for polozka in radek:
                        try:
                            ryba = polozka.find('div', class_='text').text
                            vaha1 = polozka.find('div', class_='col overflow nowrap weight').text
                            lokace = polozka.find('div', class_='col overflow nowrap location').text
                            bait = polozka.find('div', class_='bait_icon').get('title')
                        except:
                            ryba = '----'
                            vaha1 = '----'
                            lokace = '----'
                            bait = '----'
                            icon_link = '----'
                        if '----' not in ryba:
                            data1 = (ryba, vaha1, lokace,)
                            if ';' in bait:
                                bait_x1 = bait.split('; ')
                                data1 = (ryba, vaha1, lokace, bait_x1[0], bait_x1[1])
                            else:
                                data1 = (ryba, vaha1, lokace, bait, '')
                            data_all.append(data1)
                            for i in range(0, 4):
                                try:
                                    vaha2 = (polozka.find_all(id='-0-1'))[i].text
                                    lokace2 = (polozka.find_all(id='-0-2'))[i].text
                                    bait2 = (polozka.find_all('div', class_='bait_icon'))[i + 1].get('title')
                                except:
                                    vaha2 = '----'
                                    lokace2 = '----'
                                    bait2 = '----'
                                if '----' not in vaha2:
                                    data2 = (ryba, vaha2, lokace2,)
                                    if ';' in bait2:
                                        bait_x2 = bait2.split('; ')
                                        data2 = (ryba, vaha2, lokace2, bait_x2[0], bait_x2[1])
                                    else:
                                        data2 = (ryba, vaha2, lokace2, bait2, '')
                                    data_all.append(data2)

                file_path = os.path.join(self.dir_path , f'd_{rod_type}_{region.rstrip("/").replace("/", "_")}.json')
                print(file_path)

                # Check if the file exists
                if os.path.exists(file_path):
                    os.remove(file_path)

                # Write data to JSON file in the specified folder
                with open(file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data_all, json_file, ensure_ascii=False, indent=2)

        # Enqueue a message to indicate that scraping is complete
        queue.put("Scraping complete")

    # check if scraping is complete
    def check_scraping_complete(self, queue):
        try:
            message = queue.get_nowait()
            if message == "Scraping complete":
                self.master.quit()
        except Empty:
            self.master.after(100, self.check_scraping_complete, queue)

    # scraping on background while running gui - prevent gui lags
    def scrape_in_background(self, queue):
        scrape_thread = threading.Thread(target=self.scrape_and_close, args=(queue,))
        scrape_thread.start()

        # Check if scraping is complete periodically
        self.master.after(100, self.check_scraping_complete, queue)

if __name__ == "__main__":
    app = customtkinter.CTk()
    RF4ScraperApp(app)
    app.mainloop()