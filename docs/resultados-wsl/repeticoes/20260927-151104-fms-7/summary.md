# Execução `20260927-151104-fms-7`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 20 sondas): média 4.95 ms, mín 3.75, máx 9.02
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 107.3 | 159/1636 | 0 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 124.7 | 239/1523 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 109.6 | 242/1566 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 124.3 | 239/1497 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 136.9 | 293/1522 | 0 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 155.3 | 323/1491 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 209.3 | 320/1477 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 967.4 | 1815/10712 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 276.3, 469.8, 676.9, 879.3, 1078.2

Tempo por passo: ciclo 1 **6.28 ms**; ciclos 2–5 **4.56 ms**

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
