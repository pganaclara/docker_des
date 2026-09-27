# Execução `20260927-172346-fms-3`

- problema `fms`, família `LMOD`, **3 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04d74714`
- RTT de aplicação (nó 1, 20 sondas): média 4.30 ms, mín 2.53, máx 5.98
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 | 0 | 60/40/40 | 0 | 302 (62) | 21052.9 | 150/598 | 0 | PASS | não |
| 2 | S3 S4 | 0 | 20/20/10 | 80 | 217 (49) | 15121.0 | 286/462 | 0 | PASS | não |
| 3 | S5 S6 | 0 | 30/0/0 | 110 | 279 (79) | 19481.9 | 312/436 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55655.8 | 748/1496 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 6560.8, 11503.6, 16451.4, 21391.0, 26338.4

Tempo por passo: ciclo 1 **149.11 ms**; ciclos 2–5 **112.37 ms**

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
