# Execução `20260927-150346-fms-7-loss5-fast`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 10 sondas): média 3.26 ms, mín 2.24, máx 3.55
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 54.4 | 207/2005 | 49 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 55.2 | 314/1903 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 51.7 | 320/1876 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 59.2 | 318/1878 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 70.2 | 363/1856 | 8 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 75.9 | 393/1829 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 101.8 | 393/1829 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 468.4 | 2308/13176 | 57 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 3717.6, 5257.7, 7204.8, 9947.4, 13162.1

Tempo por passo: ciclo 1 **84.49 ms**; ciclos 2–5 **53.66 ms**

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
