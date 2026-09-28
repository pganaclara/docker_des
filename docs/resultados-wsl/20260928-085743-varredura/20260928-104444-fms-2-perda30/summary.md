# Execução `20260928-104444-fms-2-perda30`

- problema `fms`, família `LMOD`, **2 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **13 executados**, 0 pulados, 207 não alcançados (execução interrompida)
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 6 sondas): média 4.30 ms, mín 4.12, máx 4.55
- resultado: **halt** — SAFE HALT nos nós [1, 2]

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 2 | 8/3/2 | 0 | 33 (33) | 2306.2 | 71/102 | 15 | PASS | **NOTIFY unacknowledged — a participant may have missed an uncontrollable shared event** |
| 2 | S4 S5 S6 | 2 | 0/0/0 | 6 | 39 (39) | 2816.3 | 149/44 | 0 | PASS | **a peer halted** |
| **total** | | | | | **72 (72)** | 5122.5 | 220/146 | 15 | | |

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | edbd7971 | edbd7971 | ✅ |
| outcome | complete|halt|incomplete | halt | ✅ |
| consistency across nodes | consistente | consistente até o SAFE HALT (1 evento em voo: 1-2) | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
