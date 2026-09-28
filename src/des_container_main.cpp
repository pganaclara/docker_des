// =============================================================================
// des_container_main.cpp — the SAME engine, one node per container
// =============================================================================
//
// This file plays the part des_distributed.ino plays on an ESP32 and
// host_main.cpp plays on a Linux PC: it chooses the deployment, brings the link
// up and calls des_setup() / des_loop(). Everything else — the EC-ElGamal core,
// the two-phase commit, the routing derived from the generated header, the
// oracle — is engine/des_generic.h, byte-for-byte the file that runs on the
// boards (see engine/UPSTREAM.md). Four things are specific to a container:
//
//   1. The cell key is read at START-UP from a Docker secret, so it is never
//      baked into an image layer. The engine applies sizeof() to DES_AUTH_KEY;
//      a 65-byte array satisfies that exactly as the string literal does on the
//      ESP32, so the engine is unchanged and the HMAC key bytes are the same
//      64 characters an ESP32 would compile in. A container and a board holding
//      the same key are peers.
//
//   2. Every decryption can be made to cost what it costs on an ESP32-S3
//      (section 5 below; on by default).
//
//   3. A container has to END. After the scripted run the node keeps serving
//      its peers for DES_LINGER_MS — they may still be retransmitting a COMMIT
//      it must acknowledge — then prints one machine-readable line
//      (@@RESULT {...}) and exits with a status code that says how it went.
//
//   4. A watchdog (DES_RUN_TIMEOUT_S) ends a run that cannot finish — a peer
//      whose container never started, for instance: the engine waits for every
//      peer indefinitely by design, which is right for boards being flashed one
//      by one and wrong for a batch of containers.
//
// Build (the Dockerfile does this once per node id; one command line):
//   g++ -std=c++17 -O2 -Iengine -Isrc -DDES_NODE_ID=3 -DDES_NUM_NODES=7
//       -DDES_DATA_HEADER='"supervisor_data_fms.h"' -DDES_FAMILY=DES_FAMILY_LMOD
//       -o des_node3 src/des_container_main.cpp -l:libmbedcrypto.a
//
// Exit status: 0 = every step fired, oracle PASS, no halt
//              1 = ran to the end, but with skipped steps or an oracle mismatch
//              2 = SAFE HALT
//              3 = configuration error (key, transport, node id)
//              4 = watchdog: the run did not finish in DES_RUN_TIMEOUT_S
// =============================================================================

#include <cerrno>
#include <csignal>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <ifaddrs.h>
#include <net/if.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

// ── deployment configuration (compile time — the Dockerfile sets these) ─────
#ifndef DES_DATA_HEADER
#define DES_DATA_HEADER "supervisor_data_fms.h"
#endif
#ifndef DES_NODE_ID
#define DES_NODE_ID 1
#endif
#ifndef DES_NUM_NODES
#define DES_NUM_NODES 7
#endif
#ifndef DES_FAMILY
#define DES_FAMILY DES_FAMILY_LMOD
#endif
#ifndef DES_WORK_MS
#define DES_WORK_MS 0
#endif

// ── 1. the cell key, filled at start-up ─────────────────────────────────────
// Exactly 64 characters, e.g. `python3 -c "import secrets;print(secrets.token_hex(32))"`
// (scripts/gen-key.sh does it). Fixed length, because the engine takes the key
// length from sizeof(DES_AUTH_KEY) at compile time.
#define DES_KEY_CHARS 64
static char g_des_auth_key[DES_KEY_CHARS + 1];
#define DES_AUTH_KEY g_des_auth_key

#include "des_generic.h"

// ── 5. emulate the ESP32's cost of a decryption (ON by default) ─────────────
// On an ESP32-S3 one blinded scalar multiplication costs ~69 ms; on a PC it
// costs well under a millisecond, which moves the bottleneck from cryptography
// to coordination and turns "distributing is faster" around (docs/arquitetura
// §7.3). So every DECRYPTION is made to take at least DES_EMU_SCALARMUL_MS
// (default 69 ms, the ESP32-S3 figure), by sleeping out the difference.
// DES_EMU_SCALARMUL_MS=0 turns it off and runs at the PC's own speed.
//
// The engine is not touched. The Dockerfile links with
// -Wl,--wrap=mbedtls_ecp_mul, so the engine's calls land here and are passed
// on to the real function. Only the call whose scalar is the negated private
// key — row_decrypt(), the one decryption the engine performs — is slowed;
// encryption at start-up and the self-test are not. The decryption COUNT is
// unchanged, and so are all the checks.
//
// Sleeping, not spinning: each board has a core of its own, and seven
// spinning containers on a laptop with fewer free cores would measure CPU
// contention instead of the ESP32.
#define DES_EMU_DEFAULT_MS 69.0      // ESP32-S3, measured in esp32_crypto
static uint32_t g_emu_mul_us = 0;

extern "C" int __real_mbedtls_ecp_mul(mbedtls_ecp_group* grp, mbedtls_ecp_point* R,
                                      const mbedtls_mpi* m, const mbedtls_ecp_point* P,
                                      int (*f_rng)(void*, unsigned char*, size_t),
                                      void* p_rng);
extern "C" int __wrap_mbedtls_ecp_mul(mbedtls_ecp_group* grp, mbedtls_ecp_point* R,
                                      const mbedtls_mpi* m, const mbedtls_ecp_point* P,
                                      int (*f_rng)(void*, unsigned char*, size_t),
                                      void* p_rng) {
    uint64_t t0 = des_micros();
    int ret = __real_mbedtls_ecp_mul(grp, R, m, P, f_rng, p_rng);
    if (g_emu_mul_us && m == &g_neg_priv) {
        uint64_t spent = des_micros() - t0;
        if (spent < g_emu_mul_us) {
            uint64_t left = g_emu_mul_us - spent;
            struct timespec ts;
            ts.tv_sec  = (time_t)(left / 1000000u);
            ts.tv_nsec = (long)(left % 1000000u) * 1000L;
            while (nanosleep(&ts, &ts) != 0 && errno == EINTR) {}
        }
    }
    return ret;
}

// The engine asks the platform which interface to join the multicast group on.
// $DES_IFACE_IP when set, else the first non-loopback, multicast-capable IPv4
// that is up — in a container attached to one network, that is eth0.
static uint32_t des_local_ipv4() {
    if (const char* env = getenv("DES_IFACE_IP")) return inet_addr(env);

    struct ifaddrs* ifa = nullptr;
    if (getifaddrs(&ifa) != 0) return htonl(INADDR_ANY);
    uint32_t found = htonl(INADDR_ANY);
    for (struct ifaddrs* p = ifa; p; p = p->ifa_next) {
        if (!p->ifa_addr || p->ifa_addr->sa_family != AF_INET) continue;
        if (!(p->ifa_flags & IFF_UP))        continue;
        if (p->ifa_flags & IFF_LOOPBACK)     continue;
        if (!(p->ifa_flags & IFF_MULTICAST)) continue;
        found = ((struct sockaddr_in*)p->ifa_addr)->sin_addr.s_addr;
        break;
    }
    freeifaddrs(ifa);
    return found;
}

// Key from $DES_AUTH_KEY_FILE (default: the Docker secret mount point), or —
// for a quick manual run only — from $DES_AUTH_KEY_VALUE. Surrounding
// whitespace, such as the newline an editor adds, is ignored.
static bool load_key() {
    char buf[256] = {0};
    const char* src = nullptr;
    if (const char* v = getenv("DES_AUTH_KEY_VALUE")) {
        snprintf(buf, sizeof(buf), "%s", v);
        src = "$DES_AUTH_KEY_VALUE";
    } else {
        const char* path = getenv("DES_AUTH_KEY_FILE");
        if (!path) path = "/run/secrets/des_auth_key";
        FILE* f = fopen(path, "r");
        if (!f) {
            fprintf(stderr, "[key] cannot open %s: %s\n"
                    "      run scripts/gen-key.sh, or set DES_AUTH_KEY_FILE\n",
                    path, strerror(errno));
            return false;
        }
        size_t n = fread(buf, 1, sizeof(buf) - 1, f);
        fclose(f);
        buf[n] = 0;
        src = path;
    }
    char* b = buf;
    while (*b == ' ' || *b == '\t' || *b == '\r' || *b == '\n') ++b;
    size_t n = strlen(b);
    while (n && (b[n-1] == ' ' || b[n-1] == '\t' || b[n-1] == '\r' || b[n-1] == '\n'))
        b[--n] = 0;
    if (n != DES_KEY_CHARS) {
        fprintf(stderr, "[key] %s holds %zu characters; the cell key must be exactly "
                "%d (scripts/gen-key.sh makes one)\n", src, n, DES_KEY_CHARS);
        return false;
    }
    memcpy(g_des_auth_key, b, DES_KEY_CHARS);
    g_des_auth_key[DES_KEY_CHARS] = 0;
    return true;
}

static uint32_t env_u32(const char* name, uint32_t dflt) {
    const char* v = getenv(name);
    return (v && *v) ? (uint32_t)strtoul(v, nullptr, 10) : dflt;
}

static void on_watchdog(int) {
    static const char msg[] =
        "\n[watchdog] the run did not finish within DES_RUN_TIMEOUT_S — exiting 4\n";
    ssize_t w = write(STDOUT_FILENO, msg, sizeof(msg) - 1);
    (void)w;
    _exit(4);
}

// The engine drops a received frame when rand() % 100 < DES_SIMULATE_LOSS_PCT
// and never seeds rand(), so every run (and every node) would lose the same
// frames. Seeded here, per node and per run: $DES_LOSS_SEED when set (to
// replay a run), else from the clock, the pid and the node id.
static unsigned g_loss_seed = 0;

// One line a script can parse, printed last. Everything in it comes from the
// engine's own counters; decryption counts per step are in the log lines above.
static void print_result(int code) {
    printf("@@RESULT {\"node\":%d,\"nodes\":%d,\"family\":\"%s\",\"data\":\"%s\","
           "\"transport\":\"%s\",\"fingerprint\":\"%08x\",\"supervisors\":[",
           (int)DES_NODE_ID, (int)DES_NUM_NODES, DES_FAMILY_NAME, DES_DATA_HEADER,
           DES_TRANSPORT_IMPL.name, (unsigned)g_cfg);
    for (size_t i = 0; i < g_sups.size(); ++i) {
        char nm[16];
        printf("%s\"%s\"", i ? "," : "", sup_name(g_sups[i].desc, nm));
    }
    printf("],\"fired\":{\"local\":%u,\"ctrl\":%u,\"unctrl\":%u},\"applied_for_peers\":%u,"
           "\"skips\":%u,\"impossible\":%u,\"tx\":%u,\"rx\":%u,\"retx\":%u,"
           "\"auth_bad\":%u,\"replays\":%u,\"challenges\":%u,\"mac_us\":%.2f,"
           "\"rxq_peak\":%u,\"rxq_drops\":%u,\"sync_wait_ms\":%.1f,"
           "\"oracle\":\"%s\",\"safe_halt\":%s,\"halt_reason\":\"%s\","
           "\"cycle_end_ms\":[",
           (unsigned)g_acc_local.n, (unsigned)g_acc_ctrl.n, (unsigned)g_acc_unctrl.n,
           (unsigned)g_acc_part.n, (unsigned)g_skips, (unsigned)g_impossible,
           (unsigned)g_tx, (unsigned)g_rx, (unsigned)g_retx, (unsigned)g_auth_bad,
           (unsigned)g_replays, (unsigned)g_challenges, g_mac_us,
           (unsigned)g_rxq_peak, (unsigned)g_rxq_drops, g_sync_us / 1000.0,
           g_he_mismatch ? "FAIL" : "PASS", g_safe_halt ? "true" : "false",
           g_halt_why ? g_halt_why : "");
    for (int c = 0; c < g_cycles_done; ++c)
        printf("%s%.1f", c ? "," : "", g_cycle_end_ms[c]);
    printf("],\"rounds\":%d,\"work_ms\":%d,\"emu_scalarmul_ms\":%.1f,"
           "\"loss_pct\":%d,\"loss_seed\":%u,\"exit\":%d}\n",
           (int)DES_ROUNDS, (int)DES_WORK_MS, g_emu_mul_us / 1000.0,
           (int)DES_SIMULATE_LOSS_PCT, g_loss_seed, code);
    fflush(stdout);
}

int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);

    // The node identity is compiled in, because the engine's routing tables are
    // macro-driven. Refuse a mismatch rather than run as the wrong node.
    if (argc >= 2) {
        int id = atoi(argv[1]);
        int n  = argc >= 3 ? atoi(argv[2]) : DES_NUM_NODES;
        if (id != DES_NODE_ID || n != DES_NUM_NODES) {
            fprintf(stderr, "this binary is node %d of %d, not %d of %d\n",
                    (int)DES_NODE_ID, (int)DES_NUM_NODES, id, n);
            return 3;
        }
    }
    if (!load_key()) return 3;

    // Fractional milliseconds allowed (e.g. 69 or 68.6); unset or empty means
    // the default, 0 means off.
    {
        const char* e = getenv("DES_EMU_SCALARMUL_MS");
        double ms = (e && *e) ? atof(e) : DES_EMU_DEFAULT_MS;
        g_emu_mul_us = ms > 0 ? (uint32_t)(ms * 1000.0 + 0.5) : 0;
    }

    uint32_t timeout_s = env_u32("DES_RUN_TIMEOUT_S", 900);
    if (timeout_s) { signal(SIGALRM, on_watchdog); alarm(timeout_s); }

    printf("des_container: node %d of %d, %s, data %s, transport %s\n",
           (int)DES_NODE_ID, (int)DES_NUM_NODES, DES_FAMILY_NAME, DES_DATA_HEADER,
           DES_TRANSPORT_IMPL.name);
    if (g_emu_mul_us)
        printf("des_container: EMULATING the ESP32 — every decryption takes at "
               "least %.1f ms (DES_EMU_SCALARMUL_MS)\n", g_emu_mul_us / 1000.0);
    else
        printf("des_container: ESP32 emulation OFF (DES_EMU_SCALARMUL_MS=0) — "
               "decryptions run at this machine's own speed\n");

    if (const char* e = getenv("DES_LOSS_SEED"); e && *e) {
        g_loss_seed = (unsigned)strtoul(e, nullptr, 10);
    } else {
        struct timespec now;
        clock_gettime(CLOCK_REALTIME, &now);
        g_loss_seed = (unsigned)(now.tv_nsec ^ (now.tv_sec << 20) ^ (getpid() << 8))
                      ^ (unsigned)DES_NODE_ID * 2654435761u;
    }
    srand(g_loss_seed);
    if (DES_SIMULATE_LOSS_PCT > 0)
        printf("des_container: dropping %d %% of received frames, seed %u "
               "(DES_LOSS_SEED to replay)\n", (int)DES_SIMULATE_LOSS_PCT, g_loss_seed);

    des_setup();          // rendezvous, probe, the scripted run, the summary

    // Keep answering: a peer may still be retransmitting a COMMIT or NOTIFY
    // whose ACK was lost (up to DES_ACK_RETRIES x DES_ACK_TIMEOUT_MS = 7.5 s),
    // and a late SAFE HALT must still be heard and repeated.
    uint32_t linger = env_u32("DES_LINGER_MS", 10000);
    uint32_t t0 = des_millis();
    while (des_millis() - t0 < linger) des_loop();
    alarm(0);

    int code = g_safe_halt ? 2 : (g_skips || g_he_mismatch) ? 1 : 0;
    print_result(code);
    return code;
}
