#!/usr/bin/env python3
"""Scaling table for a sweep over the number of containers.

    python3 scripts/scaling.py results/<timestamp>-varredura

Reads every run folder under the directory (each with summary.json, written
by scripts/run.sh), groups them by scenario, and for the fms-N runs writes
escala.md / escala.json next to them:

  * time per step, cycle 1 and cycles 2-5 — mean ± sample sd when repeated;
  * speed-up over the single-container run (cycle 1 and steady state);
  * the LOWER BOUND the busiest node imposes: its cycle-1 decryptions × the
    emulated cost of one decryption ÷ steps per cycle. Nodes only work in
    parallel between two shared events, so the cell can never beat its most
    loaded node; the distance to the bound is coordination;
  * the partition (which supervisors on which node) and the checks;
  * when the directory also holds fms-N-<tag> runs (another partition of the
    same N, e.g. fms-4-s5), a table comparing them with the block partition.

Exit status 1 if any run failed its checks.
"""
import json
import math
import pathlib
import re
import sys


def mean_sd(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None
    m = sum(xs) / len(xs)
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) if len(xs) > 1 else 0.0
    return m, sd


def show(m, sd, n, d=1):
    if m is None:
        return "—"
    return f"{m:.{d}f}" if n == 1 else f"{m:.{d}f} ± {sd:.{d}f}"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = pathlib.Path(sys.argv[1])
    groups = {}
    for j in sorted(root.glob("*/summary.json")):
        name = re.sub(r"^\d{8}-\d{6}-", "", j.parent.name)
        groups.setdefault(name, []).append(json.loads(j.read_text()))
    # fms-N is the default block partition; fms-N-<tag> is another partition
    # of the same N (e.g. fms-4-s5: S5 isolated), compared at the end.
    series = {}
    for name, runs in groups.items():
        if (m := re.fullmatch(r"fms-(\d+)(?:-([\w]+))?", name)):
            series.setdefault(m.group(2), {})[int(m.group(1))] = runs
    if None not in series:
        print(f"nenhuma execução fms-N em {root}")
        return 2

    bad = 0

    def row(n, runs):
        nonlocal bad
        bad += sum(not r["all_checks_ok"] for r in runs)
        first = runs[0]
        emu = first["nodes"][0]["result"].get("emu_scalarmul_ms", 0) or 0
        seq = first["seq_len"]
        busiest = max(x["dec_by_cycle"].get("1", 0) for x in first["nodes"])
        c1 = mean_sd([r["per_step_ms_cycle1"] for r in runs])
        ss = mean_sd([r["per_step_ms_steady"] for r in runs])
        return {
            "nodes": n, "runs": len(runs),
            "checks_ok": sum(r["all_checks_ok"] for r in runs),
            "fingerprint": ",".join(sorted({",".join(r["fingerprints"]) for r in runs})),
            "decryptions": sorted({r["decryptions_total"] for r in runs}),
            "partition": [" ".join(x["result"]["supervisors"]) for x in first["nodes"]],
            "busiest_cycle1_dec": busiest,
            "emu_ms": emu,
            "bound_ms": busiest * emu / seq if emu and seq else None,
            "c1_mean": c1[0], "c1_sd": c1[1], "ss_mean": ss[0], "ss_sd": ss[1],
        }

    rows = [row(n, runs) for n, runs in sorted(series[None].items())]
    others = {tag: {n: row(n, runs) for n, runs in by_n.items()}
              for tag, by_n in series.items() if tag is not None}

    base = next((r for r in rows if r["nodes"] == 1), None)
    for r in rows:
        r["speedup_c1"] = base["c1_mean"] / r["c1_mean"] if base and r["c1_mean"] else None
        r["speedup_ss"] = base["ss_mean"] / r["ss_mean"] if base and r["ss_mean"] else None

    emu = rows[0]["emu_ms"]
    md = [f"# Escala: FMS em {', '.join(str(r['nodes']) for r in rows)} containers\n",
          (f"Cada decifração leva **{emu:g} ms**, como no ESP32-S3 "
           "(`DES_EMU_SCALARMUL_MS`)." if emu else
           "Emulação **desligada**: decifrações na velocidade desta máquina."),
          f"Repetições por configuração: {', '.join(str(r['runs']) for r in rows)}. "
          "Tempos em ms por passo (média ± desvio padrão quando repetido).\n",
          "| containers | ms/passo, ciclo 1 | aceleração | ms/passo, ciclos 2–5 | aceleração "
          "| limite (nó mais carregado) | acima do limite | verificações |",
          "|---|---|---|---|---|---|---|---|"]
    def x(v):
        return "—" if v is None else f"{v:.2f}×"

    for r in rows:
        k = r["runs"]
        bound = "—" if r["bound_ms"] is None else f"{r['bound_ms']:.1f}"
        over = ("—" if r["bound_ms"] is None or r["c1_mean"] is None
                else f"{r['c1_mean'] - r['bound_ms']:.1f}")
        md.append(f"| {r['nodes']} | {show(r['c1_mean'], r['c1_sd'], k)} | {x(r['speedup_c1'])} "
                  f"| {show(r['ss_mean'], r['ss_sd'], k)} | {x(r['speedup_ss'])} "
                  f"| {bound} | {over} | {r['checks_ok']}/{k} |")
    md.append("\nAceleração = tempo com 1 container ÷ tempo com N. Limite = decifrações "
              "do nó mais carregado no ciclo 1 × custo de uma decifração ÷ passos do "
              "ciclo: os nós só trabalham em paralelo entre dois eventos compartilhados, "
              "então a célula nunca é mais rápida que seu nó mais carregado.\n")
    md.append("## Partição e invariantes\n")
    md.append("| containers | supervisores por container | decifrações no ciclo 1 do mais carregado "
              "| decifrações (total) | impressão digital |")
    md.append("|---|---|---|---|---|")
    for r in rows:
        md.append(f"| {r['nodes']} | {' · '.join(r['partition'])} | {r['busiest_cycle1_dec']} "
                  f"| {', '.join(map(str, r['decryptions']))} | `{r['fingerprint']}` |")
    for tag, by_n in sorted(others.items()):
        blocks = {r["nodes"]: r for r in rows}
        md.append(f"\n## Comparação: partição `{tag}` × blocos contíguos\n")
        md.append("Mesmo número de containers, outra distribuição dos supervisores. "
                  "Δ = variação do tempo por passo em relação aos blocos "
                  "(negativo = mais rápido).\n")
        md.append("| containers | partição `" + tag + "` | ciclo 1: blocos | ciclo 1: `" + tag +
                  "` | Δ | ciclos 2–5: blocos | ciclos 2–5: `" + tag + "` | Δ "
                  "| limite: blocos | limite: `" + tag + "` | verificações |")
        md.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for n in sorted(by_n):
            o, b = by_n[n], blocks.get(n)
            if not b:
                continue

            def ms(v):
                return "—" if v is None else f"{v:.1f}"

            def d(a, c):
                return "—" if a is None or c is None else f"{100 * (a / c - 1):+.1f} %"
            md.append(
                f"| {n} | {' · '.join(o['partition'])} "
                f"| {show(b['c1_mean'], b['c1_sd'], b['runs'])} "
                f"| {show(o['c1_mean'], o['c1_sd'], o['runs'])} | {d(o['c1_mean'], b['c1_mean'])} "
                f"| {show(b['ss_mean'], b['ss_sd'], b['runs'])} "
                f"| {show(o['ss_mean'], o['ss_sd'], o['runs'])} | {d(o['ss_mean'], b['ss_mean'])} "
                f"| {ms(b['bound_ms'])} | {ms(o['bound_ms'])} "
                f"| {o['checks_ok']}/{o['runs']} |")
        md.append("\nCom 1 e com 7 containers as duas partições coincidem "
                  "(1 container: todos juntos; 7: um por container).")

    text = "\n".join(md) + "\n"
    (root / "escala.md").write_text(text)
    (root / "escala.json").write_text(json.dumps(
        {"blocos": rows, **{tag: [by_n[n] for n in sorted(by_n)] for tag, by_n in others.items()}}
        if others else rows, indent=2, ensure_ascii=False) + "\n")
    print(text)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
