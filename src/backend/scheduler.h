#ifndef SCHEDULER_H
#define SCHEDULER_H

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdbool.h>

#define MAX_PROCESSES 100

typedef enum {
    STATE_READY,
    STATE_RUNNING,
    STATE_WAITING,
    STATE_TERMINATED
} ProcessState;

// MLFQ Specific Data Structure
typedef struct {
    int queue_level;      // Current Queue (0, 1, 2)
    int time_in_queue;    // For Aging
    int quantum_used;     // Tracks time used in current quantum
} MLFQData;

// Process Control Block (PCB)
typedef struct {
    int pid;
    int arrival_time;
    int burst_time;
    int remaining_time;
    int priority;
    int waiting_time;
    int turnaround_time;
    int completion_time;
    ProcessState state;
    
    // Pointer to MLFQ specific data (NULL for other algorithms)
    MLFQData *mlfq_data; 
} Process;

typedef struct {
    Process *processes[MAX_PROCESSES];
    int process_count;
    int current_time;
    bool simulation_running;
    pthread_mutex_t lock;
} SystemState;

// --- Function Prototypes ---
void init_system(SystemState *sys);
void add_process(SystemState *sys, int pid, int arrival, int burst, int priority);
void run_scheduler(SystemState *sys, char *algorithm, int quantum);

// IPC
void init_ipc(char *socket_path);
void connect_to_ui();
void send_update_to_ui(SystemState *sys);
void close_ipc();

#endif