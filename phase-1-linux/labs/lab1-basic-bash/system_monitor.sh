#!/usr/bin/env bash

LOG_DIR="$(dirname "$0")/logs"
LOG_FILE="$LOG_DIR/system_monitor.log"

mkdir -p "$LOG_DIR"

TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

# CPU load (1 min)
CPU_LOAD=$(cut -d ' ' -f1 /proc/loadavg)

# RAM usage
MEM_TOTAL=$(grep MemTotal /proc/meminfo | awk '{print $2}')
MEM_AVAILABLE=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
MEM_USED=$((MEM_TOTAL - MEM_AVAILABLE))
MEM_USED_PERCENT=$((MEM_USED * 100 / MEM_TOTAL))

echo "$TIMESTAMP | CPU load: $CPU_LOAD | RAM used: ${MEM_USED_PERCENT}%" >> "$LOG_FILE"
