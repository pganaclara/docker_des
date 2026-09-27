# Execução `20260927-150301-fms-7-wifi`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`, netem `delay 7ms 3ms loss 1%`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 20 sondas): média 20.56 ms, mín 16.34, máx 24.36
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 227.8 | 176/2478 | 16 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 320.8 | 387/2212 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 309.5 | 387/2227 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 338.4 | 391/2276 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 353.9 | 398/2238 | 10 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 395.5 | 476/2173 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 496.2 | 478/2188 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2442.1 | 2693/15792 | 26 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 2156.8, 12275.4, 22127.6, 33436.6, 43550.7

Tempo por passo: ciclo 1 **49.02 ms**; ciclos 2–5 **235.19 ms**

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
