# Process Scheduler Simulator

A hybrid simulator that demonstrates classic CPU scheduling algorithms (FCFS, SJF, Priority, Round Robin) with a C-based scheduler kernel and a Python (Flet) front-end for real-time visualization.

## Table of Contents

- Project overview
- Features
- Prerequisites
- Build & run
- Project structure
- Contributing

## Project overview

This repository contains a minimal process scheduler kernel written in C (under `src/backend`) and a Python-based UI/monitor (under `src/frontend`). The components communicate via IPC to stream scheduler state for visualization and analysis.

## Features

- Implements FCFS, non-preemptive SJF, Priority, and Round Robin
- Real-time Gantt chart visualization and process metrics (CT, TAT, WT)
- Separate backend (C) and frontend (Python) for performance and clarity
- Simple IPC-based protocol to transfer scheduler snapshots to the UI

## Prerequisites

- Linux (recommended) or WSL2 on Windows
- GCC and Make (build-essential)
- Python 3.10+ and `pip`

Dependencies are listed in `requirements.txt`.

## Build & run

1. Build the C kernel

```bash
make
```

The build produces the scheduler binary at `bin/scheduler`.

2. Prepare Python environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the frontend UI

```bash
python3 src/frontend/main.py
```

4. (Alternative) Run the backend-only simulator

```bash
./bin/scheduler
```

Notes:
- The frontend listens for scheduler updates (default IPC socket/path may be implemented in `src/backend/ipc.c` and `src/frontend/ipc.py`).
- If the project requires a specific socket path (for example `/tmp/scheduler_socket`), ensure both components use the same path.

## Project structure

```
.
├── Makefile
├── README.md
├── requirements.txt
├── bin/                 # Compiled binaries (output)
├── logs/                # Simulation logs and reports
└── src/
	├── backend/        # C scheduler kernel
	│   ├── main.c
	│   ├── scheduler.h
	│   ├── algorithms.c
	│   ├── process.c
	│   └── ipc.c
	└── frontend/       # Python Flet UI
		├── main.py
		├── client.py
		├── dashboard.py
		├── gantt_chart.py
		└── ipc.py
```

## Contributing

If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Open a pull request with a clear description of changes

## Authors

- Abdul Wasay Sial — Lead developer
- Faseeh Anjum — Backend (C)
- Dua Nadeem — Documentation
- Nosheen Asif — Frontend (UI)

## License

This project is provided under the MIT License. See the `LICENSE` file for details.

---

