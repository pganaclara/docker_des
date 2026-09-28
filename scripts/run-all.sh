#!/usr/bin/env bash
# =============================================================================
# run-all.sh — the scaling sweep: FMS on 1, 2, 3, 4, 5, 6 and 7 containers
# =============================================================================
#   scripts/run-all.sh                     the sweep, once
#   REPEAT=5 scripts/run-all.sh            the sweep, 5 times (mean ± sd)
#   scripts/run-all.sh 1 2 7               only these node counts
#   scripts/run-all.sh s5                  S5 isolated vs block partition, N = 1..7
#   scripts/run-all.sh 4 4-s5              any scenario fms-<arg>
#   scripts/run-all.sh sobrecarga          container overhead: N = 1, 2, 4, 7 as
#                                          containers on the bridge (ponte), on
#                                          the host's network (host) and as
#                                          plain processes (nativo)
#   scripts/run-all.sh perda               frame loss: 2 nodes at 1-30 %, 7 nodes
#                                          at 1-10 % (scripts/loss.py)
#
# Every decryption takes 69 ms, as on an ESP32-S3 (compose.yaml default);
# DES_EMU_SCALARMUL_MS=0 scripts/run-all.sh runs at the PC's own speed.
#
# Writes everything to results/<timestamp>-varredura/: one folder per run
# (scripts/run.sh), plus escala.md / escala.json (scripts/scaling.py): time
# per step against the number of containers, the speed-up over one container,
# and the lower bound set by the busiest node's decryptions; and latencia.md /
# latencia.csv (scripts/latency.py): per-step latency percentiles; and, for the
# overhead scenarios, sobrecarga.md / sobrecarga.json (scripts/overhead.py).
# =============================================================================
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

names=()
if (($#)); then
    for a in "$@"; do
        if [[ $a == s5 ]]; then
            # S5 isolated against the block partition, same N side by side.
            names+=(fms-1)
            for n in 2 3 4 5 6; do names+=("fms-$n" "fms-$n-s5"); done
            names+=(fms-7)
        elif [[ $a == perda ]]; then
            for p in 1 5 10 20 30; do names+=("fms-2-perda$p"); done
            for p in 1 5 10; do names+=("fms-7-perda$p"); done
        elif [[ $a == sobrecarga ]]; then
            names+=(fms-1-ponte fms-1-nativo)
            for n in 2 4 7; do names+=("fms-$n-ponte" "fms-$n-host" "fms-$n-nativo"); done
        elif [[ $a =~ ^[0-9]+(-[a-z0-9]+)?$ ]]; then names+=("fms-$a")
        else names+=("${a%.env}"); fi
    done
else
    for n in 1 2 3 4 5 6 7; do names+=("fms-$n"); done
fi
repeat=${REPEAT:-1}

batch="results/$(date +%Y%m%d-%H%M%S)-varredura"
mkdir -p "$batch"
echo "emulação: DES_EMU_SCALARMUL_MS=${DES_EMU_SCALARMUL_MS:-69} ms  ·  repetições: $repeat  ·  saída: $batch"

declare -A pass fail skip built
for ((r = 1; r <= repeat; ++r)); do
    for n in "${names[@]}"; do
        f="scenarios/$n.env"
        [[ -f $f ]] || { skip[$n]="no such scenario"; continue; }
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
python3 scripts/latency.py "$batch" > /dev/null &&
    echo "percentis de latência por passo: $batch/latencia.md"
if compgen -G "$batch/*-fms-*-perda*" > /dev/null; then
    python3 scripts/loss.py "$batch" || status=1
fi
if compgen -G "$batch/*-fms-*-ponte" > /dev/null; then
    python3 scripts/overhead.py "$batch" || status=1
fi
exit $status
