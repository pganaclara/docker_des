# Execução `20260927-210351-fms-3-s5`

- problema `fms`, família `LMOD`, **3 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `6d9dd456`
- RTT de aplicação (nó 1, 20 sondas): média 2.80 ms, mín 2.23, máx 3.43
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S2 S6 | 0 | 70/60/50 | 0 | 351 (79) | 24314.7 | 200/647 | 0 | PASS | não |
| 2 | S1 S3 S4 | 0 | 40/0/0 | 110 | 318 (70) | 22015.8 | 318/529 | 0 | PASS | não |
| 3 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8934.6 | 329/518 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55265.1 | 847/1694 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 6230.4, 11400.8, 16571.0, 21742.0, 26907.1

Tempo por passo: ciclo 1 **141.60 ms**; ciclos 2–5 **117.48 ms**

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
