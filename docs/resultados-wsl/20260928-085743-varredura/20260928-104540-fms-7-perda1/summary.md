# Execução `20260928-104540-fms-7-perda1`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 19 sondas): média 4.67 ms, mín 2.79, máx 5.86
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 7063.1 | 180/2310 | 14 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7058.1 | 360/2130 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6986.4 | 367/2120 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7191.1 | 361/2130 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7975.9 | 380/2103 | 5 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9029.8 | 437/2059 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10533.3 | 430/2059 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55837.7 | 2515/14911 | 19 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 10121.3, 15837.3, 25000.0, 34639.8, 45377.5

Tempo por passo: ciclo 1 **230.03 ms**; ciclos 2–5 **200.32 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | 04511541 | 04511541 | ✅ |
| decryptions, whole cell | 798 | 798 | ✅ |
| decryptions, whole cell, cycle 1 | 190 | 190 | ✅ |
| outcome | complete|halt|incomplete | complete | ✅ |
| consistency across nodes | consistente | consistente | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
