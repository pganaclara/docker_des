# Execução `20260927-204000-fms-4-s5`

- problema `fms`, família `LMOD`, **4 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `10c88d9b`
- RTT de aplicação (nó 1, 20 sondas): média 3.85 ms, mín 2.35, máx 5.06
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14072.4 | 154/931 | 0 | PASS | não |
| 2 | S2 S6 | 0 | 50/20/10 | 80 | 250 (58) | 17464.7 | 284/801 | 0 | PASS | não |
| 3 | S3 S4 | 0 | 20/0/0 | 110 | 217 (49) | 15111.6 | 320/765 | 0 | PASS | não |
| 4 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8989.5 | 327/758 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55638.2 | 1085/3255 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 5160.1, 8995.5, 12827.5, 16676.6, 20526.2

Tempo por passo: ciclo 1 **117.28 ms**; ciclos 2–5 **87.31 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| decryptions, whole cell | 798 | 798 | ✅ |
| decryptions, whole cell, cycle 1 | 190 | 190 | ✅ |
| outcome | complete | complete | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
