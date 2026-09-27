#!/usr/bin/env bash
# =============================================================================
# sync-engine.sh — refresh engine/ from a clone of esp32_crypto
# =============================================================================
#   scripts/sync-engine.sh ../esp32_crypto            copy, re-hash, record commit
#   scripts/sync-engine.sh --check ../esp32_crypto    only report differences
#
# engine/ must stay a verbatim copy of esp32_crypto/des_distributed/ — that is
# what makes "the container runs the same code as the boards" true. This script
# is the only thing that should ever write to it.
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

check=0
if [[ ${1:-} == --check ]]; then check=1; shift; fi
up=${1:?usage: scripts/sync-engine.sh [--check] <path-to-esp32_crypto-clone>}
src="$up/des_distributed"
[[ -f $src/des_generic.h ]] || { echo "$src/des_generic.h not found" >&2; exit 2; }

files=(des_generic.h des_transport.h
       supervisor_data_small_factory.h
       supervisor_data_extended_small_factory.h
       supervisor_data_fms.h)

changed=0
for f in "${files[@]}"; do
    if ! cmp -s "$src/$f" "engine/$f"; then
        echo "differs: $f"; changed=1
        ((check)) || cp "$src/$f" "engine/$f"
    fi
done
if ((check)); then
    ((changed)) && exit 1
    echo "engine/ matches $src"; exit 0
fi

(cd engine && sha256sum "${files[@]}" > SHA256SUMS)
commit=$(git -C "$up" log -1 --format='%H   (%cs)%n"%s"' 2>/dev/null || echo "unknown")
python3 - "$commit" <<'EOF'
import pathlib, re, sys
p = pathlib.Path("engine/UPSTREAM.md")
s = p.read_text()
s = re.sub(r"(no commit:\n\n```\n).*?(\n```)", lambda m: m.group(1) + sys.argv[1] + m.group(2), s, flags=re.S)
p.write_text(s)
EOF
if ((changed)); then
    echo "engine/ updated; SHA256SUMS and UPSTREAM.md rewritten. Rebuild and rerun"
    echo "scenarios/fms-2.env: its EXPECT_* values must still hold."
else
    echo "engine/ already matched; hashes and UPSTREAM.md refreshed"
fi
