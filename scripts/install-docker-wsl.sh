#!/usr/bin/env bash
# =============================================================================
# install-docker-wsl.sh — Docker Engine + Compose inside WSL 2 (Ubuntu)
# =============================================================================
# Run INSIDE the WSL Ubuntu terminal (not PowerShell), from the repo root:
#
#     bash scripts/install-docker-wsl.sh
#
# What it does, following the official procedure
# (https://docs.docker.com/engine/install/ubuntu/):
#   1. checks it is running under WSL 2, on Ubuntu;
#   2. enables systemd in /etc/wsl.conf if it is off (Docker's daemon is a
#      systemd service) — then asks you to restart WSL once, and stops;
#   3. removes the distribution's unofficial docker packages, if present;
#   4. adds Docker's apt repository and signing key;
#   5. installs docker-ce, the CLI, containerd, buildx and the compose plugin;
#   6. adds you to the `docker` group and starts the service;
#   7. installs python3 (used by scripts/summarize.py) if missing.
#
# Idempotent: running it again only re-checks. It does NOT install Docker
# Desktop — the alternative, if you prefer a Windows GUI; the repo works with
# either. Do not install both: Docker Desktop's WSL integration and a native
# Engine in the same distro fight over /var/run/docker.sock.
# =============================================================================
set -euo pipefail

say()  { printf '\033[1;34m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m[!] %s\033[0m\n' "$*"; }
die()  { printf '\033[1;31m[x] %s\033[0m\n' "$*" >&2; exit 1; }

[[ $EUID -ne 0 ]] || die "run as your normal user (the script calls sudo itself)"

# ---- 1. environment -------------------------------------------------------
if ! grep -qiE 'microsoft|wsl' /proc/version; then
    warn "this does not look like WSL; continuing as plain Ubuntu"
elif grep -qi 'microsoft-standard' /proc/version; then
    say "WSL 2 detected ($(uname -r))"
else
    die "WSL 1 detected — Docker needs WSL 2. In PowerShell: wsl --set-version <distro> 2"
fi
# shellcheck source=/dev/null
. /etc/os-release
[[ ${ID:-} == ubuntu ]] || die "this script targets Ubuntu (found ${PRETTY_NAME:-unknown})"
say "$PRETTY_NAME"

# ---- 2. systemd -------------------------------------------------------------
if [[ "$(ps -p 1 -o comm= 2>/dev/null)" != systemd ]]; then
    if grep -qE '^\s*systemd\s*=\s*true' /etc/wsl.conf 2>/dev/null; then
        die "systemd is enabled in /etc/wsl.conf but not running yet.
    In PowerShell run:  wsl --shutdown
    then reopen Ubuntu and run this script again."
    fi
    say "enabling systemd in /etc/wsl.conf"
    if grep -q '^\[boot\]' /etc/wsl.conf 2>/dev/null; then
        sudo sed -i '/^\[boot\]/a systemd=true' /etc/wsl.conf
    else
        printf '\n[boot]\nsystemd=true\n' | sudo tee -a /etc/wsl.conf >/dev/null
    fi
    cat <<'EOF'

    systemd has been enabled. WSL must restart once for it to take effect:
      1. close this terminal
      2. in PowerShell:   wsl --shutdown
      3. reopen Ubuntu and run:   bash scripts/install-docker-wsl.sh

EOF
    exit 0
fi
say "systemd is running"

# ---- 3. unofficial packages ---------------------------------------------------
conflicting=()
for p in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
    dpkg -s "$p" >/dev/null 2>&1 && conflicting+=("$p")
done
if ((${#conflicting[@]})); then
    say "removing conflicting packages: ${conflicting[*]}"
    sudo apt-get remove -y "${conflicting[@]}"
fi

# ---- 4. Docker's apt repository -----------------------------------------------
if [[ ! -f /etc/apt/sources.list.d/docker.list && ! -f /etc/apt/sources.list.d/docker.sources ]]; then
    say "adding Docker's apt repository"
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu ${UBUNTU_CODENAME:-$VERSION_CODENAME} stable" \
        | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
fi

# ---- 5. install -----------------------------------------------------------------
say "installing Docker Engine, CLI, containerd, buildx, compose"
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
                        docker-buildx-plugin docker-compose-plugin

# ---- 6. group + service -----------------------------------------------------------
me=$(id -un)           # $USER is not always set (e.g. under `wsl -e`)
if ! id -nG "$me" | tr ' ' '\n' | grep -qx docker; then
    say "adding $me to the docker group (takes effect in a new shell)"
    sudo usermod -aG docker "$me"
    newgroup=1
fi
sudo systemctl enable --now docker.service containerd.service

# ---- 7. helpers -------------------------------------------------------------------
command -v python3 >/dev/null || sudo apt-get install -y python3

# ---- check ------------------------------------------------------------------------
say "versions"
sudo docker version --format 'engine {{.Server.Version}}  client {{.Client.Version}}' \
    || die "the Docker daemon is not answering — see: sudo systemctl status docker"
sudo docker compose version
if zcat /proc/config.gz 2>/dev/null | grep -q '^CONFIG_NET_SCH_NETEM=[ym]'; then
    say "this kernel has netem: scenarios/fms-7-wifi.env will work"
else
    warn "this WSL kernel has no netem: use scenarios/fms-7-loss5.env for loss;"
    warn "fms-7-wifi.env (delay + loss via tc) needs a custom WSL kernel"
fi

cat <<EOF

Done. $( [[ ${newgroup:-0} == 1 ]] && echo "Open a NEW terminal (or run: newgrp docker) so the docker group applies, then:" || echo "Next:")

    docker run --rm hello-world
    scripts/run.sh scenarios/fms-7.env

EOF
