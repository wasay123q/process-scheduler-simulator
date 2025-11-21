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

## 🆕 Recent Updates (November 2025)

### ✨ New Algorithms
- **SRTN (Shortest Remaining Time Next)**: Preemptive SJF providing optimal average waiting time
- **MLFQ (Multi-Level Feedback Queue)**: Real-world scheduler with 3-level dynamic priority queues

### 🎨 UI Enhancements
- **Material Design 3**: Modern cream/golden light theme for professional aesthetics
- **Queue Level Tracking**: Live display of MLFQ queue assignments (Q0/Q1/Q2) with color coding
- **Clear Queue Button**: Quick process removal without restarting application
- **Resizable Window**: Maximize, minimize, and resize window for better viewing
- **Grid Lines**: Timeline grid overlay for precise time visualization
- **Contextual Help**: Algorithm-specific info boxes (MLFQ quantum details, RR time slice)

### 🔧 Technical Improvements
- **Dynamic Column Visibility**: Queue column appears only for MLFQ algorithm
- **Enhanced IPC**: Queue level data transmission in JSON protocol
- **Aging Mechanism**: MLFQ prevents starvation via automatic priority promotion
- **Memory Management**: Proper cleanup of MLFQ data structures

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
| **SRTN** | Preemptive | Shortest Remaining Time Next | Preemptive SJF, optimal average waiting time |
| **Priority** | Non-Preemptive | Priority-based selection | Lower number = higher priority |
| **Round Robin** | Preemptive | Time-slice based scheduling | Fairness with configurable quantum |
| **MLFQ** | Preemptive | Multi-Level Feedback Queue | Real-world scheduler with dynamic priorities |

### 🎨 Visualization Features

- **📈 Real-Time Gantt Chart**: Live timeline visualization with color-coded processes and grid lines
- **📊 Process State Monitoring**: Track process states (Ready, Running, Waiting, Terminated)
- **📉 Metrics Dashboard**: Real-time computation of CT, TAT, and WT
- **🎯 MLFQ Queue Tracking**: Dynamic queue level display (Q0/Q1/Q2) with color coding
- **🎭 Smooth Animations**: 60 FPS synchronized rendering (100ms tick rate)
- **🌈 Material Design 3**: Cream/golden light theme with professional aesthetics
- **🗑️ Queue Management**: Clear queue button for quick process removal
- **📐 Responsive Layout**: Resizable, maximizable, and minimizable window
- **ℹ️ Contextual Help**: Algorithm-specific configuration info boxes

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
┌──────────────────────────────────────────────────────────────────────┐
│  🖥️  PROCESS SCHEDULER                         STATUS: COMPLETED ✓  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌────────────────────┐  ┌───────────────────────────────────────┐  │
│  │  CONFIGURATION     │  │      LIVE TIMELINE (Grid View)        │  │
│  ├────────────────────┤  │  ┌───┬───┬───┬───┬───┬───┬───┬───┐   │  │
│  │ Algorithm: MLFQ ▼  │  │  │P1 │P2 │P3 │P1 │P2 │P3 │P1 │P2 │   │  │
│  │                    │  │  └───┴───┴───┴───┴───┴───┴───┴───┘   │  │
│  │ ℹ️ MLFQ Queues     │  │  │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │   │  │
│  │ Q0: Quantum=2      │  └───────────────────────────────────────┘  │
│  │ Q1: Quantum=4      │                                              │
│  │ Q2: Quantum=8      │  ┌───────────────────────────────────────┐  │
│  │ New → Q0           │  │      PROCESS QUEUE (Scrollable)       │  │
│  │                    │  ├────┬─────┬─────┬──────┬───┬────┬────┬───┤│
│  │ ADD PROCESS        │  │PID │Arr. │Burst│Prior.│ Q │ CT │TAT │WT ││
│  │ PID: 4             │  ├────┼─────┼─────┼──────┼───┼────┼────┼───┤│
│  │ Arrival: 0         │  │ 1  │  0  │  6  │  1   │Q1 │ 13 │ 13 │ 7 ││
│  │ Burst: 5           │  │ 2  │  0  │ 20  │  1   │Q2 │ 29 │ 29 │ 9 ││
│  │ Priority: 1        │  │ 3  │  0  │  3  │  1   │Q0 │ 11 │ 11 │ 8 ││
│  │                    │  └────┴─────┴─────┴──────┴───┴────┴────┴───┘│
│  │ [➕ Add Process]   │                                              │
│  │ [🗑️ Clear Queue]   │  Material Design 3 • Cream/Golden Theme    │
│  │                    │  Resizable • Grid Lines • Queue Tracking    │
│  │ [▶️ START]         │                                              │
│  └────────────────────┘                                              │
└──────────────────────────────────────────────────────────────────────┘
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
      "wt": 0,
      "queue": 0
    }
  ]
}
```

**Fields**:
- `time`: Current simulation time
- `pid`: Process ID
- `state`: Process state (0=Ready, 1=Running, 2=Waiting, 3=Terminated)
- `remaining`: Remaining burst time
- `ct`: Completion time (0 if not completed)
- `tat`: Turnaround time (0 if not completed)
- `wt`: Waiting time (0 if not completed)
- `queue`: MLFQ queue level (0-2, or -1 for non-MLFQ algorithms)

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

# Example: SRTN (Preemptive SJF)
./bin/scheduler SRTN 1 3 <<EOF
1 0 8 1
2 1 4 1
3 2 2 1
EOF

# Example: MLFQ (Multi-Level Feedback Queue)
./bin/scheduler MLFQ 2 3 <<EOF
1 0 10 1
2 0 20 1
3 0 3 1
EOF
```

**Input Format**: `PID ArrivalTime BurstTime Priority`

**Supported Algorithms**: `FCFS`, `SJF`, `SRTN`, `Priority`, `RR`, `MLFQ`

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

### SRTN (Shortest Remaining Time Next)

**Characteristics**:
- Preemptive version of SJF
- Selects process with minimum remaining time
- Optimal for minimizing average waiting time
- Can preempt currently running process

**Implementation** (`algorithms.c:53-65`):
```c
int min_remaining = 999999;
for (int i = 0; i < sys->process_count; i++) {
    Process *p = sys->processes[i];
    if (p->state != STATE_TERMINATED && 
        p->arrival_time <= sys->current_time) {
        if (p->remaining_time < min_remaining) {
            min_remaining = p->remaining_time;
            selected_idx = i;
        }
    }
}
```

**Pros**: Optimal average waiting time, responsive to short jobs  
**Cons**: High context switching, starvation for long processes, requires burst time knowledge

---

### MLFQ (Multi-Level Feedback Queue)

**Characteristics**:
- **3-level priority queues** (Q0=High, Q1=Medium, Q2=Low)
- **Dynamic priority adjustment** based on CPU usage
- **Variable time quantums**: Q0=2 units, Q1=4 units, Q2=8 units
- **Aging mechanism** prevents starvation
- **Preemptive** - new processes preempt lower-priority ones

**Implementation** (`algorithms.c:67-140`):
```c
static int mlfq_quantums[3] = {2, 4, 8};  // Quantum per queue

// Initialize MLFQ data structures
for (int i = 0; i < sys->process_count; i++) {
    if (p->mlfq_data == NULL) {
        p->mlfq_data = malloc(sizeof(MLFQData));
        p->mlfq_data->queue_level = 0;  // Start in Q0
    }
}

// Check quantum exhaustion and demote if needed
if (quantum_counter >= mlfq_quantums[queue]) {
    if (queue < 2) p->mlfq_data->queue_level++;  // Demote
    quantum_counter = 0;
}

// Aging: Promote processes waiting > 10 time units
if (p->mlfq_data->time_in_queue > 10 && queue > 0) {
    p->mlfq_data->queue_level--;  // Promote
}
```

**Queue Behavior**:
- **Q0 (Interactive)**: Short quantum (2), high priority, minimal latency
- **Q1 (Mixed)**: Medium quantum (4), balanced performance
- **Q2 (Batch)**: Long quantum (8), CPU-bound tasks

**Pros**: Balances responsiveness and throughput, favors interactive processes, prevents starvation via aging  
**Cons**: Complex implementation, requires tuning quantum values, more context switches

**Real-World Usage**: Similar algorithms used in Windows, macOS, Linux CFS

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
| **scheduler.h** | 60 | Core data structures: `Process` (PCB), `MLFQData`, `SystemState`, prototypes |
| **main.c** | 60 | Entry point, argument parsing, process input, cleanup, metric reporting |
| **algorithms.c** | 200 | 6 algorithm implementations (FCFS, SJF, SRTN, Priority, RR, MLFQ) |
| **process.c** | 45 | System initialization, process creation, MLFQ data setup |
| **ipc.c** | 90 | Socket setup, connection handling, JSON transmission with queue data |

#### Frontend (Python)

| File | Lines | Purpose |
|------|-------|---------|
| **main.py** | 615 | Material Design 3 UI, Gantt chart, queue tracking, algorithm selection |
| **ipc.py** | 80 | Socket server, connection acceptance, JSON deserialization |
| **dashboard.py** | 200 | (Legacy) CustomTkinter dashboard implementation |
| **gantt_chart.py** | 120 | (Legacy) Gantt chart canvas rendering |
| **client.py** | - | (Legacy) Client utilities |

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
    MLFQData *mlfq_data;    // MLFQ queue level data (NULL if not MLFQ)
} Process;
```

**MLFQ Data Structure**:
```c
typedef struct {
    int queue_level;        // 0=High, 1=Medium, 2=Low
    int time_in_queue;      // For aging mechanism
    int quantum_used;       // Track quantum consumption
} MLFQData;
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

| Algorithm | Avg TAT | Avg WT | Context Switches | Best For |
|-----------|---------|--------|------------------|----------|
| FCFS | 12.50 | 7.00 | 3 | Simple batch systems |
| SJF | 9.75 | 4.25 | 3 | Known burst times, batch jobs |
| SRTN | 8.50 | 3.00 | 15 | Optimal waiting time, dynamic workloads |
| Priority | 10.25 | 4.75 | 3 | Mission-critical tasks |
| RR (Q=2) | 13.25 | 7.75 | 12 | Time-sharing, interactive systems |
| MLFQ | 10.00 | 4.50 | 18 | General-purpose, mixed workloads |

**Analysis**:
- **SRTN** provides optimal average waiting time but highest context switching
- **SJF** balances performance with low overhead (non-preemptive)
- **RR** ensures fairness with predictable response times
- **MLFQ** adapts to workload characteristics, favoring interactive processes
- **Priority** respects process importance but risks starvation

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

- [x] Preemptive SJF (SRTN) algorithm ✅
- [x] Multi-level feedback queue scheduling ✅
- [x] Queue level visualization for MLFQ ✅
- [x] Clear queue functionality ✅
- [x] Resizable/maximizable window ✅
- [ ] Save/load simulation configurations
- [ ] Export Gantt chart as image/PDF
- [ ] Real-time algorithm performance comparison
- [ ] Multi-core simulation support
- [ ] Custom MLFQ quantum configuration via UI
- [ ] Process arrival rate simulation (Poisson distribution)
- [ ] CPU utilization and throughput metrics

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

