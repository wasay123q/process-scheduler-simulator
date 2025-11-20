#include "scheduler.h"
#include <string.h>

// External function from ipc.c
extern void connect_to_ui();
extern void close_ipc();

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Usage: %s <Algorithm> <Quantum> <Process_Count>\n", argv[0]);
        printf("Algorithms: FCFS, SJF, RR, Priority\n");
        return 1;
    }

    char *algorithm = argv[1];
    int quantum = atoi(argv[2]);
    int process_count = atoi(argv[3]);

    // 1. Initialize System
    SystemState system;
    init_system(&system);

    // 2. Connect to Python UI (IPC)
    connect_to_ui();

    // 3. Input Processes
    // We expect input in format: PID Arrival Burst Priority
    // Python will pipe this data into stdin
    printf("Waiting for %d processes...\n", process_count);
    for (int i = 0; i < process_count; i++) {
        int pid, arrival, burst, priority;
        if (scanf("%d %d %d %d", &pid, &arrival, &burst, &priority) == 4) {
            add_process(&system, pid, arrival, burst, priority);
        }
    }

    // 4. Run Simulation
    run_scheduler(&system, algorithm, quantum);

    // 5. Final Reporting
    printf("\n--- Final Metrics ---\n");
    printf("PID\tTurnaround\tWaiting\n");
    float avg_tat = 0, avg_wt = 0;
    
    for (int i = 0; i < system.process_count; i++) {
        Process *p = system.processes[i];
        printf("%d\t%d\t\t%d\n", p->pid, p->turnaround_time, p->waiting_time);
        avg_tat += p->turnaround_time;
        avg_wt += p->waiting_time;
    }
    
    printf("--------------------------------------------\n");
    printf("Average Turnaround Time: %.2f\n", avg_tat / system.process_count);
    printf("Average Waiting Time: %.2f\n", avg_wt / system.process_count);

    close_ipc();
    return 0;
}