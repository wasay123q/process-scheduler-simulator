#include "scheduler.h"
#include <unistd.h> 
#include <string.h>
#include <stdlib.h> // Added for malloc
#include <stdio.h>  // Added for printf

// Static variables to hold Round Robin state between ticks
static int rr_last_idx = -1;
static int rr_quantum_timer = 0;

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
    // --- SJF ---
    else if (strcmp(algorithm, "SJF") == 0) {
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
    // --- Priority ---
    else if (strcmp(algorithm, "Priority") == 0) {
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
    // --- SRTN (Shortest Remaining Time Next) ---
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
    // --- RR (Round Robin) ---
    else if (strcmp(algorithm, "RR") == 0) {
        if (sys->current_time == 0) {
            rr_last_idx = -1;
            rr_quantum_timer = 0;
        }
        if (rr_last_idx != -1) {
            Process *prev = sys->processes[rr_last_idx];
            if (prev->state != STATE_TERMINATED && rr_quantum_timer < quantum) {
                rr_quantum_timer++; 
                return rr_last_idx;
            }
        }
        rr_quantum_timer = 1; 
        int start_pos = (rr_last_idx == -1) ? 0 : (rr_last_idx + 1) % sys->process_count;
        int count = 0;
        while (count < sys->process_count) {
            int idx = (start_pos + count) % sys->process_count;
            Process *p = sys->processes[idx];
            if (p->state != STATE_TERMINATED && p->arrival_time <= sys->current_time) {
                rr_last_idx = idx;
                return idx;
            }
            count++;
        }
        return -1; 
    }
    // --- MLFQ (Multi-Level Feedback Queue) ---
    else if (strcmp(algorithm, "MLFQ") == 0) {
        static int mlfq_quantums[3] = {2, 4, 8};
        static int last_pid = -1;
        static int quantum_counter = 0;
        
        if (sys->current_time == 0) {
            last_pid = -1;
            quantum_counter = 0;
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
                        
                        // --- FIX HERE: Changed >= to > ---
                        // This allows the process to run for the full quantum duration
                        if (quantum_counter > mlfq_quantums[queue]) { 
                            // Demote
                            if (queue < 2) p->mlfq_data->queue_level++;
                            p->mlfq_data->quantum_used = 0;
                            quantum_counter = 0;
                            last_pid = -1;
                        } else {
                            selected_idx = i;
                            return selected_idx;
                        }
                    }
                    break;
                }
            }
        }
        
        // Find highest priority process
        for (int queue = 0; queue <= 2; queue++) {
            for (int i = 0; i < sys->process_count; i++) {
                Process *p = sys->processes[i];
                if (p->state != STATE_TERMINATED && p->arrival_time <= sys->current_time &&
                    p->mlfq_data != NULL && p->mlfq_data->queue_level == queue) {
                    selected_idx = i;
                    last_pid = p->pid;
                    quantum_counter = 1; // Starts at 1, so > Limit works perfectly
                    p->mlfq_data->time_in_queue = 0;
                    return selected_idx;
                }
            }
        }
        
        // Aging (Prevent Starvation)
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