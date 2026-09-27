# Execução `20260927-124920-fms-7-loss5-fast`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 10 sondas): média 4.22 ms, mín 3.01, máx 5.47
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 209.9 | 239/2191 | 69 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 241.7 | 349/2070 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 227.4 | 339/2027 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 254.8 | 339/2048 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 289.8 | 408/2034 | 11 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 332.9 | 432/2004 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 428.1 | 432/1993 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 1984.6 | 2538/14367 | 80 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 3448.5, 5429.0, 8115.0, 10805.1, 15581.5

Tempo por passo: ciclo 1 **78.38 ms**; ciclos 2–5 **68.94 ms**

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
