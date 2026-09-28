# Execução `20260927-211212-fms-5`

- problema `fms`, família `LMOD`, **5 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `6f43d6b9`
- RTT de aplicação (nó 1, 20 sondas): média 4.63 ms, mín 3.10, máx 5.59
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14103.8 | 154/1176 | 0 | PASS | não |
| 2 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6970.1 | 249/1081 | 0 | PASS | não |
| 3 | S3 S4 | 0 | 20/20/10 | 80 | 217 (49) | 15154.0 | 286/1044 | 0 | PASS | não |
| 4 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9021.1 | 324/1006 | 0 | PASS | não |
| 5 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10535.7 | 317/1013 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55784.7 | 1330/5320 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4781.1, 8420.0, 12071.1, 15702.6, 19354.8

Tempo por passo: ciclo 1 **108.66 ms**; ciclos 2–5 **82.81 ms**

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
