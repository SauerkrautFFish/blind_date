#!/bin/bash
echo "检测依赖中..."
python_version=$(python3 --version 2>&1)
# 检查当前机器是否安装了 Python
if [[ ! "$python_version" == *"Python 3.10.6"* ]]; then
    # 安装环境
    # https://www.zhihu.com/question/456908213/answer/3248085449?utm_id=0
    # https://www.jianshu.com/p/426596c4ff4c
    # https://www.xjx100.cn/news/436747.html?action=onClick
    # https://zhuanlan.zhihu.com/p/564255869

    echo "开始执行相关下载"
    echo "下载lsof"
    sudo yum install lsof -y
    echo "下载zlib zlib-dev openssl-devel..."
    sudo yum install -y zlib zlib-dev openssl-devel sqlite-devel bzip2-devel libffi libffi-devel gcc gcc-c++

    cd ~ || exit 1
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
    ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl
    cd ~ || exit 1
    rm -rf openssl-1.1.1q.tar.gz
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/openssl/lib
    echo "openssl安装完成"


    echo "下载sqlite"
    wget https://www.sqlite.org/2022/sqlite-autoconf-3390300.tar.gz
    echo "解压sqlite"
    tar zxvf sqlite-autoconf-3390300.tar.gz
    cd sqlite-autoconf-3390300/ || exit 1
    ./configure --prefix=/usr/local/sqlite3
    echo "编译sqlite"
    make
    echo "安装sqlite"
    make install
    rm -rf /usr/bin/sqlite3
    ln -s /usr/local/bin/sqlite3 /usr/bin/sqlite3
    cd ~ || exit 1
    rm -rf sqlite-autoconf-3390300.tar.gz
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/sqlite3/lib
    echo "下载sqlite成功"

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
    cd ~ || exit 1
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
echo "配置pip加速镜像成功"
# 检查是否存在该行
if ! grep -q "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/local/openssl/lib" ~/.bash_profile; then
    # 如果不存在则向文件末尾追加该行
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/openssl/lib' >> ~/.bash_profile
    echo "导入openssl到bash_profile"
fi
# 检查是否存在该行
if ! grep -q "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/local/sqlite3/lib" ~/.bash_profile; then
    # 如果不存在则向文件末尾追加该行
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/sqlite3/lib' >> ~/.bash_profile
    echo "导入sqlite3到bash_profile"
fi

source ~/.bash_profile
echo "执行bash_profile"
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
echo "success"