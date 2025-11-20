# Compiler and Flags
CC = gcc
CFLAGS = -Wall -Wextra -pthread -g
# -Wall: Show all warnings
# -Wextra: Show extra warnings
# -pthread: Enable threading support (Crucial for Concurrency)
# -g: Add debug info

# Directories
SRC_DIR = src/backend
BIN_DIR = bin
OBJ_DIR = obj

# Target Executable
TARGET = $(BIN_DIR)/scheduler

# Source and Object Files
SRCS = $(wildcard $(SRC_DIR)/*.c)
OBJS = $(patsubst $(SRC_DIR)/%.c, $(OBJ_DIR)/%.o, $(SRCS))

# Default Rule
all: $(TARGET)

# Link Logic
$(TARGET): $(OBJS)
	@mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) -o $@ $^
	@echo "Build successful! Run with: ./$(TARGET)"

# Compile Logic
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Clean Rule
clean:
	rm -rf $(BIN_DIR) $(OBJ_DIR)
	@echo "Cleaned build files."

.PHONY: all clean