import flet as ft
import subprocess
import os
from ipc import IPCServer

# --- PATHS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
C_EXECUTABLE = os.path.join(PROJECT_ROOT, "bin", "scheduler")

# --- THEME: VINTAGE CREAM ---
COL_BG = "#FFF8E1"       # Cream Background
COL_CARD = "#FFFFFF"     # White Card
COL_PRIMARY = "#5D4037"  # Deep Brown (Text/Headers)
COL_ACCENT = "#8D6E63"   # Lighter Brown (Borders)
COL_INPUT_BG = "#FFFFFF" # Input Background
COL_BTN_ADD = "#D7CCC8"  # Beige/Brown Button
COL_BTN_RUN = "#66BB6A"  # Green Button
COL_BTN_CLR = "#EF5350"  # Red Button

P_COLORS = ["#EF9A9A", "#A5D6A7", "#90CAF9", "#FFF59D", "#CE93D8", "#FFCC80"]

# --- BENCHMARK CARD COMPONENT ---
class SimCard(ft.Container):
    def __init__(self, title, sock_path):
        super().__init__()
        self.title = title
        self.sock_path = sock_path
        self.ipc = None
        self.avg_wt = 0.0
        self.finished = False
        
        self.timeline = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=1)
        self.status = ft.Text("WAITING", size=10, color="grey", weight="bold")
        self.stats_txt = ft.Text("-", size=11, color=COL_PRIMARY, weight="bold")
        
        # Inner Content Layout
        self.content = ft.Column([
            ft.Row([
                ft.Text(title, weight="bold", color=COL_PRIMARY, size=13),
                ft.Container(expand=True),
                self.status
            ]),
            ft.Container(
                content=self.timeline,
                height=45, 
                bgcolor=ft.Colors.with_opacity(0.05, "black"),
                border_radius=5, padding=4,
                border=ft.border.all(1, ft.Colors.with_opacity(0.1, COL_PRIMARY))
            ),
            ft.Row([
                ft.Text("Avg Waiting:", size=11, color="grey"),
                self.stats_txt
            ], spacing=5)
        ], spacing=5)
        
        self.bgcolor = COL_CARD
        self.padding = 12
        self.border_radius = 8
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.2, COL_PRIMARY))
        self.animate_scale = ft.Animation(200, "easeOut")

    def reset(self):
        self.timeline.controls.clear()
        self.status.value = "RUNNING"
        self.status.color = "blue"
        self.stats_txt.value = "-"
        self.finished = False
        self.avg_wt = 0
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.2, COL_PRIMARY))
        self.update()

    def update_sim(self, data):
        time = data.get("time", 0)
        procs = data.get("processes", [])
        running = -1
        
        total_wt = 0
        count = 0
        for p in procs:
            if p['ct'] > 0:
                total_wt += p['wt']
                count += 1
            if p['state'] == 1: running = p['pid']
            
        if count > 0:
            self.avg_wt = total_wt / count
            self.stats_txt.value = f"{self.avg_wt:.2f}s"

        # Draw Block
        if running != -1:
            col = P_COLORS[running % len(P_COLORS)]
            self.timeline.controls.append(
                ft.Container(width=12, height=35, bgcolor=col, border_radius=2, 
                             tooltip=f"T={time} | P{running}")
            )
        else:
            self.timeline.controls.append(ft.Container(width=12, height=35))
            
        self.timeline.scroll_to(offset=-1, duration=50)
        self.update()

    def mark_done(self):
        self.finished = True
        self.status.value = "DONE"
        self.status.color = "green"
        self.update()

    def mark_winner(self):
        self.border = ft.border.all(3, ft.Colors.GREEN) # Thicker border for winner
        self.update()

# --- MAIN APP ---
def main(page: ft.Page):
    page.title = "Process Scheduler Simulator"
    page.bgcolor = COL_BG
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1250
    page.window_height = 900
    page.window_resizable = True
    page.padding = 20

    processes = []
    global ipc
    ipc = None
    
    # --- STYLES ---
    input_style = dict(
        height=45, text_size=14, content_padding=12, 
        border_color=COL_ACCENT, bgcolor=COL_INPUT_BG, 
        border_radius=8, color=COL_PRIMARY,
        focused_border_color=COL_PRIMARY
    )

    # --- UI INPUTS ---
    input_pid = ft.TextField(label="PID", value="1", width=70, read_only=True, **input_style, expand=True)
    input_arr = ft.TextField(label="Arrival", value="0", **input_style, expand=True)
    input_bst = ft.TextField(label="Burst", value="5", **input_style, expand=True)
    input_pri = ft.TextField(label="Priority", value="1", **input_style, expand=True)

    # --- TOP RIGHT STATUS INDICATOR ---
    status_badge_text = ft.Text("IDLE", size=11, weight="bold", color=COL_PRIMARY)
    status_badge_icon = ft.Container(width=8, height=8, border_radius=4, bgcolor="grey")
    
    status_indicator = ft.Container(
        content=ft.Row([status_badge_icon, status_badge_text], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=15,
        border=ft.border.all(1, COL_ACCENT),
        bgcolor=ft.Colors.with_opacity(0.1, COL_PRIMARY)
    )

    # --- SINGLE MODE CHART ---
    timeline_row = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=2)
    ruler_row = ft.Row(scroll=ft.ScrollMode.HIDDEN, spacing=0)
    
    single_chart_view = ft.Container(
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.SHOW_CHART, color=COL_PRIMARY), ft.Text("Live Timeline", size=16, weight="bold", color=COL_PRIMARY)]),
            ft.Container(
                content=ft.Column([
                    ft.Row([timeline_row, ft.Container(width=20)], scroll=ft.ScrollMode.AUTO), 
                    ft.Container(height=1, bgcolor=COL_PRIMARY, width=3000), 
                    ruler_row
                ]),
                bgcolor=COL_CARD, height=150, border_radius=10, padding=15,
                border=ft.border.all(1, COL_ACCENT),
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.1, "black"))
            )
        ]),
        visible=True
    )

    # --- BENCHMARK MODE GRID ---
    cards = [
        SimCard("FCFS", "/tmp/s_fcfs"), SimCard("SJF", "/tmp/s_sjf"),
        SimCard("SRTN", "/tmp/s_srtn"), SimCard("Priority", "/tmp/s_prio"),
        SimCard("Round Robin", "/tmp/s_rr"), SimCard("MLFQ", "/tmp/s_mlfq")
    ]
    
    bench_res = ft.Text("", size=16, weight="bold", color=COL_PRIMARY)
    
    bench_grid_view = ft.Column([
        ft.Text("Algorithm Efficiency Comparison", size=18, weight="bold", color=COL_PRIMARY),
        ft.Container(
            content=ft.Column([
                ft.Row([cards[0], cards[1]], expand=True),
                ft.Row([cards[2], cards[3]], expand=True),
                ft.Row([cards[4], cards[5]], expand=True),
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
            expand=True 
        ),
        ft.Container(content=bench_res, alignment=ft.alignment.center, padding=10, bgcolor=COL_CARD, border_radius=10)
    ], visible=False, expand=True)

    # --- SHARED TABLE (SCROLLABLE NOW) ---
    proc_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("PID", weight="bold")),
            ft.DataColumn(ft.Text("Arrival")), ft.DataColumn(ft.Text("Burst")),
            ft.DataColumn(ft.Text("Priority")),
            ft.DataColumn(ft.Text("CT", color="green")),
            ft.DataColumn(ft.Text("TAT", color="orange")),
            ft.DataColumn(ft.Text("WT", color="red")),
        ],
        rows=[],
        heading_row_color=ft.Colors.with_opacity(0.1, COL_PRIMARY),
        border=ft.border.all(1, COL_ACCENT),
        border_radius=10,
        data_row_color=COL_CARD,
        width=1000 # Ensure table is wide enough to trigger horizontal scroll if needed
    )

    table_section = ft.Column([
        ft.Row([ft.Icon(ft.Icons.TABLE_CHART, color=COL_PRIMARY), ft.Text("Process Queue", size=16, weight="bold", color=COL_PRIMARY)]),
        ft.Container(
            content=ft.Column([proc_table], scroll=ft.ScrollMode.AUTO), # <-- ADDED SCROLL HERE
            bgcolor=COL_CARD, border_radius=10, padding=10, 
            border=ft.border.all(1, COL_ACCENT), expand=True
        )
    ], expand=True)

    # --- BUTTONS ---
    btn_run_text = ft.Text("START SIMULATION", color="white", weight="bold")
    btn_run_icon = ft.Icon(ft.Icons.PLAY_ARROW, color="white")

    # --- LOGIC ---
    def update_status(status, color):
        status_badge_text.value = status
        status_badge_icon.bgcolor = color
        page.update()

    def check_bench_done():
        if all(c.finished for c in cards):
            winner = min(cards, key=lambda c: c.avg_wt)
            winner.mark_winner() 
            bench_res.value = f"🏆 WINNER: {winner.title} is most efficient (Avg WT: {winner.avg_wt:.2f}s)"
            
            btn_run_text.value = "START SIMULATION"
            btn_run.disabled = False
            btn_run.opacity = 1.0
            update_status("COMPLETED", "green")
            page.update()

    def run_benchmark():
        input_str = "".join([f"{p[0]} {p[1]} {p[2]} {p[3]}\n" for p in processes])
        for c in cards:
            c.reset()
            def on_d(d, card=c): card.update_sim(d)
            def on_f(card=c): 
                card.mark_done()
                check_bench_done()
            
            c.ipc = IPCServer(c.sock_path, on_d, on_f)
            c.ipc.start()
            
            algo = c.title
            if "Round" in algo: algo = "RR"
            
            # Use user input for RR, otherwise 0 (ignored by others)
            # MLFQ ignores this in C, so it remains safe
            q = quantum.value if algo == "RR" else "0"
            
            cmd = [C_EXECUTABLE, algo, q, str(len(processes)), c.sock_path]
            subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True).communicate(input=input_str)

    def update_single(data):
        time = data.get("time", 0)
        procs = data.get("processes", [])
        run_pid = -1
        
        for i, p in enumerate(procs):
            if p['ct'] > 0:
                row = proc_table.rows[i]
                row.cells[4].content.value = str(p['ct'])
                row.cells[5].content.value = str(p['tat'])
                row.cells[6].content.value = str(p['wt'])
            if p['state'] == 1: run_pid = p['pid']
            
        block = None
        if run_pid != -1:
            col = P_COLORS[run_pid % len(P_COLORS)]
            # MLFQ Queue Visual
            q_lvl = -1
            for p in procs:
                if p['pid'] == run_pid:
                    q_lvl = p.get('q_lvl', -1)
                    break
            
            tip = f"T={time} | P{run_pid}"
            if q_lvl != -1: tip += f" | Q{q_lvl}"

            block = ft.Container(width=40, height=80, bgcolor=col, border_radius=4,
                                 alignment=ft.alignment.center, 
                                 content=ft.Text(f"P{run_pid}", weight="bold", color="black"),
                                 tooltip=tip)
        else:
            block = ft.Container(width=40, height=80, bgcolor=ft.Colors.with_opacity(0.05, "black"))
            
        timeline_row.controls.append(block)
        ruler_row.controls.append(ft.Container(width=40, content=ft.Text(str(time), size=10), alignment=ft.alignment.center))
        timeline_row.scroll_to(offset=-1, duration=100)
        ruler_row.scroll_to(offset=-1, duration=100)
        page.update()

    def on_single_done():
        btn_run_text.value = "START SIMULATION"
        btn_run.disabled = False
        btn_run.opacity = 1.0
        update_status("COMPLETED", "green")
        page.update()

    def start_sim(e):
        global ipc
        if not processes: return
        
        btn_run_text.value = "RUNNING..."
        btn_run.disabled = True
        btn_run.opacity = 0.7
        update_status("RUNNING", "blue")
        page.update()
        
        if dropdown.value == "Compare All Algorithms":
            run_benchmark()
        else:
            # Single Mode
            timeline_row.controls.clear()
            ruler_row.controls.clear()
            for row in proc_table.rows:
                row.cells[4].content.value = "-"
                row.cells[5].content.value = "-"
                row.cells[6].content.value = "-"
            
            ipc = IPCServer("/tmp/sock_single", update_single, on_single_done)
            ipc.start()
            
            input_str = "".join([f"{p[0]} {p[1]} {p[2]} {p[3]}\n" for p in processes])
            
            c_algo = "FCFS"
            if dropdown.value == "Shortest Job First": c_algo = "SJF"
            elif dropdown.value == "Shortest Remaining Time Next": c_algo = "SRTN"
            elif dropdown.value == "Priority Scheduling": c_algo = "Priority"
            elif dropdown.value == "Round Robin": c_algo = "RR"
            elif dropdown.value == "Multi-Level Feedback Queue": c_algo = "MLFQ"

            cmd = [C_EXECUTABLE, c_algo, quantum.value, str(len(processes)), "/tmp/sock_single"]
            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            proc.stdin.write(input_str)
            proc.stdin.flush()

    # --- SIDEBAR LOGIC ---
    def add_p(e):
        try:
            pid, arr, bst, pri = int(input_pid.value), int(input_arr.value), int(input_bst.value), int(input_pri.value)
            processes.append((pid, arr, bst, pri))
            proc_table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(pid))), ft.DataCell(ft.Text(str(arr))),
                ft.DataCell(ft.Text(str(bst))), ft.DataCell(ft.Text(str(pri))),
                ft.DataCell(ft.Text("-", color="green")), ft.DataCell(ft.Text("-", color="orange")),
                ft.DataCell(ft.Text("-", color="red"))
            ]))
            input_pid.value = str(pid + 1)
            page.update()
        except: pass

    def clear_q(e):
        processes.clear()
        proc_table.rows.clear()
        input_pid.value = "1"
        page.update()

    def on_drop_change(e):
        is_bench = (dropdown.value == "Compare All Algorithms")
        single_chart_view.visible = not is_bench
        bench_grid_view.visible = is_bench
        
        # Show Quantum input for RR OR Compare mode
        quantum.visible = (dropdown.value == "Round Robin" or is_bench)
        page.update()

    dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("First Come First Served"),
            ft.dropdown.Option("Shortest Job First"),
            ft.dropdown.Option("Shortest Remaining Time Next"),
            ft.dropdown.Option("Priority Scheduling"),
            ft.dropdown.Option("Round Robin"),
            ft.dropdown.Option("Multi-Level Feedback Queue"),
            ft.dropdown.Option("Compare All Algorithms"),
        ],
        value="First Come First Served",
        border_color=COL_ACCENT, text_size=13,
        bgcolor=COL_INPUT_BG,
        on_change=on_drop_change
    )
    
    quantum = ft.TextField(label="Quantum", value="2", visible=False, **input_style)

    # --- SIDEBAR CONSTRUCTION ---
    btn_add = ft.ElevatedButton(
        "Add Process", icon=ft.Icons.ADD_CIRCLE_OUTLINE, 
        on_click=add_p, bgcolor=COL_BTN_ADD, color=COL_PRIMARY, height=45, width=300,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )
    
    btn_clear = ft.OutlinedButton(
        "Clear Queue", icon=ft.Icons.DELETE_OUTLINE,
        on_click=clear_q, height=45, width=300,
        style=ft.ButtonStyle(
            color=COL_BTN_CLR, 
            side=ft.BorderSide(1, COL_BTN_CLR),
            shape=ft.RoundedRectangleBorder(radius=8)
        )
    )
    
    btn_run = ft.Container(
        content=ft.Row([btn_run_icon, btn_run_text], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=COL_BTN_RUN, alignment=ft.alignment.center, height=50, border_radius=8,
        on_click=start_sim,
        shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.3, "black"))
    )

    sidebar = ft.Container(
        content=ft.Column([
            ft.Text("Configuration", size=18, weight="bold", color=COL_PRIMARY),
            ft.Divider(color=COL_ACCENT, thickness=1),
            dropdown, quantum,
            ft.Container(height=15),
            ft.Text("Add Process", size=18, weight="bold", color=COL_PRIMARY),
            ft.Divider(color=COL_ACCENT, thickness=1),
            
            # --- 2x2 INPUT GRID ---
            ft.Row([input_pid, input_arr], spacing=10),
            ft.Row([input_bst, input_pri], spacing=10),
            
            ft.Container(height=5),
            btn_add, btn_clear,
            ft.Container(expand=True),
            ft.Divider(color=COL_ACCENT, thickness=1),
            btn_run
        ]),
        width=320, bgcolor=COL_CARD, border=ft.border.all(1, COL_ACCENT),
        border_radius=15, padding=25,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, "black"))
    )

    # --- MAIN VIEW CONSTRUCTION ---
    content_area = ft.Column([
        ft.Container(content=ft.Stack([single_chart_view, bench_grid_view]), expand=True), # Charts take available space
        ft.Container(height=10),
        ft.Container(content=table_section, height=300) # Fixed height for table area
    ], expand=True)

    header = ft.Row([
        ft.Container(
            content=ft.Icon(ft.Icons.ACCESS_TIME, color="white", size=28),
            bgcolor=COL_ACCENT, padding=12, border_radius=12
        ),
        ft.Column([
            ft.Text("Process Scheduler", size=26, weight="bold", color=COL_PRIMARY),
            ft.Text("Real-time CPU scheduling visualization", color="grey", size=12)
        ]),
        ft.Container(expand=True),
        status_indicator # Restored to top right
    ], alignment=ft.MainAxisAlignment.START)

    page.add(
        header,
        ft.Divider(color="transparent", height=10),
        ft.Row([sidebar, content_area], expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
    )

if __name__ == "__main__":
    ft.app(target=main)