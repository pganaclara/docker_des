#!/usr/bin/env bash
# =============================================================================
# run-all.sh — the scaling sweep: FMS on 1, 2, 3, 4, 5, 6 and 7 containers
# =============================================================================
#   scripts/run-all.sh                     the sweep, once
#   REPEAT=5 scripts/run-all.sh            the sweep, 5 times (mean ± sd)
#   scripts/run-all.sh 1 2 7               only these node counts
#   scripts/run-all.sh extras/fms-7-loss5  any other scenario, by path
#
# Every decryption takes 69 ms, as on an ESP32-S3 (compose.yaml default);
# DES_EMU_SCALARMUL_MS=0 scripts/run-all.sh runs at the PC's own speed.
#
# Writes everything to results/<timestamp>-varredura/: one folder per run
# (scripts/run.sh), plus escala.md / escala.json (scripts/scaling.py): time
# per step against the number of containers, the speed-up over one container,
# and the lower bound set by the busiest node's decryptions.
# =============================================================================
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

names=()
if (($#)); then
    for a in "$@"; do
        if [[ $a =~ ^[0-9]+$ ]]; then names+=("fms-$a"); else names+=("${a%.env}"); fi
    done
else
    for n in 1 2 3 4 5 6 7; do names+=("fms-$n"); done
fi
repeat=${REPEAT:-1}

has_netem=0
if zcat /proc/config.gz 2>/dev/null | grep -q '^CONFIG_NET_SCH_NETEM=[ym]' ||
   modinfo sch_netem >/dev/null 2>&1; then has_netem=1; fi

batch="results/$(date +%Y%m%d-%H%M%S)-varredura"
mkdir -p "$batch"
echo "emulação: DES_EMU_SCALARMUL_MS=${DES_EMU_SCALARMUL_MS:-69} ms  ·  repetições: $repeat  ·  saída: $batch"

declare -A pass fail skip built
for ((r = 1; r <= repeat; ++r)); do
    for n in "${names[@]}"; do
        f="scenarios/$n.env"
        [[ -f $f ]] || { skip[$n]="no such scenario"; continue; }
        if grep -qE '^DES_NETEM=.+' "$f" && ((!has_netem)); then
            skip[$n]="skipped (kernel has no netem)"; continue
        fi
        echo; echo "################ $n  (repetição $r/$repeat)"
        # Build each image once per sweep, not once per repetition.
        if [[ -n ${built[$n]:-} ]]; then sb=1; else sb=${DES_SKIP_BUILD:-0}; fi
        if QUIET=1 DES_SKIP_BUILD=$sb DES_RESULTS_DIR="$batch" scripts/run.sh "$f"; then
            pass[$n]=$(( ${pass[$n]:-0} + 1 ))
        else
            fail[$n]=$(( ${fail[$n]:-0} + 1 ))
        fi
        built[$n]=1
    done
done

echo; echo "================ vereditos"
status=0
for n in "${names[@]}"; do
    if [[ -n ${skip[$n]:-} ]]; then printf '  %-22s %s\n' "$n" "${skip[$n]}"; continue; fi
    p=${pass[$n]:-0}; x=${fail[$n]:-0}
    printf '  %-22s %s\n' "$n" "$( ((x)) && echo "FAIL ($x de $((p + x)))" || echo "PASS ($p de $p)")"
    ((x)) && status=1
done
echo
python3 scripts/scaling.py "$batch" || status=1
exit $status
