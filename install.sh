#!/bin/bash
# SoulChat — One-click setup / 一键安装

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# ── Detect system language for initial output ──
SYS_LANG="${LANG:-en}"

msg() {
  # msg "中文" "English"
  if [[ "$UI_LANG" == "en" ]] || { [[ -z "$UI_LANG" ]] && [[ "$SYS_LANG" != zh* ]]; }; then
    echo "  $2"
  else
    echo "  $1"
  fi
}

echo ""
echo "  SoulChat"
echo "  ──────────────────────"
echo ""

# ── 1. Check Claude Code ──
if ! command -v claude &>/dev/null; then
  msg "✘ 未检测到 Claude Code" "✘ Claude Code not found"
  echo ""
  msg "请先安装：https://claude.ai/code" "Please install first: https://claude.ai/code"
  echo ""
  exit 1
fi
msg "✓ Claude Code 已就绪" "✓ Claude Code ready"

# ── 2. Install dependencies ──
if ! command -v uv &>/dev/null; then
  msg "正在安装 uv..." "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh 2>/dev/null
  export PATH="$HOME/.local/bin:$PATH"
fi
msg "正在安装依赖..." "Installing dependencies..."
if ! uv sync --quiet; then
  msg "✘ 依赖安装失败，请检查网络" "✘ Dependency install failed, check network"
  exit 1
fi
msg "✓ 依赖已安装" "✓ Dependencies installed"

# ── 3. Create global command ──
LAUNCHER="$SCRIPT_DIR/bin/soulchat"
mkdir -p "$SCRIPT_DIR/bin"
cat > "$LAUNCHER" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
exec claude --plugin-dir .
EOF
chmod +x "$LAUNCHER"

LINK_TARGET=""
LINKED=false
# Prefer ~/.local/bin (create if needed — uv uses this too)
if [ -d "$HOME/.local/bin" ] || mkdir -p "$HOME/.local/bin" 2>/dev/null; then
  LINK_TARGET="$HOME/.local/bin/soulchat"
elif [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
  LINK_TARGET="/usr/local/bin/soulchat"
fi

if [ -n "$LINK_TARGET" ]; then
  if ln -sf "$LAUNCHER" "$LINK_TARGET" 2>/dev/null; then
    LINKED=true
    LINK_DIR="$(dirname "$LINK_TARGET")"
    # Auto-add to PATH if not already there
    if ! echo "$PATH" | tr ':' '\n' | grep -qx "$LINK_DIR"; then
      SHELL_RC="$HOME/.zshrc"
      [ -n "$BASH_VERSION" ] && SHELL_RC="$HOME/.bashrc"
      if ! grep -q "$LINK_DIR" "$SHELL_RC" 2>/dev/null; then
        echo "export PATH=\"$LINK_DIR:\$PATH\"" >> "$SHELL_RC"
      fi
      export PATH="$LINK_DIR:$PATH"
    fi
    msg "✓ 全局命令已创建：soulchat" "✓ Global command created: soulchat"
  fi
fi

if [ "$LINKED" = false ]; then
  msg "⚠ 无法创建全局命令，每次启动请运行：" "⚠ Could not create global command. To launch, run:"
  echo "  cd $SCRIPT_DIR && claude --plugin-dir ."
fi

# ── 4. Launch setup wizard ──
echo ""
msg "正在打开素材上传页面..." "Opening material upload page..."
echo "  ───────────────────────"
echo "  → http://127.0.0.1:8000"
echo ""

if command -v open &>/dev/null; then
  (sleep 1 && open "http://127.0.0.1:8000") &
elif command -v xdg-open &>/dev/null; then
  (sleep 1 && xdg-open "http://127.0.0.1:8000") &
fi

# Start wizard server (exits when user clicks "Done")
uv run python server.py

# ── 5. Read user's language choice from wizard ──
UI_LANG="zh"
if [ -f "$SCRIPT_DIR/.lang" ]; then
  UI_LANG="$(cat "$SCRIPT_DIR/.lang")"
fi

# ── 6. Launch Claude Code ──
echo ""
msg "✓ 素材已就绪" "✓ Materials ready"
msg "正在启动 SoulChat..." "Launching SoulChat..."
echo ""
if [ "$LINKED" = true ]; then
  msg "💡 下次启动只需输入：soulchat" "💡 Next time, just run: soulchat"
else
  msg "💡 下次启动请运行：" "💡 Next time, run:"
  echo "  cd $SCRIPT_DIR && claude --plugin-dir ."
fi
echo ""

cd "$SCRIPT_DIR"
exec claude --plugin-dir .
