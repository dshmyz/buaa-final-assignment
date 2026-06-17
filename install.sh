#!/bin/bash
# 快速安装脚本 - 用于安装 buaa-final-assignment skill
# 用法: bash install.sh

set -e

echo "🚀 正在安装北航结课作业 Skill..."

# 创建目标目录
TARGET_DIR="$HOME/.claude/skills/buaa-final-assignment"

# 如果已存在，询问是否覆盖
if [ -d "$TARGET_DIR" ]; then
    read -p "⚠️  目录已存在，是否覆盖? (y/N): " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        echo "❌ 安装取消"
        exit 0
    fi
    rm -rf "$TARGET_DIR"
fi

# 创建目录结构
mkdir -p "$TARGET_DIR"/{scripts,assets/templates,evals}

# 复制文件
echo "📦 复制文件..."
cp ./SKILL.md "$TARGET_DIR/"
cp ./README.md "$TARGET_DIR/"
cp ./.gitignore "$TARGET_DIR/"
cp ./scripts/build_from_template.py "$TARGET_DIR/scripts/"
cp ./assets/templates/buaa-course-paper-template.docx "$TARGET_DIR/assets/templates/"
cp ./evals/evals.json "$TARGET_DIR/evals/"

# 注册到 Claude Code
MANIFEST="$HOME/.claude/skills/.skills-manifest.json"
if [ -f "$MANIFEST" ]; then
    echo "📝 注册到 Claude Code..."
    python3 -c "
import json
from pathlib import Path

manifest_path = Path('$MANIFEST')
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

if 'buaa-final-assignment' not in manifest:
    manifest['buaa-final-assignment'] = {
        'name': 'buaa-final-assignment',
        'description': '北航结课作业/课程论文生成技能。根据模板生成可直接提交的 Word 文档，保留 Logo、封面表格、段落格式、日期自动填充，支持10阶学术改写流水线降低 AI 味。',
        'path': '$TARGET_DIR/SKILL.md'
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print('✅ 已注册到 Claude Code')
else:
    print('ℹ️  已存在注册记录，跳过')
"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "📍 安装位置: $TARGET_DIR"
echo ""
echo "🎯 使用方法:"
echo "   1. 重启 Claude Code"
echo "   2. 按 / 查看可用技能"
echo "   3. 选择 buaa-final-assignment"
echo "   4. 按提示输入课程信息即可生成论文"
echo ""
echo "📖 详细文档: $TARGET_DIR/README.md"
echo ""
