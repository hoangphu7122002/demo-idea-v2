#!/usr/bin/env bash
# Placeholder deploy: a real target would pull these tags and run migrate -> api -> worker.
set -euo pipefail
TAG="${1:?usage: deploy.sh <sha>}"
echo "would deploy backend:${TAG} (roles: migrate, api, worker) and web:${TAG}"
