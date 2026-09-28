# Execução `20260928-095720-fms-2-perda30`

- problema `fms`, família `LMOD`, **2 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **182 executados**, 38 pulados
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 13 sondas): média 3.85 ms, mín 2.50, máx 5.32
- resultado: **incomplete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 1 | 68/33/33 | 0 | 337 (85) | 23444.8 | 305/785 | 106 | PASS | não |
| 2 | S4 S5 S6 | 1 | 48/0/0 | 66 | 327 (105) | 22847.6 | 1118/213 | 0 | PASS | não |
| **total** | | | | | **664 (190)** | 46292.4 | 1423/998 | 106 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 41052.9, 91080.2, 169101.1, 276577.0, 358158.6

Tempo por passo: ciclo 1 **933.02 ms**; ciclos 2–5 **1801.74 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | edbd7971 | edbd7971 | ✅ |
| outcome | complete|halt|incomplete | incomplete | ✅ |
| consistency across nodes | consistente | consistente | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
