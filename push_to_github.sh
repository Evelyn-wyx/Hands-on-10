#!/bin/bash

# ============================================
# GitHub 推送脚本
# ============================================
# 此脚本用于将本地更改推送到 GitHub
# 使用方法: bash push_to_github.sh

echo "========================================"
echo "🚀 推送到 GitHub"
echo "========================================"

# 切换到项目目录
cd "$(dirname "$0")"

# 检查 git 状态
echo "📊 检查 Git 状态..."
git status

# 检查远程仓库
echo ""
echo "🌐 检查远程仓库..."
git remote -v

# 尝试推送
echo ""
echo "📤 正在推送到 GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✅ 推送成功!"
    echo "========================================"
    echo ""
    echo "CI/CD 工作流将自动运行"
    echo "查看: https://github.com/Evelyn-wyx/Hands-on-10/actions"
else
    echo ""
    echo "========================================"
    echo "❌ 推送失败"
    echo "========================================"
    echo ""
    echo "请确保:"
    echo "1. 已配置 GitHub 凭据"
    echo "2. 有推送权限"
    echo ""
    echo "或者使用以下命令手动推送:"
    echo "git push origin main"
fi
