#!/usr/bin/env python3
"""Aggregate repeated runs: mean, standard deviation and range per scenario.

    python3 scripts/aggregate.py <dir-with-run-folders> [more dirs...]

Every run folder is one written by scripts/run.sh (it must hold summary.json;
run scripts/summarize.py on it first if it does not). Runs are grouped by
scenario name (the folder name without its timestamp prefix).

Two kinds of quantity come out, and they are reported differently:
  * INVARIANTS — fingerprint, decryptions, steps, outcome. They must be the
    same in every repetition; the table says "igual em N/N" or lists what
    varied. A variation here is a bug, not noise.
  * MEASUREMENTS — time per step, RTT, retransmissions, steps before a halt.
    Reported as mean ± sample standard deviation [min–max], n.

Writes aggregate.md and aggregate.json in the first directory given and
prints aggregate.md.
"""
import json
import math
import pathlib
import re
import sys


def stats(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None
    n = len(xs)
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1)) if n > 1 else 0.0
    return {"n": n, "mean": m, "sd": sd, "min": min(xs), "max": max(xs)}


def fmt(s, digits=2):
    if not s:
        return "—"
    if s["n"] == 1:
        return f"{s['mean']:.{digits}f} (n=1)"
    cv = f", CV {100 * s['sd'] / s['mean']:.0f} %" if s["mean"] else ""
    return (f"{s['mean']:.{digits}f} ± {s['sd']:.{digits}f} "
            f"[{s['min']:.{digits}f}–{s['max']:.{digits}f}]{cv}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    runs = {}
    for root in map(pathlib.Path, sys.argv[1:]):
        for j in sorted(root.glob("*/summary.json")):
            name = re.sub(r"^\d{8}-\d{6}-", "", j.parent.name)
            runs.setdefault(name, []).append(json.loads(j.read_text()))

    out, md = {}, ["# Repetições agregadas\n",
                   "Invariantes: têm de ser idênticos em todas as repetições. "
                   "Medidas: média ± desvio padrão amostral [mín–máx], "
                   "coeficiente de variação.\n"]

    md.append("## Invariantes\n")
    md.append("| cenário | n | todas as verificações | impressão digital | decifrações (ciclo 1) "
              "| por nó | desfecho |")
    md.append("|---|---|---|---|---|---|---|")
    for name in sorted(runs):
        rs = runs[name]
        n = len(rs)

        def same(key):
            vals = [key(r) for r in rs]
            first = vals[0]
            return (f"{first} (igual em {n}/{n})" if all(v == first for v in vals)
                    else "varia: " + ", ".join(sorted({str(v) for v in vals})))

        ok = sum(r["all_checks_ok"] for r in rs)
        halted = all(r["outcome"] == "halt" for r in rs)
        fp = same(lambda r: ",".join(r["fingerprints"]))
        dec = ("varia até o halt" if halted else
               same(lambda r: "%d (%d)" % (r["decryptions_total"], r["decryptions_cycle1"])))
        per = ("—" if halted else
               same(lambda r: " + ".join(str(x["dec_total"]) for x in r["nodes"])))
        md.append(f"| `{name}` | {n} | {ok}/{n} | {fp} | {dec} | {per} "
                  f"| {same(lambda r: r['outcome'])} |")

    md.append("\n## Medidas\n")
    md.append("| cenário | ms/passo, ciclo 1 | ms/passo, ciclos 2–5 | RTT de aplicação, ms "
              "| retransmissões | passos até o halt |")
    md.append("|---|---|---|---|---|---|")
    for name in sorted(runs):
        rs = runs[name]
        c1 = stats([r["per_step_ms_cycle1"] for r in rs])
        ss = stats([r["per_step_ms_steady"] for r in rs])
        rtt = stats([r["rtt_ms"]["avg"] if r["rtt_ms"] else None for r in rs])
        retx = stats([sum((x["result"] or {}).get("retx", 0) for x in r["nodes"]) for r in rs])
        halt = (stats([r["steps_fired"] for r in rs])
                if all(r["outcome"] == "halt" for r in rs) else None)
        out[name] = {"n": len(rs), "per_step_ms_cycle1": c1, "per_step_ms_steady": ss,
                     "rtt_ms": rtt, "retx": retx, "steps_before_halt": halt,
                     "all_checks_ok": sum(r["all_checks_ok"] for r in rs)}
        md.append(f"| `{name}` | {fmt(c1)} | {fmt(ss)} | {fmt(rtt)} | {fmt(retx, 0)} "
                  f"| {fmt(halt, 0) if halt else '—'} |")

    text = "\n".join(md) + "\n"
    first = pathlib.Path(sys.argv[1])
    (first / "aggregate.md").write_text(text)
    (first / "aggregate.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
