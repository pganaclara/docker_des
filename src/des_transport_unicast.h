// =============================================================================
// des_transport_unicast.h — UDP/IP unicast fan-out, a second DesTransport
// =============================================================================
//
// The engine's own binding is UDP/IP multicast (engine/des_transport.h), and on
// one Docker bridge network that is what runs by default: a user-defined bridge
// forwards multicast between the containers attached to it. Some container
// networks do not — Swarm overlay networks and most Kubernetes CNIs drop it —
// so this file adds the other obvious binding: the same 44-byte frame, sent by
// plain unicast UDP to each peer in turn.
//
// It implements the same four-function contract, and nothing else changes. The
// protocol above already supplies sequencing, acknowledgement, retransmission
// and atomicity end to end (Saltzer, Reed & Clark 1984), so a transport only
// has to be best effort; fan-out is exactly that. Every frame is still signed
// and checked by the engine, so the source address of a datagram is never
// trusted and does not need to be.
//
// Peers are named, not numbered by address:
//
//     DES_PEERS=node1,node2,node3:5077,...      in node-id order, host[:port]
//
// Entry k is node k+1. This node's own entry is skipped. Names are resolved
// with getaddrinfo(), so Docker's embedded DNS (service name -> container IP)
// does the discovery. A name that does not resolve yet — its container has not
// started — is retried every 500 ms, and a resolved one is refreshed every 5 s,
// so a peer whose container is recreated with a new address is found again.
//
// Cost: one sendto() per peer per frame instead of one per frame. With seven
// nodes that is six datagrams where multicast sends one; on a bridge network
// both are memory copies, and the engine's frames are 44 bytes.
// =============================================================================

#pragma once
#include <netdb.h>
#include <stdlib.h>
#include <string>
#include <vector>

struct DesUniPeer {
    std::string        host;
    uint16_t           port = DES_MCAST_PORT;
    int                node = 0;          // 1-based node id this entry stands for
    struct sockaddr_in addr;
    bool               resolved = false;
    uint32_t           t_resolve = 0;     // last attempt, des_millis()
};

static std::vector<DesUniPeer> des_uni_peers;
static int                     des_uni_fd = -1;

static bool des_uni_resolve(DesUniPeer& p) {
    p.t_resolve = des_millis();
    struct addrinfo hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family   = AF_INET;
    hints.ai_socktype = SOCK_DGRAM;
    struct addrinfo* res = nullptr;
    if (getaddrinfo(p.host.c_str(), nullptr, &hints, &res) != 0 || !res) {
        if (res) freeaddrinfo(res);
        return false;
    }
    struct sockaddr_in a;
    memcpy(&a, res->ai_addr, sizeof(a));
    a.sin_port = htons(p.port);
    freeaddrinfo(res);
    bool changed = !p.resolved || a.sin_addr.s_addr != p.addr.sin_addr.s_addr;
    p.addr = a;
    if (changed) {
        char ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &a.sin_addr, ip, sizeof(ip));
        DES_LOG("[net] peer node %d = %s -> %s:%u\n", p.node, p.host.c_str(), ip,
                (unsigned)p.port);
    }
    p.resolved = true;
    return true;
}

// "node1,node2:6000, node3" -> one entry per peer, this node's own skipped.
static bool des_uni_parse(const char* list) {
    des_uni_peers.clear();
    int node = 0;
    const char* s = list;
    while (*s) {
        const char* e = strchr(s, ',');
        std::string item = e ? std::string(s, e - s) : std::string(s);
        s = e ? e + 1 : s + strlen(s);
        // trim
        size_t b = item.find_first_not_of(" \t"), z = item.find_last_not_of(" \t");
        if (b == std::string::npos) continue;
        item = item.substr(b, z - b + 1);
        ++node;
        if (node > DES_NUM_NODES) break;         // extra names are harmless
        if (node == DES_NODE_ID) continue;       // not to myself
        DesUniPeer p;
        p.node = node;
        size_t colon = item.rfind(':');
        if (colon != std::string::npos) {
            p.host = item.substr(0, colon);
            p.port = (uint16_t)atoi(item.c_str() + colon + 1);
        } else {
            p.host = item;
        }
        memset(&p.addr, 0, sizeof(p.addr));
        des_uni_peers.push_back(p);
    }
    if (node < DES_NUM_NODES) {
        DES_LOG("[net] DES_PEERS names %d node(s), but this cell has %d\n", node,
                (int)DES_NUM_NODES);
        return false;
    }
    return true;
}

static bool des_uni_begin() {
    const char* list = getenv("DES_PEERS");
    if (!list || !*list) {
        DES_LOG("[net] unicast transport needs DES_PEERS=host1,host2,... "
                "(node-id order)\n");
        return false;
    }
    if (!des_uni_parse(list)) return false;

    des_uni_fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (des_uni_fd < 0) { DES_LOG("[net] socket() failed\n"); return false; }
    int yes = 1;
    setsockopt(des_uni_fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes));
    struct sockaddr_in local;
    memset(&local, 0, sizeof(local));
    local.sin_family      = AF_INET;
    local.sin_addr.s_addr = htonl(INADDR_ANY);
    local.sin_port        = htons(DES_MCAST_PORT);
    if (bind(des_uni_fd, (struct sockaddr*)&local, sizeof(local)) < 0) {
        DES_LOG("[net] bind() failed\n"); return false;
    }
    des_sock_nonblock(des_uni_fd);

    int ok = 0;
    for (auto& p : des_uni_peers) ok += des_uni_resolve(p) ? 1 : 0;
    DES_LOG("[net] UDP unicast fan-out to %d peer(s), port %d, frame=%d B "
            "(%d resolved now, the rest are retried)\n",
            (int)des_uni_peers.size(), (int)DES_MCAST_PORT, (int)DES_FRAME_BYTES, ok);
    return true;
}

static bool des_uni_send(const void* frame, int len) {
    if (des_uni_fd < 0) return false;
    bool any = false;
    for (auto& p : des_uni_peers) {
        if (!p.resolved) continue;
        if (sendto(des_uni_fd, frame, len, 0, (struct sockaddr*)&p.addr,
                   sizeof(p.addr)) == len) any = true;
    }
    return any;
}

// Same contract as the multicast poll: return the next datagram of exactly
// `len` bytes, consuming and skipping anything else on the port.
static bool des_uni_poll(void* frame, int len) {
    if (des_uni_fd < 0) return false;
    for (;;) {
        int n = recvfrom(des_uni_fd, frame, len, MSG_DONTWAIT, nullptr, nullptr);
        if (n < 0)    return false;
        if (n == len) return true;
    }
}

// Called from he_yield(), i.e. often, including between scalar
// multiplications — so it only does work when a timer says so.
static void des_uni_service() {
    uint32_t now = des_millis();
    for (auto& p : des_uni_peers) {
        uint32_t every = p.resolved ? 5000 : 500;
        if (now - p.t_resolve >= every) des_uni_resolve(p);
    }
}

static DesTransport des_unicast_transport = {
    "UDP/IP unicast fan-out",
    des_uni_begin, des_uni_send, des_uni_poll, des_uni_service
};
