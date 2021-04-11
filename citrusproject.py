from pywinauto import Desktop
from datetime import datetime, timedelta
import time

import tkinter
import tkinter.font


class CitrusProject:
    def __init__(self):
        self.app_dict = {}
        self.snooze_duration = timedelta(minutes=10)

    def update_app_list(self):
        windows = Desktop(backend="uia").windows()
        current_list = []
        for w in windows:
            window_name = w.window_text().split('-')[-1].strip()
            if window_name not in {'', 'Taskbar', 'Program Manager', 'Citri'}:
                current_list.append(window_name)

        if not self.app_dict:
            for n in current_list:
                self.app_dict[n] = [datetime.now() + timedelta(hours=1), 1]
        else:
            for n in current_list:
                if n not in self.app_dict:
                    self.app_dict[n] = [datetime.now() + timedelta(hours=1), 1]
        self.remove_apps(current_list)

    def remove_apps(self, current_list):
        app_dict_keys = list(self.app_dict.keys())
        for app in app_dict_keys:
            if app not in current_list:
                del self.app_dict[app]

    def set_time(self, app_name, end_time):
        if app_name not in self.app_dict.keys():
            return False
        self.app_dict[app_name][0] = end_time
        return True

    def check_finished(self):
        finished = []
        for app_name, time_info in self.app_dict.items():
            if time_info[0] <= datetime.now() and time_info[1] > 0:
                finished.append(app_name)
        return finished

    def set_snooze(self, td):
        self.snooze_duration = td

    def snooze(self, app_name):
        if app_name not in self.app_dict.keys():
            return False
        self.app_dict[app_name][0] = datetime.now() + self.snooze_duration
        self.app_dict[app_name][1] += 1
        return True


class RootWindow(tkinter.Frame):
    def __init__(self, master, cp):
        tkinter.Frame.__init__(self, master)
        self.cp = cp
        self.master = master
        self.master.title('Set Time - Citri')
        self.master.geometry('400x600')
        self.master.resizable(False, False)

        def_font = tkinter.font.nametofont("TkDefaultFont")
        def_font.config(size=14)

        self.app_list_label = tkinter.Label(self.master, text='List of Applications')
        self.app_list_label.place(x=5, y=5)
        self.app_list = tkinter.Text(self.master)
        self.app_list.place(x=5, y=35, width=390, height=200)

        self.input_label = tkinter.Label(self.master, text='Name of Application')
        self.input_label.place(x=5, y=250)
        self.input = tkinter.Entry(self.master)
        self.input.place(x=5, y=280, width=390, height=20)  

        self.radiovar = tkinter.IntVar()

        self.radio1 = tkinter.Radiobutton(self.master, text='How long from now: ', variable=self.radiovar, value=1)
        self.radio1.place(x=5, y=320)
        self.radio1_h = tkinter.Entry(self.master)
        self.radio1_h.place(x=230, y=330, width=20, height=20)
        self.radio1_h_label = tkinter.Label(self.master, text='h') 
        self.radio1_h_label.place(x=250, y=325)
        self.radio1_m = tkinter.Entry(self.master)
        self.radio1_m.place(x=280, y=330, width=20, height=20)
        self.radio1_m_label = tkinter.Label(self.master, text='m') 
        self.radio1_m_label.place(x=300, y=325)
        self.radio1_s = tkinter.Entry(self.master)
        self.radio1_s.place(x=330, y=330, width=20, height=20)
        self.radio1_s_label = tkinter.Label(self.master, text='s') 
        self.radio1_s_label.place(x=350, y=325)
        
        self.radio2 = tkinter.Radiobutton(self.master, text='Set (Military) time: ', variable=self.radiovar, value=2)
        self.radio2.place(x=5, y=350)
        self.radio2_h_label = tkinter.Label(self.master, text='h')
        self.radio2_h_label.place(x=250, y=360)
        self.radio2_h = tkinter.Entry(self.master)
        self.radio2_h.place(x=230, y=365, width=20, height=20)
        self.radio2_h_label = tkinter.Label(self.master, text='h') 
        self.radio2_h_label.place(x=250, y=360)
        self.radio2_m = tkinter.Entry(self.master)
        self.radio2_m.place(x=280, y=365, width=20, height=20)
        self.radio2_m_label = tkinter.Label(self.master, text='m') 
        self.radio2_m_label.place(x=300, y=360)
        self.radio2_s = tkinter.Entry(self.master)
        self.radio2_s.place(x=330, y=365, width=20, height=20)
        self.radio2_s_label = tkinter.Label(self.master, text='s') 
        self.radio2_s_label.place(x=350, y=360)

        self.radio3 = tkinter.Radiobutton(self.master, text='Disable', variable=self.radiovar, value=3)
        self.radio3.place(x=5, y=380)

        self.uwu = tkinter.Button(self.master, text='Save', command=self.save)
        self.uwu.place(x=300, y=400)

        self.owo_h_label = tkinter.Label(self.master, text='h')
        self.owo_h_label.place(x=250, y=470)
        self.owo_h = tkinter.Entry(self.master)
        self.owo_h.place(x=230, y=475, width=20, height=20)
        self.owo_h_label = tkinter.Label(self.master, text='h') 
        self.owo_h_label.place(x=250, y=470)
        self.owo_m = tkinter.Entry(self.master)
        self.owo_m.place(x=280, y=475, width=20, height=20)
        self.owo_m_label = tkinter.Label(self.master, text='m') 
        self.owo_m_label.place(x=300, y=470)
        self.owo_s = tkinter.Entry(self.master)
        self.owo_s.place(x=330, y=475, width=20, height=20)
        self.owo_s_label = tkinter.Label(self.master, text='s') 
        self.owo_s_label.place(x=350, y=470)
        self.owo = tkinter.Button(self.master, text='Set Snooze', command=self.snooze)
        self.owo.place(x=250, y=500)

        self.image = tkinter.PhotoImage(file='citri_idle.png').subsample(2, 2)
        self.citri_image = tkinter.Button(self.master, image=self.image, borderwidth=0, command=self.pet)
        self.citri_image.place(x=15, y=430)

        self.citri_says = tkinter.Label(self.master, text='You can set my reminders here!')
        self.citri_says.place(x=5, y=565)

        self.update()

    def update(self):
        cp.update_app_list()
        app_list_text = ""
        for a, t in cp.app_dict.items():
            app_list_text += (a + '\n')
        self.set_app_list_text(app_list_text)
        if cp.check_finished():
            for app_name in cp.check_finished():
                self.popup(app_name)
        self.after(1000, self.update)

    def set_app_list_text(self, text):
        self.app_list.delete(1.0, 'end')
        self.app_list.insert(1.0, text)

    def popup(self, app_name):
        Popup(self, app_name, cp)

    def save(self):
        findApps = self.input.get()
        if findApps not in cp.app_dict.keys():
            self.sad()
            self.citri_says.config(text="Please input a valid application...")
        elif self.radiovar.get() not in {1, 2, 3}:
            self.sad()
            self.citri_says.config(text="You need to select an option...")
        else:
            if self.radiovar.get() == 1: ##timer
                try:
                    if not self.radio1_h.get():
                        hour = 0
                    else:
                        hour = int(self.radio1_h.get())
                    if not self.radio1_m.get():
                        minute = 0
                    else:
                        minute = int(self.radio1_m.get())
                    if not self.radio1_s.get():
                        sec = 0
                    else:
                        sec = int(self.radio1_s.get())

                    if hour < 0 or minute not in range(0, 60) or sec not in range(0, 60):
                        self.sad()
                        self.citri_says.config(text="Sorry but that time is invalid...")
                    else:
                        cp.app_dict[findApps] = [datetime.now() + timedelta(hours=hour, minutes=minute, seconds=sec), 1]

                except ValueError:
                    self.sad()
                    self.citri_says.config(text="Sorry but that time is invalid...")
           
            elif self.radiovar.get() == 2: ##actual time
                try:
                    if not self.radio2_h.get():
                        hour = 0
                    else:
                        hour = int(self.radio2_h.get())
                    if not self.radio2_m.get():
                        minute = 0
                    else:
                        minute = int(self.radio2_m.get())
                    if not self.radio2_s.get():
                        sec = 0
                    else:
                        sec = int(self.radio2_s.get())

                    if hour not in range(0, 24) or minute not in range(0, 60) or sec not in range(0, 60):
                        self.sad()
                        self.citri_says.config(text="Sorry but that time is invalid...")
                    else:
                        new_time = datetime.now()
                        new_time = new_time.replace(hour=hour, minute=minute, second=sec)
                        if new_time < datetime.now():
                            new_time += timedelta(days=1)
                        cp.app_dict[findApps] = [new_time, 1]

                except ValueError:
                    self.sad()
                    self.citri_says.config(text="Sorry but that time is invalid...")

            elif self.radiovar.get() == 3:
                cp.app_dict[findApps][1] = 0

    def snooze(self):
        try:
            if not self.owo_h.get():
                hour = 0
            else:
                hour = int(self.owo_h.get())
            if not self.owo_m.get():
                minute = 0
            else:
                minute = int(self.owo_m.get())
            if not self.owo_s.get():
                sec = 0
            else:
                sec = int(self.owo_s.get())

            if hour not in range(0, 24) or minute not in range(0, 60) or sec not in range(0, 60):
                self.sad()
                self.citri_says.config(text="Sorry but that time is invalid...")
            else:
                cp.set_snooze(timedelta(hours=hour, minutes=minute, seconds=sec))

        except ValueError:
            self.sad()
            self.citri_says.config(text="Sorry but that time is invalid...")
    
    def idle(self):
        self.image = tkinter.PhotoImage(file='citri_idle.png').subsample(2, 2)
        self.citri_image = tkinter.Button(self.master, image=self.image, borderwidth=0, command=self.pet)
        self.citri_image.place(x=15, y=430)

    def pet(self):
        self.image = tkinter.PhotoImage(file='citri_joy.png').subsample(2, 2)
        self.citri_image = tkinter.Button(self.master, image=self.image, borderwidth=0)
        self.citri_image.place(x=15, y=430)
    
    def sad(self):
        self.image = tkinter.PhotoImage(file='citri_sad.png').subsample(2, 2)
        self.citri_image = tkinter.Button(self.master, image=self.image, borderwidth=0, command=self.idle)
        self.citri_image.place(x=15, y=430)

class Popup(tkinter.Toplevel):
    def __init__(self, master, app_name, cp):
        tkinter.Toplevel.__init__(self, master)
        self.app_name = app_name
        self.cp = cp

        self.title('Citri')
        width = 800
        height = 300
        x = int((self.winfo_screenwidth() / 2) - (width / 2))
        y = int((self.winfo_screenheight() / 2) - (height / 2))
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.attributes("-topmost", True)
        self.resizable(False, False)

        self.image = tkinter.PhotoImage(file='citri_idle.png')

        self.textLabel = tkinter.Label(self,
                                  text=f"Hey, you've been using {app_name} for a while, maybe you should take a break and drink some water!",
                                  wraplength=460)
        if cp.app_dict[app_name][1] == 3:
            self.textLabel = tkinter.Label(self,
                                      text=f"I see you've been delaying taking a break from {app_name} twice now. Maybe go outside for a bit!",
                                      wraplength=460)
        if cp.app_dict[app_name][1] == 4:
            self.textLabel = tkinter.Label(self,
                                      text=f"Alright, I think it's really time for you to take a break from {app_name} now. Why don't you give yourself a five minute break?",
                                      wraplength=460)
            self.image = tkinter.PhotoImage(file='citri_sad.png')
        if cp.app_dict[app_name][1] >= 5:
            self.textLabel = tkinter.Label(self,
                                      text=f"HEY! Are you just brushing me off??",
                                      wraplength=460)
            self.image = tkinter.PhotoImage(file='citri_angry.png')

        self.citriLabel = tkinter.Button(self, image=self.image, command=self.pet, 
                                    borderwidth=0)

        self.opt1Button = tkinter.Button(self, text='OK Citri!', command=self.close_ok, padx=20)
        self.opt2Button = tkinter.Button(self, text='Remind me later Citri!', command=self.close_snooze, padx=20)

        self.citriLabel.grid(row=0, column=0, padx=10, pady=10, rowspan=2)
        self.textLabel.grid(row=0, column=1, columnspan=2)
        self.opt1Button.grid(row=1, column=1, padx=10)
        self.opt2Button.grid(row=1, column=2, padx=10)

        self.protocol("WM_DELETE_WINDOW", self.close_ok)
        self.transient(master)
        self.grab_set()
        master.wait_window(self)
    
    def close_ok(self):
        cp.app_dict[self.app_name][1] = 0
        self.destroy()

    def close_snooze(self):
        cp.snooze(self.app_name)
        self.destroy()
    
    def pet(self):
        self.image = tkinter.PhotoImage(file='citri_joy.png')
        self.citriLabel = tkinter.Button(self, image=self.image, command=self.pet, 
                                    borderwidth=0)
        self.citriLabel.grid(row=0, column=0, padx=10, pady=10, rowspan=2)


if __name__ == '__main__':
    cp = CitrusProject()

    cp.update_app_list()
    
    # print(cp.set_time('Visual Studio Code', datetime.now() + timedelta(seconds=2)))

    root = tkinter.Tk()
    rw = RootWindow(root, cp)
    root.mainloop()
