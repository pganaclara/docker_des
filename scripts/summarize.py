#!/usr/bin/env python3
"""Summarise one run directory written by scripts/run.sh.

    python3 scripts/summarize.py results/<run>/

Reads nodeK.log / nodeK.exit / scenario.env, writes summary.md and
summary.json next to them, and prints summary.md.

Everything is taken from what the nodes printed: the engine's per-step lines
("... 1.4 ms HE   2 dec ...") for the decryption counts, and the @@RESULT line
the container entry point prints last for the counters. Nothing is inferred.

If scenario.env carries EXPECT_* values, each is checked and reported:
    EXPECT_FINGERPRINT          config fingerprint every node must print
    EXPECT_DEC_PER_NODE         "405 393"   decryptions per node, whole run
    EXPECT_DEC_CYCLE1_PER_NODE  "85 105"    decryptions per node, cycle 1
    EXPECT_DEC_TOTAL            798         decryptions, whole cell
    EXPECT_DEC_CYCLE1_TOTAL     190         decryptions, whole cell, cycle 1
    EXPECT_MONO                 PASS        monolithic cross-check verdict
    EXPECT_OUTCOME              complete | halt
Exit status 0 when every expectation holds, 1 otherwise.
"""
import json
import pathlib
import re
import sys

DEC = re.compile(r"([\d.]+) ms HE\s+(\d+) dec")
CYCLE = re.compile(r"^-- cycle (\d+)/(\d+) --$")
RUN = re.compile(r"RUN — SIM_SEQ driver — (\d+) cycles x (\d+) steps")
PROBE = re.compile(r"(\d+) probes: avg ([\d.]+) ms\s+min ([\d.]+) ms\s+max ([\d.]+) ms")
MONO = re.compile(r"distributed vs MONOLITHIC sup\.\s*:\s*(PASS|FAIL|off)")
SKIP = re.compile(r"^c\d+\s+s\d+\s+SKIP\s")


def read_env(path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def parse_node(log_path):
    text = log_path.read_text(errors="replace")
    node = {"log": log_path.name, "dec_total": 0, "dec_by_cycle": {},
            "he_ms_total": 0.0, "skip_lines": 0, "selftest": "PASS",
            "mono": None, "rtt": None, "result": None, "seq_len": None}
    cycle = 0
    for line in text.splitlines():
        m = CYCLE.match(line)
        if m:
            cycle = int(m.group(1))
            continue
        m = DEC.search(line)
        if m:
            d = int(m.group(2))
            node["dec_total"] += d
            node["he_ms_total"] += float(m.group(1))
            node["dec_by_cycle"][cycle] = node["dec_by_cycle"].get(cycle, 0) + d
        if SKIP.match(line):
            node["skip_lines"] += 1
        if "FAIL" in line and ("Enc(" in line or "curve " in line or "frame tag" in line):
            node["selftest"] = "FAIL"
        m = RUN.search(line)
        if m:
            node["seq_len"] = int(m.group(2))
        m = PROBE.search(line)
        if m:
            node["rtt"] = {"n": int(m.group(1)), "avg": float(m.group(2)),
                           "min": float(m.group(3)), "max": float(m.group(4))}
        m = MONO.search(line)
        if m:
            node["mono"] = m.group(1)
        if line.startswith("@@RESULT "):
            try:
                node["result"] = json.loads(line[len("@@RESULT "):])
            except json.JSONDecodeError:
                pass
    exit_file = log_path.with_suffix(".exit")
    node["exit"] = int(exit_file.read_text().strip()) if exit_file.exists() else None
    return node


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    run = pathlib.Path(sys.argv[1])
    env = read_env(run / "scenario.env")
    logs = sorted(run.glob("node*.log"), key=lambda p: int(re.sub(r"\D", "", p.stem)))
    if not logs:
        print(f"no node*.log in {run}")
        return 2
    nodes = [parse_node(p) for p in logs]

    res = [n["result"] for n in nodes]
    have_all = all(r is not None for r in res)
    fps = sorted({r["fingerprint"] for r in res if r})
    rounds = next((r["rounds"] for r in res if r), None)
    seq_len = next((n["seq_len"] for n in nodes if n["seq_len"]), None)
    halted = [r["node"] for r in res if r and r["safe_halt"]]
    skips = sum(r["skips"] for r in res if r)
    # Each step of the trace has exactly one owner, which reports it as fired
    # (local/2pc/notify) or skipped. A halted run stops short of both.
    fired = sum(r["fired"]["local"] + r["fired"]["ctrl"] + r["fired"]["unctrl"]
                for r in res if r)
    dec_total = sum(n["dec_total"] for n in nodes)
    dec_c1 = sum(n["dec_by_cycle"].get(1, 0) for n in nodes)
    complete = have_all and skips == 0 and rounds and seq_len and fired == rounds * seq_len
    outcome = "halt" if halted else ("complete" if complete else "incomplete")

    # A cycle is over when its LATEST node says so (engine/des_generic.h, run clock).
    ends = [r["cycle_end_ms"] for r in res if r]
    n_cycles = min((len(e) for e in ends), default=0)
    cycle_end = [max(e[c] for e in ends) for c in range(n_cycles)]
    per_step_c1 = cycle_end[0] / seq_len if cycle_end and seq_len else None
    per_step_rest = ((cycle_end[-1] - cycle_end[0]) / ((n_cycles - 1) * seq_len)
                     if n_cycles > 1 and seq_len else None)
    rtt = next((n["rtt"] for n in nodes if n["rtt"]), None)
    mono = next((n["mono"] for n in nodes if n["mono"]), None)

    checks = []

    def check(name, expected, got):
        checks.append({"check": name, "expected": expected, "got": got,
                       "ok": str(expected) == str(got)})

    if "EXPECT_FINGERPRINT" in env:
        check("config fingerprint", env["EXPECT_FINGERPRINT"],
              fps[0] if len(fps) == 1 else "/".join(fps) or "-")
    if "EXPECT_DEC_PER_NODE" in env:
        check("decryptions per node", env["EXPECT_DEC_PER_NODE"],
              " ".join(str(n["dec_total"]) for n in nodes))
    if "EXPECT_DEC_CYCLE1_PER_NODE" in env:
        check("decryptions per node, cycle 1", env["EXPECT_DEC_CYCLE1_PER_NODE"],
              " ".join(str(n["dec_by_cycle"].get(1, 0)) for n in nodes))
    if "EXPECT_DEC_TOTAL" in env:
        check("decryptions, whole cell", env["EXPECT_DEC_TOTAL"], dec_total)
    if "EXPECT_DEC_CYCLE1_TOTAL" in env:
        check("decryptions, whole cell, cycle 1", env["EXPECT_DEC_CYCLE1_TOTAL"], dec_c1)
    if "EXPECT_MONO" in env:
        check("monolithic cross-check", env["EXPECT_MONO"], mono or "-")
    check("outcome", env.get("EXPECT_OUTCOME", "complete"), outcome)
    if outcome == "complete":
        check("same fingerprint on every node", 1, len(fps))
        check("oracle PASS on every node", True,
              all(r["oracle"] == "PASS" for r in res if r))
        check("crypto self-test PASS on every node", True,
              all(n["selftest"] == "PASS" for n in nodes))

    # ---- markdown ---------------------------------------------------------
    md = []
    md.append(f"# Execução `{run.name}`\n")
    md.append(f"- problema `{env.get('DES_PROBLEM', '?')}`, família `{env.get('DES_FAMILY', '?')}`, "
              f"**{len(nodes)} containers**, UDP multicast")
    if rounds and seq_len:
        rest = rounds * seq_len - fired - skips
        md.append(f"- {rounds} ciclos × {seq_len} passos = {rounds * seq_len} passos; "
                  f"**{fired} executados**, {skips} pulados"
                  + (f", {rest} não alcançados (execução interrompida)" if rest else ""))
    md.append(f"- impressão digital da configuração: `{', '.join(fps) or '-'}`")
    if rtt:
        md.append(f"- RTT de aplicação (nó 1, {rtt['n']} sondas): média {rtt['avg']:.2f} ms, "
                  f"mín {rtt['min']:.2f}, máx {rtt['max']:.2f}")
    md.append(f"- resultado: **{outcome}**"
              + (f" — SAFE HALT nos nós {halted}" if halted else ""))
    md.append("")
    md.append("| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares "
              "| decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for n, r in zip(nodes, res):
        if not r:
            md.append(f"| {n['log']} | ? | {n['exit']} | sem @@RESULT | | {n['dec_total']} | | | | | |")
            continue
        f = r["fired"]
        md.append(f"| {r['node']} | {' '.join(r['supervisors'])} | {n['exit']} "
                  f"| {f['local']}/{f['ctrl']}/{f['unctrl']} | {r['applied_for_peers']} "
                  f"| {n['dec_total']} ({n['dec_by_cycle'].get(1, 0)}) | {n['he_ms_total']:.1f} "
                  f"| {r['tx']}/{r['rx']} | {r['retx']} | {r['oracle']} "
                  f"| {'**' + r['halt_reason'] + '**' if r['safe_halt'] else 'não'} |")
    md.append(f"| **total** | | | | | **{dec_total} ({dec_c1})** | "
              f"{sum(n['he_ms_total'] for n in nodes):.1f} | "
              f"{sum(r['tx'] for r in res if r)}/{sum(r['rx'] for r in res if r)} | "
              f"{sum(r['retx'] for r in res if r)} | | |")
    md.append("")
    if cycle_end:
        md.append("Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: "
                  + ", ".join(f"{c:.1f}" for c in cycle_end))
        if per_step_c1 is not None:
            md.append(f"\nTempo por passo: ciclo 1 **{per_step_c1:.2f} ms**"
                      + (f"; ciclos 2–{n_cycles} **{per_step_rest:.2f} ms**"
                         if per_step_rest is not None else ""))
        md.append("")
    if mono:
        md.append(f"Verificação cruzada com o supervisor MONOLÍTICO: **{mono}**\n")
    md.append("## Verificações\n")
    md.append("| verificação | esperado | obtido | |")
    md.append("|---|---|---|---|")
    for c in checks:
        md.append(f"| {c['check']} | {c['expected']} | {c['got']} | {'✅' if c['ok'] else '❌'} |")
    ok = all(c["ok"] for c in checks)
    md.append("")
    md.append("**TODAS AS VERIFICAÇÕES PASSARAM**" if ok else "**HÁ VERIFICAÇÕES QUE FALHARAM**")
    md_text = "\n".join(md) + "\n"

    (run / "summary.md").write_text(md_text)
    (run / "summary.json").write_text(json.dumps({
        "run": run.name, "scenario": env, "outcome": outcome, "halted_nodes": halted,
        "fingerprints": fps, "rounds": rounds, "seq_len": seq_len,
        "steps_fired": fired, "skips": skips,
        "decryptions_total": dec_total, "decryptions_cycle1": dec_c1,
        "cycle_end_ms": cycle_end, "per_step_ms_cycle1": per_step_c1,
        "per_step_ms_steady": per_step_rest, "rtt_ms": rtt, "mono": mono,
        "checks": checks, "all_checks_ok": ok,
        "nodes": [{k: v for k, v in n.items()} for n in nodes],
    }, indent=2, ensure_ascii=False) + "\n")
    print(md_text)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
