#!/usr/bin/env bash
# =============================================================================
# run.sh — build, run and summarise one scenario
# =============================================================================
#   scripts/run.sh                              scenarios/fms-7.env
#   scripts/run.sh scenarios/fms-2.env
#   QUIET=1 scripts/run.sh scenarios/fms-7.env  no live log, summary only
#   DES_SKIP_BUILD=1 scripts/run.sh ...          reuse the image already built
#
# Starts node1..nodeN (N = DES_NUM_NODES of the scenario), waits for every
# container to exit, then writes to results/<timestamp>-<scenario>/:
#   nodeK.log      the node's full log
#   summary.md     per-node table and verdict (scripts/summarize.py)
#   summary.json   the same, machine-readable
# Exit status: summarize.py's — 0 when every expectation in the scenario holds
# (EXPECT_* lines, including the outcome: a scenario written to halt passes
# when it halts), 1 otherwise.
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

scenario=${1:-scenarios/fms-7.env}
[[ -f $scenario ]] || { echo "no such scenario: $scenario" >&2; exit 2; }

# Only N is needed here; compose reads the whole file itself.
nodes=$(sed -n 's/^DES_NUM_NODES=["]*\([0-9]\+\).*/\1/p' "$scenario")
[[ -n $nodes ]] || { echo "$scenario does not set DES_NUM_NODES" >&2; exit 2; }
(( nodes >= 1 && nodes <= 7 )) || {
    echo "compose.yaml defines node1..node7; add services for $nodes nodes" >&2; exit 2; }

[[ -s secrets/des_auth_key ]] || scripts/gen-key.sh

name=$(basename "$scenario" .env)
out="results/$(date +%Y%m%d-%H%M%S)-$name"
mkdir -p "$out"
cp "$scenario" "$out/scenario.env"

services=()
for ((k = 1; k <= nodes; ++k)); do services+=("node$k"); done
dc=(docker compose --env-file "$scenario")

if [[ ${DES_SKIP_BUILD:-0} == 1 ]]; then
    echo "== build skipped (DES_SKIP_BUILD=1): using the existing image"
else
    echo "== build ($scenario)"
    "${dc[@]}" build "${services[0]}"
fi
"${dc[@]}" down --remove-orphans >/dev/null 2>&1 || true

echo "== run: ${services[*]}"
if [[ ${QUIET:-0} == 1 ]]; then
    "${dc[@]}" up --no-build --detach "${services[@]}" >/dev/null
    "${dc[@]}" wait "${services[@]}" >/dev/null || true
else
    # Attached: interleaved, prefixed logs; returns when every node has exited.
    "${dc[@]}" up --no-build "${services[@]}" || true
fi

echo "== collect -> $out"
for s in "${services[@]}"; do
    "${dc[@]}" logs --no-color --no-log-prefix "$s" > "$out/$s.log" 2>&1 || true
    cid=$("${dc[@]}" ps -aq "$s")
    code=$(docker inspect -f '{{.State.ExitCode}}' "$cid" 2>/dev/null || echo 255)
    echo "$code" > "$out/$s.exit"
done
docker image inspect -f '{{.Id}}' "$("${dc[@]}" config --images | head -1)" \
    > "$out/image.id" 2>/dev/null || true
docker run --rm --entrypoint cat "$("${dc[@]}" config --images | head -1)" \
    /opt/des/bin/BUILD_INFO > "$out/BUILD_INFO" 2>/dev/null || true
"${dc[@]}" down --remove-orphans >/dev/null 2>&1 || true

python3 scripts/summarize.py "$out"
