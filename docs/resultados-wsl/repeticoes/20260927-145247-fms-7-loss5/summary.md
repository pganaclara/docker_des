# Execução `20260927-145247-fms-7-loss5`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 12 sondas): média 4.38 ms, mín 3.61, máx 4.96
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 264.6 | 225/4372 | 65 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 317.4 | 745/3898 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 315.8 | 754/3854 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 304.4 | 751/3920 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 336.3 | 731/3937 | 14 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 367.6 | 835/3828 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 452.7 | 839/3840 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2358.8 | 4880/27649 | 79 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 19175.8, 60648.1, 92954.8, 115421.1, 147711.0

Tempo por passo: ciclo 1 **435.81 ms**; ciclos 2–5 **730.31 ms**

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
