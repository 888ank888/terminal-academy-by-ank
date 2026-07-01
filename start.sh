#!/zsh
# Start the Terminal Academy desktop application with one command
echo "[SYSTEM] Resolving ports and starting Terminal Academy dev stack..."
lsof -ti:5173 | xargs kill -9 2>/dev/null || true
cd "$(dirname "$0")/terminal-academy-desktop"
npm run desktop
