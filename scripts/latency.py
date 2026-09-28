#!/usr/bin/env python3
"""Per-step latency percentiles for one or more sweep directories.

    python3 scripts/latency.py results/<timestamp>-varredura [more dirs...]

Reads every run folder (written by scripts/run.sh) and groups the runs by
scenario, pooling cycles and repetitions. Two kinds of latency:

1. EVENT latency, from the lines the engine prints for every step:
     decision (owner)   "c1 s3 2pc 31  139.7 ms HE ... + 4.9 ms peer-wait"
                        = homomorphic step + waiting for the peers, i.e. the
                        duration of fire(): what the owner spends deciding
                        and committing one event. Split by class:
                        local (no network), 2pc (shared, controllable) and
                        notify (shared, uncontrollable).
     apply (participant) "· apply 31  215.0 ms HE ... from node 1"
                        = the homomorphic step a participant runs for a
                        shared event another node committed.
   Available for every run, old ones included.

2. CELL inter-completion interval, from nodeK.ts.log (the same log with
   Docker's per-line timestamps; scripts/run.sh saves it since this script
   exists). Every step of the trace completes on exactly one node, the owner's
   driver line; sorting those completions on the common clock gives the time
   between one step finishing anywhere in the cell and the next. Runs without
   .ts.log files are skipped for this part. Docker stamps with the host wall
   clock, which WSL 2 steps by ~11 s now and then; samples the step would
   corrupt are dropped (see run_samples) and the count is reported.

Reported per scenario and class: n, mean, p50, p90, p95, p99, max (ms),
separately for cycle 1 and cycles 2..R (cycle 1 does more decryptions).
p99 needs ~100 samples to mean anything: the table says n so it can be read
accordingly.

Writes latencia.md, latencia.json and latencia.csv (every sample, for
plotting) in the first directory given, and prints latencia.md.
"""
import csv
import json
import math
import pathlib
import re
import sys
from datetime import datetime

DRIVER = re.compile(r"^c(\d+)\s+s(\d+)\s+(local|2pc|notify)\s+(\S+)\s+([\d.]+) ms HE"
                    r"(?:.*?\+ ([\d.]+) ms peer-wait)?")
APPLY = re.compile(r"^\s+·\s+apply\s+(\S+)\s+([\d.]+) ms HE")
CYCLE = re.compile(r"^-- cycle (\d+)/\d+ --$")
DONE = re.compile(r"^-- cycle \d+/\d+ done at ([\d.]+) ms --$")
TS = re.compile(r"^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(?:\.(\d+))?(Z|[+-]\d\d:\d\d)\s(.*)$")
PCTS = (50, 90, 95, 99)


def pct(sorted_xs, p):
    """Nearest-rank percentile (no interpolation)."""
    if not sorted_xs:
        return None
    k = max(1, math.ceil(p / 100 * len(sorted_xs)))
    return sorted_xs[k - 1]


def stats(xs):
    xs = sorted(xs)
    if not xs:
        return None
    out = {"n": len(xs), "mean": sum(xs) / len(xs), "max": xs[-1]}
    for p in PCTS:
        out[f"p{p}"] = pct(xs, p)
    return out


def parse_ts(stamp, frac, tz):
    # Docker prints nanoseconds; datetime takes microseconds.
    frac = (frac or "0")[:6].ljust(6, "0")
    tz = "+00:00" if tz == "Z" else tz
    return datetime.fromisoformat(f"{stamp}.{frac}{tz}").timestamp()


cell_dropped = [0, 0, 0]                     # intervals, completions, cycles
CLOCK_TOL_MS = 200.0


def run_samples(run):
    """(event samples, cell interval samples) for one run folder."""
    events, cell = [], []
    for log in sorted(run.glob("node*.log")):
        if log.name.endswith(".ts.log"):
            continue
        cycle = 0
        for line in log.read_text(errors="replace").splitlines():
            if (m := CYCLE.match(line)):
                cycle = int(m.group(1))
            elif (m := DRIVER.match(line)):
                he = float(m.group(5))
                wait = float(m.group(6)) if m.group(6) else 0.0
                events.append((int(m.group(1)), m.group(3), he + wait, log.stem))
            elif (m := APPLY.match(line)):
                events.append((cycle, "apply", float(m.group(2)), log.stem))

    # Docker stamps each line with the host's wall clock when it reads it. On
    # WSL 2 that clock is occasionally stepped (Hyper-V time sync): a handful
    # of lines, on every node at once, come out ~11 s in the future and the
    # next ones are back in the past. A line cannot be stamped later than one
    # the same container printed after it, nor earlier than one it printed
    # before, so such lines are marked invalid, and so is every interval that
    # would span one of them (by trace position), instead of inventing a gap.
    completions, bad_keys, done_marks = [], set(), []   # (time, cycle, step)
    for ts in sorted(run.glob("node*.ts.log")):
        rows = []
        for line in ts.read_text(errors="replace").splitlines():
            m = TS.match(line)
            if m:
                done = DONE.match(m.group(4))
                rows.append((parse_ts(m.group(1), m.group(2), m.group(3)),
                             float(done.group(1)) if done else DRIVER.match(m.group(4))))
        ok = [True] * len(rows)
        low = math.inf                      # forward jumps: later than a successor
        for i in range(len(rows) - 1, -1, -1):
            if rows[i][0] > low:
                ok[i] = False
            low = min(low, rows[i][0])
        high = -math.inf                    # backward jumps: earlier than a predecessor
        for i, (t, _) in enumerate(rows):
            if not ok[i]:
                continue
            if t < high:
                ok[i] = False
            high = max(high, t)
        for (t, d), good in zip(rows, ok):
            if isinstance(d, float):
                if good:
                    done_marks.append((t, d))
                continue
            if not d:
                continue
            key = (int(d.group(1)), int(d.group(2)))
            if good:
                completions.append((t,) + key)
            else:
                bad_keys.add(key)
    completions.sort()
    # A step that is not undone (the clock jumps and stays there) keeps the
    # order and cannot be seen that way. The engine's run clock is immune: each
    # node prints "-- cycle c/R done at X ms --" on it, so Docker time minus X
    # is the run clock's zero on the Docker clock, the same on every such line
    # while the host clock behaves (median over them all = the estimate).
    # Cycle c is trusted only if the cell's last completion of c and of c-1
    # both sit where summary.json (cycle_end_ms) says, within CLOCK_TOL_MS.
    ends = json.loads((run / "summary.json").read_text()).get("cycle_end_ms") or []
    zeros = sorted(t - x / 1000.0 for t, x in done_marks)
    t0 = zeros[len(zeros) // 2] if zeros else None
    last = {}
    for t, c, _ in completions:
        last[c] = max(last.get(c, t), t)

    def off(c):
        if c == 0:
            return False
        if t0 is None or c not in last or c > len(ends):
            return True
        return abs((last[c] - t0) * 1000.0 - ends[c - 1]) > CLOCK_TOL_MS

    bad_cycles = {c for c in last if off(c) or off(c - 1)}
    dropped = 0
    for (t0, c0, s0), (t1, c1, s1) in zip(completions, completions[1:]):
        lo, hi = sorted(((c0, s0), (c1, s1)))
        if c1 in bad_cycles or any(lo < k < hi for k in bad_keys):
            dropped += 1
            continue
        cell.append((c1, (t1 - t0) * 1000.0))
    cell_dropped[2] += len(bad_cycles)
    cell_dropped[0] += dropped
    cell_dropped[1] += len(bad_keys)
    return events, cell


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    roots = [pathlib.Path(a) for a in sys.argv[1:]]
    groups = {}
    for root in roots:
        for s in sorted(root.glob("*/summary.json")):
            name = re.sub(r"^\d{8}-\d{6}-", "", s.parent.name)
            groups.setdefault(name, []).append(s.parent)

    def order(name):
        m = re.fullmatch(r"fms-(\d+)(?:-(\w+))?", name)
        return (int(m.group(1)), m.group(2) or "") if m else (99, name)

    table, raw = {}, []
    for name in sorted(groups, key=order):
        ev, ce = [], []
        for i, run in enumerate(groups[name]):
            e, c = run_samples(run)
            ev += e
            ce += c
            raw += [(name, run.name, cyc, cls, round(v, 3), node) for cyc, cls, v, node in e]
            raw += [(name, run.name, cyc, "cell", round(v, 3), "") for cyc, v in c]
        entry = {"runs": len(groups[name])}
        for phase, keep in (("ciclo 1", lambda c: c == 1), ("ciclos 2+", lambda c: c >= 2)):
            for cls in ("local", "2pc", "notify", "apply"):
                s = stats([v for c, k, v, _ in ev if k == cls and keep(c)])
                if s:
                    entry[f"{cls} · {phase}"] = s
            s = stats([v for c, v in ce if keep(c)])
            if s:
                entry[f"célula · {phase}"] = s
        table[name] = entry

    md = ["# Latência por passo: percentis\n",
          "Em ms. Amostras agrupadas por cenário (todos os ciclos da fase e todas as "
          "repetições). Percentil pelo posto mais próximo; com n < 100 o p99 é "
          "praticamente o máximo.\n",
          "- **local / 2pc / notify**: latência de *decisão* no nó dono do evento "
          "(passo homomórfico + espera pelos pares).",
          "- **apply**: passo homomórfico de um participante ao aplicar um evento "
          "compartilhado.",
          "- **célula**: intervalo entre a conclusão de um passo e a do seguinte, "
          "em qualquer nó, no relógio comum (exige `nodeK.ts.log`). Linhas com "
          "carimbo fora de ordem no próprio nó (relógio do host saltou) são "
          "descartadas, junto com os intervalos que as atravessariam.\n"]
    for name, entry in table.items():
        md.append(f"## `{name}` ({entry['runs']} execuções)\n")
        md.append("| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |")
        md.append("|---|---|---|---|---|---|---|---|---|")
        for key, s in entry.items():
            if key == "runs":
                continue
            cls, phase = key.split(" · ")
            md.append(f"| {cls} | {phase} | {s['n']} | {s['mean']:.1f} | "
                      + " | ".join(f"{s[f'p{p}']:.1f}" for p in PCTS)
                      + f" | {s['max']:.1f} |")
        if not any(k.startswith("célula") for k in entry):
            md.append("\n(sem `nodeK.ts.log`: intervalo da célula não disponível "
                      "para estas execuções)")
        md.append("")
    if cell_dropped[1]:
        md.append(f"Carimbos inválidos descartados: {cell_dropped[1]} conclusões de passo, "
                  f"{cell_dropped[2]} ciclos inteiros cujo início ou fim nos carimbos diverge do "
                  f"relógio do motor em mais de {CLOCK_TOL_MS:.0f} ms, "
                  f"{cell_dropped[0]} intervalos da célula (em todas as execuções).\n")
    text = "\n".join(md) + "\n"

    out = roots[0]
    (out / "latencia.md").write_text(text)
    (out / "latencia.json").write_text(json.dumps(table, indent=2, ensure_ascii=False) + "\n")
    with (out / "latencia.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cenario", "execucao", "ciclo", "classe", "ms", "no"])
        w.writerows(raw)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
