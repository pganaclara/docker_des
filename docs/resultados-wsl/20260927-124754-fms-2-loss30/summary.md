# Execução `20260927-124754-fms-2-loss30`

- problema `fms`, família `LMOD`, **2 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **32 executados**, 0 pulados, 188 não alcançados (execução interrompida)
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 9 sondas): média 4.64 ms, mín 4.28, máx 5.93
- resultado: **halt** — SAFE HALT nos nós [1, 2]

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 2 | 13/5/5 | 0 | 58 (58) | 55.6 | 74/133 | 25 | PASS | **COMMIT unacknowledged — a participant may not have applied a shared event** |
| 2 | S4 S5 S6 | 2 | 9/0/0 | 11 | 77 (77) | 103.4 | 196/47 | 0 | PASS | **a peer halted** |
| **total** | | | | | **135 (135)** | 159.0 | 270/180 | 25 | | |

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| outcome | halt | halt | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
