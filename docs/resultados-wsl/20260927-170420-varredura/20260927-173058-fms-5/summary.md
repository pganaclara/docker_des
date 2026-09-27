# Execução `20260927-173058-fms-5`

- problema `fms`, família `LMOD`, **5 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `6f43d6b9`
- RTT de aplicação (nó 1, 20 sondas): média 3.11 ms, mín 2.31, máx 4.54
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14076.3 | 155/1184 | 0 | PASS | não |
| 2 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6965.0 | 249/1090 | 0 | PASS | não |
| 3 | S3 S4 | 0 | 20/20/10 | 80 | 217 (49) | 15118.9 | 286/1053 | 0 | PASS | não |
| 4 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8990.3 | 329/1010 | 0 | PASS | não |
| 5 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10470.1 | 320/1019 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55620.6 | 1339/5356 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4698.6, 8336.1, 11978.7, 15622.8, 19267.6

Tempo por passo: ciclo 1 **106.79 ms**; ciclos 2–5 **82.78 ms**

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
