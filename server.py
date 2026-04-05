"""SoulChat 安装向导 — 素材上传与解析，完成后自动退出"""

import shutil
import sys
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

from extractors import convert

app = FastAPI(title="SoulChat Setup")

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
INPUT_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".epub", ".txt", ".md", ".json"}
MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20MB
MAX_PASTE_SIZE = 2_000_000  # 2M chars


@app.get("/", response_class=HTMLResponse)
async def index():
    return (BASE_DIR / "web" / "index.html").read_text(encoding="utf-8")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if file.size and file.size > MAX_UPLOAD_SIZE:
        return JSONResponse({"ok": False, "error": "文件过大，最大 20MB"}, status_code=413)
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        return JSONResponse(
            {"ok": False, "error": f"不支持的格式: {suffix}，支持 {', '.join(sorted(ALLOWED_EXTENSIONS))}"},
            status_code=400,
        )

    # 防止路径遍历
    safe_name = Path(file.filename).name
    dest = INPUT_DIR / safe_name
    if not dest.resolve().is_relative_to(INPUT_DIR.resolve()):
        return JSONResponse({"ok": False, "error": "非法文件名"}, status_code=400)

    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        text = convert(dest)
    except Exception as e:
        return JSONResponse({"ok": False, "error": f"解析失败: {e}"}, status_code=400)

    txt_name = dest.stem + ".txt"
    txt_path = INPUT_DIR / txt_name
    txt_path.write_text(text, encoding="utf-8")

    return {
        "ok": True,
        "filename": file.filename,
        "output": txt_name,
        "chars": len(text),
        "preview": text[:500],
    }


@app.post("/paste")
async def paste(text: str = Form(...), name: str = Form("paste")):
    if not text.strip():
        return JSONResponse({"ok": False, "error": "内容为空"}, status_code=400)
    if len(text) > MAX_PASTE_SIZE:
        return JSONResponse({"ok": False, "error": f"文本过长，最大 {MAX_PASTE_SIZE:,} 字符"}, status_code=413)

    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    txt_path = INPUT_DIR / f"{safe_name}.txt"
    txt_path.write_text(text.strip(), encoding="utf-8")

    return {
        "ok": True,
        "output": txt_path.name,
        "chars": len(text.strip()),
        "preview": text.strip()[:500],
    }


@app.post("/shutdown")
async def shutdown(lang: str = "zh"):
    """向导完成，保存语言偏好，关闭服务器"""
    (BASE_DIR / ".lang").write_text(lang)
    import asyncio
    asyncio.get_running_loop().call_later(0.5, lambda: sys.exit(0))
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
