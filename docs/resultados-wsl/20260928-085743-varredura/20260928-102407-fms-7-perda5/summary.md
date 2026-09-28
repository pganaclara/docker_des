# Execução `20260928-102407-fms-7-perda5`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 12 sondas): média 4.48 ms, mín 3.30, máx 5.68
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 7058.7 | 239/4827 | 77 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7061.0 | 833/4305 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6978.0 | 838/4272 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7194.9 | 823/4312 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7975.7 | 816/4323 | 13 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9041.3 | 907/4234 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10549.4 | 910/4226 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55859.0 | 5366/30499 | 90 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 28959.1, 74055.2, 109239.4, 134877.3, 174728.4

Tempo por passo: ciclo 1 **658.16 ms**; ciclos 2–5 **828.23 ms**

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
