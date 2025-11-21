#include "scheduler.h"
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <string.h>

#define SOCKET_PATH "/tmp/scheduler_socket"

int sockfd = -1;

// Connect to the Python UI Server
void connect_to_ui() {
    struct sockaddr_un addr;

    // Create socket
    if ((sockfd = socket(AF_UNIX, SOCK_STREAM, 0)) == -1) {
        perror("Socket error");
        return;
    }

    // Set up address
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCKET_PATH, sizeof(addr.sun_path) - 1);

    // Connect
    if (connect(sockfd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
        close(sockfd);
        sockfd = -1;
    }
}

// Send JSON update
void send_update_to_ui(SystemState *sys) {
    if (sockfd == -1) return; // No UI connected

    char buffer[4096]; // Increased buffer size for more data
    char process_list[3000] = "[";

    // 1. Build Process List JSON
    for (int i = 0; i < sys->process_count; i++) {
        char p_buff[128];
        Process *p = sys->processes[i];
        
        // ADDED: ct (Completion), tat (Turnaround), wt (Waiting), queue (MLFQ)
        int queue_level = (p->mlfq_data != NULL) ? p->mlfq_data->queue_level : -1;
        sprintf(p_buff, "{\"pid\": %d, \"state\": %d, \"remaining\": %d, \"ct\": %d, \"tat\": %d, \"wt\": %d, \"queue\": %d}%s", 
                p->pid, p->state, p->remaining_time, 
                p->completion_time, p->turnaround_time, p->waiting_time, queue_level,
                (i < sys->process_count - 1) ? "," : "");
        strcat(process_list, p_buff);
    }
    strcat(process_list, "]");

    // 2. Build Final JSON Packet
    sprintf(buffer, "{\"time\": %d, \"processes\": %s}\n", sys->current_time, process_list);

    // 3. Send to Python
    if (write(sockfd, buffer, strlen(buffer)) == -1) {
        close(sockfd);
        sockfd = -1;
    }
}

// Clean up socket on exit
void close_ipc() {
    if (sockfd != -1) {
        close(sockfd);
    }
}