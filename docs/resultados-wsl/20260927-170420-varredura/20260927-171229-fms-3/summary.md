# Execução `20260927-171229-fms-3`

- problema `fms`, família `LMOD`, **3 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04d74714`
- RTT de aplicação (nó 1, 20 sondas): média 3.08 ms, mín 2.24, máx 4.73
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 | 0 | 60/40/40 | 0 | 302 (62) | 21071.3 | 150/597 | 0 | PASS | não |
| 2 | S3 S4 | 0 | 20/20/10 | 80 | 217 (49) | 15123.9 | 285/462 | 0 | PASS | não |
| 3 | S5 S6 | 0 | 30/0/0 | 110 | 279 (79) | 19485.8 | 312/435 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55681.0 | 747/1494 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 6554.8, 11499.1, 16460.3, 21426.9, 26379.3

Tempo por passo: ciclo 1 **148.97 ms**; ciclos 2–5 **112.64 ms**

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
