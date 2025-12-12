#include "scheduler.h"
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <string.h>

char current_socket_path[256];
int sockfd = -1;

void init_ipc(char *path) {
    strncpy(current_socket_path, path, sizeof(current_socket_path) - 1);
}

void connect_to_ui() {
    struct sockaddr_un addr;
    if ((sockfd = socket(AF_UNIX, SOCK_STREAM, 0)) == -1) return;

    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, current_socket_path, sizeof(addr.sun_path) - 1);

    if (connect(sockfd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
        close(sockfd);
        sockfd = -1;
    }
}

void send_update_to_ui(SystemState *sys) {
    if (sockfd == -1) return;

    char buffer[4096];
    char process_list[3000] = "[";

    for (int i = 0; i < sys->process_count; i++) {
        char p_buff[128];
        Process *p = sys->processes[i];
        
        // Get Queue Level (default to -1 if not MLFQ)
        int q_lvl = (p->mlfq_data != NULL) ? p->mlfq_data->queue_level : -1;

        sprintf(p_buff, "{\"pid\": %d, \"state\": %d, \"remaining\": %d, \"ct\": %d, \"tat\": %d, \"wt\": %d, \"q_lvl\": %d}%s", 
                p->pid, p->state, p->remaining_time, 
                p->completion_time, p->turnaround_time, p->waiting_time, q_lvl,
                (i < sys->process_count - 1) ? "," : "");
        strcat(process_list, p_buff);
    }
    strcat(process_list, "]");
    sprintf(buffer, "{\"time\": %d, \"processes\": %s}\n", sys->current_time, process_list);

    if (write(sockfd, buffer, strlen(buffer)) == -1) {
        close(sockfd);
        sockfd = -1;
    }
}

void close_ipc() {
    if (sockfd != -1) close(sockfd);
}