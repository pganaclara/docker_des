# Execução `20260927-150623-fms-7-loss5-fast`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 9 sondas): média 4.20 ms, mín 2.35, máx 5.21
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 303.3 | 230/2181 | 68 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 331.4 | 350/2086 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 341.3 | 347/2088 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 335.2 | 348/2081 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 365.7 | 399/1985 | 11 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 417.2 | 430/1980 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 492.0 | 431/1961 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2586.1 | 2535/14362 | 79 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 3444.4, 5986.2, 9537.5, 12627.3, 16896.2

Tempo por passo: ciclo 1 **78.28 ms**; ciclos 2–5 **76.43 ms**

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
