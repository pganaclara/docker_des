#!/usr/bin/env python3
"""Robustness to frame loss: what happened in the fms-N-perdaP runs.

    python3 scripts/loss.py results/<timestamp>-varredura

Reads the fms-N-perdaP runs under the directory (scripts/run-all.sh perda) and
writes perda.md / perda.json next to them. Per N and loss P:

  * outcome of each repetition: complete, SAFE HALT, or incomplete (the run
    finished with skipped steps: an owner gave up on an event before its
    commit point, so nothing was applied anywhere);
  * steps executed (of 220), skips, retransmissions (all nodes);
  * time per step when the run completed (engine run clock);
  * the SAFETY checks, which must hold in every run whatever the outcome:
    consistency across nodes (summarize.py: every pair of nodes executed the
    shared events they have in common in the same order; after a SAFE HALT one
    may be one commit ahead) and the homomorphic oracle on every node.

Exit status 1 if any run failed a check (a divergence, an oracle failure...).
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
    return m, (math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) if len(xs) > 1 else 0.0)


def show(ms, d=1):
    m, sd = ms
    return "—" if m is None else f"{m:.{d}f} ± {sd:.{d}f}"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = pathlib.Path(sys.argv[1])
    cells = {}
    for j in sorted(root.glob("*/summary.json")):
        name = re.sub(r"^\d{8}-\d{6}-", "", j.parent.name)
        if (m := re.fullmatch(r"fms-(\d+)-perda(\d+)", name)):
            cells.setdefault((int(m.group(1)), int(m.group(2))), []).append(
                json.loads(j.read_text()))
    if not cells:
        print(f"nenhuma execução fms-N-perdaP em {root}")
        return 2

    bad, table = 0, []
    for (n, p), runs in sorted(cells.items()):
        bad += sum(not r["all_checks_ok"] for r in runs)
        total = runs[0]["rounds"] * runs[0]["seq_len"]
        outcomes = [r["outcome"] for r in runs]
        consistent = sum(not r["consistency"].startswith("DIVERGENTE") for r in runs)
        at_halt = sum(r["consistency"].startswith("consistente até") for r in runs)
        oracle = sum(all(x["result"] and x["result"]["oracle"] == "PASS" for x in r["nodes"])
                     for r in runs)
        retx = [sum(x["result"]["retx"] for x in r["nodes"] if x["result"]) for r in runs]
        done = [r for r in runs if r["outcome"] == "complete"]
        reasons = sorted({x["result"]["halt_reason"] for r in runs for x in r["nodes"]
                          if x["result"] and x["result"]["safe_halt"]})
        table.append({
            "nodes": n, "loss_pct": p, "runs": len(runs), "steps_total": total,
            "complete": outcomes.count("complete"), "halt": outcomes.count("halt"),
            "incomplete": outcomes.count("incomplete"),
            "steps_fired": [r["steps_fired"] for r in runs],
            "skips": [r["skips"] for r in runs], "retx": retx,
            "consistent": consistent, "consistent_at_halt": at_halt, "oracle_ok": oracle,
            "checks_ok": sum(r["all_checks_ok"] for r in runs),
            "per_step_c1_complete": [r["per_step_ms_cycle1"] for r in done],
            "per_step_steady_complete": [r["per_step_ms_steady"] for r in done],
            "halt_reasons": reasons,
            "seeds": [sorted({x["result"].get("loss_seed") for x in r["nodes"] if x["result"]})
                      for r in runs],
        })

    md = ["# Robustez a perda de quadros\n",
          "Cada nó descarta P % dos quadros que recebe, depois da autenticação "
          "(`DES_SIMULATE_LOSS_PCT`), com sorteio novo por execução e por nó. "
          "Decifração emulada a 69 ms e *timeouts* do motor (1,5 s) como no ESP32.\n",
          "## Desfecho\n",
          "**completa**: os 220 passos; **SAFE HALT**: um COMMIT/NOTIFY esgotou as "
          "retransmissões depois do ponto de commit e a célula parou; **incompleta**: "
          "terminou com passos pulados (o dono desistiu *antes* do commit, nada foi "
          "aplicado).\n",
          "| nós | perda | execuções | completa | SAFE HALT | incompleta | passos executados "
          "| pulados | retransmissões |",
          "|---|---|---|---|---|---|---|---|---|"]
    for t in table:
        md.append(f"| {t['nodes']} | {t['loss_pct']} % | {t['runs']} | {t['complete']} "
                  f"| {t['halt']} | {t['incomplete']} "
                  f"| {show(mean_sd(t['steps_fired']))} de {t['steps_total']} "
                  f"| {show(mean_sd(t['skips']))} | {show(mean_sd(t['retx']))} |")
    md += ["\n## Segurança (tem de valer em toda execução)\n",
           "| nós | perda | consistência entre nós | (das quais: 1 evento em voo no SAFE HALT) "
           "| oráculo PASS em todo nó | todas as verificações |",
           "|---|---|---|---|---|---|"]
    for t in table:
        md.append(f"| {t['nodes']} | {t['loss_pct']} % | {t['consistent']}/{t['runs']} "
                  f"| {t['consistent_at_halt']} | {t['oracle_ok']}/{t['runs']} "
                  f"| {t['checks_ok']}/{t['runs']} |")
    md += ["\n## Tempo por passo das execuções completas (ms)\n",
           "Compare com a varredura sem perda: 2 nós ≈ 196 / 149, 7 nós ≈ 90 / 61 ms "
           "(ciclo 1 / ciclos 2–5).\n",
           "| nós | perda | completas | ciclo 1 | ciclos 2–5 |", "|---|---|---|---|---|"]
    for t in table:
        md.append(f"| {t['nodes']} | {t['loss_pct']} % | {t['complete']} "
                  f"| {show(mean_sd(t['per_step_c1_complete']))} "
                  f"| {show(mean_sd(t['per_step_steady_complete']))} |")
    reasons = [(t["nodes"], t["loss_pct"], r) for t in table for r in t["halt_reasons"]]
    if reasons:
        md += ["\n## Motivos de SAFE HALT\n"]
        md += [f"- {n} nós, {p} %: {r}" for n, p, r in reasons]
    text = "\n".join(md) + "\n"
    (root / "perda.md").write_text(text)
    (root / "perda.json").write_text(json.dumps(table, indent=2, ensure_ascii=False) + "\n")
    print(text)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
