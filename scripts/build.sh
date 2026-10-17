#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts
{
  printf 'Jenkins lab build report\n'
  printf 'UTC: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  printf 'Build: %s\n' "${BUILD_NUMBER:-local}"
  printf 'Commit: %s\n' "${GIT_COMMIT:-local}"
} > artifacts/report.txt
test -s artifacts/report.txt
cat artifacts/report.txt
