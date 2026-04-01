#!/bin/bash

# 推送代码到 GitHub 脚本
# 使用方法: bash scripts/push_to_github.sh

echo "=========================================="
echo "推送代码到 GitHub"
echo "=========================================="

cd /workspace/projects

# 检查是否有未提交的更改
if [ -n "$(git status --short)" ]; then
    echo "发现未提交的更改，正在提交..."
    git add .
    git commit -m "feat: 完整项目代码，包含 HTML 可视化和定时推送配置"
fi

# 检查远程仓库
if git remote | grep -q "origin"; then
    echo "远程仓库已配置"
    git remote -v
else
    echo ""
    echo "⚠️  未配置远程仓库"
    echo ""
    echo "请选择："
    echo "1. 使用已有仓库 chixinxin1"
    echo "2. 创建新仓库"
    echo ""
    read -p "请输入选择 (1 或 2): " choice
    
    if [ "$choice" = "1" ]; then
        git remote add origin https://github.com/xc27471013-source/chixinxin1.git
    else
        echo ""
        read -p "请输入新仓库地址 (如 https://github.com/用户名/仓库名.git): " repo_url
        git remote add origin "$repo_url"
    fi
fi

echo ""
echo "正在推送代码..."
git push -u origin main

echo ""
echo "✅ 推送完成！"
echo ""
echo "下一步："
echo "1. 回到 Render 选择这个仓库"
echo "2. 配置部署参数"
