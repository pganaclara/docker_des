#!/bin/sh
# =============================================================================
# des-entrypoint — start one supervisor node inside its container
# =============================================================================
#   des-entrypoint <node-id>        (compose passes it as `command`)
#
# 1. Picks the binary compiled for that node id (the engine's routing tables are
#    compile-time, so the image carries one binary per node).
# 2. Optionally shapes this container's egress with netem — delay, jitter and
#    loss on eth0 — to emulate a Wi-Fi link like the ESP32 testbed's
#    (DES_NETEM="delay 5ms 2ms loss 1%"). Needs cap_add: NET_ADMIN.
# 3. Drops root and execs the node, so the node is PID 1's direct replacement
#    and receives docker's SIGTERM.
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

if [ -n "${DES_NETEM:-}" ]; then
    dev="${DES_NETEM_DEV:-eth0}"
    # shellcheck disable=SC2086  # DES_NETEM is a list of netem arguments
    if ! tc qdisc replace dev "$dev" root netem ${DES_NETEM}; then
        echo "[netem] could not shape $dev — the service needs cap_add: [NET_ADMIN]" >&2
        echo "        and the host kernel needs sch_netem (modprobe sch_netem)" >&2
        exit 3
    fi
    echo "[netem] $dev egress: ${DES_NETEM}"
fi

# Root was only needed for tc. The node itself runs unprivileged, with no
# capabilities and no way to regain them.
exec setpriv --reuid=des --regid=des --init-groups --no-new-privs \
     "$bin" "$id" "$nodes"
