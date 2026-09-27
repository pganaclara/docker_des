# Execução `20260927-144135-fms-7-unicast`

- problema `fms`, família `LMOD`, **7 containers**, transporte `unicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 20 sondas): média 3.07 ms, mín 2.33, máx 4.94
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 59.4 | 163/1675 | 0 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 71.5 | 244/1594 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 68.5 | 244/1582 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 70.2 | 246/1592 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 78.4 | 296/1540 | 0 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 92.8 | 324/1514 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 118.5 | 321/1427 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 559.3 | 1838/10924 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 221.8, 398.7, 566.1, 742.2, 924.2

Tempo por passo: ciclo 1 **5.04 ms**; ciclos 2–5 **3.99 ms**

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
