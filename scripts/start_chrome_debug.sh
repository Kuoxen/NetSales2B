#!/bin/bash

# 启动Chrome调试模式脚本
echo "启动Chrome调试模式..."

# 检查Chrome是否已经在运行
if pgrep -f "Google Chrome" > /dev/null; then
    echo "检测到Chrome正在运行，请先关闭所有Chrome窗口"
    echo "然后重新运行此脚本"
    exit 1
fi

# 启动Chrome调试模式
echo "正在启动Chrome调试模式..."
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --remote-debugging-port=9222 \
    --user-data-dir=/tmp/chrome-debug \
    --no-first-run \
    --no-default-browser-check \
    --disable-default-apps \
    --disable-popup-blocking \
    --disable-web-security \
    --disable-features=VizDisplayCompositor

echo "Chrome调试模式已启动"
echo "现在可以运行 shopee_shop_visitor.py 脚本" 