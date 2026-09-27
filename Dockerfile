# syntax=docker/dockerfile:1
# =============================================================================
# docker_des — one DES supervisor node per container
# =============================================================================
# The image carries one binary per node id, all compiled from the same engine
# (engine/des_generic.h, byte-identical to the ESP32 build) with the same
# settings except DES_NODE_ID. The container's `command` says which node it is.
#
#   docker compose build                          (reads compose.yaml / .env)
#   docker build -t docker-des --build-arg DES_NUM_NODES=2 .
#
# Ubuntu 26.04 LTS because its libmbedtls-dev is 3.6.x — the same LTS branch
# ESP-IDF 5.x, and so Arduino-ESP32 core 3.x, builds the boards with. Ubuntu
# 24.04 ships mbedTLS 2.28, which cannot parse the compressed EC points the
# engine stores its ciphertexts as.
# =============================================================================
ARG UBUNTU_IMAGE=ubuntu:26.04

# ---- build ------------------------------------------------------------------
FROM ${UBUNTU_IMAGE} AS build
RUN apt-get update \
 && apt-get install -y --no-install-recommends g++ libmbedtls-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY engine/ engine/
COPY src/ src/
# The engine must be the upstream file, unedited (engine/UPSTREAM.md).
RUN cd engine && sha256sum -c --quiet SHA256SUMS

# Deployment. Every node of a cell must be built from the same values: the
# engine hashes them into the configuration fingerprint in every frame.
ARG DES_PROBLEM=fms
ARG DES_NUM_NODES=7
ARG DES_FAMILY=LMOD
ARG DES_ROUNDS=5
ARG DES_WORK_MS=0
# Anything else the engine takes as a macro, e.g.
#   "-DDES_SUP_NODE_MAP={1,1,2,2,3,3,4}"  "-DDES_BENCH_LOCKSTEP=1"
ARG DES_EXTRA_FLAGS=""

RUN set -eu; mkdir -p /out; pids=""; \
    for id in $(seq 1 "$DES_NUM_NODES"); do \
      g++ -std=c++17 -O2 -Wall -Wextra -Iengine -Isrc \
          -DDES_DATA_HEADER="\"supervisor_data_${DES_PROBLEM}.h\"" \
          -DDES_NODE_ID="$id" -DDES_NUM_NODES="$DES_NUM_NODES" \
          -DDES_FAMILY="DES_FAMILY_${DES_FAMILY}" \
          -DDES_ROUNDS="$DES_ROUNDS" -DDES_WORK_MS="$DES_WORK_MS" \
          $DES_EXTRA_FLAGS \
          -o "/out/des_node$id" src/des_container_main.cpp \
          -l:libmbedcrypto.a & \
      pids="$pids $!"; \
    done; \
    for p in $pids; do wait "$p"; done; \
    { echo "DES_PROBLEM=$DES_PROBLEM"; echo "DES_NUM_NODES=$DES_NUM_NODES"; \
      echo "DES_FAMILY=$DES_FAMILY"; echo "DES_ROUNDS=$DES_ROUNDS"; \
      echo "DES_WORK_MS=$DES_WORK_MS"; echo "DES_EXTRA_FLAGS=$DES_EXTRA_FLAGS"; \
      echo "mbedtls=$(dpkg-query -W -f='${Version}' libmbedtls-dev)"; \
      echo "gxx=$(g++ -dumpfullversion)"; } > /out/BUILD_INFO; \
    cat /out/BUILD_INFO

# ---- runtime ----------------------------------------------------------------
FROM ${UBUNTU_IMAGE}
# iproute2 only for the optional netem link emulation (tc).
RUN apt-get update \
 && apt-get install -y --no-install-recommends iproute2 \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --system --no-create-home --shell /usr/sbin/nologin des
COPY --from=build /out/ /opt/des/bin/
COPY --chmod=0755 docker/entrypoint.sh /usr/local/bin/des-entrypoint
# The multicast group port (engine/des_transport.h); unicast uses it too.
EXPOSE 5077/udp
ENTRYPOINT ["des-entrypoint"]
