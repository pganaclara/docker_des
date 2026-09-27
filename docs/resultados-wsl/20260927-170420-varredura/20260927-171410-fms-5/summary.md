# Execução `20260927-171410-fms-5`

- problema `fms`, família `LMOD`, **5 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `6f43d6b9`
- RTT de aplicação (nó 1, 20 sondas): média 4.51 ms, mín 3.21, máx 6.03
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14078.3 | 154/1176 | 0 | PASS | não |
| 2 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6961.0 | 246/1084 | 0 | PASS | não |
| 3 | S3 S4 | 0 | 20/20/10 | 80 | 217 (49) | 15118.9 | 287/1043 | 0 | PASS | não |
| 4 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8999.1 | 326/1004 | 0 | PASS | não |
| 5 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10483.9 | 317/1013 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55641.2 | 1330/5320 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4743.6, 8367.8, 12008.6, 15659.3, 19277.0

Tempo por passo: ciclo 1 **107.81 ms**; ciclos 2–5 **82.58 ms**

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
