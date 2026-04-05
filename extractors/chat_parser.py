"""ChatGPT / Claude 导出 JSON → 对话文本 + 风格摘要"""

import json
from pathlib import Path


def parse_chat_json(file_path: Path) -> str:
    data = json.loads(file_path.read_text(encoding="utf-8"))

    # 尝试检测格式
    if isinstance(data, list) and len(data) > 0:
        first = data[0]
        if "mapping" in first:
            return _parse_chatgpt(data)
        if "uuid" in first and "chat_messages" in first:
            return _parse_claude(data)

    # 单个对话对象
    if isinstance(data, dict):
        if "mapping" in data:
            return _parse_chatgpt([data])
        if "chat_messages" in data:
            return _parse_claude([data])

    raise ValueError("无法识别的 JSON 格式。支持 ChatGPT 和 Claude 官方导出格式。")


def _parse_chatgpt(conversations: list[dict]) -> str:
    """解析 ChatGPT conversations.json 导出格式"""
    all_messages = []

    for conv in conversations:
        title = conv.get("title", "无标题")
        all_messages.append(f"## {title}\n")

        mapping = conv.get("mapping", {})
        # 按 create_time 排序
        nodes = []
        for node in mapping.values():
            msg = node.get("message")
            if msg and msg.get("content", {}).get("parts"):
                role = msg.get("author", {}).get("role", "unknown")
                text = "\n".join(
                    str(p) for p in msg["content"]["parts"] if isinstance(p, str)
                )
                create_time = msg.get("create_time") or 0
                if text.strip():
                    nodes.append((create_time, role, text.strip()))

        nodes.sort(key=lambda x: x[0])
        for _, role, text in nodes:
            label = "用户" if role == "user" else "助手"
            all_messages.append(f"**{label}**: {text}")

    return "\n\n".join(all_messages)


def _parse_claude(conversations: list[dict]) -> str:
    """解析 Claude conversations.json 导出格式"""
    all_messages = []

    for conv in conversations:
        name = conv.get("name", "无标题")
        all_messages.append(f"## {name}\n")

        for msg in conv.get("chat_messages", []):
            role = msg.get("sender", "unknown")
            content = msg.get("text", "")
            if not content and "content" in msg:
                parts = msg["content"]
                if isinstance(parts, list):
                    content = "\n".join(
                        p.get("text", "") for p in parts if isinstance(p, dict)
                    )
            if content.strip():
                label = "用户" if role == "human" else "助手"
                all_messages.append(f"**{label}**: {content.strip()}")

    return "\n\n".join(all_messages)
