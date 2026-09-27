# Execução `20260927-210736-fms-6-s5`

- problema `fms`, família `LMOD`, **6 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `22301a79`
- RTT de aplicação (nó 1, 20 sondas): média 3.19 ms, mín 2.23, máx 3.46
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S2 | 0 | 40/40/40 | 0 | 201 (41) | 13938.3 | 156/1429 | 0 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 6988.6 | 247/1338 | 0 | PASS | não |
| 3 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7128.0 | 247/1338 | 0 | PASS | não |
| 4 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7892.1 | 291/1294 | 0 | PASS | não |
| 5 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10398.5 | 318/1267 | 0 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8932.5 | 326/1259 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55278.0 | 1585/7925 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4169.6, 7517.6, 10887.9, 14227.6, 17575.3

Tempo por passo: ciclo 1 **94.76 ms**; ciclos 2–5 **76.17 ms**

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
