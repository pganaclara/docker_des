#!/usr/bin/env python3
"""Container overhead: the same cell as containers on a bridge, as containers
on the host's network, and as plain processes.

    python3 scripts/overhead.py results/<timestamp>-varredura

Reads the fms-N-ponte / fms-N-host / fms-N-nativo runs under the directory
(scripts/run-all.sh sobrecarga) and writes sobrecarga.md / sobrecarga.json
next to them. The three modes run the SAME binaries (one image, built once per
N), so any difference is where they run:

  ponte   one container per node, bridge network "cell" (veth + bridge)
  host    one container per node, the host's network stack (no veth/bridge)
  nativo  no container at all: plain processes on the host

Per N and mode:
  * time per step, cycle 1 and cycles 2-5 (engine's run clock), mean ± sd;
  * difference to ponte with a 95 % Welch confidence interval;
  * the network's share, which is where containers can cost something:
    the application RTT the engine measures before the run (20 probes, node 1)
    and the peer-wait of 2PC and NOTIFY events (time the owner waits for the
    others after its own homomorphic step), p50 over cycles 2-5.

Exit status 1 if any run failed its checks.
"""
import json
import math
import pathlib
import re
import sys

MODES = ("ponte", "host", "nativo")
DRIVER = re.compile(r"^c(\d+)\s+s\d+\s+(2pc|notify)\s+\S+\s+[\d.]+ ms HE"
                    r".*?\+ ([\d.]+) ms peer-wait")


def mean_sd(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, 0
    m = sum(xs) / len(xs)
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) if len(xs) > 1 else 0.0
    return m, sd, len(xs)


def _betacf(a, b, x):
    # Continued fraction for the incomplete beta (Numerical Recipes, Lentz).
    tiny = 1e-300
    c, d = 1.0, 1.0 - (a + b) * x / (a + 1)
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 300):
        for num in (m * (b - m) * x / ((a + 2 * m - 1) * (a + 2 * m)),
                    -(a + m) * (a + b + m) * x / ((a + 2 * m) * (a + 2 * m + 1))):
            d = 1.0 + num * d
            d = 1.0 / (d if abs(d) > tiny else tiny)
            c = 1.0 + num / c
            c = c if abs(c) > tiny else tiny
            h *= d * c
        if abs(d * c - 1.0) < 1e-12:
            break
    return h


def t_cdf(t, df):
    x = df / (df + t * t)
    lb = (math.lgamma(df / 2 + 0.5) - math.lgamma(df / 2) - math.lgamma(0.5)
          + (df / 2) * math.log(x) + 0.5 * math.log1p(-x))
    ib = math.exp(lb) * _betacf(df / 2, 0.5, x) / (df / 2)
    return 1 - 0.5 * ib if t >= 0 else 0.5 * ib


def t_quantile(p, df):
    lo, hi = 0.0, 1000.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if t_cdf(mid, df) < p else (lo, mid)
    return (lo + hi) / 2


def welch(a, b):
    """Mean difference a - b and its 95 % Welch confidence interval."""
    (ma, sa, na), (mb, sb, nb) = mean_sd(a), mean_sd(b)
    if ma is None or mb is None:
        return None
    diff = ma - mb
    if na < 2 or nb < 2:
        return diff, None, None
    va, vb = sa * sa / na, sb * sb / nb
    se = math.sqrt(va + vb)
    if se == 0:
        return diff, diff, diff
    df = (va + vb) ** 2 / (va * va / (na - 1) + vb * vb / (nb - 1))
    h = t_quantile(0.975, df) * se
    return diff, diff - h, diff + h


def p50(xs):
    xs = sorted(xs)
    return xs[max(1, math.ceil(len(xs) / 2)) - 1] if xs else None


def peer_waits(run):
    out = {"2pc": [], "notify": []}
    for log in run.glob("node*.log"):
        if log.name.endswith(".ts.log"):
            continue
        for line in log.read_text(errors="replace").splitlines():
            m = DRIVER.match(line)
            if m and int(m.group(1)) >= 2:
                out[m.group(2)].append(float(m.group(3)))
    return out


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = pathlib.Path(sys.argv[1])
    cells = {}                                  # (n, mode) -> [run dirs]
    for j in sorted(root.glob("*/summary.json")):
        name = re.sub(r"^\d{8}-\d{6}-", "", j.parent.name)
        if (m := re.fullmatch(r"fms-(\d+)-(" + "|".join(MODES) + ")", name)):
            cells.setdefault((int(m.group(1)), m.group(2)), []).append(j.parent)
    if not cells:
        print(f"nenhuma execução fms-N-{{{','.join(MODES)}}} em {root}")
        return 2

    bad = 0
    stats = {}
    for (n, mode), runs in cells.items():
        sums = [json.loads((r / "summary.json").read_text()) for r in runs]
        bad += sum(not s["all_checks_ok"] for s in sums)
        waits = {"2pc": [], "notify": []}
        for r in runs:
            for k, v in peer_waits(r).items():
                waits[k] += v
        c1 = [s["per_step_ms_cycle1"] for s in sums]
        ss = [s["per_step_ms_steady"] for s in sums]
        rtt = [s["rtt_ms"]["avg"] for s in sums if s.get("rtt_ms")]
        emu = sums[0]["nodes"][0]["result"].get("emu_scalarmul_ms", 0) or 0
        stats[(n, mode)] = {
            "nodes": n, "mode": mode, "runs": len(runs),
            "checks_ok": sum(s["all_checks_ok"] for s in sums),
            "fingerprints": sorted({f for s in sums for f in s["fingerprints"]}),
            "emu_ms": emu, "c1": c1, "ss": ss, "rtt": rtt,
            "c1_mean": mean_sd(c1)[0], "c1_sd": mean_sd(c1)[1],
            "ss_mean": mean_sd(ss)[0], "ss_sd": mean_sd(ss)[1],
            "rtt_mean": mean_sd(rtt)[0], "rtt_sd": mean_sd(rtt)[1],
            "wait_2pc_p50": p50(waits["2pc"]), "wait_notify_p50": p50(waits["notify"]),
            "wait_2pc_n": len(waits["2pc"]), "wait_notify_n": len(waits["notify"]),
        }

    def show(m, sd, k, d=1):
        if m is None:
            return "—"
        return f"{m:.{d}f}" if k == 1 else f"{m:.{d}f} ± {sd:.{d}f}"

    def delta(w, d=1):
        if w is None:
            return "—"
        diff, lo, hi = w
        if lo is None:
            return f"{diff:+.{d}f}"
        star = "**" if lo > 0 or hi < 0 else ""
        return f"{star}{diff:+.{d}f}{star} [{lo:+.{d}f}; {hi:+.{d}f}]"

    ns = sorted({n for n, _ in stats})
    emu = next(iter(stats.values()))["emu_ms"]
    md = ["# Sobrecarga do container\n",
          "Mesma célula, mesmos binários (uma imagem por N, estáticos, "
          "`-DDES_MCAST_LOOP=1`), três lugares para rodar:\n",
          "- **ponte**: um container por nó na rede *bridge* `cell` (veth + bridge), "
          "como a varredura principal;",
          "- **host**: um container por nó na pilha de rede do host "
          "(`compose.host.yaml`): sem veth nem bridge;",
          "- **nativo**: sem container, processos comuns no host.\n",
          (f"Cada decifração leva **{emu:g} ms** (`DES_EMU_SCALARMUL_MS`)." if emu else
           "Emulação **desligada**: decifrações na velocidade desta máquina.")
          + " Tempos em ms, média ± desvio padrão; Δ = modo − ponte com IC 95 % "
          "de Welch, em negrito quando o IC não contém zero.\n",
          "## Tempo por passo\n",
          "| nós | modo | execuções | ciclo 1 | Δ ciclo 1 | ciclos 2–5 | Δ ciclos 2–5 | verificações |",
          "|---|---|---|---|---|---|---|---|"]
    for n in ns:
        base = stats.get((n, "ponte"))
        for mode in MODES:
            s = stats.get((n, mode))
            if not s:
                continue
            same = mode == "ponte" or not base
            md.append(f"| {n} | {mode} | {s['runs']} "
                      f"| {show(s['c1_mean'], s['c1_sd'], s['runs'])} "
                      f"| {'—' if same else delta(welch(s['c1'], base['c1']))} "
                      f"| {show(s['ss_mean'], s['ss_sd'], s['runs'])} "
                      f"| {'—' if same else delta(welch(s['ss'], base['ss']))} "
                      f"| {s['checks_ok']}/{s['runs']} |")
            if not same:
                s["delta_c1"] = welch(s["c1"], base["c1"])
                s["delta_ss"] = welch(s["ss"], base["ss"])
    md += ["\n## A parte da rede\n",
           "RTT de aplicação: 20 sondas do nó 1 antes da execução (média por execução, "
           "depois média ± dp entre execuções). Espera pelos pares: p50 do tempo que o "
           "dono de um evento compartilhado espera pelos outros depois do seu passo "
           "homomórfico, ciclos 2–5, todas as execuções.\n",
           "| nós | modo | RTT (ms) | Δ RTT | espera 2PC p50 (n) | espera NOTIFY p50 (n) |",
           "|---|---|---|---|---|---|"]
    for n in ns:
        if n == 1:
            continue
        base = stats.get((n, "ponte"))
        for mode in MODES:
            s = stats.get((n, mode))
            if not s:
                continue
            k = len(s["rtt"])
            dr = "—" if mode == "ponte" or not base else delta(welch(s["rtt"], base["rtt"]), 2)
            w2 = "—" if s["wait_2pc_p50"] is None else f"{s['wait_2pc_p50']:.1f} ({s['wait_2pc_n']})"
            wn = ("—" if s["wait_notify_p50"] is None
                  else f"{s['wait_notify_p50']:.1f} ({s['wait_notify_n']})")
            md.append(f"| {n} | {mode} | {show(s['rtt_mean'], s['rtt_sd'], k, 2)} | {dr} "
                      f"| {w2} | {wn} |")
    md += ["\n## Invariantes\n",
           "| nós | modo | impressão digital |", "|---|---|---|"]
    for (n, mode) in sorted(stats, key=lambda k: (k[0], MODES.index(k[1]))):
        md.append(f"| {n} | {mode} | `{', '.join(stats[(n, mode)]['fingerprints'])}` |")
    text = "\n".join(md) + "\n"
    (root / "sobrecarga.md").write_text(text)
    (root / "sobrecarga.json").write_text(json.dumps(
        [stats[k] for k in sorted(stats, key=lambda k: (k[0], MODES.index(k[1])))],
        indent=2, ensure_ascii=False) + "\n")
    print(text)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
