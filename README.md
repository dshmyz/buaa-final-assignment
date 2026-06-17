# 北航结课作业/课程论文辅助 Skill

一个用于 AI 智能体的技能，辅助用户根据北航模板准备课程论文 Word 文档。支持 Claude Code、Trae、Codex 等多个平台。

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

---

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
    "description": "北航结课作业/课程论文辅助技能",
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

---

## 📦 支持的平台

### 国际平台

| 平台 | 支持程度 | 安装路径 | 说明 |
|------|---------|---------|------|
| **Claude Code** | ✅ 完全支持 | `~/.claude/skills/` | 推荐，格式完全兼容 |
| **Trae** | ✅ 完全支持 | `~/.trae/builtin_skills/` | 与 Claude Code 格式兼容 |
| **Codex** | ⚠️ 部分兼容 | `~/.codex/skills/` | 会自动转换为 AGENTS.md 格式 |

### 国内平台

| 平台 | 公司 | 支持程度 | 安装路径 | 规则格式 |
|------|------|---------|---------|---------|
| **CodeBuddy** | 腾讯 | ✅ 支持 | `.codebuddy/rules/` | Markdown 规则文件 |
| **通义灵码** | 阿里 | ✅ 支持 | `.lingma/rules/` | Markdown 规则文件 |
| **CodeGeeX** | 智谱AI | ✅ 支持 | `.codegeex/` | Markdown 规则文件 |
| **Fitten Code** | - | ✅ 支持 | `~/.fitten/rules/` | Markdown 规则文件 |

---

## 📖 详细使用文档

### 项目结构

```
buaa-final-assignment/
├── SKILL.md                              # 技能说明（Claude Code 格式）
├── README.md                             # 使用文档
├── install.sh                            # 多平台安装脚本
├── .gitignore                            # Git 忽略规则
├── scripts/
│   └── build_from_template.py            # DOCX 文档生成脚本（核心引擎）
├── assets/
│   └── templates/
│       └── buaa-course-paper-template.docx  # 北航课程论文模板
└── evals/
    └── evals.json                        # 测试用例
```

### 核心组件

| 文件 | 用途 | 说明 |
|------|------|------|
| `SKILL.md` | Claude Code 技能定义 | 包含触发条件、工作流、格式要求等 |
| `install.sh` | 多平台安装脚本 | 自动检测平台，支持 Claude/Trae/国内平台 |
| `build_from_template.py` | DOCX 生成引擎 | 解析模板、填充内容、保留格式 |
| `buaa-course-paper-template.docx` | 北航模板 | 包含封面表格、段落样式、Logo |

### 使用方法

#### 方法 1：通过 AI 智能体使用（推荐）

1. 安装技能到你的 AI 智能体
2. 重启智能体
3. 输入：`/buaa-final-assignment` 或 `帮我做北航结课论文`
4. 按提示输入课程信息、姓名、学号等
5. AI 会生成草稿供你审核修改

#### 方法 2：直接使用脚本

```bash
# 准备内容 JSON
cat > paper.json << 'EOF'
{
  "title": "你的论文题目",
  "cover": [
    "课程名称：课程名",
    "姓名：姓名",
    "学号：学号",
    "学院：学院"
  ],
  "abstract": "你的摘要...",
  "keywords": "关键词1；关键词2",
  "sections": [
    {"title": "引言", "paragraphs": ["..."]},
    {"title": "一、...", "paragraphs": ["..."]}
  ],
  "references": ["[1] ..."],
  "ai_disclosure": ""
}
EOF

# 生成文档
python scripts/build_from_template.py \
  --template assets/templates/buaa-course-paper-template.docx \
  --content paper.json \
  --output "课程名-学号-姓名-论文题目.docx"
```

### 格式规范

#### 封面表格

| 位置 | 内容 | 字体 | 字号 |
|------|------|------|------|
| Row 1 | 论文题目 | 黑体 | 二号（44） |
| Row 3 | 课程名称 | 宋体 + Times New Roman | 四号（28） |
| Row 4 | 姓名+学号 | 宋体 + Times New Roman | 四号（28） |
| Row 5 | 学院 | 宋体 + Times New Roman | 四号（28） |
| Row 6 | 日期 | 宋体 + Times New Roman | 四号（28） |

#### 正文格式

| 位置 | 字体 | 字号 | 加粗 | 首行缩进 |
|------|------|------|------|---------|
| 论文题目 | 宋体 | 三号（32） | ✓ | 无 |
| 一级标题 | 黑体 | 三号（32） | ✗ | 无 |
| **二级标题** | **宋体** | **小四（24）** | **✓** | **有（和正文一样）** |
| 正文段落 | 宋体 | 小四（24） | ✗ | 有（480） |
| 摘要 | 宋体 | 小四（24） | ✗ | 有（440） |
| 关键词 | 宋体 | 小四（24） | ✗ | 有（440） |

### 10 阶语言优化流水线

技能会自动执行以下流程优化论文语言：

| 阶段 | 步骤 | 目的 |
|------|------|------|
| 一阶处理 | 1. 口语正式化 | 去口语化 |
| 一阶处理 | 2. 套话清理 | 删除"众所周知"等 |
| 一阶处理 | 3. 客观转写 | 第一人称改第三人称 |
| 二阶重构 | 4. 长句拆分 | 拆解复杂句 |
| 二阶重构 | 5. 逻辑衔接 | 优化过渡词 |
| 二阶重构 | 6. 适度名词化 | 提升信息密度 |
| 三阶校准 | 7. 术语校准 | 规范专业术语 |
| 三阶校准 | 8. 冗余压缩 | 删除重复修饰 |
| 三阶校准 | 9. 重点调整 | 调整句子焦点 |
| 最终审计 | 10. 语义核验 | 确保不改变原意 |

### 常见问题

#### Q: 生成的文档格式不对怎么办？

A: 检查是否使用了正确的模板文件 `buaa-course-paper-template.docx`。如果格式仍有问题，可能是模板文件损坏，重新克隆仓库即可。

#### Q: 封面表格没有正确填充？

A: 确保 `paper.json` 中的 `cover` 字段格式正确，包含 4 个元素：`["课程名称：...", "姓名：...", "学号：...", "学院：..."]`

#### Q: 日期不是当前日期？

A: 脚本会自动使用当前系统日期，格式为 `YYYY年MM月DD日`。如果日期错误，检查系统时间设置。

#### Q: 支持 PDF 模板吗？

A: 目前只支持 `.docx` 格式的模板。如果只有 PDF，需要先转换为 Word 格式。

#### Q: 如何修改论文内容？

A: 生成后用 Word 打开，直接编辑内容。格式会自动保留，无需担心格式错乱。

### 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建 Pull Request

### 更新日志

#### v1.0.0 (2026-06-17)

- ✨ 初始发布
- ✅ 支持北航课程论文模板
- ✅ 支持 Claude Code、Trae、Codex
- ✅ 支持国内平台：CodeBuddy、通义灵码、CodeGeeX、Fitten
- ✅ 一键安装脚本
- ✅ 10 阶语言优化流水线
- ✅ 多种安装方式

### 许可证

MIT License

### 联系方式

- GitHub: https://github.com/dshmyz/buaa-final-assignment
- Issues: https://github.com/dshmyz/buaa-final-assignment/issues

---

## 📊 技术栈

- **Python 3.x** - 文档生成脚本
- **xml.etree.ElementTree** - DOCX XML 解析
- **json** - 配置文件处理
- **zipfile** - DOCX 压缩包处理

## 🙏 致谢

- 北京航空航天大学 - 提供课程论文模板
- Claude Code - 技能框架设计参考
- 所有贡献者和用户

---

**⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！**
