# 北航结课作业/课程论文生成 Skill

一个用于 AI 智能体的技能，帮助生成符合北航模板要求的课程论文 Word 文档。支持 Claude Code、Trae、Codex 等多个平台。

## ✨ 功能特点

- **模板保留**：完全保留原模板的 Logo、封面表格、段落样式、字体字号
- **自动填充**：封面信息自动填入表格，日期使用当前系统日期
- **格式标准**：
  - 封面题目：黑体二号
  - 封面其他内容：宋体四号，数字字母用 Times New Roman
  - 正文标题：宋体三号加粗
  - 标题段落：黑体三号，无首行缩进
  - 正文段落：宋体小四，首行缩进
- **学术改写**：内置 10 阶学术语言优化流水线，降低 AI 味
- **智能收集**：引导式提问收集必要信息，缺项先用占位符
- **多平台支持**：支持 Claude Code、Trae、Codex 等多个 AI 智能体

## 🚀 快速安装（一键脚本）

### 推荐方式：自动检测平台

```bash
# 克隆仓库
git clone https://github.com/dshmyz/buaa-final-assignment.git

# 运行安装脚本（自动检测已安装的平台）
cd buaa-final-assignment
bash install.sh
```

### 指定平台安装

```bash
# 只安装到 Claude Code
bash install.sh --platform claude

# 只安装到 Trae
bash install.sh --platform trae

# 只安装到 Codex（部分兼容）
bash install.sh --platform codex

# 安装到所有已检测到的平台
bash install.sh --all
```

### 查看支持的平台

```bash
bash install.sh --list
```

## 📦 支持的平台

| 平台 | 支持程度 | 安装路径 | 说明 |
|------|---------|---------|------|
| **Claude Code** | ✅ 完全支持 | `~/.claude/skills/` | 推荐，格式完全兼容 |
| **Trae** | ✅ 完全支持 | `~/.trae/builtin_skills/` | 与 Claude Code 格式兼容 |
| **Codex** | ⚠️ 部分兼容 | `~/.codex/skills/` | 会自动转换为 AGENTS.md 格式 |

## 📋 手动安装

### Claude Code

```bash
git clone https://github.com/dshmyz/buaa-final-assignment.git
cp -r buaa-final-assignment ~/.claude/skills/
# 手动编辑 ~/.claude/skills/.skills-manifest.json 添加注册信息
```

### Trae

```bash
git clone https://github.com/dshmyz/buaa-final-assignment.git
cp -r buaa-final-assignment ~/.trae/builtin_skills/
# 重启 Trae 即可
```

### Codex

```bash
git clone https://github.com/dshmyz/buaa-final-assignment.git
cp -r buaa-final-assignment ~/.codex/skills/
# 注意：需要将 SKILL.md 转换为 AGENTS.md 格式
# 建议使用安装脚本自动转换
```

`your_paper.json` 格式：

```json
{
  "title": "论文题目",
  "cover": [
    "课程名称：...",
    "姓名：...",
    "学号：...",
    "学院：...",
    "专业：..."
  ],
  "abstract": "摘要正文...",
  "keywords": "关键词1；关键词2；关键词3",
  "sections": [
    {"title": "引言", "paragraphs": ["..."]},
    {"title": "一、...", "paragraphs": ["..."]}
  ],
  "references": ["[1] ...", "[2] ..."],
  "ai_disclosure": ""
}
```

## 📝 格式要求

### 封面表格

- Row 1（论文题目）：**黑体二号**（size=44）
- Row 3-6（课程名、姓名、学院、日期）：**宋体四号**（size=28），数字字母用 Times New Roman

### 正文格式

- 论文标题：宋体三号加粗
- 一级标题：黑体三号，无首行缩进
- 正文段落：宋体小四，首行缩进
- 参考文献标题：黑体三号，无首行缩进
- 参考文献条目：宋体小四，首行缩进

## 🔄 学术改写流水线

内置 10 阶学术语言优化：

1. 口语正式化
2. 套话清理
3. 客观转写
4. 长句拆分
5. 逻辑衔接
6. 适度名词化
7. 术语校准
8. 冗余压缩
9. 重点调整
10. 语义核验

## 📋 自检清单

生成文档后自动检查：

- ✅ Logo 保留
- ✅ 封面表格内容填入
- ✅ 段落格式正确
- ✅ 字体字号正确
- ✅ 日期自动填入
- ✅ 无模板残留
- ✅ 引用规范

## 📄 License

MIT License
