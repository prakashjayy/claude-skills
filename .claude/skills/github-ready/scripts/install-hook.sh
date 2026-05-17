#!/bin/sh
# Installs a commit-msg hook that strips Co-Authored-By lines from Anthropic.
# Safe to run multiple times (idempotent).

HOOK=".git/hooks/commit-msg"

if [ ! -d ".git" ]; then
  echo "ERROR: not a git repository. Run from the repo root." >&2
  exit 1
fi

mkdir -p .git/hooks

cat > "$HOOK" <<'HOOK_BODY'
#!/bin/sh
# Strip Co-Authored-By trailers added by AI assistants.
sed -i.bak '/^Co-Authored-By:.*noreply@anthropic\.com/Id' "$1"
rm -f "$1.bak"
HOOK_BODY

chmod +x "$HOOK"
echo "commit-msg hook installed at $HOOK"
