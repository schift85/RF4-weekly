import customtkinter


class CustomApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry('1920x1080')
        self.clr1 = '#292929'
        self.clr2 = '#323332'
        self.create_widgets()

    def create_widgets(self):
        self.create_frames()
        self.create_top_frames()
        self.create_left_frames()
        self.app_title()

    def create_frames(self):
        self.top_frame = customtkinter.CTkFrame(self.master, height=80)
        self.top_frame.pack(pady=(20, 10), padx=30, side='top', fill='x')

        self.bottom_frame = customtkinter.CTkFrame(self.master, height=50, fg_color='blue')
        self.bottom_frame.pack(pady=(10, 20), padx=30, side='bottom', fill='x')

        self.left_frame = customtkinter.CTkFrame(self.master, width=500, fg_color='blue')
        self.left_frame.pack(padx=30, pady=10, side='left', fill='y')

        self.right_frame = customtkinter.CTkFrame(self.master, fg_color='blue')
        self.right_frame.pack(padx=(0, 30), pady=10, side='right', fill='both', expand=True)

    def create_top_frames(self):
        # frame for button refresh
        self.top_bt_frame = customtkinter.CTkFrame(self.top_frame, width=260, height=50, fg_color='red')
        self.top_bt_frame.pack(padx=20, pady=10, side='left')

        # frame for app title
        self.txt_frame = customtkinter.CTkFrame(self.top_frame, height=50)
        self.txt_frame.pack(padx=20, pady=10, side='left', fill='x', expand=True)

        # frame for last update datetime
        self.top_update_frame = customtkinter.CTkFrame(self.top_frame, width=260, height=50, fg_color='red')
        self.top_update_frame.pack(padx=20, pady=10, side='right')

    def create_left_frames(self):
        # buttons - rod type
        self.left_bt_frame_1 = customtkinter.CTkFrame(self.left_frame, width=460, height=60, fg_color='red')
        self.left_bt_frame_1.pack(padx=20, pady=10, side='top')

        # button select map
        self.left_bt_frame_2 = customtkinter.CTkFrame(self.left_frame, width=460, height=80, fg_color='red')
        self.left_bt_frame_2.pack(padx=20, pady=10, side='top')

        # map label for picture
        self.left_map_frame_2 = customtkinter.CTkLabel(self.left_frame, width=460, height=460, fg_color='red',
                                                       text='', corner_radius=5)
        self.left_map_frame_2.pack(padx=20, pady=(20, 10), side='top')

        # logo frame
        self.left_map_frame_3 = customtkinter.CTkLabel(self.left_frame, width=460, fg_color='red', text='',
                                                       corner_radius=5)
        self.left_map_frame_3.pack(padx=20, pady=(20, 10), side='bottom', fill='y')




## naplneni frames jednotlivyma objektama ...... tlacitka, texty, tabulka atd
    def app_title(self):
        self.app_title_text = customtkinter.CTkLabel(self.txt_frame, text='RF4 Weekly records', font=('Roboto', 24, 'bold'))
        self.app_title_text.pack(padx=30, pady=5, fill='x')


def main():
    root = customtkinter.CTk()
    app = CustomApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()