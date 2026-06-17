# 北航结课作业/课程论文生成 Skill

一个用于 Claude Code 的技能，帮助生成符合北航模板要求的课程论文 Word 文档。

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

## 📦 内置模板

- `assets/templates/buaa-course-paper-template.docx` - 北航课程论文模板

## 🚀 使用方法

### 1. 安装 Skill

把 `buaa-final-assignment` 目录复制到 Claude Code 的 skills 目录：

```bash
cp -r buaa-final-assignment ~/.claude/skills/
```

然后在 `~/.claude/skills/.skills-manifest.json` 中注册：

```json
{
  "buaa-final-assignment": {
    "name": "buaa-final-assignment",
    "description": "北航结课作业/课程论文生成技能",
    "path": "/path/to/.claude/skills/buaa-final-assignment/SKILL.md"
  }
}
```

### 2. 在 Claude Code 中使用

重启 Claude Code，然后：

1. 输入 `/` 查看可用技能
2. 选择 `buaa-final-assignment`
3. 按提示输入课程信息、姓名、学号等
4. Claude 会自动生成符合要求的 Word 文档

### 3. 直接使用脚本

如果你只是想用脚本生成文档：

```bash
python scripts/build_from_template.py \
  --template assets/templates/buaa-course-paper-template.docx \
  --content your_paper.json \
  --output "课程名-学号-姓名-论文题目.docx"
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
