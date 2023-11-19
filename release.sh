#!/bin/bash
python_version=$(python3 --version 2>&1)
# 检查当前机器是否安装了 Python
if [[ ! "$python_version" == *"Python 3.10.6"* ]]; then
    # 安装Python 3.10（使用yum包管理器）
    # https://www.zhihu.com/question/456908213/answer/3248085449?utm_id=0
    echo "没有发现python, 开始执行相关下载"

    echo "下载zlib zlib-dev openssl-devel..."
    sudo yum install -y zlib zlib-dev openssl-devel sqlite-devel bzip2-devel libffi libffi-devel gcc gcc-c++

    cd ~
    echo "下载openssl1.1.1."
    wget https://www.openssl.org/source/openssl-1.1.1q.tar.gz
    echo "解压openssl1.1.1"
    tar xzf openssl-1.1.1q.tar.gz
    cd openssl-1.1.1q || exit 1
    echo "指定openssl1.1.1安装路径"
    ./config --prefix=/usr/local/openssl
    echo "安装openssl1.1.1"
    make && make install
    echo "openssl动态软链"
    echo "/usr/local/lib64/" >> /etc/ld.so.conf
    ldconfig
    rm -rf /usr/bin/openssl
    ln -s /usr/local/bin/openssl /usr/bin/openssl
    echo "openssl安装完成"
    cd ~
    rm -rf openssl-1.1.1q.tar.gz
    echo "下载python3.10.6"
    wget https://www.python.org/ftp/python/3.10.6/Python-3.10.6.tgz
    echo "解压python3.10.6"
    tar -zxvf Python-3.10.6.tgz
    cd Python-3.10.6 || exit 1
    echo "指定python3安装路径"
    ./configure --prefix=/usr/local//python3 --with-openssl=/usr/local//openssl
    echo "安装python3"
    make && make install
    rm -rf /usr/bin/python3 & rm -rf /usr/bin/pip3
    ln -s /usr/local/python3/bin/python3.10 /usr/bin/python3
    ln -s /usr/local/python3/bin/pip3.10 /usr/bin/pip3
    if [ $? -ne 0 ]; then
        echo "下载Python 3.10.6失败"
        exit 1
    fi
    rm -rf Python-3.10.6.tgz
    echo "下载python3.10.6成功"

    echo "更新pip"
    # 更新pip到最新版本
    pip3 install --upgrade pip
    echo "更新pip成功"
fi

cat <<EOF > ~/.pip/config.ini
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host=mirrors.aliyun.com
EOF

# 进入项目目录
cd ~/blind_date || exit 1
echo "进入项目根目录"

echo "下载项目依赖"
# 安装依赖包
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "下载项目依赖失败"
    exit 1
fi
echo "下载项目依赖成功"
# 定义要使用的端口号
PORT=8068

# 检查端口是否被占用
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null; then
    echo "端口 $PORT 已被占用."
    kill -9 $(lsof -ti :$PORT)
    echo "已杀死占用端口 $PORT 的进程."
fi

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
echo "启动服务成功"

exit 0