# Execução `20260927-143544-fms-2-loss30`

- problema `fms`, família `LMOD`, **2 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **101 executados**, 0 pulados, 119 não alcançados (execução interrompida)
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 9 sondas): média 2.87 ms, mín 2.32, máx 3.54
- resultado: **halt** — SAFE HALT nos nós [1, 2]

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 2 | 40/19/18 | 0 | 193 (85) | 146.5 | 144/279 | 53 | PASS | **NOTIFY unacknowledged — a participant may have missed an uncontrollable shared event** |
| 2 | S4 S5 S6 | 2 | 24/0/0 | 38 | 195 (105) | 206.5 | 416/99 | 0 | PASS | **a peer halted** |
| **total** | | | | | **388 (190)** | 353.0 | 560/378 | 53 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 37489.6, 72823.9

Tempo por passo: ciclo 1 **852.04 ms**; ciclos 2–2 **803.05 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| outcome | halt | halt | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
