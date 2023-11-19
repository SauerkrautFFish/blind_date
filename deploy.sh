#!/bin/bash

# 定义要使用的端口号
PORT=8068

# 检查端口是否被占用
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null; then
    echo "端口 $PORT 已被占用."
    kill -9 $(lsof -ti :$PORT)
    echo "已杀死占用端口 $PORT 的进程."
fi

cd ~/blind_date || exit 1

echo "执行Django迁移命令"
# 执行Django迁移命令
python3 manage.py migrate

if [ $? -ne 0 ]; then
    echo "迁移命令执行失败"
    exit 1
fi
echo "迁移命令执行成功"
echo "启动服务中..."
# 启动Django服务
nohup python3 manage.py runserver 0.0.0.0:$PORT &
echo "启动服务成功, 端口号:$PORT"

exit 0