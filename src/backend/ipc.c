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
        // If connection fails, we just print to console (fallback)
        // printf("Warning: UI not connected. Running in console mode.\n");
        close(sockfd);
        sockfd = -1;
    }
}

// Send JSON update
void send_update_to_ui(SystemState *sys) {
    if (sockfd == -1) return; // No UI connected

    char buffer[1024];
    char process_list[512] = "[";

    // 1. Build Process List JSON
    for (int i = 0; i < sys->process_count; i++) {
        char p_buff[64];
        Process *p = sys->processes[i];
        
        sprintf(p_buff, "{\"pid\": %d, \"state\": %d, \"remaining\": %d}%s", 
                p->pid, p->state, p->remaining_time, 
                (i < sys->process_count - 1) ? "," : "");
        strcat(process_list, p_buff);
    }
    strcat(process_list, "]");

    // 2. Build Final JSON Packet
    // Format: { "time": 5, "processes": [...] }
    sprintf(buffer, "{\"time\": %d, \"processes\": %s}\n", sys->current_time, process_list);

    // 3. Send to Python
    if (write(sockfd, buffer, strlen(buffer)) == -1) {
        perror("IPC Write Error");
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