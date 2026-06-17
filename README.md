# 北航结课作业/课程论文生成 Skill

一个用于 AI 智能体的技能，帮助生成符合北航模板要求的课程论文 Word 文档。支持 Claude Code、Trae、Codex 等多个平台。

## ⚠️ 免责声明

### 学术诚信

- **本工具仅供参考和学习使用**，不建议直接用 AI 生成作业并提交
- 使用 AI 工具辅助学习和理解是合理的，但**直接提交 AI 生成的内容可能违反学术诚信要求**
- 各学校和课程对 AI 工具的使用政策不同，请先了解并遵守你所在学校的规定
- 本工具生成的内容**不能替代个人的思考、研究和写作过程**

### 正确使用方式

✅ **推荐的使用方式：**
- 使用本工具**学习论文结构和格式规范**
- 参考生成的内容**理解如何组织论证**
- 借鉴格式和排版**提高文档制作效率**
- 用生成的框架作为**草稿**，再进行个人化修改和完善

❌ **不推荐的使用方式：**
- 直接提交 AI 生成的论文作为最终作业
- 完全不修改就使用生成的内容
- 忽略课程要求和个人思考过程

### 责任声明

- 本工具开发者不对因使用本工具而产生的任何学术后果负责
- 用户应自行判断使用方式，并承担相应责任
- 本工具按"现状"提供，不保证生成内容的学术适用性

---

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

## 🚀 快速安装

### 方式 1：一键下载脚本（最简单）⭐

不需要 git，只需要一条命令：

```bash
# 自动下载并安装到 Claude Code
curl -fsSL https://raw.githubusercontent.com/dshmyz/buaa-final-assignment/main/install.sh | bash
```

或者下载后运行：

```bash
# 下载安装脚本
curl -fsSL -o install.sh https://raw.githubusercontent.com/dshmyz/buaa-final-assignment/main/install.sh

# 运行安装
bash install.sh
```

### 方式 2：下载 ZIP 压缩包

1. 访问 https://github.com/dshmyz/buaa-final-assignment
2. 点击绿色的 **"Code"** 按钮
3. 选择 **"Download ZIP"**
4. 解压 ZIP 文件
5. 运行安装脚本：

```bash
cd buaa-final-assignment-main
bash install.sh
```

### 方式 3：使用 git（推荐有基础的用户）

```bash
git clone https://github.com/dshmyz/buaa-final-assignment.git
cd buaa-final-assignment
bash install.sh
```

### 方式 4：手动安装（完全手动）

```bash
# 1. 创建目录
mkdir -p ~/.claude/skills/buaa-final-assignment/{scripts,assets/templates,evals}

# 2. 下载各个文件
curl -fsSL -o ~/.claude/skills/buaa-final-assignment/SKILL.md https://raw.githubusercontent.com/dshmyz/buaa-final-assignment/main/SKILL.md
curl -fsSL -o ~/.claude/skills/buaa-final-assignment/scripts/build_from_template.py https://raw.githubusercontent.com/dshmyz/buaa-final-assignment/main/scripts/build_from_template.py
curl -fsSL -o ~/.claude/skills/buaa-final-assignment/assets/templates/buaa-course-paper-template.docx https://raw.githubusercontent.com/dshmyz/buaa-final-assignment/main/assets/templates/buaa-course-paper-template.docx
curl -fsSL -o ~/.claude/skills/buaa-final-assignment/evals/evals.json https://raw.githubusercontent.com/dshmyz/buaa-final-assignment/main/evals/evals.json

# 3. 注册到 Claude Code（需要编辑文件）
# 手动编辑 ~/.claude/skills/.skills-manifest.json，添加以下内容：
```

```json
{
  "buaa-final-assignment": {
    "name": "buaa-final-assignment",
    "description": "北航结课作业/课程论文生成技能",
    "path": "/Users/你的用户名/.claude/skills/buaa-final-assignment/SKILL.md"
  }
}
```

## 🎯 安装方式对比

| 方式 | 难度 | 需要 git | 适用人群 |
|------|------|---------|---------|
| **方式 1：一键脚本** | ⭐ 最简单 | ❌ 不需要 | 所有人 |
| **方式 2：下载 ZIP** | ⭐⭐ 简单 | ❌ 不需要 | 不会命令行的人 |
| **方式 3：git clone** | ⭐⭐⭐ 中等 | ✅ 需要 | 有基础的用户 |
| **方式 4：手动下载** | ⭐⭐⭐⭐ 较难 | ❌ 不需要 | 完全手动控制 |

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
