# Execução `20260927-150115-fms-2-loss30`

- problema `fms`, família `LMOD`, **2 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **116 executados**, 0 pulados, 104 não alcançados (execução interrompida)
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 9 sondas): média 2.64 ms, mín 2.21, máx 3.36
- resultado: **halt** — SAFE HALT nos nós [1, 2]

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 2 | 43/20/20 | 0 | 208 (85) | 106.4 | 165/349 | 72 | PASS | **COMMIT unacknowledged — a participant may not have applied a shared event** |
| 2 | S4 S5 S6 | 2 | 33/0/0 | 41 | 219 (105) | 128.4 | 513/112 | 0 | PASS | **a peer halted** |
| **total** | | | | | **427 (190)** | 234.8 | 678/461 | 72 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 41565.9, 78653.9

Tempo por passo: ciclo 1 **944.68 ms**; ciclos 2–2 **842.91 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| outcome | halt | halt | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
