# Execução `20260927-144616-fms-7-loss5`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 11 sondas): média 4.03 ms, mín 2.65, máx 5.24
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 292.4 | 219/3846 | 56 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 319.6 | 643/3368 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 302.4 | 653/3426 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 326.5 | 647/3418 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 343.0 | 648/3438 | 9 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 389.4 | 730/3310 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 470.6 | 726/3348 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2443.9 | 4266/24154 | 65 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 20126.2, 39228.3, 61655.0, 90949.2, 117927.6

Tempo por passo: ciclo 1 **457.41 ms**; ciclos 2–5 **555.69 ms**

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
