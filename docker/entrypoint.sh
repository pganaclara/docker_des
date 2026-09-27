#!/bin/sh
# =============================================================================
# des-entrypoint — start one supervisor node inside its container
# =============================================================================
#   des-entrypoint <node-id>        (compose passes it as `command`)
#
# Picks the binary compiled for that node id (the engine's routing tables are
# compile-time, so the image carries one binary per node) and execs it, so the
# node replaces the shell and receives docker's SIGTERM. The image runs as the
# unprivileged user `des` (Dockerfile).
# =============================================================================
set -eu

id="${1:-${DES_NODE_ID:-}}"
if [ -z "$id" ]; then
    echo "usage: des-entrypoint <node-id>" >&2
    exit 3
fi
bin="/opt/des/bin/des_node${id}"
if [ ! -x "$bin" ]; then
    echo "this image has no binary for node ${id}:" >&2
    cat /opt/des/bin/BUILD_INFO >&2
    echo "rebuild with DES_NUM_NODES >= ${id}" >&2
    exit 3
fi
nodes="$(sed -n 's/^DES_NUM_NODES=//p' /opt/des/bin/BUILD_INFO)"

exec "$bin" "$id" "$nodes"
