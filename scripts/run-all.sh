#!/usr/bin/env bash
# =============================================================================
# run-all.sh — every scenario in scenarios/, one after the other, one verdict
# =============================================================================
#   scripts/run-all.sh                  all of them
#   scripts/run-all.sh fms-2 fms-7      only these (names without .env)
#
# Scenarios that shape the link with netem (DES_NETEM set) are skipped when the
# kernel has no sch_netem — the default WSL 2 kernel does not.
# =============================================================================
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

if (($#)); then names=("$@"); else
    names=(); for f in scenarios/*.env; do names+=("$(basename "$f" .env)"); done
fi

has_netem=0
if zcat /proc/config.gz 2>/dev/null | grep -q '^CONFIG_NET_SCH_NETEM=[ym]' ||
   modinfo sch_netem >/dev/null 2>&1; then has_netem=1; fi

declare -A verdict
for n in "${names[@]}"; do
    f="scenarios/$n.env"
    [[ -f $f ]] || { verdict[$n]="no such scenario"; continue; }
    if grep -qE '^DES_NETEM=.+' "$f" && ((!has_netem)); then
        verdict[$n]="skipped (kernel has no netem)"; continue
    fi
    echo; echo "################ $n"
    if QUIET=1 scripts/run.sh "$f"; then verdict[$n]="PASS"; else verdict[$n]="FAIL"; fi
done

echo; echo "================ verdicts"
fail=0
for n in "${names[@]}"; do
    printf '  %-22s %s\n' "$n" "${verdict[$n]}"
    [[ ${verdict[$n]} == FAIL || ${verdict[$n]} == "no such scenario" ]] && fail=1
done
exit $fail
