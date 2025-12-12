#include "scheduler.h"
#include <string.h>

void init_system(SystemState *sys) {
    sys->process_count = 0;
    sys->current_time = 0;
    sys->simulation_running = false;
    if (pthread_mutex_init(&sys->lock, NULL) != 0) {
        perror("Mutex init failed");
        exit(1);
    }
}

void add_process(SystemState *sys, int pid, int arrival, int burst, int priority) {
    if (sys->process_count >= MAX_PROCESSES) return;

    Process *p = (Process *)malloc(sizeof(Process));
    p->pid = pid;
    p->arrival_time = arrival;
    p->burst_time = burst;
    p->remaining_time = burst;
    p->priority = priority;
    p->waiting_time = 0;
    p->turnaround_time = 0;
    p->completion_time = 0;
    p->state = STATE_READY;
    p->mlfq_data = NULL; // Init to NULL

    pthread_mutex_lock(&sys->lock);
    sys->processes[sys->process_count++] = p;
    pthread_mutex_unlock(&sys->lock);
}