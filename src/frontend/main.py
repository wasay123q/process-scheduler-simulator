import flet as ft
import subprocess
import os
from ipc import IPCServer

# --- MATERIAL DESIGN 3 THEME ---
C_EXECUTABLE = "./bin/scheduler"

# Cream & Golden Light Color Palette
COLOR_BG = "#FFF8E1"              # Warm cream background
COLOR_SURFACE = "#FFFBF0"         # Lighter cream surface
COLOR_SURFACE_VARIANT = "#F5E6D3" # Beige containers
COLOR_SURFACE_CONTAINER = "#FAF3E0" # Cards with slight cream
COLOR_PRIMARY = "#D4A574"         # Golden brown primary
COLOR_PRIMARY_CONTAINER = "#E8C4A0" # Light golden container
COLOR_SECONDARY = "#A68A64"       # Darker tan
COLOR_TERTIARY = "#C8A882"        # Medium tan accent
COLOR_ON_SURFACE = "#3E2723"      # Dark brown text
COLOR_ON_PRIMARY = "#FFFFFF"      # White text on primary
COLOR_OUTLINE = "#B8956A"         # Golden brown borders
COLOR_SUCCESS = "#6A9955"         # Muted green
COLOR_WARNING = "#C89F5D"         # Golden warning
COLOR_ERROR = "#B55A5A"           # Muted red

# Process Colors (Soft pastel palette for light theme)
P_COLORS = [
    "#A7C7E7",  # Soft Blue
    "#F4A7B9",  # Soft Pink  
    "#B8E6B8",  # Soft Green
    "#FFD98E",  # Soft Yellow
    "#D4B5E1",  # Soft Purple
    "#FFBB9A",  # Soft Peach
]

def main(page: ft.Page):
    # --- 1. Page Setup ---
    page.title = "Process Scheduler - Material Design"
    page.bgcolor = COLOR_BG
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 1450
    page.window_height = 920
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
    }
    page.theme = ft.Theme(
        color_scheme_seed=COLOR_PRIMARY,
        use_material3=True,
    )
    
    # State
    processes = [] 
    ipc = None
    subprocess_proc = None

    # --- 2. UI Components ---

    status_text = ft.Text("IDLE", size=12, weight=ft.FontWeight.W_600, color=COLOR_SECONDARY)
    status_container = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.CIRCLE, size=10, color=COLOR_SECONDARY),
            ft.Container(width=8),
            status_text
        ], spacing=0),
        bgcolor=COLOR_SURFACE_VARIANT, 
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        border_radius=24,
        border=ft.border.all(2, COLOR_OUTLINE),
        animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=3,
            color=ft.Colors.with_opacity(0.15, COLOR_SECONDARY),
            offset=ft.Offset(0, 2),
        )
    )

    header = ft.Row([
        ft.Container(
            content=ft.Icon(ft.Icons.SCHEDULE, color=COLOR_ON_PRIMARY, size=36),
            bgcolor=COLOR_PRIMARY,
            border_radius=12,
            padding=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color=ft.Colors.with_opacity(0.3, COLOR_PRIMARY),
                offset=ft.Offset(0, 2),
            ),
        ),
        ft.Container(width=16),
        ft.Column([
            ft.Text("Process Scheduler", size=32, weight=ft.FontWeight.W_700, color=COLOR_ON_SURFACE),
            ft.Text("Real-time CPU scheduling visualization", size=15, weight=ft.FontWeight.W_400, color=COLOR_SECONDARY),
        ], spacing=4),
        ft.Container(expand=True),
        status_container
    ], alignment=ft.MainAxisAlignment.START)

    # --- LEFT SIDEBAR (Inputs) ---
    
    algo_dropdown = ft.Dropdown(
        label="Scheduling Algorithm", 
        width=300,
        options=[
            ft.dropdown.Option("FCFS", "First Come First Served"), 
            ft.dropdown.Option("SJF", "Shortest Job First"),
            ft.dropdown.Option("Priority", "Priority Scheduling"), 
            ft.dropdown.Option("RR", "Round Robin"),
        ],
        value="FCFS", 
        border_color=COLOR_OUTLINE,
        focused_border_color=COLOR_PRIMARY,
        text_style=ft.TextStyle(color=COLOR_ON_SURFACE, size=14, weight=ft.FontWeight.W_500),
        label_style=ft.TextStyle(color=COLOR_SECONDARY, size=12),
        bgcolor=COLOR_SURFACE,
        border_radius=10,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
    )

    quantum_field = ft.TextField(
        label="Time Quantum", 
        value="2", 
        width=300,
        visible=False, 
        border_color=COLOR_OUTLINE,
        focused_border_color=COLOR_PRIMARY,
        text_style=ft.TextStyle(color=COLOR_ON_SURFACE, size=14, weight=ft.FontWeight.W_500),
        label_style=ft.TextStyle(color=COLOR_SECONDARY, size=12),
        bgcolor=COLOR_SURFACE,
        border_radius=10,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
        helper_text="Time slice for Round Robin",
        helper_style=ft.TextStyle(color=COLOR_SECONDARY, size=11),
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    def on_algo_change(e):
        quantum_field.visible = (algo_dropdown.value == "RR")
        page.update()
    algo_dropdown.on_change = on_algo_change

    input_pid = ft.TextField(
        label="PID", value="1", width=140, read_only=True,
        border_color=COLOR_OUTLINE, text_style=ft.TextStyle(size=14, color=COLOR_ON_SURFACE, weight=ft.FontWeight.W_500),
        label_style=ft.TextStyle(color=COLOR_SECONDARY, size=12),
        bgcolor=COLOR_SURFACE_VARIANT, border_radius=10,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
    )
    input_arr = ft.TextField(
        label="Arrival", value="0", width=140,
        border_color=COLOR_OUTLINE, focused_border_color=COLOR_PRIMARY,
        text_style=ft.TextStyle(color=COLOR_ON_SURFACE, size=14, weight=ft.FontWeight.W_500),
        label_style=ft.TextStyle(color=COLOR_SECONDARY, size=12),
        bgcolor=COLOR_SURFACE, border_radius=10,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    input_bst = ft.TextField(
        label="Burst", value="5", width=140,
        border_color=COLOR_OUTLINE, focused_border_color=COLOR_PRIMARY,
        text_style=ft.TextStyle(color=COLOR_ON_SURFACE, size=14, weight=ft.FontWeight.W_500),
        label_style=ft.TextStyle(color=COLOR_SECONDARY, size=12),
        bgcolor=COLOR_SURFACE, border_radius=10,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    input_pri = ft.TextField(
        label="Priority", value="1", width=140,
        border_color=COLOR_OUTLINE, focused_border_color=COLOR_PRIMARY,
        text_style=ft.TextStyle(color=COLOR_ON_SURFACE, size=14, weight=ft.FontWeight.W_500),
        label_style=ft.TextStyle(color=COLOR_SECONDARY, size=12),
        bgcolor=COLOR_SURFACE, border_radius=10,
        content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # Process Table with Metrics
    proc_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("PID", size=14, weight=ft.FontWeight.W_700, color=COLOR_PRIMARY)),
            ft.DataColumn(ft.Text("Arrival", size=14, weight=ft.FontWeight.W_700, color=COLOR_ON_SURFACE)),
            ft.DataColumn(ft.Text("Burst", size=14, weight=ft.FontWeight.W_700, color=COLOR_ON_SURFACE)),
            ft.DataColumn(ft.Text("Priority", size=14, weight=ft.FontWeight.W_700, color=COLOR_ON_SURFACE)),
            ft.DataColumn(ft.Text("CT", size=14, weight=ft.FontWeight.W_700, color=COLOR_SUCCESS)), 
            ft.DataColumn(ft.Text("TAT", size=14, weight=ft.FontWeight.W_700, color=COLOR_WARNING)), 
            ft.DataColumn(ft.Text("WT", size=14, weight=ft.FontWeight.W_700, color=COLOR_ERROR)),       
        ],
        rows=[],
        border=ft.border.all(1, ft.Colors.with_opacity(0.3, COLOR_OUTLINE)),
        border_radius=10,
        heading_row_color=COLOR_PRIMARY_CONTAINER,
        heading_row_height=52,
        data_row_min_height=48,
        horizontal_lines=ft.BorderSide(1, ft.Colors.with_opacity(0.15, COLOR_OUTLINE)),
        show_checkbox_column=False,
    )

    def add_process(e):
        try:
            pid = int(input_pid.value)
            arr = int(input_arr.value)
            bst = int(input_bst.value)
            pri = int(input_pri.value)
            processes.append((pid, arr, bst, pri))
            
            # Initialize row with "—"
            proc_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(pid), size=14, weight=ft.FontWeight.W_700, color=COLOR_PRIMARY)),
                        ft.DataCell(ft.Text(str(arr), size=14, weight=ft.FontWeight.W_500, color=COLOR_ON_SURFACE)),
                        ft.DataCell(ft.Text(str(bst), size=14, weight=ft.FontWeight.W_500, color=COLOR_ON_SURFACE)),
                        ft.DataCell(ft.Text(str(pri), size=14, weight=ft.FontWeight.W_500, color=COLOR_ON_SURFACE)),
                        ft.DataCell(ft.Text("—", size=14, weight=ft.FontWeight.W_400, color=COLOR_SECONDARY)), 
                        ft.DataCell(ft.Text("—", size=14, weight=ft.FontWeight.W_400, color=COLOR_SECONDARY)), 
                        ft.DataCell(ft.Text("—", size=14, weight=ft.FontWeight.W_400, color=COLOR_SECONDARY)), 
                    ],
                    color=COLOR_SURFACE_VARIANT if len(proc_table.rows) % 2 == 0 else COLOR_SURFACE,
                )
            )
            input_pid.value = str(pid + 1)
            page.update()
        except ValueError: pass

    btn_add = ft.ElevatedButton(
        "Add Process", 
        icon=ft.Icons.ADD_CIRCLE_OUTLINE, 
        style=ft.ButtonStyle(
            color=COLOR_ON_PRIMARY,
            bgcolor=COLOR_PRIMARY,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            text_style=ft.TextStyle(size=15, weight=ft.FontWeight.W_600),
            shadow_color=ft.Colors.with_opacity(0.25, COLOR_PRIMARY),
            elevation=3,
        ),
        on_click=add_process, 
        width=300,
    )

    # --- RIGHT SIDE (Visualization) ---
    
    timeline_row = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=3)
    ruler_row = ft.Row(scroll=ft.ScrollMode.HIDDEN, spacing=0)
    
    # Create grid lines container
    grid_lines = ft.Row(spacing=0)
    for i in range(50):  # 50 grid lines
        if i % 5 == 0:
            grid_lines.controls.append(
                ft.Container(width=45, height=120, 
                           border=ft.border.only(left=ft.BorderSide(1, ft.Colors.with_opacity(0.2, COLOR_OUTLINE))))
            )
        else:
            grid_lines.controls.append(
                ft.Container(width=45, height=120,
                           border=ft.border.only(left=ft.BorderSide(1, ft.Colors.with_opacity(0.08, COLOR_OUTLINE))))
            )
    
    gantt_container = ft.Container(
        content=ft.Stack([
            grid_lines,  # Grid in background
            ft.Column([
                timeline_row,
                ft.Container(height=2, bgcolor=COLOR_PRIMARY, width=3000, opacity=0.3),
                ruler_row
            ], spacing=8),
        ]),
        bgcolor=COLOR_SURFACE,
        height=180, 
        border_radius=12, 
        padding=16,
        border=ft.border.all(2, COLOR_OUTLINE),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=ft.Colors.with_opacity(0.15, COLOR_SECONDARY),
            offset=ft.Offset(0, 2),
        )
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
                row.cells[4].content.color = COLOR_SUCCESS
                row.cells[4].content.weight = ft.FontWeight.W_600
                
                row.cells[5].content.value = str(p['tat'])
                row.cells[5].content.color = COLOR_WARNING
                row.cells[5].content.weight = ft.FontWeight.W_600
                
                row.cells[6].content.value = str(p['wt'])
                row.cells[6].content.color = COLOR_ERROR
                row.cells[6].content.weight = ft.FontWeight.W_600

            if p['state'] == 1: # RUNNING
                running_pid = p['pid']
        
        # --- VISUALIZATION LOGIC ---
        block = None
        if running_pid != -1:
            # CASE A: Process is Running -> Colored Block
            color = P_COLORS[running_pid % len(P_COLORS)]
            block = ft.Container(
                width=45, 
                height=100, 
                bgcolor=color, 
                border_radius=8,
                alignment=ft.alignment.center,
                content=ft.Text(
                    f"P{running_pid}", 
                    size=14, 
                    weight=ft.FontWeight.W_900, 
                    color=COLOR_ON_SURFACE
                ),
                tooltip=f"Time: {time}\nProcess: P{running_pid}",
                scale=ft.Scale(0.8),
                animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color=ft.Colors.with_opacity(0.25, color),
                    offset=ft.Offset(0, 2),
                ),
                border=ft.border.all(2, ft.Colors.with_opacity(0.4, COLOR_OUTLINE)),
            )
        else:
            # CASE B: CPU Idle or Finished -> Transparent Spacer
            block = ft.Container(
                width=45, height=110, 
                bgcolor=ft.Colors.with_opacity(0.08, COLOR_OUTLINE), 
                border_radius=8,
                border=ft.border.all(1, ft.Colors.with_opacity(0.1, COLOR_OUTLINE)),
            )

        # Create the Ruler Label
        ruler_text = ft.Container(
            width=45, alignment=ft.alignment.center,
            content=ft.Text(
                str(time), 
                size=11, 
                weight=ft.FontWeight.W_500,
                color=COLOR_OUTLINE
            )
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
        status_text.value = "COMPLETED"
        status_text.color = COLOR_SUCCESS
        status_container.bgcolor = ft.Colors.with_opacity(0.15, COLOR_SUCCESS)
        status_container.border = ft.border.all(1, COLOR_SUCCESS)
        status_container.content.controls[0].color = COLOR_SUCCESS  # Icon
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

        global ipc, subprocess_proc
        ipc = IPCServer(update_ui_from_ipc, on_sim_finished) 
        if ipc.start():
            status_text.value = "RUNNING"
            status_text.color = COLOR_PRIMARY
            status_container.bgcolor = ft.Colors.with_opacity(0.15, COLOR_PRIMARY)
            status_container.border = ft.border.all(1, COLOR_PRIMARY)
            status_container.content.controls[0].color = COLOR_PRIMARY  # Icon

        cmd = [C_EXECUTABLE, algo_dropdown.value, quantum_field.value, str(len(processes))]
        subprocess_proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        input_str = ""
        for p in processes:
            input_str += f"{p[0]} {p[1]} {p[2]} {p[3]}\n"
        
        subprocess_proc.stdin.write(input_str)
        subprocess_proc.stdin.flush()

        btn_start.disabled = True
        btn_start.text = "Running..."
        page.update()

    btn_start = ft.ElevatedButton(
        "START SIMULATION", 
        icon=ft.Icons.PLAY_ARROW_ROUNDED, 
        style=ft.ButtonStyle(
            color=COLOR_ON_PRIMARY,
            bgcolor=COLOR_SUCCESS,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=28, vertical=18),
            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_700, letter_spacing=0.5),
            shadow_color=ft.Colors.with_opacity(0.3, COLOR_SUCCESS),
            elevation=4,
        ),
        on_click=start_simulation,
        width=300,
    )

    # --- LAYOUT ---
    sidebar = ft.Container(
        width=360, 
        bgcolor=COLOR_SURFACE, 
        border_radius=12, 
        padding=20,
        border=ft.border.all(2, COLOR_OUTLINE),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=ft.Colors.with_opacity(0.15, COLOR_SECONDARY),
            offset=ft.Offset(0, 2),
        ),
        alignment=ft.alignment.top_left,
        content=ft.Column([
            ft.Text(
                "Configuration", 
                size=20, 
                weight=ft.FontWeight.W_700, 
                color=COLOR_ON_SURFACE
            ),
            ft.Divider(height=1, thickness=2, color=COLOR_OUTLINE),
            ft.Container(height=12),
            algo_dropdown, 
            ft.Container(height=12),
            quantum_field, 
            ft.Container(height=24),
            ft.Text(
                "Add Process", 
                size=20, 
                weight=ft.FontWeight.W_700, 
                color=COLOR_ON_SURFACE
            ),
            ft.Divider(height=1, thickness=2, color=COLOR_OUTLINE),
            ft.Container(height=12),
            ft.Row([input_pid, input_arr], spacing=16),
            ft.Container(height=12),
            ft.Row([input_bst, input_pri], spacing=16),
            ft.Container(height=16),
            btn_add, 
            ft.Container(expand=True),
            ft.Divider(height=1, thickness=2, color=COLOR_OUTLINE), 
            ft.Container(height=16),
            btn_start
        ], spacing=0)
    )

    main_view = ft.Container(
        expand=True, 
        padding=12,
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.TIMELINE, size=22, color=COLOR_PRIMARY),
                ft.Container(width=10),
                ft.Text(
                    "Live Timeline", 
                    size=22, 
                    weight=ft.FontWeight.W_700, 
                    color=COLOR_ON_SURFACE
                ),
            ]),
            ft.Container(height=8),
            gantt_container, 
            ft.Container(height=20),
            ft.Row([
                ft.Icon(ft.Icons.TABLE_ROWS, size=22, color=COLOR_PRIMARY),
                ft.Container(width=10),
                ft.Text(
                    "Process Queue", 
                    size=22, 
                    weight=ft.FontWeight.W_700, 
                    color=COLOR_ON_SURFACE
                ),
            ]),
            ft.Container(height=8),
            ft.Container(
                content=ft.Column([
                    proc_table,
                ], scroll=ft.ScrollMode.AUTO),
                bgcolor=COLOR_SURFACE, 
                border_radius=12, 
                padding=12, 
                expand=True,
                border=ft.border.all(2, COLOR_OUTLINE),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color=ft.Colors.with_opacity(0.15, COLOR_SECONDARY),
                    offset=ft.Offset(0, 2),
                ),
            )
        ], spacing=0, expand=True)
    )

    # Cleanup handler
    def on_window_event(e):
        if e.data == "close":
            try:
                # Cleanup IPC
                if ipc:
                    ipc.running = False
                    ipc.cleanup()
                
                # Terminate subprocess
                if subprocess_proc:
                    subprocess_proc.terminate()
                    subprocess_proc.wait(timeout=1)
            except:
                pass
    
    page.on_window_event = on_window_event

    page.add(
        header, 
        ft.Container(height=24), 
        ft.Row(
            [sidebar, ft.Container(width=24), main_view], 
            expand=True, 
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )

if __name__ == "__main__":
    try:
        ft.app(target=main, view=ft.AppView.FLET_APP)
    except KeyboardInterrupt:
        pass