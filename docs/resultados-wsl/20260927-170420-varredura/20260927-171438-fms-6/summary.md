# Execução `20260927-171438-fms-6`

- problema `fms`, família `LMOD`, **6 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `8d540ec9`
- RTT de aplicação (nó 1, 20 sondas): média 4.37 ms, mín 2.97, máx 5.35
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14099.3 | 157/1441 | 0 | PASS | não |
| 2 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6971.0 | 249/1349 | 0 | PASS | não |
| 3 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7194.2 | 252/1346 | 0 | PASS | não |
| 4 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7970.3 | 293/1305 | 0 | PASS | não |
| 5 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9027.9 | 329/1269 | 0 | PASS | não |
| 6 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10533.5 | 318/1280 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55796.2 | 1598/7990 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4355.2, 7760.6, 11153.5, 14561.6, 17958.0

Tempo por passo: ciclo 1 **98.98 ms**; ciclos 2–5 **77.29 ms**

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
