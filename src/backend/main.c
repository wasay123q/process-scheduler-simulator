#include "scheduler.h"
#include <string.h>

extern void init_ipc(char *path);
extern void connect_to_ui();
extern void close_ipc();

int main(int argc, char *argv[]) {
    if (argc < 5) {
        printf("Usage: %s <Algo> <Quantum> <Count> <SocketPath>\n", argv[0]);
        return 1;
    }

    char *algorithm = argv[1];
    int quantum = atoi(argv[2]);
    int process_count = atoi(argv[3]);
    char *socket_path = argv[4];

    SystemState system;
    init_system(&system);

    init_ipc(socket_path);
    connect_to_ui();

    for (int i = 0; i < process_count; i++) {
        int pid, arrival, burst, priority;
        if (scanf("%d %d %d %d", &pid, &arrival, &burst, &priority) == 4) {
            add_process(&system, pid, arrival, burst, priority);
        }
    }

    run_scheduler(&system, algorithm, quantum);
    close_ipc();
    return 0;
}