# Execução `20260928-095131-fms-2-perda5`

- problema `fms`, família `LMOD`, **2 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 18 sondas): média 3.64 ms, mín 2.33, máx 4.54
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 0 | 80/40/40 | 0 | 405 (85) | 28148.5 | 173/336 | 22 | PASS | não |
| 2 | S4 S5 S6 | 0 | 60/0/0 | 80 | 393 (105) | 27364.8 | 353/157 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55513.3 | 526/493 | 22 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 18443.5, 30337.6, 38582.2, 59775.9, 69318.7

Tempo por passo: ciclo 1 **419.17 ms**; ciclos 2–5 **289.06 ms**

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
