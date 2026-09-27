# Execução `20260927-172556-fms-6`

- problema `fms`, família `LMOD`, **6 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `8d540ec9`
- RTT de aplicação (nó 1, 20 sondas): média 4.49 ms, mín 3.10, máx 6.22
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14085.4 | 159/1433 | 0 | PASS | não |
| 2 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6967.9 | 247/1345 | 0 | PASS | não |
| 3 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7180.3 | 249/1343 | 0 | PASS | não |
| 4 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7955.2 | 293/1299 | 0 | PASS | não |
| 5 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8996.3 | 326/1266 | 0 | PASS | não |
| 6 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10503.8 | 318/1274 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55688.9 | 1592/7960 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4289.4, 7671.0, 11071.5, 14480.7, 17885.4

Tempo por passo: ciclo 1 **97.49 ms**; ciclos 2–5 **77.25 ms**

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
