---
name: soulchat
description: Extract personas from materials and start chatting. Auto-guides users through the full flow. 从素材提取人格并开始聊天，自动引导全流程。
allowed-tools: Read Write Edit Bash Grep Glob
argument-hint: "[<name> | group/群聊 | extract | list | delete <name>]"
---

# SoulChat

## Arguments 参数

`$ARGUMENTS`

## Quick Start 快捷用法

- `/soulchat Jobs` → Chat with Jobs directly 直接和 Jobs 聊天
- `/soulchat group` or `/soulchat 群聊` → Group chat with all personas 所有人格群聊
- `/soulchat` → Guided flow 进入引导

If `$ARGUMENTS` matches an existing persona name → execute soul-toggle on {name}, skip guidance.
如果参数匹配已有人格名字，直接执行 soul-toggle on {名字}，跳过引导。

If `$ARGUMENTS` is "group" or "群聊" → execute soul-toggle group.
如果参数是「群聊」或「group」，直接执行 soul-toggle group。

## Guided Flow 引导流程（no args or no match 无参数或不匹配时）

Do NOT show a command table. Guide the user like a friend, in natural language.
不要显示命令表。像朋友一样用自然语言引导。

1. Check `skills/personas/` for existing personas 检查是否已有人格：
   - **1 persona 有 1 个** → "Want to chat with {name}? Just say the name. 要和 {名字} 聊吗？"
   - **Multiple 有多个** → List names, then say:
     "Who do you want to chat with? Just say a name. Or say 'group' to chat with everyone.
      想和谁聊？说名字就行。也可以说『群聊』让大家一起。
      Next time: `/soulchat Jobs` to skip this step. 下次可以直接 `/soulchat 名字` 跳过这步。"
   - **None 没有** → Continue to step 2 继续

2. Check `input/` for materials 检查素材：
   - **Has 1 material 只有 1 个素材** → **DO NOT ASK. DO NOT show options 1/2/3. Immediately start extraction with this file. Say only:** "正在为你创建人格..." / "Creating persona from {filename}..." then go straight to Extract.
     **不要问。不要显示选项。直接用这个文件开始提取。只说一句"正在创建..."然后开干。**
   - **Has multiple 有多个素材** → List filenames ONLY, ask: "Which one? 用哪个？" Nothing else.
     只列文件名，问「用哪个？」不要加多余选项。
   - **Empty 没有素材** → "Who do you want to chat with? You can:
     1. Describe the person directly 直接描述这个人的特点
     2. Give me a file path 给我一个文件路径
     3. If the file is on Desktop/Downloads, run in terminal: `! cp ~/Desktop/file input/`
        如果文件在桌面或下载文件夹，先运行：`! cp ~/Desktop/文件名 input/`"

3. If user gives a file path, parse with extractors (supports PDF/ePub/JSON/TXT/MD):
   如果用户给了文件路径，用 extractors 解析：
   ```bash
   uv run python -c "from extractors import convert; print(convert('path'))"
   ```
   Save result to `input/`. If read fails (permission issue), prompt user to `! cp` first.
   保存到 `input/`。如果读取失败（权限问题），提示用户先用 `! cp`。

4. Once material is selected, start extraction immediately. No extra commands needed.
   选定素材后直接开始提取，不需要用户再输入任何命令。

**Tone: friendly and concise. No technical jargon. Never mention SKILL.md / persona / extract.**
**语气：简洁友好，不用技术术语，不提 SKILL.md / persona / extract。**

## Extract 提取人格

When user provides material (file or description), extract persona:
当用户提供了素材（文件或描述），执行提取：

1. Read the material file in `input/` (already pre-processed and sampled for large files). **Read the whole file in one go — do NOT split into multiple reads.** Focus on extracting personality, not memorizing every detail.
   读取 `input/` 中的素材文件（大文件已预处理采样）。**一次性读完，不要分多次读。** 专注提取人格特征，不需要记住每个细节。

   Analyze 分析：
   - **Identity 核心身份**: Who is this person, background 这个人是谁，什么背景
   - **Personality 性格特征**: Key personality traits 突出的性格标签
   - **Speech style 语言风格**: Catchphrases, sentence patterns, vocabulary, emotional expression 口头禅、句式偏好、常用词汇、情绪表达
   - **Response language 回复语言**: Match the source material's language 根据素材语言决定
   - **Knowledge 知识边界**: Expert topics 擅长什么话题
   - **Constraints 行为约束**: What they won't do 不会做的事
   - **Example dialogues 示例对话**: 3-5 rounds of typical conversation 3-5 轮典型对话

2. Read `templates/soul_template.md`, generate persona file following the template.
   读取模板，按模板格式生成人格文件。

3. Auto-name using the person's name (English kebab-case), save to `skills/personas/{name}/SKILL.md`.
   自动用人物名字命名（kebab-case），保存到 `skills/personas/{name}/SKILL.md`。

4. After creation, tell user:
   创建完成后：
   ```
   ✅ {display_name} is ready! 已就绪！
   
   Start chatting now? 现在要开始聊天吗？
   ```
   If yes → execute soul-toggle on. 用户说是 → 自动执行 soul-toggle on。
   If other personas exist, also suggest: "Or say 'group' to chat with everyone.
   也可以说『群聊』让大家一起聊。"

## List 列出人格

List all personas in `skills/personas/`, show name + one-line description.
列出所有人格，简洁展示名字和一句话描述。

## Delete 删除 <name>

Confirm, then delete `skills/personas/{name}/` directory.
确认后删除人格目录。
