# Execução `20260928-104039-fms-2-perda10`

- problema `fms`, família `LMOD`, **2 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 13 sondas): média 3.72 ms, mín 2.64, máx 4.90
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 0 | 80/40/40 | 0 | 405 (85) | 28280.6 | 167/312 | 18 | PASS | não |
| 2 | S4 S5 S6 | 0 | 60/0/0 | 80 | 393 (105) | 27513.6 | 337/152 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55794.2 | 504/464 | 18 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 9293.4, 24579.8, 39215.6, 52577.5, 63866.8

Tempo por passo: ciclo 1 **211.21 ms**; ciclos 2–5 **310.08 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | edbd7971 | edbd7971 | ✅ |
| decryptions, whole cell | 798 | 798 | ✅ |
| decryptions, whole cell, cycle 1 | 190 | 190 | ✅ |
| outcome | complete|halt|incomplete | complete | ✅ |
| consistency across nodes | consistente | consistente | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
