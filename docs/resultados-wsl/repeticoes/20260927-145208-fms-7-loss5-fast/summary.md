# Execução `20260927-145208-fms-7-loss5-fast`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 11 sondas): média 4.04 ms, mín 2.60, máx 5.27
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 288.2 | 217/2054 | 54 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 319.9 | 325/1967 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 320.9 | 330/1905 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 325.6 | 321/1986 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 363.8 | 387/1923 | 16 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 403.6 | 410/1850 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 487.2 | 412/1899 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2509.2 | 2402/13584 | 70 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 3481.9, 4802.9, 7247.5, 10003.4, 14220.4

Tempo por passo: ciclo 1 **79.13 ms**; ciclos 2–5 **61.01 ms**

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
