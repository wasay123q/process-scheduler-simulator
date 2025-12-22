#include "scheduler.h"
#include <unistd.h> 
#include <string.h>
#include <stdlib.h> 
#include <stdio.h>
#include <stdbool.h>

// --- QUEUE HELPERS FOR ROUND ROBIN ---
#define MAX_Q 200
static int rr_queue[MAX_Q];
static int rr_front = 0;
static int rr_rear = 0;
static int rr_count = 0;
static int rr_enqueued_tracker[MAX_Q]; 

void enqueue(int pid_idx) {
    if (rr_count >= MAX_Q) return;
    rr_queue[rr_rear] = pid_idx;
    rr_rear = (rr_rear + 1) % MAX_Q;
    rr_count++;
}

int dequeue() {
    if (rr_count == 0) return -1;
    int pid_idx = rr_queue[rr_front];
    rr_front = (rr_front + 1) % MAX_Q;
    rr_count--;
    return pid_idx;
}

// Static variables for Round Robin algorithm
static int rr_quantum_timer = 0;
static int rr_current_proc_idx = -1;

// Static variables for MLFQ Round Robin Rotation
static int mlfq_rr_start_idx[3] = {0, 0, 0}; // Track search start for each queue

int select_process(SystemState *sys, char *algorithm, int quantum) {
    int selected_idx = -1;

    // --- FCFS ---
    if (strcmp(algorithm, "FCFS") == 0) {
        for (int i = 0; i < sys->process_count; i++) {
            Process *p = sys->processes[i];
            if (p->state != STATE_TERMINATED && p->arrival_time <= sys->current_time) {
                if (selected_idx == -1 || p->arrival_time < sys->processes[selected_idx]->arrival_time) {
                    selected_idx = i;
                }
            }
        }
    }
    // --- SJF (Non-Preemptive) ---
    else if (strcmp(algorithm, "SJF") == 0) {
        for (int i = 0; i < sys->process_count; i++) {
            if (sys->processes[i]->state == STATE_RUNNING) {
                return i;
            }
        }
        int min_burst = 999999;
        for (int i = 0; i < sys->process_count; i++) {
            Process *p = sys->processes[i];
            if (p->state != STATE_TERMINATED && p->arrival_time <= sys->current_time) {
                if (p->burst_time < min_burst) {
                    min_burst = p->burst_time;
                    selected_idx = i;
                }
            }
        }
    }
    // --- Priority (Non-Preemptive) ---
    else if (strcmp(algorithm, "Priority") == 0) {
        for (int i = 0; i < sys->process_count; i++) {
            if (sys->processes[i]->state == STATE_RUNNING) {
                return i;
            }
        }
        int highest_priority = 999999;
        for (int i = 0; i < sys->process_count; i++) {
            Process *p = sys->processes[i];
            if (p->state != STATE_TERMINATED && p->arrival_time <= sys->current_time) {
                if (p->priority < highest_priority) {
                    highest_priority = p->priority;
                    selected_idx = i;
                }
            }
        }
    }
    // --- SRTN (Preemptive) ---
    else if (strcmp(algorithm, "SRTN") == 0) {
        int min_remaining = 999999;
        for (int i = 0; i < sys->process_count; i++) {
            Process *p = sys->processes[i];
            if (p->state != STATE_TERMINATED && p->arrival_time <= sys->current_time) {
                if (p->remaining_time < min_remaining) {
                    min_remaining = p->remaining_time;
                    selected_idx = i;
                }
            }
        }
    }
    // --- RR (Standard FIFO) ---
    else if (strcmp(algorithm, "RR") == 0) {
        if (sys->current_time == 0) {
            rr_front = 0; rr_rear = 0; rr_count = 0;
            rr_quantum_timer = 0;
            rr_current_proc_idx = -1;
            for(int k=0; k<MAX_Q; k++) rr_enqueued_tracker[k] = 0;
        }

        for (int i = 0; i < sys->process_count; i++) {
            Process *p = sys->processes[i];
            if (p->arrival_time <= sys->current_time && 
                p->state != STATE_TERMINATED && 
                rr_enqueued_tracker[i] == 0) {
                enqueue(i);
                rr_enqueued_tracker[i] = 1;
            }
        }

        if (rr_current_proc_idx != -1) {
            Process *curr = sys->processes[rr_current_proc_idx];
            if (curr->state == STATE_TERMINATED) {
                rr_current_proc_idx = -1;
                rr_quantum_timer = 0;
            } else {
                if (rr_quantum_timer < quantum) {
                    rr_quantum_timer++;
                    return rr_current_proc_idx;
                } else {
                    enqueue(rr_current_proc_idx);
                    rr_current_proc_idx = -1;
                    rr_quantum_timer = 0;
                }
            }
        }

        if (rr_current_proc_idx == -1) {
            int next_idx = dequeue();
            if (next_idx != -1) {
                rr_current_proc_idx = next_idx;
                rr_quantum_timer = 1; 
                return rr_current_proc_idx;
            }
        }
        return -1;
    }
    // --- MLFQ (With Round Robin Rotation) ---
    else if (strcmp(algorithm, "MLFQ") == 0) {
        static int mlfq_quantums[3] = {2, 4, 8};
        static int last_pid = -1;
        static int quantum_counter = 0;
        
        if (sys->current_time == 0) {
            last_pid = -1;
            quantum_counter = 0;
            mlfq_rr_start_idx[0] = 0;
            mlfq_rr_start_idx[1] = 0;
            mlfq_rr_start_idx[2] = 0;
        }
        
        // Init data
        for (int i = 0; i < sys->process_count; i++) {
            Process *p = sys->processes[i];
            if (p->mlfq_data == NULL && p->arrival_time <= sys->current_time) {
                p->mlfq_data = (MLFQData *)malloc(sizeof(MLFQData));
                p->mlfq_data->queue_level = 0;
                p->mlfq_data->time_in_queue = 0;
                p->mlfq_data->quantum_used = 0;
            }
        }
        
        // Continue current process if possible
        if (last_pid != -1) {
            for (int i = 0; i < sys->process_count; i++) {
                if (sys->processes[i]->pid == last_pid) {
                    Process *p = sys->processes[i];
                    if (p->state != STATE_TERMINATED && p->mlfq_data != NULL) {
                        int queue = p->mlfq_data->queue_level;
                        quantum_counter++;
                        
                        if (quantum_counter > mlfq_quantums[queue]) { 
                            // Demote and Reset
                            if (queue < 2) p->mlfq_data->queue_level++;
                            p->mlfq_data->quantum_used = 0;
                            quantum_counter = 0;
                            last_pid = -1; 
                            
                            // Important: Don't return here. Let the scheduler pick the NEXT process.
                            // This ensures fairness immediately.
                        } else {
                            selected_idx = i;
                            return selected_idx;
                        }
                    } else {
                         // Process finished or something weird happened
                         last_pid = -1;
                    }
                    break;
                }
            }
        }
        
        // Find process by scanning queues 0->1->2 with Rotation
        for (int queue = 0; queue <= 2; queue++) {
            int start_k = mlfq_rr_start_idx[queue];
            
            // Loop count times to scan everyone once
            for (int k = 0; k < sys->process_count; k++) {
                int idx = (start_k + k) % sys->process_count; // Wrap around
                Process *p = sys->processes[idx];
                
                if (p->state != STATE_TERMINATED && p->arrival_time <= sys->current_time &&
                    p->mlfq_data != NULL && p->mlfq_data->queue_level == queue) {
                    
                    selected_idx = idx;
                    last_pid = p->pid;
                    quantum_counter = 1;
                    p->mlfq_data->time_in_queue = 0;
                    
                    // Save position for NEXT search to ensure rotation
                    mlfq_rr_start_idx[queue] = (idx + 1) % sys->process_count;
                    return selected_idx;
                }
            }
        }
        
        // Aging
        for (int i = 0; i < sys->process_count; i++) {
            Process *p = sys->processes[i];
            if (p->state == STATE_READY && p->mlfq_data != NULL) {
                p->mlfq_data->time_in_queue++;
                if (p->mlfq_data->time_in_queue > 10 && p->mlfq_data->queue_level > 0) {
                    p->mlfq_data->queue_level--;
                    p->mlfq_data->time_in_queue = 0;
                }
            }
        }
        
        return -1;
    }
    
    return selected_idx;
}

void run_scheduler(SystemState *sys, char *algorithm, int quantum) {
    sys->simulation_running = true;
    int completed_processes = 0;

    printf("Starting Simulation: %s\n", algorithm);

    while (completed_processes < sys->process_count) {
        pthread_mutex_lock(&sys->lock);

        int idx = select_process(sys, algorithm, quantum);

        if (idx != -1) {
            Process *p = sys->processes[idx];
            p->state = STATE_RUNNING;
            p->remaining_time--;
        }

        // Update Waiting Processes
        for (int i = 0; i < sys->process_count; i++) {
            if (i != idx && sys->processes[i]->state != STATE_TERMINATED && sys->processes[i]->arrival_time <= sys->current_time) {
                sys->processes[i]->state = STATE_READY; 
            }
        }

        send_update_to_ui(sys);

        if (idx != -1) {
            Process *p = sys->processes[idx];
            if (p->remaining_time == 0) {
                p->state = STATE_TERMINATED;
                p->completion_time = sys->current_time + 1;
                p->turnaround_time = p->completion_time - p->arrival_time;
                p->waiting_time = p->turnaround_time - p->burst_time;
                completed_processes++;
            }
        }

        sys->current_time++;
        pthread_mutex_unlock(&sys->lock);
        usleep(100000); 
    }

    // Final Update
    pthread_mutex_lock(&sys->lock);
    send_update_to_ui(sys);
    pthread_mutex_unlock(&sys->lock);

    sys->simulation_running = false;
    printf("Simulation Finished.\n");
}