#!/usr/bin/env bash
# Build, audit and publish pixiespantryshop.com to the gh-pages branch.
#
#   hub/deploy.sh            # build + audit + show what would change (dry run)
#   hub/deploy.sh --push     # ...and commit + push to gh-pages (goes live)
#
# ig/ and pins/ exist only on gh-pages (social image assets added by hand). They are never
# touched or deleted by a deploy. Everything else on gh-pages is replaced by hub/dist/.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 hub/build.py
python3 hub/audit.py | sed -n '/AUDIT CHECKS/,$p' | tee /tmp/pp_audit.txt
grep -q "clean" /tmp/pp_audit.txt || { echo "Audit not clean -- refusing to deploy."; exit 1; }

WT=.worktrees/ghp
if [ ! -e "$WT/.git" ]; then
  git fetch -q origin gh-pages --depth 1
  git worktree add -f "$WT" origin/gh-pages >/dev/null
fi
git -C "$WT" fetch -q origin gh-pages --depth 1
git -C "$WT" checkout -q --detach origin/gh-pages

rsync -a --delete --exclude '.git' --exclude 'ig/' --exclude 'pins/' hub/dist/ "$WT"/
git -C "$WT" add -A
echo "--- changes vs live:"
git -C "$WT" diff --cached --stat | tail -3

if [ "${1:-}" = "--push" ]; then
  git -C "$WT" commit -qm "Deploy $(date -u +%Y-%m-%dT%H:%MZ) from $(git rev-parse --short HEAD)"
  git -C "$WT" push -q origin HEAD:gh-pages
  echo "Live. GitHub Pages usually updates within a minute or two."
else
  git -C "$WT" reset -q
  echo "Dry run only. Re-run with --push to go live."
fi
