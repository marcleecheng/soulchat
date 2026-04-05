# SoulChat Plugin

Create AI companions with soul — from chat logs, books, or a simple description.

从对话记录、书籍、或一段描述，创建有灵魂的 AI 聊天伙伴。

---

## What is SoulChat? 这是什么？

SoulChat is a [Claude Code](https://claude.ai/code) plugin that lets you create AI personas from any material and have persistent, in-character conversations with them — solo or in group chat.

SoulChat 是一个 Claude Code 插件，能从任何素材提取 AI 人格，并进行持续的角色对话——支持单聊和群聊。

**Example 举例：**
- Upload Steve Jobs' biography → chat with "Jobs" about product design
- 上传乔布斯传记 → 和"乔布斯"聊产品设计
- Export your ChatGPT history → recreate that conversation style
- 导出你的 ChatGPT 对话记录 → 重现那个聊天风格
- Just describe someone → instant persona
- 直接描述一个人 → 立刻生成人格

## Supported Formats 支持格式

PDF · ePub · TXT · Markdown · ChatGPT export JSON · Claude export JSON · Direct text description 直接文字描述

---

## Install 安装

> Requires 依赖: [Claude Code](https://claude.ai/code) + macOS or Linux

### Option A: One-click Install 一键安装（Recommended 推荐）

Best for most users. A setup wizard opens in your browser to guide you through everything.

适合大多数用户。浏览器会打开安装向导，一步步引导你完成。

```bash
git clone https://github.com/marcleecheng/soulchat
cd soulchat
./install.sh
```

What happens 会发生什么：
1. Installs dependencies automatically 自动安装依赖
2. Opens a browser wizard — upload your materials (books, chat exports, etc.) 打开浏览器向导——上传你的素材
3. Creates a global `soulchat` command 创建全局 `soulchat` 命令
4. Launches Claude Code with SoulChat loaded 自动启动 Claude Code 并加载 SoulChat

### Option B: Manual Setup 手动安装

For users comfortable with the terminal who want more control.

适合熟悉终端、想要更多控制的用户。

```bash
git clone https://github.com/marcleecheng/soulchat
cd soulchat
uv sync                          # Install dependencies 安装依赖
claude --plugin-dir .             # Launch with plugin loaded 启动并加载插件
```

Then inside Claude Code, type `/soulchat` to start.

在 Claude Code 中输入 `/soulchat` 开始。

---

## Launch Again 再次启动

After closing the terminal, here's how to get back in 关闭终端后，如何再次进入：

**If you used Option A 如果你用了一键安装：**
```bash
soulchat
```

**If `soulchat` command is not found, or you used Option B 如果命令找不到，或用了手动安装：**
```bash
cd soulchat                # Go to the folder you cloned 进入你 clone 的目录
claude --plugin-dir .      # Launch Claude Code with SoulChat 启动 Claude Code 并加载 SoulChat
```

Then type `/soulchat` to start chatting. 然后输入 `/soulchat` 开始聊天。

You can also place materials directly in `input/` before launching, or provide file paths during the guided flow.

也可以提前把素材放到 `input/` 目录，或在引导流程中提供文件路径。

---

## Usage 使用

### Quick Start 快捷用法

```
/soulchat              → Guided flow (first time) 引导流程（首次使用）
/soulchat Jobs         → Chat with Jobs directly 直接和 Jobs 聊天
/soulchat group        → Group chat with all personas 所有人格群聊
```

### Chat Commands 聊天指令

Once in a conversation, these commands are always available:

进入对话后，以下指令随时可用：

| Command 指令 | Action 效果 |
|---|---|
| `exit` / `退出` | Leave persona mode 退出角色模式 |
| `switch` / `换人` | Switch to another persona 切换人格 |
| `group` / `群聊` | Enter group chat mode 进入群聊 |
| `solo Name` / `单聊 Name` | Switch to solo chat with someone 单聊指定人格 |
| `@Name` | In group chat, make someone respond 群聊中指定某人回话 |
| `add` / `新人格` | Create a new persona 创建新人格 |

### Group Chat 群聊模式

Group chat simulates real group dynamics — not everyone responds to every message. Personas speak based on relevance, expertise, and personality. Typically 1–4 people reply per round, with natural pauses between speakers.

群聊模拟真实群组动态——不是每个人都会回复每条消息。人格根据相关性、专业度和性格决定是否发言。每轮通常 1-4 人回复，发言之间有自然停顿。

### Real-time Topics 实时话题

Personas can search the web when you discuss current events, then respond in character with their own perspective.

当你聊到时事新闻时，人格会搜索网络获取信息，然后以角色的视角和态度回应。

---

## Privacy 隐私

Your materials and generated personas are stored **locally only** in `input/` and `skills/personas/`. Nothing is uploaded anywhere. These directories are git-ignored by default.

你上传的素材和生成的人格文件仅保存在本地的 `input/` 和 `skills/personas/`，不会上传到任何地方。这些目录默认被 git 忽略。

---

## Project Structure 项目结构

```
soulchat/
├── install.sh              # One-click setup script 一键安装脚本
├── server.py               # Setup wizard server 安装向导服务
├── web/index.html           # Upload wizard UI 上传向导页面
├── extractors/              # File parsers (PDF, ePub, JSON, TXT)
├── skills/
│   ├── soulchat/SKILL.md   # Main command 主命令
│   ├── soul-toggle/SKILL.md # Chat mode controller 聊天模式控制
│   └── personas/            # Generated personas (git-ignored)
├── templates/               # Persona template 人格模板
└── input/                   # User materials (git-ignored)
```

## License

MIT
