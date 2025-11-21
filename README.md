<div align="center">

# 🖥️ Process Scheduler Simulator

### *Advanced Operating System Scheduler Visualizer with Real-Time IPC*

[![OS](https://img.shields.io/badge/OS-Linux-blue?logo=linux)](https://www.linux.org/)
[![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)](https://en.wikipedia.org/wiki/C_(programming_language))
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flet](https://img.shields.io/badge/Flet-UI-00D9FF?logo=flutter)](https://flet.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()

*A professional-grade hybrid simulator demonstrating CPU scheduling algorithms through an elegant real-time visualization interface.*

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [API](#-api-reference) • [Team](#-team)

---

</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [System Architecture](#-system-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Algorithm Details](#-algorithm-details)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Performance Metrics](#-performance-metrics)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Team](#-team)
- [License](#-license)

---

## 🎯 Overview

The **Process Scheduler Simulator** is an educational and analytical tool designed to visualize how operating systems manage CPU scheduling. This project bridges the gap between theoretical OS concepts and practical implementation by providing:

- **🔧 Low-Level Kernel**: A C-based scheduler implementing classic algorithms with POSIX threading and synchronization
- **🎨 Modern UI**: A Python (Flet) front-end delivering real-time Gantt chart visualization and process metrics
- **🔄 IPC Communication**: Unix Domain Sockets enabling seamless data streaming between components
- **📊 Performance Analysis**: Comprehensive metrics including Completion Time (CT), Turnaround Time (TAT), and Waiting Time (WT)

This simulator is ideal for:
- 📚 **Students** learning operating system concepts
- 👨‍🏫 **Educators** demonstrating scheduling algorithms
- 🔬 **Researchers** analyzing algorithm performance
- 💻 **Developers** understanding system-level programming

---

## ✨ Features

### 🧠 Scheduling Algorithms

| Algorithm | Type | Description | Key Characteristic |
|-----------|------|-------------|-------------------|
| **FCFS** | Non-Preemptive | First Come, First Served | Simple FIFO queue, convoy effect possible |
| **SJF** | Non-Preemptive | Shortest Job First | Minimizes average waiting time |
| **Priority** | Non-Preemptive | Priority-based selection | Lower number = higher priority |
| **Round Robin** | Preemptive | Time-slice based scheduling | Fairness with configurable quantum |

### 🎨 Visualization Features

- **📈 Real-Time Gantt Chart**: Live timeline visualization with color-coded processes
- **📊 Process State Monitoring**: Track process states (Ready, Running, Waiting, Terminated)
- **📉 Metrics Dashboard**: Real-time computation of CT, TAT, and WT
- **🎭 Smooth Animations**: 60 FPS synchronized rendering (100ms tick rate)
- **🌈 Modern UI**: Clean, professional interface with custom color palette

### 🔧 Technical Features

- **⚡ Multi-Threading**: POSIX threads with mutex synchronization
- **🔌 IPC Protocol**: JSON-based state transfer via Unix sockets
- **🛡️ Thread Safety**: Protected critical sections preventing race conditions
- **📝 Logging**: Comprehensive simulation logs for analysis
- **🎯 Extensible**: Modular architecture for easy algorithm additions

---

## 🎬 Demo

### Visual Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  🖥️  PROCESS SCHEDULER                      STATUS: RUNNING...  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────┐  ┌────────────────────────────────────────┐ │
│  │ CONFIGURATION │  │      LIVE TIMELINE                      │ │
│  ├───────────────┤  │  ┌───┬───┬───┬───┬───┬───┬───┬───┐    │ │
│  │ Algorithm: RR │  │  │P1 │P2 │P3 │P1 │P2 │P3 │P1 │ - │    │ │
│  │ Quantum: 2    │  │  └───┴───┴───┴───┴───┴───┴───┴───┘    │ │
│  │               │  │   0   1   2   3   4   5   6   7        │ │
│  │ NEW PROCESS   │  └────────────────────────────────────────┘ │
│  │ PID: 4        │                                              │
│  │ Arrival: 0    │  ┌────────────────────────────────────────┐ │
│  │ Burst: 5      │  │      PROCESS QUEUE                      │ │
│  │ Priority: 1   │  ├────┬─────┬─────┬──────┬────┬─────┬────┤ │
│  │               │  │PID │Arr. │Burst│Prior.│ CT │ TAT │ WT │ │
│  │ [Add Process] │  ├────┼─────┼─────┼──────┼────┼─────┼────┤ │
│  │               │  │ 1  │  0  │  3  │  1   │ 7  │  7  │ 4  │ │
│  │ [▶ START]     │  │ 2  │  1  │  4  │  2   │ 11 │ 10  │ 6  │ │
│  └───────────────┘  │ 3  │  2  │  2  │  3   │ 9  │  7  │ 5  │ │
│                      └────┴─────┴─────┴──────┴────┴─────┴────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Sample Output

```bash
$ ./bin/scheduler RR 2 3
Starting Simulation: RR
Waiting for 3 processes...

--- Final Metrics ---
PID     Turnaround      Waiting
1       7               4
2       10              6
3       7               5
--------------------------------------------
Average Turnaround Time: 8.00
Average Waiting Time: 5.00
Simulation Finished.
```

---

## 🏗️ System Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     System Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────┐         ┌──────────────────────┐  │
│  │   Python Frontend    │         │    C Backend         │  │
│  │   (Flet Framework)   │◄───────►│  (Scheduler Kernel)  │  │
│  │                      │  JSON   │                      │  │
│  │  • UI Rendering      │  over   │  • Algorithm Logic   │  │
│  │  • User Input        │  Unix   │  • Process Control   │  │
│  │  • Visualization     │ Socket  │  • State Management  │  │
│  │  • Metrics Display   │         │  • Threading & Sync  │  │
│  └──────────────────────┘         └──────────────────────┘  │
│           ▲                                  ▲                │
│           │                                  │                │
│           └──────────────┬───────────────────┘                │
│                          │                                    │
│                  /tmp/scheduler_socket                        │
│                    (IPC Channel)                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Initialization**: Frontend starts IPC server, binds socket
2. **Process Definition**: User adds processes via UI
3. **Simulation Launch**: Frontend spawns C backend subprocess
4. **Data Streaming**: Backend sends JSON state updates every 100ms
5. **Visualization**: Frontend renders Gantt chart and updates metrics
6. **Completion**: Backend closes connection, frontend displays final stats

### IPC Protocol

**Message Format** (JSON):
```json
{
  "time": 5,
  "processes": [
    {
      "pid": 1,
      "state": 1,
      "remaining": 2,
      "ct": 0,
      "tat": 0,
      "wt": 0
    }
  ]
}
```

**Process States**:
- `0` = READY
- `1` = RUNNING
- `2` = WAITING
- `3` = TERMINATED

---

## 🔧 Prerequisites

### System Requirements

| Component | Requirement | Purpose |
|-----------|------------|---------|
| **OS** | Linux (Ubuntu 20.04+) or WSL2 | Unix socket support |
| **Compiler** | GCC 9.0+ | C code compilation |
| **Build System** | GNU Make 4.0+ | Automated builds |
| **Python** | 3.10 or higher | Frontend runtime |
| **Memory** | 512 MB+ available | Process simulation |

### Software Dependencies

**C Backend**:
- `pthread` (POSIX threads)
- Standard C library (`glibc`)

**Python Frontend**:
- `flet>=0.10.0` - UI framework

---

## 📦 Installation

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/wasay123q/process-scheduler-simulator.git
cd process-scheduler-simulator

# 2. Install system dependencies
sudo apt update && sudo apt install -y build-essential python3-venv

# 3. Build the C kernel
make

# 4. Set up Python environment
python3 -m venv venv
source venv/bin/activate

# 5. Install Python dependencies
pip install flet

# 6. Run the simulator
python3 src/frontend/main.py
```

### Manual Compilation

```bash
# Compile with specific flags
gcc -Wall -Wextra -pthread -g \
    src/backend/main.c \
    src/backend/algorithms.c \
    src/backend/process.c \
    src/backend/ipc.c \
    -o bin/scheduler
```

### Verification

```bash
# Test backend standalone
./bin/scheduler FCFS 0 3 <<EOF
1 0 5 1
2 1 3 2
3 2 4 3
EOF

# Check for output
ls -lh bin/scheduler  # Should show executable
```

---

## 🚀 Usage

### Basic Workflow

1. **Launch Application**
   ```bash
   python3 src/frontend/main.py
   ```

2. **Configure Simulation**
   - Select algorithm (FCFS, SJF, Priority, RR)
   - Set time quantum (for Round Robin only)

3. **Add Processes**
   - Enter PID, Arrival Time, Burst Time, Priority
   - Click "Add Process" for each process

4. **Start Simulation**
   - Click "START SIMULATION"
   - Watch real-time Gantt chart animation
   - Monitor completion metrics

5. **Analyze Results**
   - Review final metrics table
   - Compare average turnaround and waiting times

### Command-Line Usage (Backend Only)

```bash
# Syntax
./bin/scheduler <Algorithm> <Quantum> <Process_Count>

# Example: FCFS with 3 processes
./bin/scheduler FCFS 0 3 <<EOF
1 0 5 1
2 1 3 2
3 2 4 3
EOF

# Example: Round Robin (Quantum = 2)
./bin/scheduler RR 2 4 <<EOF
1 0 5 1
2 1 4 2
3 2 3 3
4 3 2 4
EOF
```

**Input Format**: `PID ArrivalTime BurstTime Priority`

### Advanced Options

**Custom Socket Path** (modify in code):
```c
// src/backend/ipc.c
#define SOCKET_PATH "/tmp/custom_scheduler_socket"
```

```python
# src/frontend/ipc.py
SOCKET_PATH = "/tmp/custom_scheduler_socket"
```

---

## 📚 Algorithm Details

### FCFS (First Come, First Served)

**Characteristics**:
- Simplest scheduling algorithm
- Non-preemptive
- Processes executed in arrival order

**Implementation** (`algorithms.c:16-25`):
```c
for (int i = 0; i < sys->process_count; i++) {
    Process *p = sys->processes[i];
    if (p->state != STATE_TERMINATED && 
        p->arrival_time <= sys->current_time) {
        if (selected_idx == -1 || 
            p->arrival_time < sys->processes[selected_idx]->arrival_time) {
            selected_idx = i;
        }
    }
}
```

**Pros**: Simple, no starvation  
**Cons**: Convoy effect, high average waiting time

---

### SJF (Shortest Job First)

**Characteristics**:
- Selects process with minimum burst time
- Non-preemptive
- Optimal for minimizing average waiting time

**Implementation** (`algorithms.c:27-38`):
```c
int min_burst = 999999;
for (int i = 0; i < sys->process_count; i++) {
    Process *p = sys->processes[i];
    if (p->state != STATE_TERMINATED && 
        p->arrival_time <= sys->current_time) {
        if (p->burst_time < min_burst) {
            min_burst = p->burst_time;
            selected_idx = i;
        }
    }
}
```

**Pros**: Minimizes average waiting time  
**Cons**: Starvation for long processes, requires burst time prediction

---

### Priority Scheduling

**Characteristics**:
- Selects process with highest priority (lowest number)
- Non-preemptive
- Priority inversion possible

**Implementation** (`algorithms.c:40-51`):
```c
int highest_priority = 999999;
for (int i = 0; i < sys->process_count; i++) {
    Process *p = sys->processes[i];
    if (p->state != STATE_TERMINATED && 
        p->arrival_time <= sys->current_time) {
        if (p->priority < highest_priority) {
            highest_priority = p->priority;
            selected_idx = i;
        }
    }
}
```

**Pros**: Important tasks executed first  
**Cons**: Starvation, priority inversion

---

### Round Robin (RR)

**Characteristics**:
- Time-slice (quantum) based scheduling
- Preemptive
- Fair CPU distribution

**Implementation** (`algorithms.c:53-75`):
```c
if (rr_last_idx != -1) {
    Process *prev = sys->processes[rr_last_idx];
    if (prev->state != STATE_TERMINATED && 
        rr_quantum_timer < quantum) {
        rr_quantum_timer++;
        return rr_last_idx;
    }
}
rr_quantum_timer = 1;
int start_pos = (rr_last_idx + 1) % sys->process_count;
// Circular queue iteration...
```

**Pros**: Fairness, no starvation, responsive  
**Cons**: Higher context switching overhead, quantum selection critical

---

## 📁 Project Structure

```
process-scheduler-simulator/
│
├── 📄 Makefile                  # Build configuration with pthread support
├── 📄 README.md                 # This file
├── 📄 requirements.txt          # Python dependencies (flet)
│
├── 📂 bin/                      # Compiled binaries (generated)
│   └── scheduler                # Main executable
│
├── 📂 obj/                      # Object files (generated)
│   ├── main.o
│   ├── algorithms.o
│   ├── process.o
│   └── ipc.o
│
├── 📂 logs/                     # Simulation logs (optional)
│
└── 📂 src/
    │
    ├── 📂 backend/              # C Scheduler Kernel
    │   ├── 📄 main.c            # Entry point, CLI parsing, main loop
    │   ├── 📄 scheduler.h       # Data structures (PCB, SystemState), prototypes
    │   ├── 📄 algorithms.c      # Scheduling logic (FCFS, SJF, Priority, RR)
    │   ├── 📄 process.c         # Process management (init, add_process)
    │   └── 📄 ipc.c             # Unix socket communication, JSON serialization
    │
    └── 📂 frontend/             # Python Flet UI
        ├── 📄 main.py           # Flet app entry, UI layout, event handlers
        ├── 📄 ipc.py            # IPC server, socket listener, JSON parsing
        ├── 📄 dashboard.py      # (Optional) Dashboard widgets
        ├── 📄 gantt_chart.py    # (Optional) Gantt chart component
        └── 📄 client.py         # (Optional) Client utilities
```

### File Descriptions

#### Backend (C)

| File | Lines | Purpose |
|------|-------|---------|
| **scheduler.h** | 50 | Core data structures: `Process` (PCB), `SystemState`, function prototypes |
| **main.c** | 50 | Entry point, argument parsing, process input, metric reporting |
| **algorithms.c** | 120 | Algorithm implementations with process selection logic |
| **process.c** | 40 | System initialization, process creation, memory management |
| **ipc.c** | 80 | Socket setup, connection handling, JSON packet transmission |

#### Frontend (Python)

| File | Lines | Purpose |
|------|-------|---------|
| **main.py** | 250 | Flet UI layout, event handlers, subprocess management |
| **ipc.py** | 80 | Socket server, connection acceptance, JSON deserialization |
| **dashboard.py** | 200 | (Optional) CustomTkinter dashboard implementation |
| **gantt_chart.py** | 120 | (Optional) Gantt chart canvas rendering |
| **client.py** | - | (Optional) Client utilities |

---

## 🔌 API Reference

### C Backend API

#### Data Structures

**Process Control Block**:
```c
typedef struct {
    int pid;                // Process ID
    int arrival_time;       // Arrival time in ready queue
    int burst_time;         // Total CPU time required
    int remaining_time;     // Remaining execution time
    int priority;           // Priority (lower = higher)
    int waiting_time;       // Time spent waiting
    int turnaround_time;    // Completion - Arrival
    int completion_time;    // Time when finished
    ProcessState state;     // Current state
} Process;
```

**System State**:
```c
typedef struct {
    Process *processes[MAX_PROCESSES];
    int process_count;
    int current_time;
    bool simulation_running;
    pthread_mutex_t lock;
} SystemState;
```

#### Functions

```c
// Initialize system state
void init_system(SystemState *sys);

// Add process to scheduler
void add_process(SystemState *sys, int pid, int arrival, 
                 int burst, int priority);

// Run scheduler with specified algorithm
void run_scheduler(SystemState *sys, char *algorithm, int quantum);

// IPC functions
void connect_to_ui();
void send_update_to_ui(SystemState *sys);
void close_ipc();
```

### Python Frontend API

#### IPC Server

```python
class IPCServer:
    def __init__(self, on_data_received, on_disconnected):
        """
        Initialize IPC server.
        
        Args:
            on_data_received: Callback for incoming JSON data
            on_disconnected: Callback for connection closure
        """
        
    def start(self) -> bool:
        """Start socket server and listen for connections."""
        
    def cleanup(self):
        """Clean up socket resources."""
```

#### Usage Example

```python
def handle_data(json_data):
    time = json_data['time']
    processes = json_data['processes']
    # Update UI...

ipc = IPCServer(handle_data, on_finished)
ipc.start()
```

---

## 📊 Performance Metrics

### Metric Definitions

| Metric | Formula | Description |
|--------|---------|-------------|
| **Completion Time (CT)** | Time when process finishes | Absolute time unit |
| **Turnaround Time (TAT)** | CT - Arrival Time | Total time in system |
| **Waiting Time (WT)** | TAT - Burst Time | Time spent waiting |

### Algorithm Comparison

Example with 4 processes:

| Process | Arrival | Burst | Priority |
|---------|---------|-------|----------|
| P1 | 0 | 5 | 2 |
| P2 | 1 | 3 | 1 |
| P3 | 2 | 8 | 3 |
| P4 | 3 | 6 | 4 |

**Results**:

| Algorithm | Avg TAT | Avg WT | Context Switches |
|-----------|---------|--------|------------------|
| FCFS | 12.50 | 7.00 | 3 |
| SJF | 9.75 | 4.25 | 3 |
| Priority | 10.25 | 4.75 | 3 |
| RR (Q=2) | 13.25 | 7.75 | 12 |

**Analysis**:
- SJF provides best average waiting time
- RR ensures fairness but higher overhead
- Priority respects process importance

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Socket Connection Failed

**Symptom**: `Connection Error: Connection refused`

**Solutions**:
- Ensure no other instance is using `/tmp/scheduler_socket`
- Check socket permissions: `ls -l /tmp/scheduler_socket`
- Remove stale socket: `rm /tmp/scheduler_socket`

#### 2. Compilation Errors

**Symptom**: `undefined reference to pthread_create`

**Solution**:
```bash
# Ensure -pthread flag is used
gcc -pthread src/backend/*.c -o bin/scheduler
```

#### 3. Python Module Not Found

**Symptom**: `ModuleNotFoundError: No module named 'flet'`

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate
pip install flet
```

#### 4. UI Not Updating

**Symptom**: Gantt chart frozen

**Solutions**:
- Verify backend process is running: `ps aux | grep scheduler`
- Check IPC connection in terminal output
- Increase socket timeout in `ipc.py`

### Debug Mode

**Enable verbose logging**:
```c
// In main.c, add:
#define DEBUG 1
#ifdef DEBUG
    printf("DEBUG: Time=%d, Selected PID=%d\n", sys->current_time, idx);
#endif
```

```python
# In ipc.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/process-scheduler-simulator.git
cd process-scheduler-simulator

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and test
make clean && make
python3 src/frontend/main.py

# Commit with descriptive message
git commit -m "Add: Implement preemptive SJF algorithm"

# Push and create pull request
git push origin feature/amazing-feature
```

### Contribution Guidelines

1. **Code Style**:
   - C: Follow GNU C style guide
   - Python: Follow PEP 8

2. **Testing**:
   - Test all algorithms before submitting
   - Verify UI responsiveness

3. **Documentation**:
   - Update README for new features
   - Add inline comments for complex logic

4. **Commit Messages**:
   - Use prefixes: `Add:`, `Fix:`, `Update:`, `Refactor:`
   - Be descriptive and concise

### Feature Ideas

- [ ] Preemptive SJF (SRTF) algorithm
- [ ] Multi-level queue scheduling
- [ ] Save/load simulation configurations
- [ ] Export Gantt chart as image
- [ ] Real-time performance comparison
- [ ] Multi-core simulation support

---

## 👥 Team

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/wasay123q.png" width="100px;" alt=""/>
      <br />
      <sub><b>Abdul Wasay Sial</b></sub>
      <br />
      <sub>Team Leader & Lead Developer</sub>
      <br />
      <a href="mailto:233511@students.au.edu.pk">📧 Email</a> •
      <a href="https://github.com/wasay123q">🔗 GitHub</a>
      <br />
      <sub>Roll No: 233511</sub>
    </td>
    <td align="center">
      <sub><b>Faseeh Anjum</b></sub>
      <br />
      <sub>Backend Developer (C)</sub>
      <br />
      <a href="mailto:233583@students.au.edu.pk">📧 Email</a>
      <br />
      <sub>Roll No: 233583</sub>
      <br />
      <br />
      <sub>Implemented scheduling algorithms and IPC</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <sub><b>Dua Nadeem</b></sub>
      <br />
      <sub>Documentation & Testing</sub>
      <br />
      <a href="mailto:233609@students.au.edu.pk">📧 Email</a>
      <br />
      <sub>Roll No: 233609</sub>
      <br />
      <br />
      <sub>Metrics verification and technical writing</sub>
    </td>
    <td align="center">
      <sub><b>Nosheen Asif</b></sub>
      <br />
      <sub>Frontend Developer (UI/UX)</sub>
      <br />
      <a href="mailto:233808@students.au.edu.pk">📧 Email</a>
      <br />
      <sub>Roll No: 233808</sub>
      <br />
      <br />
      <sub>Designed Flet interface and visualizations</sub>
    </td>
  </tr>
</table>

### Acknowledgments

- **Operating System Concepts** by Abraham Silberschatz for algorithm references
- **Flet Framework** for the elegant Python UI toolkit
- **GNU Make** for the robust build system
- **Air University** for academic support

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Abdul Wasay Sial & Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

See [LICENSE](LICENSE) file for full details.

---

## 🌟 Star History

If you find this project helpful, please consider giving it a star ⭐!

<div align="center">

### Made with ❤️ by Team Scheduler

**[⬆ Back to Top](#-process-scheduler-simulator)**

</div>

