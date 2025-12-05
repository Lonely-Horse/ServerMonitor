#!/bin/bash

BASE_DIR=$(cd "$(dirname"$0")" && pwd)
LOG_FILE="$BASE_DIR/logs/server.log"

echo "项目的根目录:$BASE_DIR"

export PYTHONPATH=$BASE_DIR

echo "清理旧服务中..."
fuser -k 6000/tcp > /dev/null 2>&1

echo "启动ServerMonitor..."
nohup python3 "$BASE_DIR/app/main.py" > "$LOG_FILE" 2>&1 &

sleep 2
if ps -ef | grep "app/main.py" | grep -v grep > /dev/null; then
	echo "✅服务已后台启动"
	echo "日志:tail -f logs/server.log"

else
	echo "❌ 启动失败，请检查logs/server.log"
fi

exit

