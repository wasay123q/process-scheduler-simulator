import customtkinter as ctk
from tkinter import ttk

class Dashboard(ctk.CTk):
    def __init__(self, start_callback):
        super().__init__()
        self.start_callback = start_callback
        self.process_list = [] 

        # 1. Window Setup (Dark Theme)
        self.title("Process Scheduler // v2.0")
        self.geometry("1200x800")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue") # Standard base, we override manually
        
        # Background color for the whole app
        self.configure(fg_color="#0f0f0f")

        # Fonts
        self.font_header = ctk.CTkFont(family="Roboto", size=24, weight="bold")
        self.font_sub = ctk.CTkFont(family="Roboto", size=14)
        self.font_mono = ctk.CTkFont(family="Consolas", size=12)

        # Layout Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(1, weight=1)

        # --- HEADER ---
        self.header = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="#1a1a1a")
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        ctk.CTkLabel(self.header, text="PROCESS SCHEDULING VISUALIZER", font=self.font_header, text_color="#ffffff").pack(side="left", padx=20, pady=15)
        ctk.CTkLabel(self.header, text="STATUS: READY", text_color="#00ff9f", font=self.font_mono).pack(side="right", padx=20)

        # --- LEFT PANEL (Control Deck) ---
        self.controls = ctk.CTkFrame(self, corner_radius=15, fg_color="#1e1e1e")
        self.controls.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        ctk.CTkLabel(self.controls, text="CONFIGURATION", font=("Arial", 12, "bold"), text_color="#888888").pack(pady=(20, 10), anchor="w", padx=20)

        # Algorithm Selector
        self.algo_var = ctk.StringVar(value="FCFS")
        self.algo_menu = ctk.CTkOptionMenu(self.controls, variable=self.algo_var, 
                                           values=["FCFS", "SJF", "Priority", "RR"],
                                           fg_color="#2b2b2b", button_color="#3a3a3a",
                                           text_color="white", width=200, height=40)
        self.algo_menu.pack(pady=10)
        
        self.quantum_entry = ctk.CTkEntry(self.controls, placeholder_text="Quantum (RR)", width=200, fg_color="#2b2b2b", border_width=0)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.pack(pady=5)

        # Input Card
        self.input_card = ctk.CTkFrame(self.controls, fg_color="#252525", corner_radius=10)
        self.input_card.pack(pady=20, padx=15, fill="x")
        
        ctk.CTkLabel(self.input_card, text="NEW PROCESS", text_color="#00f2ff").pack(pady=10)
        
        self.pid_entry = self.create_modern_input(self.input_card, "PID", "1")
        self.arrival_entry = self.create_modern_input(self.input_card, "Arrival", "0")
        self.burst_entry = self.create_modern_input(self.input_card, "Burst", "5")
        self.priority_entry = self.create_modern_input(self.input_card, "Priority", "1")

        ctk.CTkButton(self.input_card, text="+ ADD PROCESS", fg_color="#00f2ff", text_color="black", 
                      hover_color="#00c8d6", command=self.add_process_ui).pack(pady=15, padx=10, fill="x")

        # Start Button
        ctk.CTkButton(self.controls, text="▶ RUN SIMULATION", fg_color="#00ff9f", text_color="black", 
                      height=50, font=("Arial", 14, "bold"), hover_color="#00cc7a", 
                      command=self.on_start).pack(side="bottom", pady=20, padx=20, fill="x")


        # --- RIGHT PANEL (Visualization) ---
        self.viz_area = ctk.CTkFrame(self, fg_color="transparent")
        self.viz_area.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=10)

        # 1. Gantt Chart Container
        ctk.CTkLabel(self.viz_area, text="TIMELINE VISUALIZATION", font=("Arial", 12, "bold"), text_color="#888888").pack(anchor="w", pady=(0, 5))
        self.chart_frame = ctk.CTkFrame(self.viz_area, height=220, fg_color="#1a1a1a", corner_radius=15)
        self.chart_frame.pack(fill="x", pady=(0, 20))
        
        # (Gantt Chart will be inserted here by main.py)

        # 2. Data Table Container
        ctk.CTkLabel(self.viz_area, text="PROCESS QUEUE & METRICS", font=("Arial", 12, "bold"), text_color="#888888").pack(anchor="w", pady=(0, 5))
        self.table_frame = ctk.CTkFrame(self.viz_area, fg_color="#1e1e1e", corner_radius=15)
        self.table_frame.pack(fill="both", expand=True)
        
        # Custom Table Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="#1e1e1e", 
                        foreground="white", 
                        fieldbackground="#1e1e1e", 
                        borderwidth=0, 
                        rowheight=30,
                        font=("Roboto", 11))
        style.configure("Treeview.Heading", 
                        background="#2b2b2b", 
                        foreground="#00f2ff", 
                        borderwidth=0,
                        font=("Roboto", 10, "bold"))
        style.map("Treeview", background=[("selected", "#3B8ED0")])

        self.tree = ttk.Treeview(self.table_frame, columns=("PID", "Arrival", "Burst", "Priority"), show="headings")
        self.tree.heading("PID", text="PROCESS ID")
        self.tree.heading("Arrival", text="ARRIVAL TIME")
        self.tree.heading("Burst", text="BURST TIME")
        self.tree.heading("Priority", text="PRIORITY")
        
        # Center text
        for col in ("PID", "Arrival", "Burst", "Priority"):
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=15)

    def create_modern_input(self, parent, placeholder, default):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=2, padx=10, fill="x")
        ctk.CTkLabel(frame, text=placeholder, width=60, anchor="w", text_color="#aaaaaa").pack(side="left")
        entry = ctk.CTkEntry(frame, width=100, fg_color="#333333", border_width=0, height=28)
        entry.insert(0, default)
        entry.pack(side="right", expand=True, fill="x", padx=(10, 0))
        return entry

    def add_process_ui(self):
        try:
            pid = int(self.pid_entry.get())
            arr = int(self.arrival_entry.get())
            bst = int(self.burst_entry.get())
            pri = int(self.priority_entry.get())
            
            self.process_list.append((pid, arr, bst, pri))
            self.tree.insert("", "end", values=(pid, arr, bst, pri))
            
            # Auto-increment PID
            self.pid_entry.delete(0, "end")
            self.pid_entry.insert(0, str(pid + 1))
        except ValueError:
            pass

    def on_start(self):
        algo = self.algo_var.get()
        quantum = self.quantum_entry.get()
        self.start_callback(algo, quantum, self.process_list)