# Execução `20260928-093932-fms-7-perda10`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **151 executados**, 69 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 6 sondas): média 4.21 ms, mín 3.55, máx 4.67
- resultado: **incomplete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 1 | 14/28/28 | 0 | 71 (17) | 4938.6 | 492/11918 | 190 | PASS | não |
| 2 | S1 | 1 | 14/0/0 | 56 | 71 (17) | 4943.4 | 2240/10335 | 0 | PASS | não |
| 3 | S2 | 1 | 14/0/0 | 56 | 70 (14) | 4866.5 | 2231/10297 | 0 | PASS | não |
| 4 | S3 | 1 | 14/0/0 | 56 | 73 (19) | 5120.6 | 2238/10338 | 0 | PASS | não |
| 5 | S4 | 1 | 0/14/7 | 56 | 81 (19) | 5684.4 | 1885/10595 | 24 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 77 | 92 (30) | 6436.0 | 2415/10165 | 0 | PASS | não |
| 7 | S6 | 1 | 18/0/0 | 77 | 105 (31) | 7350.9 | 2199/10265 | 0 | PASS | não |
| **total** | | | | | **563 (147)** | 39340.4 | 13700/73913 | 214 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 107927.6, 210718.4, 351953.4, 499717.6, 591743.1

Tempo por passo: ciclo 1 **2452.90 ms**; ciclos 2–5 **2748.95 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | 04511541 | 04511541 | ✅ |
| outcome | complete|halt|incomplete | incomplete | ✅ |
| consistency across nodes | consistente | consistente | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
