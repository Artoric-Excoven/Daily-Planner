import tkinter as tk
from tkinter import ttk
import math
import time
import datetime
import threading
import re
import queue

sanity = 100
coins = 100
tasks = 0
task_columns = 4

thread_event = {}
thread_object = {}

class Task_Frame(ttk.Frame):
    def __init__(self, master, task_id, added, **kwargs):
        super().__init__(master)

        if added == True:
            self.task_id = task_id
            self.add_time = 0
            # kwargs
            self.configure(style="task.TFrame")

            self.name_var = tk.StringVar(value=f"{task_id}")
            self.name_entry = ttk.Entry(self, textvariable=self.name_var, state="readonly", width=3, font=("Roboto", 20))
            self.name_entry.grid(row=0, column=0, columnspan=1, pady=2, sticky="e")

            # Initial length check
            title_text = kwargs["title"]
            desc_text = kwargs["desc"]
            title_text_length = len(title_text)
            desc_text_length = len(desc_text)
            text_list = [title_text_length, desc_text_length]

            box_height = max(text_list) // 6
            if box_height == 1:
                box_height = 0.5

            self.task_text_var = tk.Text(self, width=13, height = box_height)
            self.task_text_var.insert("1.0", title_text)
            self.task_text_var.config(state=tk.DISABLED, foreground="#ffffff", font=("Roboto", 20), background = "#7293c5")
            self.task_text_var.grid(row=0, column=1, columnspan=1, pady=2, sticky="e")

            self.task_desc_var = tk.Text(self, width=15, height = box_height)
            self.task_desc_var.insert("1.0", desc_text)
            self.task_desc_var.config(state=tk.DISABLED, foreground="#ffffff", font=("Roboto", 20), background = "#7293c5")
            self.task_desc_var.grid(row=0, column=2, columnspan=1, pady=2, sticky="e")

            deadline_text = kwargs["deadline"]
            self.task_deadline_var = tk.Text(self, width=10, height=box_height)
            if deadline_text[-1] == "m" or deadline_text[-1] == "M":
                if int(deadline_text[:-1]) <=60:
                    self.task_deadline_var.insert("1.0", f"{deadline_text[:-1]}m")
                else:
                    self.task_deadline_var.insert("1.0", f"{math.ceil(int(deadline_text[:-1])//60)}h")
            else:
                self.task_deadline_var.insert("1.0", f"{deadline_text[:-1]}h")
            
            self.task_deadline_var.config(state=tk.DISABLED, foreground="#ffffff", font=("Roboto", 20), background = "#7293c5")
            self.task_deadline_var.grid(row=0, column=3, columnspan=1, pady=2, sticky="e")

            diff_slider=kwargs["diff"]
            self.task_diff_var = tk.Text(self, width=12, height=box_height)
            self.task_diff_var.insert("1.0", diff_slider)
            self.task_diff_var.config(state=tk.DISABLED, foreground="#ffffff", font=("Roboto", 20), background = "#7293c5")
            self.task_diff_var.grid(row=0, column=4, columnspan=1, pady=2, sticky="e")

            def deadline_countdown(master):
                global sanity
                if deadline_text[-1] == "m" or deadline_text[-1] == "M":
                    if int(deadline_text[:-1]) <=60:
                        time_left_seconds = int(deadline_text[:-1]) * 60
                    else:
                        time_left_seconds = int(deadline_text[:-1]) * 60
                        current_hour =  math.ceil(int(deadline_text[:-1])//60)
                else:
                    time_left_seconds = int(deadline_text[:-1]) * 3600
                    current_hour = int(deadline_text[:-1])
                current_min = 60
                while time_left_seconds > 3600:
                    time.sleep(1)
                    time_left_seconds -= 1
                    time_left_hours = math.ceil(time_left_seconds/3600)
                    self.task_deadline_var.config(state=tk.NORMAL)
                    self.task_deadline_var.delete("1.0", "end-1c")
                    self.task_deadline_var.insert("1.0", f"{time_left_hours}h")
                    self.task_deadline_var.config(state=tk.DISABLED)

                    if self.add_time != 0:
                        time_left_seconds += self.add_time
                        self.add_time = 0
                        time_left_hours = math.ceil(time_left_seconds/3600)

                    if current_hour > time_left_hours:
                        self.task_deadline_var.config(state=tk.NORMAL)
                        self.task_deadline_var.delete("1.0", "end-1c")
                        self.task_deadline_var.insert("1.0", f"{time_left_hours}h")
                        self.task_deadline_var.config(state=tk.DISABLED)
                    current_hour = time_left_hours
                
                self.task_deadline_var.config(state=tk.NORMAL)
                self.task_deadline_var.delete("1.0", "end-1c")
                self.task_deadline_var.insert("1.0", f"{current_min}m")
                self.task_deadline_var.config(state=tk.DISABLED)

                while time_left_seconds <=3600:
                    time.sleep(1)
                    time_left_seconds -= 1
                    time_left_minutes = math.ceil(time_left_seconds/60)
                    if self.add_time != 0:
                        time_left_seconds += self.add_time
                        self.add_time = 0
                        time_left_minutes = math.ceil(time_left_seconds/60)
                        try:
                            self.task_deadline_var.config(state=tk.NORMAL)
                        except Exception as e:
                            print(e)
                        self.task_deadline_var.delete("1.0", "end-1c")
                        self.task_deadline_var.insert("1.0", f"{time_left_minutes}m")
                        self.task_deadline_var.config(state=tk.DISABLED)

                    if time_left_seconds < 1:
                        self.task_deadline_var.config(state=tk.NORMAL)
                        self.task_deadline_var.delete("1.0", "end-1c")
                        self.task_deadline_var.insert("1.0", f"TIMED OUT")
                        self.task_deadline_var.config(state=tk.DISABLED)

                        sanity -= int(diff_slider) * 5
                        print(f"Current sanity = {sanity}")
                        if sanity <= 0:
                            sanity=0

                            break
                        else:
                            break
                    
                    elif time_left_seconds < 60:
                        self.task_deadline_var.config(state=tk.NORMAL)
                        self.task_deadline_var.delete("1.0", "end-1c")
                        self.task_deadline_var.insert("1.0", f"{time_left_seconds}s")
                        self.task_deadline_var.config(state=tk.DISABLED)
                    elif current_min > time_left_minutes:
                        self.task_deadline_var.config(state=tk.NORMAL)
                        self.task_deadline_var.delete("1.0", "end-1c")
                        self.task_deadline_var.insert("1.0", f"{time_left_minutes}m")
                        self.task_deadline_var.config(state=tk.DISABLED)
                    current_min = time_left_minutes


            # thread
            thread_name = int(f"{task_id}")
            stop_thread_event = threading.Event()
            def threading_add():
                task_add_thread = threading.Thread(target=deadline_countdown, args=(stop_thread_event,), name=thread_name, daemon=True)

                global thread_event
                thread_event[thread_name] = stop_thread_event
                global thread_object
                thread_object[thread_name] = task_add_thread
                try:
                    task_add_thread.start()
                    return task_add_thread
                except Exception as e:
                    print(e)
                
            self.active_thread = threading_add()

        else:
            # title
            self.task_text_placeholder = tk.Label(
                root,
                text="[Task Title]",
                font= ("Saint", 25, "bold"),
                fg = "#1c5f40", bg = "#131516",
                relief=tk.FLAT,
                padx=10, pady=10
            )
            self.task_text_placeholder.pack(pady=5)
            self.task_text_placeholder.place(x=1050,y=200)
            
            self.task_text_input = tk.Text(root, width=100, height=5)
            self.task_text_input.pack(pady=5)
            self.task_text_input.place(x=1050, y=265)

            # desc
            self.task_desc_placeholder = tk.Label(
                root,
                text="[Task Description]",
                font= ("Saint", 25, "bold"),
                fg = "#1c5f40", bg = "#131516",
                relief=tk.FLAT,
                padx=10, pady=10
            )
            self.task_desc_placeholder.pack(pady=5)
            self.task_desc_placeholder.place(x=1050,y=350)

            self.task_desc_input = tk.Text(root, width=100, height=5)
            self.task_desc_input.pack(pady=5)
            self.task_desc_input.place(x=1050, y=415)

            # deadline
            possible_input = ["m", "M", "h", "H", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            possible_input_alpha_only = ["m", "M", "h", "H"]
            self.task_deadline_placeholder = tk.Label(
                root,
                text="[Deadline]",
                font= ("Saint", 25, "bold"),
                fg = "#1c5f40", bg = "#131516",
                relief=tk.FLAT,
                padx=10, pady=10
            )
            self.task_deadline_placeholder.pack(pady=5)
            self.task_deadline_placeholder.place(x=1050,y=500)

            self.task_deadline_input = tk.Text(root, width=100, height=5)
            self.task_deadline_input.pack(pady=5)
            self.task_deadline_input.place(x=1050, y=565)

            # slider
            self.task_diff_placeholder = tk.Label(
                root,
                text="[Difficulty]",
                font= ("Saint", 25, "bold"),
                fg = "#1c5f40", bg = "#131516",
                relief=tk.FLAT,
                padx=10, pady=10
            )
            self.task_diff_placeholder.pack(pady=5)
            self.task_diff_placeholder.place(x=1050,y=650)

            self.task_diff_slider_input = tk.Scale(
                root,
                from_=1,
                to=5,
                orient="horizontal",
            )
            self.task_diff_slider_input.pack(pady=5)
            self.task_diff_slider_input.place(x=1050, y=715)

            # confirmation
            conf_btn = tk.Button(root, text="Confirm Task")
            conf_btn.pack()
            conf_btn.place(x=1600, y=700)
            def wait_for_conf_btn():
                continuation_flag = tk.IntVar(value=0)
                conf_btn.config(command=lambda: continuation_flag.set(1))
                loop = True
                deadline_pattern = r"^[0-9]+[mMhH]$"
                while loop == True:
                    conf_btn.wait_variable(continuation_flag)
                    for i in self.task_deadline_input.get("1.0", "end-1c"):
                        if i not in possible_input:
                            print("Wrong character found!")
                        elif self.task_deadline_input.get("1.0", "end-1c")[-1] not in possible_input_alpha_only:
                            print("End with M/H !")
                        elif int(self.task_deadline_input.get("1.0", "end-1c")[:-1]) < 1:
                            print("Enter a number >=1 !")
                        elif bool(re.match(deadline_pattern, self.task_deadline_input.get("1.0", "end-1c"))) == True:
                            loop = False
                        else:
                            print("Enter a deadline!")
                
            
            wait_for_conf_btn()

            conf_btn.destroy()
            self.task_text_placeholder.destroy()
            self.task_desc_placeholder.destroy()
            self.task_deadline_placeholder.destroy()
            self.task_diff_placeholder.destroy()

            self.task_text_input_extract  = self.task_text_input.get("1.0", "end-1c")
            self.task_desc_input_extract  = self.task_desc_input.get("1.0", "end-1c")
            self.task_deadline_input_extract  = self.task_deadline_input.get("1.0", "end-1c")
            self.task_diff_slider_extract  = self.task_diff_slider_input.get()

            self.task_text_input.destroy()
            self.task_desc_input.destroy()
            self.task_deadline_input.destroy()
            self.task_diff_slider_input.destroy()


def WINDOW_CREATION():
    window = tk.Tk()
    window.geometry("1920x1080")
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    window.title("Frontline Focus")
    window.config(background="#2a2f33")

    Title_Label = tk.Label(
        window,
        text="Frontline Focus",
        font=("Saint", 25, "bold"),
        fg="#178578", bg="#2a2f33"
    )
    Title_Label.pack()

    Descriptor_Label_Title = tk.Label(
        window,
        text="TASK TITLE",
        font=("Roboto"),
        padx=20, pady=20,
        width=20,
        fg="#ffffff", bg="#263B74",
        relief="raised"
    )
    Descriptor_Label_Desc = tk.Label(
        window,
        text="DESCRIPTION",
        font=("Roboto"),
        padx=20, pady=20,
        width=23,
        fg="#ffffff", bg="#263B74",
        relief="raised"
    )
    Descriptor_Label_Deadline = tk.Label(
        window,
        text="DEADLINE",
        font=("Roboto"),
        padx=20, pady=20,
        fg="#ffffff", bg="#263B74",
        width=12,
        relief="raised"
    )
    Descriptor_Label_Diff = tk.Label(
        window,
        text="DIFFICULTY (CAT)",
        font=("Roboto"),
        padx=20, pady=20,
        fg="#ffffff", bg="#263B74",
        width=15,
        relief="raised"
    )

    Descriptor_Label_Title.place(x=1050,y=140)
    Descriptor_Label_Desc.place(x=1274,y=140)
    Descriptor_Label_Deadline.place(x=1506,y=140)
    Descriptor_Label_Diff.place(x=1657,y=140)

    # sanity bar backdrop
    sanity_backdrop = tk.Frame(window, background="#263B74", width=900, height=150)
    sanity_backdrop.pack_propagate(False)
    sanity_backdrop.place(x=10, y=700)

    sanity_text = tk.Label(
        sanity_backdrop,
        text="SANITY LEVEL",
        font=("Roboto", 25, "bold"),
        fg="#ffffff", bg="#263B74",
        padx=20, pady=20
    )
    sanity_text.pack(anchor="nw", padx=10)

    box_in_sanity_1 = tk.Frame(sanity_backdrop, bg="#ffffff", width=900, height=100)
    box_in_sanity_1.pack_propagate(False)
    box_in_sanity_1.pack(anchor="nw", padx=10, pady=15)

    box_in_sanity_2 = tk.Frame(box_in_sanity_1, bg="#1a1c2e", width=900, height=100)
    box_in_sanity_2.pack_propagate(False)
    box_in_sanity_2.pack(padx=3, pady=3)

    sanity_bar = tk.Frame(box_in_sanity_2, bg="#19ff4b", height=100, width=900)
    sanity_bar.place(x=0, y=0, height=100, width=900)

    sanity_percent = tk.Label(
        box_in_sanity_2,
        text="100%",
        font=("Roboto", 25, "bold"),
        fg="#19ff4b", bg="#263B74",
        padx=20, pady=20
    )
    sanity_percent.place(relx=0.5, rely=0.5, anchor="center")
    

    # coins box
    coins_backdrop = tk.Frame(window, background="#263B74", width=450, height=110)
    coins_backdrop.pack_propagate(False)
    coins_backdrop.place(x=10, y=860)

    coins_inner = tk.Frame(coins_backdrop, background="#1a1c2e", width=450, height=60)
    coins_inner.pack(fill="both", expand=True,padx=10, pady=10)

    coin_icon = tk.PhotoImage(file="coin.png")
    coin_img = tk.Label(coins_inner, image=coin_icon, bg="#1a1c2e")
    coin_img.image = coin_icon
    coin_img.pack(side="left", padx=10)

    coins_text = tk.Label(
        coins_inner,
        text=f"COINS: {coins}",
        font=("Roboto", 40, "bold"),
        fg="#ffffff", bg="#1a1c2e"
    )
    coins_text.pack(side="right", padx=10)

    # char images
    try:
        high_img = tk.PhotoImage(file="high_san.png")
        mid_img = tk.PhotoImage(file="mid_san.png")
        low_img = tk.PhotoImage(file="low_san.png")
        print("Images loaded successfully")
    except Exception as e:
        print("Image load error:", e)

    window.update_idletasks()
    san_img_frame = tk.Frame(window, background="#1a1c2e")
    san_img_frame.place(x=10, y=50,
                        width=sanity_backdrop.winfo_x() + sanity_backdrop.winfo_width()-10,
                        height=sanity_backdrop.winfo_y() - 50)

    san_img_label = tk.Label(san_img_frame, bg="#1a1c2e")
    san_img_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # time + countdown
    time_backdrop = tk.Frame(window, background="#263B74", width=440, height=110)
    time_backdrop.pack_propagate(False)
    time_backdrop.place(x=470, y=860)  # right of coin box (coin box at x=10, width=450)

    time_inner = tk.Frame(time_backdrop, background="#1a1c2e", width=440, height=110)
    time_inner.pack(fill="both", expand=True, padx=10, pady=10)

    current_time_label = tk.Label(
        time_inner,
        text="--:--:--",
        font=("Roboto", 30, "bold"),
        fg="#ffffff", bg="#1a1c2e"
    )
    current_time_label.pack(anchor="n")

    countdown_label = tk.Label(
        time_inner,
        text="24h:00m:00s",
        font=("Roboto", 25, "bold"),
        fg="#ffffff", bg="#1a1c2e"
    )
    countdown_label.pack(anchor="s", pady=5)


    def update_time_and_countdown():
        # current time
        now = datetime.datetime.now()
        current_time_label.config(text=now.strftime("%H:%M:%S"))

        # seconds till midnight
        tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        delta = tomorrow - now
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        countdown_label.config(text=f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s")

        window.after(1000, update_time_and_countdown)

    update_time_and_countdown()


    def update_san_img():
        global sanity
        if sanity >= 67:
            san_img_label.config(image=high_img)
            san_img_label.image = high_img
        elif sanity >= 33:
            san_img_label.config(image=mid_img)
            san_img_label.image = mid_img
        else:
            san_img_label.config(image=low_img)
            san_img_label.image = low_img
        window.after(200, update_san_img)

    update_san_img()


    def update_coins():
        global coins
        coins_text.config(text=f"COINS: {coins}")
        window.after(200, update_coins)

    update_coins()

        


    return window, sanity_bar, sanity_percent, box_in_sanity_2





class Adding_Configuration:
    def __init__(self, root, sanity_bar, sanity_percent, shared_queue, box_in_sanity_2):
        self.root = root
        self.sanity_bar = sanity_bar
        self.sanity_percent = sanity_percent
        self.shared_queue = shared_queue
        self.box_in_sanity_2 = box_in_sanity_2
        self.internal_sanity_thread()
        self.task_frames = {}

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TLabel", background="black", foreground="white",)
        style.configure("TButton", background="#83999C", foreground="#ffffff", font=("Roboto", 20),)
        style.configure("task.TFrame", background="#2a2f33",)

        self.grid_frame = ttk.Frame(self.root, style="task.TFrame")
        self.grid_frame.pack(padx=10, pady=10)
        self.grid_frame.place(x=885, y=200)

        self.grid_frame.columnconfigure(0, weight=0, minsize=90)   # narrow column for buttons
        self.grid_frame.columnconfigure(1, weight=1)               # wide column for tasks

        self.add_btn = ttk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_btn.pack(pady=5)
        self.add_btn.place(x=1690, y=90)

    def add_task(self):
        self.add_btn.pack_forget()
        self.add_btn.place_forget()

        if len(self.task_frames) == 0:
            task_id = 1
        else:
            task_id = max(self.task_frames) + 1
        print(f"task_id: {task_id}")

        added = False
        frame = Task_Frame(self.grid_frame, task_id, added)

        task_container = ttk.Frame(self.grid_frame, style="task.TFrame")
        task_container.grid(row=len(self.task_frames), column=0, columnspan=2, padx=5, pady=5, sticky="w")

        button_frame = ttk.Frame(task_container, style="task.TFrame")
        button_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        complete_btn = ttk.Button(button_frame, text="+", width=2,
                                command=lambda: [self.removal_update(task_id),
                                                self.add_coins(diff=frame.task_diff_slider_extract),
                                                self.add_sanity(diff=frame.task_diff_slider_extract),
                                                complete_btn.destroy(),
                                                add_time_btn.destroy(),
                                                remove_btn.destroy()])
        complete_btn.pack(side="left", padx=2)

        add_time_btn = ttk.Button(button_frame, text="1m", width=3,
                                command=lambda: self.add_time_func(frame_add))
        add_time_btn.pack(side="left", padx=2)

        remove_btn = ttk.Button(button_frame, text="-", width=2,
                                command=lambda: [self.removal_update(task_id),
                                                complete_btn.destroy(),
                                                add_time_btn.destroy(),
                                                remove_btn.destroy()])
        remove_btn.pack(side="left", padx=2)

        added = True
        frame_add = Task_Frame(task_container, task_id, added,
                            title=frame.task_text_input_extract,
                            desc=frame.task_desc_input_extract,
                            deadline=frame.task_deadline_input_extract,
                            diff=frame.task_diff_slider_extract)
        frame_add.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.task_frames[task_id] = task_container

        self.add_btn.pack(pady=5)
        self.add_btn.place(x=1690, y=90)


    def removal_update(self, task_id):
        global thread_event
        global thread_object

        if task_id in thread_object.keys():
            thread_event[task_id].set()
            if task_id in thread_object:
                del thread_object[task_id]
            del thread_event[task_id]
            print(f"Thread for task {task_id} removed")

        if task_id in self.task_frames:
            self.task_frames[task_id].destroy()
            del self.task_frames[task_id]
            print(f"UI for task {task_id} removed")

        for idx, container in enumerate(self.task_frames.values()):
            container.grid(row=idx, column=0, columnspan=2, padx=5, pady=5, sticky="w")




    def add_coins(self, **kwargs):
        global coins
        diff = kwargs["diff"]
        coins += diff
        print(f"Total coins: {coins}")

    def add_sanity(self, **kwargs):
        global sanity
        diff = kwargs["diff"]

        if sanity < 100:
            sanity += diff * 5
            if sanity >= 100:
                sanity = 100

            sanity_bar_width = sanity / 100 * self.box_in_sanity_2.winfo_width()
            self.sanity_bar.place_configure(width=sanity_bar_width)
            self.sanity_percent.config(text=f"{sanity}%")

            print("sanity bar changed (add)")
            print(f"[ADD] Sanity: {sanity}, Bar width set to: {sanity_bar_width}")
            print(f"Container width: {self.box_in_sanity_2.winfo_width()}, Bar width: {sanity_bar_width}")



    def add_time_func(self, task_frame):
        global coins
        if coins > 0:
            task_frame.add_time += 60   # increment this task’s add_time
            coins -= 1
            print(f"Added 1 min to Task {task_frame.task_id}, coins left: {coins}")


    def internal_sanity_thread(self):
        try:
            command = self.shared_queue.get_nowait()
            if command == "RUN_SANITY_REMOVAL":
                self.remove_sanity()
        except queue.Empty:
            pass

        self.root.after(100, self.internal_sanity_thread)

    
    def remove_sanity(self):
        global sanity
        sanity_bar_width = sanity / 100 * self.box_in_sanity_2.winfo_width()
        self.sanity_bar.place_configure(width=sanity_bar_width)
        self.sanity_percent.config(text=f"{sanity}%")

        print("sanity bar changed (remove)")
        print(f"[REMOVE] Sanity: {sanity}, Bar width set to: {sanity_bar_width}")
        print(f"Container width: {self.box_in_sanity_2.winfo_width()}, Bar width: {sanity_bar_width}")



def sanity_thread(comm_queue):
    global sanity
    read_sanity = sanity

    while True:
        time.sleep(0.1)
        if read_sanity != sanity:
            read_sanity = sanity
            comm_queue.put("RUN_SANITY_REMOVAL")



shared_queue = queue.Queue()
sanity_listener = threading.Thread(target=sanity_thread,args=(shared_queue,), daemon=True)
sanity_listener.start()

root, sanity_bar, sanity_percent, box_in_sanity_2 = WINDOW_CREATION()
app = Adding_Configuration(root, sanity_bar, sanity_percent, shared_queue, box_in_sanity_2)
app.root.mainloop()