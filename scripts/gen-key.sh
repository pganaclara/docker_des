#!/usr/bin/env bash
# =============================================================================
# gen-key.sh — create the cell's shared authentication key
# =============================================================================
# Every frame is signed with HMAC-SHA256 under this key (engine/des_generic.h,
# section 6a). All nodes of a cell need the same one. It is handed to the
# containers as a Docker secret (compose.yaml), so it never enters an image.
#
#   scripts/gen-key.sh            create secrets/des_auth_key if missing
#   scripts/gen-key.sh --force    replace it
#
# To let an ESP32 join the same cell, put the same 64 characters in its
# secrets.h as DES_AUTH_KEY.
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

key_file=secrets/des_auth_key
mkdir -p secrets
chmod 700 secrets            # the directory keeps other host users out

if [[ -s $key_file && ${1:-} != --force ]]; then
    echo "$key_file already exists (use --force to replace it)"
    exit 0
fi

# 32 random bytes as 64 hex characters, same as secrets.token_hex(32).
key=$(od -An -N32 -tx1 /dev/urandom | tr -d ' \n')
[[ ${#key} -eq 64 ]] || { echo "could not read /dev/urandom" >&2; exit 1; }
printf '%s\n' "$key" > "$key_file"
# Readable by the container's unprivileged user, which is not your host uid.
chmod 644 "$key_file"
echo "wrote $key_file (64 hex characters)"
