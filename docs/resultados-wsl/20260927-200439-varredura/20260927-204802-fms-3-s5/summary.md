# Execução `20260927-204802-fms-3-s5`

- problema `fms`, família `LMOD`, **3 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `6d9dd456`
- RTT de aplicação (nó 1, 20 sondas): média 4.23 ms, mín 2.77, máx 5.01
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S2 S6 | 0 | 70/60/50 | 0 | 351 (79) | 24573.5 | 200/645 | 0 | PASS | não |
| 2 | S1 S3 S4 | 0 | 40/0/0 | 110 | 318 (70) | 22173.7 | 317/528 | 0 | PASS | não |
| 3 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9010.9 | 328/517 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55758.1 | 845/1690 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 6359.0, 11584.1, 16828.0, 22076.4, 27319.2

Tempo por passo: ciclo 1 **144.52 ms**; ciclos 2–5 **119.09 ms**

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
