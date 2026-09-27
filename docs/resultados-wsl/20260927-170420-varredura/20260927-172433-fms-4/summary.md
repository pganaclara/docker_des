# Execução `20260927-172433-fms-4`

- problema `fms`, família `LMOD`, **4 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `457cc268`
- RTT de aplicação (nó 1, 20 sondas): média 4.29 ms, mín 2.90, máx 5.32
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14094.7 | 152/847 | 0 | PASS | não |
| 2 | S2 S3 | 0 | 40/0/0 | 80 | 203 (43) | 14160.6 | 246/753 | 0 | PASS | não |
| 3 | S4 S5 | 0 | 0/20/10 | 80 | 243 (67) | 16975.4 | 285/714 | 0 | PASS | não |
| 4 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10531.2 | 316/683 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55761.9 | 999/2997 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 5869.1, 9997.8, 14139.1, 18265.6, 22399.0

Tempo por passo: ciclo 1 **133.39 ms**; ciclos 2–5 **93.92 ms**

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
