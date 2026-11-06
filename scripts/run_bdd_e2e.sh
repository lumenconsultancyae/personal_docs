#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${PORTFOLIO_BASE_URL:-http://host.docker.internal:3005}"
MAX_ATTEMPTS=30
SLEEP_SECONDS=2

echo "Waiting for portfolio application health at ${BASE_URL} ..."
for ((i = 1; i <= MAX_ATTEMPTS; i++)); do
    if curl -fsS "${BASE_URL}/" >/dev/null 2>&1; then
        echo "Application is healthy at ${BASE_URL} (attempt ${i}/${MAX_ATTEMPTS})."
        break
    fi
    if [ "${i}" -eq "${MAX_ATTEMPTS}" ]; then
        echo "ERROR: Application at ${BASE_URL} did not become ready within $((MAX_ATTEMPTS * SLEEP_SECONDS))s." >&2
        exit 1
    fi
    sleep "${SLEEP_SECONDS}"
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}/tests/bdd"
behave features/portfolio_ux.feature
