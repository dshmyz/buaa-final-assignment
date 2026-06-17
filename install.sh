#!/bin/bash
# 多平台技能安装脚本
# 支持：Claude Code, Codex, Trae
# 用法: bash install.sh [--platform PLATFORM]

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "🚀 北航结课作业 Skill 安装程序"
echo ""

# 检测平台
detect_platform() {
    if [ -d "$HOME/.claude" ] && [ -f "$HOME/.claude/skills/.skills-manifest.json" ]; then
        echo "claude"
    elif [ -d "$HOME/.trae" ]; then
        echo "trae"
    elif [ -d "$HOME/.codex" ]; then
        echo "codex"
    else
        echo "unknown"
    fi
}

# 安装到 Claude Code
install_claude() {
    echo "📦 安装到 Claude Code..."
    TARGET_DIR="$HOME/.claude/skills/buaa-final-assignment"
    MANIFEST="$HOME/.claude/skills/.skills-manifest.json"

    # 创建目标目录
    if [ -d "$TARGET_DIR" ]; then
        read -p "⚠️  目录已存在，是否覆盖? (y/N): " confirm
        if [[ ! $confirm =~ ^[Yy]$ ]]; then
            echo "❌ 安装取消"
            exit 0
        fi
        rm -rf "$TARGET_DIR"
    fi

    mkdir -p "$TARGET_DIR"/{scripts,assets/templates,evals}

    # 复制文件
    echo "📦 复制文件..."
    cp ./SKILL.md "$TARGET_DIR/"
    cp ./README.md "$TARGET_DIR/"
    cp ./.gitignore "$TARGET_DIR/"
    cp ./scripts/build_from_template.py "$TARGET_DIR/scripts/"
    cp ./assets/templates/buaa-course-paper-template.docx "$TARGET_DIR/assets/templates/"
    cp ./evals/evals.json "$TARGET_DIR/evals/"

    # 注册到清单
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
        'description': '北航结课作业/课程论文生成技能。根据模板生成可直接提交的 Word 文档。',
        'path': '$TARGET_DIR/SKILL.md'
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print('✅ 已注册到 Claude Code')
else:
    print('ℹ️  已存在注册记录，跳过')
"
    fi

    echo "✅ Claude Code 安装完成"
}

# 安装到 Trae
install_trae() {
    echo "📦 安装到 Trae..."
    TARGET_DIR="$HOME/.trae/builtin_skills/buaa-final-assignment"

    # 创建目标目录
    if [ -d "$TARGET_DIR" ]; then
        read -p "⚠️  目录已存在，是否覆盖? (y/N): " confirm
        if [[ ! $confirm =~ ^[Yy]$ ]]; then
            echo "❌ 安装取消"
            exit 0
        fi
        rm -rf "$TARGET_DIR"
    fi

    mkdir -p "$TARGET_DIR"/{scripts,assets/templates,evals}

    # 复制文件
    echo "📦 复制文件..."
    cp ./SKILL.md "$TARGET_DIR/"
    cp ./README.md "$TARGET_DIR/"
    cp ./.gitignore "$TARGET_DIR/"
    cp ./scripts/build_from_template.py "$TARGET_DIR/scripts/"
    cp ./assets/templates/buaa-course-paper-template.docx "$TARGET_DIR/assets/templates/"
    cp ./evals/evals.json "$TARGET_DIR/evals/"

    echo "✅ Trae 安装完成"
    echo "💡 重启 Trae 即可使用"
}

# 安装到腾讯 CodeBuddy
install_codebuddy() {
    echo "📦 安装到腾讯 CodeBuddy..."
    TARGET_DIR=".codebuddy/rules"

    mkdir -p "$TARGET_DIR"

    # 转换 SKILL.md 为规则文件
    echo "🔄 转换为 CodeBuddy 规则格式..."
    python3 -c "
import re
from pathlib import Path

skill_md = Path('./SKILL.md').read_text(encoding='utf-8')

# 移除 YAML frontmatter
skill_md = re.sub(r'^---.*?---\n', '', skill_md, flags=re.DOTALL)

rules_md = f'''# BUAA Final Assignment Skill

> 北航结课作业/课程论文生成技能

{skill_md}
'''

Path('$TARGET_DIR/buaa-final-assignment.md').write_text(rules_md, encoding='utf-8')
print('✅ 已转换为 CodeBuddy 规则')
"

    echo "✅ CodeBuddy 安装完成"
    echo "💡 重启 IDE 即可使用"
}

# 安装到通义灵码
install_lingma() {
    echo "📦 安装到通义灵码..."
    TARGET_DIR=".lingma/rules"

    mkdir -p "$TARGET_DIR"

    # 转换 SKILL.md 为规则文件
    echo "🔄 转换为通义灵码规则格式..."
    python3 -c "
import re
from pathlib import Path

skill_md = Path('./SKILL.md').read_text(encoding='utf-8')

# 移除 YAML frontmatter
skill_md = re.sub(r'^---.*?---\n', '', skill_md, flags=re.DOTALL)

rules_md = f'''# BUAA Final Assignment Skill

> 北航结课作业/课程论文生成技能

{skill_md}
'''

Path('$TARGET_DIR/buaa-final-assignment.md').write_text(rules_md, encoding='utf-8')
print('✅ 已转换为通义灵码规则')
"

    echo "✅ 通义灵码安装完成"
    echo "💡 重启 IDE 即可使用"
}

# 安装到 CodeGeeX
install_codegeex() {
    echo "📦 安装到 CodeGeeX..."
    TARGET_DIR=".codegeex"

    mkdir -p "$TARGET_DIR"

    # 转换 SKILL.md 为规则文件
    echo "🔄 转换为 CodeGeeX 规则格式..."
    python3 -c "
import re
from pathlib import Path

skill_md = Path('./SKILL.md').read_text(encoding='utf-8')

# 移除 YAML frontmatter
skill_md = re.sub(r'^---.*?---\n', '', skill_md, flags=re.DOTALL)

rules_md = f'''# BUAA Final Assignment Skill

> 北航结课作业/课程论文生成技能

{skill_md}
'''

Path('$TARGET_DIR/rules.md').write_text(rules_md, encoding='utf-8')
print('✅ 已转换为 CodeGeeX 规则')
"

    echo "✅ CodeGeeX 安装完成"
    echo "💡 重启 IDE 即可使用"
}

# 安装到 Fitten Code

# 安装到 Fitten Code
install_fitten() {
    echo "📦 安装到 Fitten Code..."
    TARGET_DIR="$HOME/.fitten/rules"

    mkdir -p "$TARGET_DIR"

    # 转换 SKILL.md 为规则文件
    echo "🔄 转换为 Fitten Code 规则格式..."
    python3 -c "
import re
from pathlib import Path

skill_md = Path('./SKILL.md').read_text(encoding='utf-8')

# 移除 YAML frontmatter
skill_md = re.sub(r'^---.*?---\n', '', skill_md, flags=re.DOTALL)

rules_md = f'''# BUAA Final Assignment Skill

> 北航结课作业/课程论文生成技能

{skill_md}
'''

Path('$TARGET_DIR/buaa-final-assignment.md').write_text(rules_md, encoding='utf-8')
print('✅ 已转换为 Fitten Code 规则')
"

    echo "✅ Fitten Code 安装完成"
    echo "💡 重启 IDE 即可使用"
}

# 显示帮助
show_help() {
    echo "用法: bash install.sh [选项]"
    echo ""
    echo "选项:"
    echo "  -p, --platform PLATFORM   指定安装平台"
    echo "  -a, --all                 安装到所有检测到的平台"
    echo "  -l, --list                列出所有支持的平台"
    echo "  -h, --help                显示此帮助信息"
    echo ""
    echo "支持的平台:"
    echo "  Claude Code (推荐)    ~/.claude/skills/"
    echo "  Trae                  ~/.trae/builtin_skills/"
    echo "  CodeBuddy (腾讯)      .codebuddy/rules/"
    echo "  通义灵码 (阿里)       .lingma/rules/"
    echo "  CodeGeeX (智谱AI)     .codegeex/"
    echo "  Fitten Code           ~/.fitten/rules/"
    echo "  Codex (OpenAI)        ~/.codex/skills/ (部分兼容)"
    echo ""
    echo "示例:"
    echo "  bash install.sh                        # 自动检测并安装"
    echo "  bash install.sh --platform claude      # 安装到 Claude Code"
    echo "  bash install.sh --platform codebuddy   # 安装到腾讯 CodeBuddy"
    echo "  bash install.sh --all                  # 安装到所有平台"
    echo ""
}

# 列出支持的平台
list_platforms() {
    echo "支持的平台:"
    echo ""
    echo "国际平台:"
    echo "  claude    Claude Code (推荐)"
    echo "  trael     Trae (ByteDance)"
    echo "  codex     Codex (OpenAI) - 部分兼容"
    echo ""
    echo "国内平台:"
    echo "  codebuddy 腾讯 CodeBuddy (原 WorkBuddy)"
    echo "  lingma    阿里 通义灵码"
    echo "  codegeex  智谱AI CodeGeeX"
    echo "  fitten    Fitten Code"
    echo ""
    echo "  all       所有平台"
    echo ""
    echo "平台检测:"
    PLATFORM=$(detect_platform)
    if [ "$PLATFORM" = "claude" ]; then
        echo "  ✅ 检测到 Claude Code"
    elif [ "$PLATFORM" = "trae" ]; then
        echo "  ✅ 检测到 Trae"
    elif [ "$PLATFORM" = "codex" ]; then
        echo "  ✅ 检测到 Codex"
    else
        echo "  ⚠️  未检测到已知平台"
    fi
}

# 解析参数
PLATFORM=""
INSTALL_ALL=false

while [ $# -gt 0 ]; do
    case $1 in
        -p|--platform)
            PLATFORM="$2"
            shift 2
            ;;
        -a|--all)
            INSTALL_ALL=true
            shift
            ;;
        -l|--list)
            list_platforms
            exit 0
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "❌ 未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 如果没有指定平台，自动检测
if [ -z "$PLATFORM" ] && [ "$INSTALL_ALL" = false ]; then
    PLATFORM=$(detect_platform)
    if [ "$PLATFORM" = "unknown" ]; then
        echo "❌ 未检测到已知平台"
        echo "💡 请使用 --platform 指定平台，或使用 --all 安装到所有平台"
        list_platforms
        exit 1
    fi
    echo "🔍 自动检测到平台: $PLATFORM"
    echo ""
fi

# 执行安装
if [ "$INSTALL_ALL" = true ]; then
    echo "📦 安装到所有平台..."
    echo ""

    if [ -d "$HOME/.claude" ]; then
        install_claude
        echo ""
    fi

    if [ -d "$HOME/.trae" ]; then
        install_trae
        echo ""
    fi

    if [ -d "$HOME/.codex" ]; then
        install_codex
        echo ""
    fi

    echo "✅ 所有平台安装完成"
else
    case $PLATFORM in
        claude)
            install_claude
            ;;
        trael)
            install_trae
            ;;
        codebuddy)
            install_codebuddy
            ;;
        lingma)
            install_lingma
            ;;
        codegeex)
            install_codegeex
            ;;
        fitten)
            install_fitten
            ;;
        codex)
            install_codex
            ;;
        *)
            echo "❌ 未知平台: $PLATFORM"
            list_platforms
            exit 1
            ;;
    esac
fi

echo ""
echo "🎉 安装完成!"
echo ""
echo "📖 使用文档: $(pwd)/README.md"
echo ""
