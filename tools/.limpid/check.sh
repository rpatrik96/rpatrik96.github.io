#!/usr/bin/env bash
# Run the limpid gate over the prose in the tool pages.
#
#   tools/.limpid/check.sh                      # every tools/*/index.html
#   tools/.limpid/check.sh research-projects    # one page
#   tools/.limpid/check.sh --json               # machine-readable, for tracing
#
# LIMPID_CLI    path to apps/cli/dist/cli.js   (default: ~/Documents/GitHub/limpid/...)
# LIMPID_RULES  path to a house rules.json     (default: the vault's, if present)
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tools="$(dirname "$here")"
build="$here/build"
mkdir -p "$build"

cli="${LIMPID_CLI:-$HOME/Documents/GitHub/limpid/apps/cli/dist/cli.js}"
if [[ ! -f "$cli" ]]; then
  echo "limpid CLI not found at $cli" >&2
  echo "build it with: npm run build -w apps/cli   (in the limpid repo)" >&2
  exit 127
fi

# The house rules are the writing-voice ban list in detector form. They live with
# the vault, not in this repo, so the gate runs without them when they are absent.
default_rules="$HOME/Library/CloudStorage/GoogleDrive-reizinger.patrik@simonyi.bme.hu/My Drive/Dokumentumok/Notes/.limpid/rules.json"
rules="${LIMPID_RULES:-$default_rules}"

pages=()
passthru=()
for arg in "$@"; do
  case "$arg" in
    -*) passthru+=("$arg") ;;
    *)  pages+=("$arg") ;;
  esac
done
if [[ ${#pages[@]} -eq 0 ]]; then
  for d in "$tools"/*/; do
    [[ -f "$d/index.html" ]] && pages+=("$(basename "$d")")
  done
fi

extracted=()
for name in "${pages[@]}"; do
  page="$tools/$name/index.html"
  if [[ ! -f "$page" ]]; then
    echo "no such page: $page" >&2
    exit 1
  fi
  python3 "$here/extract_prose.py" "$page" "$build/$name.md" "$build/$name.map.json" >&2
  extracted+=("$build/$name.md")
done

args=(--register blog)
[[ -f "$rules" ]] && args+=(--rules "$rules") || echo "house rules not found at $rules; running the shipped rubric alone" >&2

node "$cli" "${extracted[@]}" "${args[@]}" ${passthru[@]+"${passthru[@]}"}
