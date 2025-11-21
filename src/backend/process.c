#include "scheduler.h"
#include <string.h>

// Initialize the SystemState structure
void init_system(SystemState *sys) {
    sys->process_count = 0;
    sys->current_time = 0;
    sys->simulation_running = false;
    
    // Initialize the mutex for thread safety (Concurrency requirement)
    if (pthread_mutex_init(&sys->lock, NULL) != 0) {
        perror("Mutex init failed");
        exit(1);
    }
}

// Add a new process to the system
void add_process(SystemState *sys, int pid, int arrival, int burst, int priority) {
    if (sys->process_count >= MAX_PROCESSES) {
        printf("Error: Max process limit reached.\n");
        return;
    }

    // Allocate memory for the new process
    Process *p = (Process *)malloc(sizeof(Process));
    p->pid = pid;
    p->arrival_time = arrival;
    p->burst_time = burst;
    p->remaining_time = burst;
    p->priority = priority;
    
    // Initialize Metrics
    p->waiting_time = 0;
    p->turnaround_time = 0;
    p->completion_time = 0;
    p->state = STATE_READY;
    p->mlfq_data = NULL;  // Initialize MLFQ data as NULL

    // Add to the array (Critical Section protected by Mutex)
    pthread_mutex_lock(&sys->lock);
    sys->processes[sys->process_count++] = p;
    pthread_mutex_unlock(&sys->lock);
}