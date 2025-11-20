import tkinter as tk
import customtkinter as ctk

class GanttChart(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # 1. Configuration
        self.configure(fg_color="#1a1a1a", corner_radius=15) # Dark background card
        
        # 2. Canvas with scrollbar
        self.canvas_height = 180
        self.time_scale = 30 # Pixels per time unit (wider for modern look)
        
        self.canvas = tk.Canvas(
            self, 
            bg="#1a1a1a", 
            height=self.canvas_height, 
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill="both", expand=True, padx=15, pady=15)

        # scrollbar (horizontal)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(fill="x", padx=10, pady=(0, 10))
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # Modern Neon Palette
        self.colors = [
            "#00f2ff", # Cyan
            "#ff0055", # Neon Red
            "#00ff9f", # Neon Green
            "#bd00ff", # Electric Purple
            "#ff9100", # Bright Orange
            "#ffe600"  # Yellow
        ]
        
        self.process_map = {} # To track drawn items

    def reset(self):
        self.canvas.delete("all")
        self.process_map = {}
        self.draw_ruler(100) # Draw initial ruler

    def draw_ruler(self, max_time):
        """Draws the timeline numbers at the bottom"""
        self.canvas.delete("ruler")
        
        for t in range(max_time + 1):
            x = t * self.time_scale
            
            # Tick mark
            self.canvas.create_line(x, self.canvas_height - 20, x, self.canvas_height, fill="#444444", tags="ruler")
            
            # Number every 5 ticks
            if t % 5 == 0:
                self.canvas.create_text(x + 2, self.canvas_height - 30, text=str(t), fill="#888888", font=("Roboto", 8), tags="ruler")

        # Update scroll region
        self.canvas.configure(scrollregion=(0, 0, max_time * self.time_scale + 100, self.canvas_height))

    def update_chart(self, data):
        """
        data: {'time': 5, 'processes': [...]}
        """
        current_time = data.get('time', 0)
        process_list = data.get('processes', [])
        
        # Redraw ruler if time expands
        if current_time * self.time_scale > self.canvas.bbox("all")[2]:
            self.draw_ruler(current_time + 20)

        # Find Running Process
        for p in process_list:
            if p['state'] == 1: # STATE_RUNNING
                self.draw_block(p['pid'], current_time)

        # Auto-scroll to the latest time
        if current_time > 5:
             self.canvas.xview_moveto(1.0)

    def draw_block(self, pid, time):
        # Visual Style
        color = self.colors[pid % len(self.colors)]
        block_h = 60
        y_pos = (self.canvas_height - block_h) / 2 - 10
        
        start_x = (time - 1) * self.time_scale
        end_x = time * self.time_scale
        
        # Draw Rounded Block (Simulated by drawing rectangle + slightly smaller overlay)
        # Main Block
        self.canvas.create_rectangle(
            start_x, y_pos, end_x, y_pos + block_h,
            fill=color, outline="", tags=f"p{pid}"
        )
        
        # Glow Effect (Optional line at bottom)
        self.canvas.create_line(start_x, y_pos + block_h, end_x, y_pos + block_h, fill="white", width=2)

        # PID Text
        self.canvas.create_text(
            (start_x + end_x) / 2, y_pos + block_h/2,
            text=f"P{pid}", fill="#000000", font=("Arial", 10, "bold")
        )