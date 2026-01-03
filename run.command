#!/bin/bash

# 切换到脚本所在目录（重要！双击运行时的工作目录通常是用户根目录）
cd "$(dirname "$0")" || exit

echo "当前目录: $(pwd)"
echo "开始执行脚本..."
echo "=========================="

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3未安装"
    echo "请安装Python3: brew install python3"
    read -p "按回车键退出..."
    exit 1
fi

# 执行Python脚本
echo "1. 执行 generate_filelist.py..."
python3 generate_filelist.py -q

if [ $? -ne 0 ]; then
    echo "Python脚本执行失败，继续吗？"
    read -p "按回车继续，或按Ctrl+C取消..."
fi

# git相关操作
echo "2. 添加文件到git..."
git add .

echo "3. 提交更改..."
git commit -m "1" || echo "提交失败或无更改可提交"

echo "4. 推送到远程仓库..."
git push --force

echo "=========================="
echo "执行完成！"

# 保持终端窗口打开，以便查看结果
read -p "按回车键退出..."