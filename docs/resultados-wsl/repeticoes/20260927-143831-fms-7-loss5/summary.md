# Execução `20260927-143831-fms-7-loss5`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 10 sondas): média 2.93 ms, mín 2.27, máx 3.81
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 67.4 | 239/4618 | 67 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 85.9 | 780/4065 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 86.1 | 789/4091 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 94.1 | 778/4024 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 100.6 | 763/4100 | 19 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 111.4 | 881/4000 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 142.7 | 875/3982 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 688.2 | 5105/28880 | 86 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 25047.0, 51399.7, 85481.0, 126765.2, 156682.7

Tempo por passo: ciclo 1 **569.25 ms**; ciclos 2–5 **747.93 ms**

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
