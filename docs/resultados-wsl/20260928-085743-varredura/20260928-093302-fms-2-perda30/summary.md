# Execução `20260928-093302-fms-2-perda30`

- problema `fms`, família `LMOD`, **2 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **32 executados**, 0 pulados, 188 não alcançados (execução interrompida)
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 9 sondas): média 3.64 ms, mín 2.62, máx 4.96
- resultado: **halt** — SAFE HALT nos nós [1, 2]

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 2 | 13/5/5 | 0 | 58 (58) | 4033.3 | 66/117 | 18 | PASS | **COMMIT unacknowledged — a participant may not have applied a shared event** |
| 2 | S4 S5 S6 | 2 | 9/0/0 | 11 | 77 (77) | 5404.5 | 157/43 | 0 | PASS | **a peer halted** |
| **total** | | | | | **135 (135)** | 9437.8 | 223/160 | 18 | | |

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
