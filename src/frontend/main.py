import flet as ft
import subprocess
import os
from ipc import IPCServer

# --- CONSTANTS & THEME ---
C_EXECUTABLE = "./bin/scheduler"
COLOR_BG = "#111111"       
COLOR_CARD = "#1A1A1A"     
COLOR_ACCENT = "#00E5FF"   
COLOR_SEC = "#D500F9"      
COLOR_TEXT = "#FFFFFF"

# Process Colors
P_COLORS = [
    ft.Colors.CYAN_400, ft.Colors.PINK_400, ft.Colors.GREEN_400,
    ft.Colors.AMBER_400, ft.Colors.PURPLE_400, ft.Colors.RED_400
]

def main(page: ft.Page):
    # --- 1. Page Setup ---
    page.title = "OS Scheduler Pro 2025"
    page.bgcolor = COLOR_BG
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window_width = 1300
    page.window_height = 850
    
    # State
    processes = [] 
    ipc = None

    # --- 2. UI Components ---

    status_text = ft.Text("STATUS: IDLE", size=12, weight="bold", color=ft.Colors.GREY_400)
    status_container = ft.Container(
        content=status_text,
        bgcolor=ft.Colors.GREY_900, padding=5, border_radius=5,
        border=ft.border.all(1, ft.Colors.GREY_800),
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT) 
    )

    header = ft.Row([
        ft.Icon(ft.Icons.MEMORY, color=COLOR_ACCENT, size=30),
        ft.Text("PROCESS SCHEDULER", size=25, weight="bold", color="white"),
        ft.Container(width=10),
        status_container
    ], alignment=ft.MainAxisAlignment.START)

    # --- LEFT SIDEBAR (Inputs) ---
    
    algo_dropdown = ft.Dropdown(
        label="Algorithm", width=280,
        options=[
            ft.dropdown.Option("FCFS"), ft.dropdown.Option("SJF"),
            ft.dropdown.Option("Priority"), ft.dropdown.Option("RR"),
        ],
        value="FCFS", border_color=COLOR_ACCENT, text_style=ft.TextStyle(color=COLOR_TEXT)
    )

    quantum_field = ft.TextField(
        label="Time Quantum", value="2", width=280, visible=False, border_color=COLOR_SEC
    )

    def on_algo_change(e):
        quantum_field.visible = (algo_dropdown.value == "RR")
        page.update()
    algo_dropdown.on_change = on_algo_change

    input_pid = ft.TextField(label="PID", value="1", width=60, read_only=True)
    input_arr = ft.TextField(label="Arrival", value="0", width=70)
    input_bst = ft.TextField(label="Burst", value="5", width=70)
    input_pri = ft.TextField(label="Priority", value="1", width=70)

    # Process Table with Metrics
    proc_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("PID", color=COLOR_ACCENT)),
            ft.DataColumn(ft.Text("Arrival")),
            ft.DataColumn(ft.Text("Burst")),
            ft.DataColumn(ft.Text("Priority")),
            ft.DataColumn(ft.Text("Comp. Time", color=ft.Colors.GREEN_400)), 
            ft.DataColumn(ft.Text("Turnaround", color=ft.Colors.ORANGE_400)), 
            ft.DataColumn(ft.Text("Waiting", color=ft.Colors.RED_400)),       
        ],
        rows=[],
        border=ft.border.all(1, "#333333"),
        heading_row_color="#222222",
    )

    def add_process(e):
        try:
            pid = int(input_pid.value)
            arr = int(input_arr.value)
            bst = int(input_bst.value)
            pri = int(input_pri.value)
            processes.append((pid, arr, bst, pri))
            
            # Initialize row with "-"
            proc_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(pid), weight="bold")),
                    ft.DataCell(ft.Text(str(arr))),
                    ft.DataCell(ft.Text(str(bst))),
                    ft.DataCell(ft.Text(str(pri))),
                    ft.DataCell(ft.Text("-", color="grey")), 
                    ft.DataCell(ft.Text("-", color="grey")), 
                    ft.DataCell(ft.Text("-", color="grey")), 
                ])
            )
            input_pid.value = str(pid + 1)
            page.update()
        except ValueError: pass

    btn_add = ft.ElevatedButton(
        "Add Process", icon=ft.Icons.ADD, bgcolor=COLOR_CARD, color="white", 
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=add_process, width=280
    )

    # --- RIGHT SIDE (Visualization) ---
    
    timeline_row = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=2)
    ruler_row = ft.Row(scroll=ft.ScrollMode.HIDDEN, spacing=0) 

    gantt_container = ft.Container(
        content=ft.Column([
            timeline_row,
            ft.Container(height=1, bgcolor="#333333", width=2000),
            ruler_row
        ], spacing=5),
        bgcolor="#000000", height=200, border_radius=10, padding=15,
        border=ft.border.all(1, "#333333"),
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.2, COLOR_ACCENT))
    )

    # --- LOGIC ---

    def update_ui_from_ipc(data):
        time = data.get("time", 0)
        procs = data.get("processes", [])
        
        running_pid = -1
        
        # Update Table Metrics
        for i, p in enumerate(procs):
            if p['ct'] > 0:
                row = proc_table.rows[i]
                row.cells[4].content.value = str(p['ct'])
                row.cells[4].content.color = ft.Colors.GREEN_400
                
                row.cells[5].content.value = str(p['tat'])
                row.cells[5].content.color = ft.Colors.ORANGE_400
                
                row.cells[6].content.value = str(p['wt'])
                row.cells[6].content.color = ft.Colors.RED_400

            if p['state'] == 1: # RUNNING
                running_pid = p['pid']
        
        # --- VISUALIZATION LOGIC ---
        block = None
        if running_pid != -1:
            # CASE A: Process is Running -> Colored Block
            color = P_COLORS[running_pid % len(P_COLORS)]
            block = ft.Container(
                width=40, height=100, bgcolor=color, border_radius=4,
                alignment=ft.alignment.center,
                content=ft.Text(f"P{running_pid}", size=12, weight="bold", color="black"),
                tooltip=f"Time: {time}\nProcess: P{running_pid}",
                scale=ft.Scale(0.5),
                animate_scale=ft.Animation(200, ft.AnimationCurve.ELASTIC_OUT),
            )
        else:
            # CASE B: CPU Idle or Finished -> Transparent Spacer
            # This ensures the ruler number still appears even if no process is running
            block = ft.Container(
                width=40, height=100, 
                bgcolor=ft.Colors.with_opacity(0.05, "white"), 
                border_radius=4,
            )

        # Create the Ruler Label
        ruler_text = ft.Container(
            width=40, alignment=ft.alignment.center,
            content=ft.Text(str(time), size=10, color="grey")
        )

        # Append Both
        timeline_row.controls.append(block)
        ruler_row.controls.append(ruler_text)
        
        # Trigger animation if it's a real block
        if running_pid != -1:
            block.scale = 1.0

        # Scroll to keep latest in view
        timeline_row.scroll_to(offset=-1, duration=100, curve=ft.AnimationCurve.LINEAR)
        ruler_row.scroll_to(offset=-1, duration=100, curve=ft.AnimationCurve.LINEAR)
        
        page.update()

    def on_sim_finished():
        status_text.value = "STATUS: COMPLETED"
        status_text.color = ft.Colors.GREEN_400
        status_container.border = ft.border.all(1, ft.Colors.GREEN_400)
        btn_start.disabled = False
        btn_start.text = "START SIMULATION"
        page.update()

    def start_simulation(e):
        if not processes: return
        
        timeline_row.controls.clear()
        ruler_row.controls.clear()
        
        # Reset Table Metrics
        for row in proc_table.rows:
            row.cells[4].content.value = "-"
            row.cells[5].content.value = "-"
            row.cells[6].content.value = "-"

        global ipc
        ipc = IPCServer(update_ui_from_ipc, on_sim_finished) 
        if ipc.start():
            status_text.value = "STATUS: RUNNING..."
            status_text.color = COLOR_ACCENT
            status_container.border = ft.border.all(1, COLOR_ACCENT)

        cmd = [C_EXECUTABLE, algo_dropdown.value, quantum_field.value, str(len(processes))]
        proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        input_str = ""
        for p in processes:
            input_str += f"{p[0]} {p[1]} {p[2]} {p[3]}\n"
        
        proc.stdin.write(input_str)
        proc.stdin.flush()

        btn_start.disabled = True
        btn_start.text = "Running..."
        page.update()

    btn_start = ft.ElevatedButton(
        "START SIMULATION", bgcolor=COLOR_ACCENT, color="black",
        icon=ft.Icons.PLAY_ARROW, width=280, height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=start_simulation
    )

    # --- LAYOUT ---
    sidebar = ft.Container(
        width=320, bgcolor=COLOR_CARD, border_radius=15, padding=20,
        content=ft.Column([
            ft.Text("CONFIGURATION", color="grey", weight="bold"), ft.Divider(color="grey"),
            algo_dropdown, quantum_field, ft.Container(height=10),
            ft.Text("NEW PROCESS", color=COLOR_ACCENT, weight="bold"),
            ft.Row([input_pid, input_arr], spacing=10),
            ft.Row([input_bst, input_pri], spacing=10),
            btn_add, ft.Divider(color="grey"), btn_start
        ])
    )

    main_view = ft.Container(
        expand=True, padding=10,
        content=ft.Column([
            ft.Text("LIVE TIMELINE", color="grey", weight="bold"),
            gantt_container, ft.Container(height=20),
            ft.Text("PROCESS QUEUE", color="grey", weight="bold"),
            ft.Container(
                content=proc_table, bgcolor=COLOR_CARD, border_radius=10, padding=10, expand=True
            )
        ])
    )

    page.add(header, ft.Divider(color="transparent", height=10), 
             ft.Row([sidebar, main_view], expand=True, vertical_alignment=ft.CrossAxisAlignment.START))

if __name__ == "__main__":
    ft.app(target=main)