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
  * the partition (which supervisors on which node) and the checks.

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
    sweep = sorted((int(m.group(1)), runs) for name, runs in groups.items()
                   if (m := re.fullmatch(r"fms-(\d+)", name)))
    if not sweep:
        print(f"nenhuma execução fms-N em {root}")
        return 2

    rows, bad = [], 0
    for n, runs in sweep:
        bad += sum(not r["all_checks_ok"] for r in runs)
        first = runs[0]
        emu = first["nodes"][0]["result"].get("emu_scalarmul_ms", 0) or 0
        seq = first["seq_len"]
        busiest = max(x["dec_by_cycle"].get("1", 0) for x in first["nodes"])
        c1 = mean_sd([r["per_step_ms_cycle1"] for r in runs])
        ss = mean_sd([r["per_step_ms_steady"] for r in runs])
        rows.append({
            "nodes": n, "runs": len(runs),
            "checks_ok": sum(r["all_checks_ok"] for r in runs),
            "fingerprint": ",".join(sorted({",".join(r["fingerprints"]) for r in runs})),
            "decryptions": sorted({r["decryptions_total"] for r in runs}),
            "partition": [" ".join(x["result"]["supervisors"]) for x in first["nodes"]],
            "busiest_cycle1_dec": busiest,
            "emu_ms": emu,
            "bound_ms": busiest * emu / seq if emu and seq else None,
            "c1_mean": c1[0], "c1_sd": c1[1], "ss_mean": ss[0], "ss_sd": ss[1],
        })

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
    for r in rows:
        k = r["runs"]
        over = (f"{r['c1_mean'] - r['bound_ms']:.1f}"
                if r["bound_ms"] is not None and r["c1_mean"] is not None else "—")
        md.append(
            f"| {r['nodes']} | {show(r['c1_mean'], r['c1_sd'], k)} "
            f"| {r['speedup_c1']:.2f}× | {show(r['ss_mean'], r['ss_sd'], k)} "
            f"| {r['speedup_ss']:.2f}× "
            f"| {'—' if r['bound_ms'] is None else f'{r[chr(98)+chr(111)+chr(117)+chr(110)+chr(100)+chr(95)+chr(109)+chr(115)]:.1f}'} "
            f"| {over} | {r['checks_ok']}/{k} |" if base else
            f"| {r['nodes']} | {show(r['c1_mean'], r['c1_sd'], k)} | — "
            f"| {show(r['ss_mean'], r['ss_sd'], k)} | — | — | — | {r['checks_ok']}/{k} |")
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
    text = "\n".join(md) + "\n"
    (root / "escala.md").write_text(text)
    (root / "escala.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
    print(text)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
