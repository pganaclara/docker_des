# Execução `20260928-100342-fms-7-perda1`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 16 sondas): média 4.72 ms, mín 2.44, máx 16.96
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 7059.6 | 182/2231 | 13 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7052.4 | 347/2074 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6981.4 | 345/2071 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7196.6 | 350/2070 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7980.3 | 377/2032 | 2 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9043.7 | 425/2000 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10567.0 | 414/1997 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55881.0 | 2440/14475 | 15 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 5223.8, 14757.0, 24953.9, 31033.1, 39900.6

Tempo por passo: ciclo 1 **118.72 ms**; ciclos 2–5 **197.03 ms**

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
