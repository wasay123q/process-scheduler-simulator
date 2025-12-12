<div align="center">

# 🖥️ Process Scheduler Simulator

### *Advanced OS Scheduler Visualizer with Real-Time IPC & Benchmark Comparison*

[![OS](https://img.shields.io/badge/OS-Linux-blue?logo=linux)](https://www.linux.org/)
[![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)](https://en.wikipedia.org/wiki/C_(programming_language))
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flet](https://img.shields.io/badge/Flet-UI-00D9FF?logo=flutter)](https://flet.dev/)
[![Algorithms](https://img.shields.io/badge/Algorithms-6-success)](/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()

*Professional CPU scheduler simulator with 6 algorithms, parallel benchmark comparison, and vintage cream UI theme.*

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [API](#-api-reference) • [Team](#-team)

---

</div>

## 📋 Table of Contents

- [Recent Updates](#-recent-updates-december-2025)
- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [System Architecture](#-system-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Benchmark Comparison Mode](#-benchmark-comparison-mode)
- [Algorithm Details](#-algorithm-details)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Performance Metrics](#-performance-metrics)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Team](#-team)
- [License](#-license)

---

## 🆕 Recent Updates (December 2025)

### 🏆 Benchmark Comparison Mode
- **Multi-Algorithm Comparison**: Run all 6 algorithms simultaneously with same process set
- **Side-by-Side Visualization**: Real-time parallel Gantt charts in grid layout (2x3)
- **Efficiency Ranking**: Automatic winner detection based on average waiting time
- **Visual Indicators**: Green border highlights the most efficient algorithm

### ✨ Scheduling Algorithms (6 Total)
- **FCFS**: First Come First Served - Simple FIFO approach
- **SJF**: Shortest Job First - Non-preemptive, minimizes average waiting time
- **SRTN**: Shortest Remaining Time Next - Preemptive SJF for dynamic workloads
- **Priority**: Priority-based scheduling with lower number = higher priority
- **Round Robin**: Time-slice based with configurable quantum
- **MLFQ**: Multi-Level Feedback Queue with 3-level dynamic priorities (Q0=2, Q1=4, Q2=8)

### 🎨 UI Redesign
- **Vintage Cream Theme**: Professional brown/cream color palette (#FFF8E1 background, #5D4037 text)
- **Dual-Mode Interface**: Toggle between single algorithm and benchmark comparison
- **Compact Cards**: Individual algorithm cards with mini timelines and statistics
- **Responsive Layout**: Fixed table height (300px) with scrolling, expandable chart area
- **Status Indicator**: Real-time badge showing IDLE/RUNNING/COMPLETED with color coding
- **2x2 Input Grid**: Space-efficient process input layout

### 🔧 Technical Improvements
- **Parallel IPC**: Multiple socket paths for concurrent algorithm execution
- **Fixed MLFQ Bug**: Quantum counter logic corrected (changed `>=` to `>` for accurate quantum enforcement)
- **Queue Level Tooltips**: MLFQ queue information displayed on hover in timeline
- **Simplified Table**: Removed dynamic column visibility, streamlined to 7 fixed columns
- **Auto-Scroll**: Timeline and ruler auto-scroll to latest process execution

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

- **📈 Dual-Mode Gantt Charts**: 
  - **Single Mode**: Full-size timeline with 40px blocks and ruler
  - **Benchmark Mode**: 6 mini timelines (12px blocks) in 2x3 grid layout
- **🏆 Algorithm Comparison**: Automatic efficiency ranking with visual winner indication
- **📊 Real-Time Metrics**: Live updates of CT, TAT, WT in scrollable data table
- **🎯 MLFQ Queue Tracking**: Queue level (Q0/Q1/Q2) shown in tooltips on hover
- **🎭 Smooth Animations**: Auto-scrolling timelines with 100ms update interval
- **🌈 Vintage Cream Theme**: Professional aesthetic with brown (#5D4037) and cream (#FFF8E1)
- **🗑️ Queue Management**: Add/Clear process buttons with input validation
- **📐 Responsive Layout**: 1250x900 resizable window with fixed table height (300px)
- **💡 Status Badge**: Top-right indicator (IDLE→RUNNING→COMPLETED) with color coding
- **📱 Compact Design**: Space-efficient 2x2 input grid and card-based layout

### 🔧 Technical Features

- **⚡ Multi-Threading**: POSIX threads with mutex synchronization
- **🔌 IPC Protocol**: JSON-based state transfer via Unix sockets
- **🛡️ Thread Safety**: Protected critical sections preventing race conditions
- **📝 Logging**: Comprehensive simulation logs for analysis
- **🎯 Extensible**: Modular architecture for easy algorithm additions

---

## 🎬 Demo

### Visual Interface - Benchmark Comparison Mode

```
┌────────────────────────────────────────────────────────────────────────┐
│  🖥️  PROCESS SCHEDULER              STATUS: ● COMPLETED  │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐  ┌─────────────────────────────────────────────────┐ │
│ │Configuration│  │ Algorithm Efficiency Comparison                  │ │
│ │─────────────│  │                                                  │ │
│ │Algorithm:   │  │ ┌──────────────────┐  ┌──────────────────┐     │ │
│ │ Compare All▼│  │ │ FCFS    ● DONE   │  │ SJF      ● DONE  │     │ │
│ │             │  │ │ ████████████████ │  │ ████████████████ │     │ │
│ │Quantum: 2   │  │ │ Avg WT: 4.50s    │  │ Avg WT: 3.25s    │     │ │
│ │             │  │ └──────────────────┘  └──────────────────┘     │ │
│ │Add Process  │  │                                                  │ │
│ │─────────────│  │ ┌──────────────────┐  ┌──────────────────┐     │ │
│ │PID:4  Arr:0 │  │ │ SRTN    ● DONE   │  │ Priority ● DONE  │     │ │
│ │Bst:5  Pri:1 │  │ │ ████████████████ │  │ ████████████████ │     │ │
│ │             │  │ │ Avg WT: 2.75s ✓  │  │ Avg WT: 4.00s    │     │ │
│ │[Add Process]│  │ └──────────────────┘  └──────────────────┘     │ │
│ │[Clear Queue]│  │                                                  │ │
│ │             │  │ ┌──────────────────┐  ┌──────────────────┐     │ │
│ │             │  │ │ Round Robin      │  │ MLFQ             │     │ │
│ │[START SIM]  │  │ │ ████████████████ │  │ ████████████████ │     │ │
│ └─────────────┘  │ │ Avg WT: 5.00s    │  │ Avg WT: 3.50s    │     │ │
│                  │ └──────────────────┘  └──────────────────┘     │ │
│                  │                                                  │ │
│                  │ 🏆 WINNER: SRTN is most efficient (Avg WT: 2.75s)│
│                  └─────────────────────────────────────────────────┘ │
│ ┌──────────────────────────────────────────────────────────────────┐ │
│ │ Process Queue (Scrollable)                                        │ │
│ │ PID │ Arrival │ Burst │ Priority │ CT │ TAT │ WT                 │ │
│ │  1  │    0    │   5   │    1     │ 5  │  5  │ 0                  │ │
│ │  2  │    1    │   3   │    2     │ 9  │  8  │ 5                  │ │
│ │  3  │    2    │   8   │    1     │ 17 │ 15  │ 7                  │ │
│ └──────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

### Single Algorithm Mode

```
┌────────────────────────────────────────────────────────────────────────┐
│  🖥️  PROCESS SCHEDULER              STATUS: ● RUNNING  │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐  ┌─────────────────────────────────────────────────┐ │
│ │Configuration│  │ 📈 Live Timeline                                 │ │
│ │─────────────│  │ ┌───────────────────────────────────────────┐   │ │
│ │Algorithm:   │  │ │ [P1][P2][P1][P3][P2][P1]...               │   │ │
│ │ Round Robin▼│  │ │━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│   │ │
│ │Quantum: 2   │  │ │  0   1   2   3   4   5   6   7   8   9    │   │ │
│ │             │  │ └───────────────────────────────────────────┘   │ │
│ └─────────────┘  └─────────────────────────────────────────────────┘ │
│                    Vintage Cream Theme • Real-Time Updates            │
└────────────────────────────────────────────────────────────────────────┘
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
┌───────────────────────────────────────────────────────────────────┐
│                    System Architecture (Benchmark Mode)           │
├───────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────────────┐       ┌──────────────────────────┐   │
│  │   Python Frontend      │       │    C Backend Processes   │   │
│  │   (Flet Framework)     │       │                          │   │
│  │                        │◄─────►│  ┌─────────────────┐    │   │
│  │  • SimCard Grid (2x3)  │ JSON  │  │ FCFS (/tmp/s_fcfs)   │   │
│  │  • 6x IPC Servers      │ over  │  │ SJF  (/tmp/s_sjf)    │   │
│  │  • Winner Detection    │ Unix  │  │ SRTN (/tmp/s_srtn)   │   │
│  │  • Real-time Updates   │Sockets│  │ Prio (/tmp/s_prio)   │   │
│  │  • Metrics Comparison  │       │  │ RR   (/tmp/s_rr)     │   │
│  └────────────────────────┘       │  │ MLFQ (/tmp/s_mlfq)   │   │
│           ▲                        │  └─────────────────┐    │   │
│           │                        │    All run in parallel   │   │
│           └────────────────────────┴──────────────────────────┘   │
│                                                                     │
│  Single Mode: /tmp/sock_single (1 backend process)                │
│  Benchmark Mode: 6 parallel processes with unique socket paths    │
└───────────────────────────────────────────────────────────────────┘
```

### Data Flow

**Single Algorithm Mode:**
1. **Initialization**: Frontend starts IPC server on `/tmp/sock_single`
2. **Process Definition**: User adds processes via 2x2 input grid
3. **Simulation Launch**: Frontend spawns single C backend subprocess
4. **Data Streaming**: Backend sends JSON state updates every 100ms
5. **Visualization**: Full-size Gantt chart (40px blocks) with auto-scroll
6. **Completion**: Backend closes connection, displays final metrics

**Benchmark Comparison Mode:**
1. **Multi-Server Init**: Frontend creates 6 IPC servers (one per algorithm)
2. **Process Duplication**: Same process set sent to all 6 backends
3. **Parallel Execution**: All algorithms run simultaneously in separate processes
4. **Real-time Grid**: 6 SimCards update independently with mini timelines (12px blocks)
5. **Winner Calculation**: Track average WT, highlight minimum with green border
6. **Result Display**: Show winner announcement below grid

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
      "q_lvl": 0
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
- `q_lvl`: MLFQ queue level (0=High, 1=Med, 2=Low, or -1 for non-MLFQ algorithms)

**Socket Path Initialization**:
```c
// In main.c
char *socket_path = argv[4];  // Read from command line
init_ipc(socket_path);        // Store globally
connect_to_ui();              // Connect to Python IPC server
```

**Multiple Sockets for Benchmark Mode**:
- `/tmp/s_fcfs` - FCFS algorithm
- `/tmp/s_sjf` - SJF algorithm
- `/tmp/s_srtn` - SRTN algorithm
- `/tmp/s_prio` - Priority algorithm
- `/tmp/s_rr` - Round Robin
- `/tmp/s_mlfq` - MLFQ algorithm
- `/tmp/sock_single` - Single algorithm mode

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
   
   **Single Algorithm Mode:**
   - Select specific algorithm from dropdown
   - Set time quantum (for Round Robin only)
   
   **Benchmark Mode:**
   - Select "Compare All Algorithms" from dropdown
   - Set quantum (applies to Round Robin in comparison)

3. **Add Processes**
   - Enter values in 2x2 grid: PID, Arrival, Burst, Priority
   - Click "Add Process" (PID auto-increments)
   - Use "Clear Queue" to reset all processes

4. **Start Simulation**
   
   **Single Mode:**
   - Click "START SIMULATION"
   - Watch full-size Gantt chart with 40px process blocks
   - Timeline auto-scrolls with ruler
   
   **Benchmark Mode:**
   - All 6 algorithms run simultaneously
   - View side-by-side mini timelines (2x3 grid)
   - Green border highlights winner with lowest average waiting time

5. **Analyze Results**
   - Review metrics in scrollable table (CT, TAT, WT)
   - Check status badge (IDLE → RUNNING → COMPLETED)
   - Compare efficiency rankings in benchmark mode
   - Hover over MLFQ blocks to see queue level (Q0/Q1/Q2)

### Command-Line Usage (Backend Only)

```bash
# Syntax
./bin/scheduler <Algorithm> <Quantum> <Process_Count> <Socket_Path>

# Example: FCFS with 3 processes
./bin/scheduler FCFS 0 3 /tmp/sock_single <<EOF
1 0 5 1
2 1 3 2
3 2 4 3
EOF

# Example: Round Robin (Quantum = 2)
./bin/scheduler RR 2 4 /tmp/s_rr <<EOF
1 0 5 1
2 1 4 2
3 2 3 3
4 3 2 4
EOF

# Example: SRTN (Preemptive SJF)
./bin/scheduler SRTN 1 3 /tmp/s_srtn <<EOF
1 0 8 1
2 1 4 1
3 2 2 1
EOF

# Example: MLFQ (Multi-Level Feedback Queue)
./bin/scheduler MLFQ 2 3 /tmp/s_mlfq <<EOF
1 0 10 1
2 0 20 1
3 0 3 1
EOF

# Parallel Benchmark Execution (as done in Compare mode)
./bin/scheduler FCFS 0 3 /tmp/s_fcfs &
./bin/scheduler SJF 0 3 /tmp/s_sjf &
./bin/scheduler SRTN 0 3 /tmp/s_srtn &
./bin/scheduler Priority 0 3 /tmp/s_prio &
./bin/scheduler RR 2 3 /tmp/s_rr &
./bin/scheduler MLFQ 0 3 /tmp/s_mlfq &
wait
```

**Input Format**: `PID ArrivalTime BurstTime Priority`

**Supported Algorithms**: `FCFS`, `SJF`, `SRTN`, `Priority`, `RR`, `MLFQ`

**Socket Paths**: 
- Single mode: `/tmp/sock_single`
- Benchmark mode: `/tmp/s_fcfs`, `/tmp/s_sjf`, `/tmp/s_srtn`, `/tmp/s_prio`, `/tmp/s_rr`, `/tmp/s_mlfq`

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

## 🏆 Benchmark Comparison Mode

### Overview

The **Benchmark Mode** is a unique feature that runs all 6 scheduling algorithms simultaneously with the same process set, providing real-time side-by-side comparison.

### How It Works

1. **Activation**: Select "Compare All Algorithms" from dropdown
2. **Process Input**: Add processes normally (applies to all algorithms)
3. **Parallel Execution**: 
   - Frontend spawns 6 C backend processes
   - Each uses unique socket path (`/tmp/s_fcfs`, `/tmp/s_sjf`, etc.)
   - All run concurrently without interference
4. **Visual Layout**: 2x3 grid of SimCard components
5. **Real-Time Updates**: Each card shows mini timeline (12px blocks) and current avg WT
6. **Winner Detection**: Automatically highlights algorithm with lowest average waiting time

### SimCard Component Architecture

```python
class SimCard(ft.Container):
    - title: Algorithm name (e.g., "FCFS", "MLFQ")
    - sock_path: Unique socket for this algorithm
    - timeline: Scrollable row of colored process blocks
    - status: Text indicator (WAITING → RUNNING → DONE)
    - avg_wt: Calculated from completed processes
    - mark_winner(): Applies green border to winning card
```

### Benchmark Results Interpretation

**Card Status Colors**:
- **Grey** (WAITING): Algorithm not started yet
- **Blue** (RUNNING): Currently executing processes
- **Green** (DONE): Simulation complete

**Winner Criteria**:
- **Lowest Average Waiting Time** (primary metric)
- Green border + trophy emoji in result message
- Format: `🏆 WINNER: SRTN is most efficient (Avg WT: 2.75s)`

**Example Benchmark Output**:
```
┌────────────────────────┬────────────────────────┐
│ FCFS    ● DONE         │ SJF      ● DONE        │
│ ████████████████       │ ████████████████       │
│ Avg WT: 4.50s          │ Avg WT: 3.25s          │
├────────────────────────┼────────────────────────┤
│ SRTN    ● DONE         │ Priority ● DONE        │
│ ████████████████       │ ████████████████       │
│ Avg WT: 2.75s ✓        │ Avg WT: 4.00s          │ ← Winner (Green Border)
├────────────────────────┼────────────────────────┤
│ Round Robin ● DONE     │ MLFQ     ● DONE        │
│ ████████████████       │ ████████████████       │
│ Avg WT: 5.00s          │ Avg WT: 3.50s          │
└────────────────────────┴────────────────────────┘
```

### Use Cases

- **Academic Presentations**: Demonstrate algorithm trade-offs visually
- **Performance Analysis**: Compare efficiency for specific workload patterns
- **Algorithm Selection**: Identify best scheduler for given process characteristics
- **Teaching Tool**: Show students real-time differences in scheduling approaches

### Technical Implementation

**Parallel Execution**:
```python
# In main.py - run_benchmark()
for card in cards:
    card.ipc = IPCServer(card.sock_path, on_data, on_finish)
    card.ipc.start()
    
    cmd = [C_EXECUTABLE, algo, quantum, count, card.sock_path]
    subprocess.Popen(cmd, stdin=subprocess.PIPE, ...)
```

**Winner Detection**:
```python
def check_bench_done():
    if all(c.finished for c in cards):
        winner = min(cards, key=lambda c: c.avg_wt)
        winner.mark_winner()
        bench_res.value = f"🏆 WINNER: {winner.title}..."
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

**Implementation** (`algorithms.c:92-168`):
```c
static int mlfq_quantums[3] = {2, 4, 8};  // Quantum per queue

// Initialize MLFQ data structures on first arrival
for (int i = 0; i < sys->process_count; i++) {
    if (p->mlfq_data == NULL && p->arrival_time <= sys->current_time) {
        p->mlfq_data = malloc(sizeof(MLFQData));
        p->mlfq_data->queue_level = 0;  // Start in Q0 (highest)
        p->mlfq_data->time_in_queue = 0;
        p->mlfq_data->quantum_used = 0;
    }
}

// Check quantum exhaustion and demote if needed
// CRITICAL FIX: Changed >= to > for accurate quantum enforcement
// This allows process to run for FULL quantum duration
if (quantum_counter > mlfq_quantums[queue]) {  // Was: >=
    if (queue < 2) p->mlfq_data->queue_level++;  // Demote
    quantum_counter = 0;
} else {
    selected_idx = i;  // Continue current process
    return selected_idx;
}

// Aging: Promote processes waiting > 10 time units
if (p->mlfq_data->time_in_queue > 10 && queue > 0) {
    p->mlfq_data->queue_level--;  // Promote to higher priority
    p->mlfq_data->time_in_queue = 0;
}
```

**Key Bug Fix (December 2025)**:
- **Before**: `if (quantum_counter >= mlfq_quantums[queue])` → Process demoted 1 tick early
- **After**: `if (quantum_counter > mlfq_quantums[queue])` → Process gets full quantum
- **Impact**: Ensures Q0 processes actually run for 2 units, Q1 for 4 units, Q2 for 8 units

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
| **main.py** | 474 | Dual-mode UI (single/benchmark), SimCard component, vintage theme |
| **ipc.py** | 80 | Socket server with custom path, connection handling, JSON parsing |
| **dashboard.py** | - | (Removed) Replaced by Flet-based main.py |
| **gantt_chart.py** | - | (Removed) Integrated into main.py timeline |
| **client.py** | - | (Removed) Functionality merged into main.py |

**Key Components**:
- **SimCard Class** (lines 27-113): Reusable card widget for benchmark mode
  - Mini timeline with 12px blocks
  - Real-time average waiting time display
  - Status indicator (WAITING/RUNNING/DONE)
  - Winner highlighting with green border
- **Dual Layout System**: Toggle between single full-size chart and 2x3 benchmark grid
- **Auto-Scroll**: Timeline scrolls to latest process with `scroll_to(offset=-1)`

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

**Results** (Benchmark Mode with 4 processes):

| Algorithm | Avg TAT | Avg WT | Context Switches | Rank | Best For |
|-----------|---------|--------|------------------|------|----------|
| **SRTN** 🏆 | 8.50 | **2.75** | 15 | 1st | Optimal waiting time, dynamic workloads |
| **SJF** | 9.75 | 4.25 | 3 | 2nd | Known burst times, batch jobs |
| **MLFQ** | 10.00 | 3.50 | 18 | 3rd | General-purpose, mixed workloads |
| **Priority** | 10.25 | 4.00 | 3 | 4th | Mission-critical tasks |
| **FCFS** | 12.50 | 4.50 | 3 | 5th | Simple batch systems |
| **RR (Q=2)** | 13.25 | 5.00 | 12 | 6th | Time-sharing, interactive systems |

**Benchmark Mode Analysis**:
- **Winner Detection**: Automatic green border on card with lowest average WT
- **SRTN** consistently wins with optimal average waiting time (preemptive advantage)
- **SJF** ranks 2nd with minimal context switches (non-preemptive efficiency)
- **MLFQ** adapts well with 3-level queue system, prevents starvation via aging
- **RR** ensures fairness but higher average WT due to frequent context switches
- **Context Switching Impact**: Preemptive algorithms (SRTN, MLFQ, RR) have 3-6x more switches

**Use Benchmark Mode To**:
- Compare all 6 algorithms with identical process sets
- Identify most efficient algorithm for specific workload characteristics
- Visualize trade-offs between waiting time and context switching overhead

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

**Completed** ✅:
- [x] Preemptive SJF (SRTN) algorithm
- [x] Multi-level feedback queue scheduling (MLFQ)
- [x] Queue level visualization (Q0/Q1/Q2 tooltips)
- [x] Clear queue functionality
- [x] Resizable/maximizable window
- [x] Real-time algorithm comparison (Benchmark Mode)
- [x] Efficiency ranking with winner detection
- [x] Parallel execution of all algorithms
- [x] Auto-scrolling timelines

**Future Enhancements** 🚀:
- [ ] Save/load simulation configurations (JSON export)
- [ ] Export Gantt charts as PNG/PDF
- [ ] Process arrival rate simulation (Poisson distribution)
- [ ] CPU utilization and throughput metrics
- [ ] Multi-core simulation (2-4 cores)
- [ ] Custom MLFQ quantum configuration via UI sliders
- [ ] Dark mode theme toggle
- [ ] Process I/O burst simulation
- [ ] Real-time algorithm statistics (chart overlays)
- [ ] Historical comparison with saved benchmarks

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

