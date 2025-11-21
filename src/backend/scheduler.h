#ifndef SCHEDULER_H
#define SCHEDULER_H

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdbool.h>

// Maximum number of processes allowed in simulation
#define MAX_PROCESSES 100

// Process States (matches your proposal's "Process State Transition Monitor")
typedef enum {
    STATE_READY,
    STATE_RUNNING,
    STATE_WAITING,
    STATE_TERMINATED
} ProcessState;

// MLFQ (Multi-Level Feedback Queue) Data
// Used to track queue level, aging, and quantum usage
typedef struct {
    int queue_level;        // 0=High, 1=Medium, 2=Low
    int time_in_queue;      // For aging mechanism (prevent starvation)
    int quantum_used;       // Track quantum consumption in current burst
} MLFQData;

// Process Control Block (PCB) - The Core Structure
// This holds all the data for a single process [cite: 12, 14]
typedef struct {
    int pid;                // Process ID
    int arrival_time;       // Time process arrives in ready queue
    int burst_time;         // Total CPU time needed
    int remaining_time;     // Time left (for preemptive algorithms like RR)
    int priority;           // Priority (Lower # = Higher Priority)
    int waiting_time;       // Metric: Time spent in Ready Queue
    int turnaround_time;    // Metric: Completion Time - Arrival Time
    int completion_time;    // Time when execution finished
    ProcessState state;     // Current state
    MLFQData *mlfq_data;    // MLFQ-specific data (NULL if not using MLFQ)
} Process;

// System State - Shared Data Structure (Critical Section)
// This holds the global state of the simulation
typedef struct {
    Process *processes[MAX_PROCESSES]; // Array of pointers to processes
    int process_count;                 // Current number of processes
    int current_time;                  // Global simulation clock
    bool simulation_running;           // Flag to control the loop
    pthread_mutex_t lock;              // Mutex for thread synchronization [cite: 21]
} SystemState;

// --- Function Prototypes ---

// Initialization
void init_system(SystemState *sys);

// Process Management
void add_process(SystemState *sys, int pid, int arrival, int burst, int priority);

// Scheduling Logic
// algorithm: "FCFS", "SJF", "RR", "Priority"
void run_scheduler(SystemState *sys, char *algorithm, int quantum);

// IPC / Communication
void connect_to_ui();
void send_update_to_ui(SystemState *sys);
void close_ipc();

#endif