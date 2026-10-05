#!/usr/bin/env bash
# Turn a fresh clone of lean-web-stack into a new project:
#   - sets PROJECT_NAME / APP_NAME in .env.example (Docker project, image names, API title)
#   - updates the API title in backend/openapi.json so the CI contract check stays green
#   - resets git history to one initial commit and drops the template's origin remote
set -euo pipefail

NAME="${1:-}"
if [[ ! "$NAME" =~ ^[a-z][a-z0-9-]*$ ]]; then
  echo "usage: scripts/new-project.sh <name>   (lowercase letters, digits, dashes; e.g. acme-notes)" >&2
  exit 1
fi

cd "$(dirname "$0")/.."

sed -i.bak -e "s/^PROJECT_NAME=.*/PROJECT_NAME=${NAME}/" -e "s/^APP_NAME=.*/APP_NAME=${NAME}/" .env.example
rm -f .env.example.bak
sed -i.bak -e "1s/.*/# ${NAME}/" README.md
rm -f README.md.bak
sed -i.bak -e "s/\"title\": \"myapp API\"/\"title\": \"${NAME} API\"/" backend/openapi.json
rm -f backend/openapi.json.bak
[[ -f .env ]] && rm .env

rm -rf .git
git init -q -b main
git add -A
git commit -q -m "chore: start ${NAME} from lean-web-stack"

echo "Project '${NAME}' ready. Next:"
echo "  git remote add origin git@github.com:<you>/${NAME}.git"
echo "  make setup"
echo "  make check"
