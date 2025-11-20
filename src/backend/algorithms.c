#include "scheduler.h"
#include <unistd.h> 
#include <string.h>

// Static variables to hold Round Robin state between ticks
static int rr_last_idx = -1;
static int rr_quantum_timer = 0;

// Helper: Find the index of the process to run based on algorithm
int select_process(SystemState *sys, char *algorithm, int quantum) {
    int selected_idx = -1;

    // --- 1. First Come First Serve (FCFS) ---
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
    // --- 2. Shortest Job First (SJF) ---
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
    // --- 3. Priority Scheduling ---
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
    // --- 4. Round Robin (RR) ---
    else if (strcmp(algorithm, "RR") == 0) {
        if (sys->current_time == 0) {
            rr_last_idx = -1;
            rr_quantum_timer = 0;
        }

        // Continue previous if valid and quantum not expired
        if (rr_last_idx != -1) {
            Process *prev = sys->processes[rr_last_idx];
            if (prev->state != STATE_TERMINATED && rr_quantum_timer < quantum) {
                rr_quantum_timer++; 
                return rr_last_idx;
            }
        }

        // Find next process
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

    return selected_idx;
}

// Main Simulation Loop
void run_scheduler(SystemState *sys, char *algorithm, int quantum) {
    sys->simulation_running = true;
    int completed_processes = 0;

    printf("Starting Simulation: %s\n", algorithm);

    while (completed_processes < sys->process_count) {
        pthread_mutex_lock(&sys->lock);

        int idx = select_process(sys, algorithm, quantum);

        if (idx != -1) {
            // Run the process
            Process *p = sys->processes[idx];
            p->state = STATE_RUNNING;
            p->remaining_time--;
            
            // BUG FIX: Do NOT check termination here.
            // We wait until AFTER sending the update to UI.
        }

        // Update others to Ready
        for (int i = 0; i < sys->process_count; i++) {
            if (i != idx && sys->processes[i]->state != STATE_TERMINATED && sys->processes[i]->arrival_time <= sys->current_time) {
                sys->processes[i]->state = STATE_READY; 
            }
        }

        // 1. Send Data to UI (Process is still marked RUNNING, so UI draws the block)
        send_update_to_ui(sys);

        // 2. NOW check if it finished
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

    sys->simulation_running = false;
    printf("Simulation Finished.\n");
}