# Execução `20260928-102219-fms-2-perda30`

- problema `fms`, família `LMOD`, **2 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **8 executados**, 0 pulados, 212 não alcançados (execução interrompida)
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 6 sondas): média 4.38 ms, mín 3.90, máx 4.93
- resultado: **halt** — SAFE HALT nos nós [1, 2]

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 2 | 6/1/1 | 0 | 19 (19) | 1332.4 | 45/45 | 4 | PASS | **COMMIT unacknowledged — a participant may not have applied a shared event** |
| 2 | S4 S5 S6 | 2 | 0/0/0 | 3 | 18 (18) | 1306.1 | 77/27 | 0 | PASS | **a peer halted** |
| **total** | | | | | **37 (37)** | 2638.5 | 122/72 | 4 | | |

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
