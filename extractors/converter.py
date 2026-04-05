"""统一文件转换入口：任意格式 → 纯文本"""

from pathlib import Path

# 超过 50K 字符采样（书籍类内容压缩，对话/描述类通常不触发）
SAMPLE_THRESHOLD = 50_000


def convert(file_path: str | Path) -> str:
    """根据文件扩展名选择解析器，返回纯文本内容。"""
    path = Path(file_path)
    suffix = path.suffix.lower()

    match suffix:
        case ".pdf":
            from .pdf_parser import parse_pdf
            text = parse_pdf(path)
        case ".epub":
            from .epub_parser import parse_epub
            text = parse_epub(path)
        case ".txt" | ".md":
            text = path.read_text(encoding="utf-8")
        case ".json":
            from .chat_parser import parse_chat_json
            text = parse_chat_json(path)
        case _:
            raise ValueError(f"不支持的文件格式: {suffix}")

    if len(text) > SAMPLE_THRESHOLD:
        text = _sample(text)

    return text


def _sample(text: str) -> str:
    """均匀采样：保留开头 + 中间跳读 + 结尾，控制在 50K 字符左右。"""
    lines = text.split("\n")
    total = len(lines)

    # 单行超长文本：按字符截取
    if total <= 1:
        return text[:50_000]

    # 目标：约 50K 字符
    target_chars = 50_000
    avg_chars_per_line = len(text) / total if total > 0 else 80
    target_lines = int(target_chars / avg_chars_per_line)

    # 分配：前 30% 给开头，50% 给中间采样，20% 给结尾
    head_lines = max(target_lines * 3 // 10, 50)
    tail_lines = max(target_lines * 2 // 10, 30)
    mid_target = target_lines - head_lines - tail_lines

    head = lines[:head_lines]
    tail = lines[-tail_lines:]
    mid_source = lines[head_lines:-tail_lines] if tail_lines else lines[head_lines:]

    # 中间部分均匀采样
    if len(mid_source) > mid_target and mid_target > 0:
        step = max(len(mid_source) // mid_target, 2)
        mid = mid_source[::step]
    else:
        mid = mid_source

    return "\n".join(head + mid + tail)
