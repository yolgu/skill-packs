#!/usr/bin/env bash
# Links this skill pack into the locations each agent harness reads.
#
#   Claude Code: ~/.claude/CLAUDE.md, ~/.claude/agents, ~/.claude/skills/<skill>
#   Codex:       ~/.codex/AGENTS.md,  ~/.codex/agents,  ~/.agents/skills/<skill>
#
# Re-running refreshes existing links and removes links to skills that left the pack.
# A real file or folder at a destination is never replaced: it is reported, and the
# script exits non-zero so the owner can move it aside and run again.
set -euo pipefail
shopt -s nullglob

PACK_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly PACK_ROOT
skipped_count=0

link() {
  local source="$1" destination="$2"
  if [[ -L "$destination" ]]; then
    ln -sfn "$source" "$destination"
  elif [[ -e "$destination" ]]; then
    echo "skipped, real file or folder exists: $destination" >&2
    skipped_count=$((skipped_count + 1))
    return 0
  else
    ln -s "$source" "$destination"
  fi
  echo "linked: $destination -> $source"
}

remove_links_to_departed_skills() {
  local skills_dir="$1" entry
  for entry in "$skills_dir"/*; do
    if [[ -L "$entry" && ! -e "$entry" && "$(readlink "$entry")" == "$PACK_ROOT"/* ]]; then
      rm "$entry"
      echo "removed link to departed skill: $entry"
    fi
  done
}

link_skills() {
  local skills_dir="$1" source_dir skill
  shift
  mkdir -p "$skills_dir"
  for source_dir in "$@"; do
    for skill in "$source_dir"/*/; do
      skill="${skill%/}"
      link "$skill" "$skills_dir/$(basename "$skill")"
    done
  done
  remove_links_to_departed_skills "$skills_dir"
}

install_claude() {
  local config_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
  mkdir -p "$config_dir"
  link "$PACK_ROOT/claude/CLAUDE.md" "$config_dir/CLAUDE.md"
  link "$PACK_ROOT/claude/agents" "$config_dir/agents"
  link_skills "$config_dir/skills" "$PACK_ROOT/common/skills" "$PACK_ROOT/claude/skills"
}

install_codex() {
  local codex_home="${CODEX_HOME:-$HOME/.codex}"
  mkdir -p "$codex_home"
  link "$PACK_ROOT/codex/AGENTS.md" "$codex_home/AGENTS.md"
  link "$PACK_ROOT/codex/agents" "$codex_home/agents"
  link_skills "$HOME/.agents/skills" "$PACK_ROOT/common/skills" "$PACK_ROOT/codex/skills"
}

main() {
  case "${1:-all}" in
    claude) install_claude ;;
    codex) install_codex ;;
    all) install_claude; install_codex ;;
    *) echo "usage: $0 [claude|codex|all]" >&2; exit 2 ;;
  esac

  if ((skipped_count > 0)); then
    echo "$skipped_count destination(s) skipped; move them aside and run again." >&2
    exit 1
  fi
}

main "$@"
