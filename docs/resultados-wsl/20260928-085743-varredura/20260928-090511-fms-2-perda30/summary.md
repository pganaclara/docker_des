# Execução `20260928-090511-fms-2-perda30`

- problema `fms`, família `LMOD`, **2 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **78 executados**, 0 pulados, 142 não alcançados (execução interrompida)
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 10 sondas): média 4.20 ms, mín 2.65, máx 4.89
- resultado: **halt** — SAFE HALT nos nós [1, 2]

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 2 | 29/14/13 | 0 | 142 (85) | 9907.9 | 125/237 | 38 | PASS | **NOTIFY unacknowledged — a participant may have missed an uncontrollable shared event** |
| 2 | S4 S5 S6 | 2 | 22/0/0 | 28 | 159 (105) | 11202.9 | 340/89 | 0 | PASS | **a peer halted** |
| **total** | | | | | **301 (190)** | 21110.8 | 465/326 | 38 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 42611.2

Tempo por passo: ciclo 1 **968.44 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | edbd7971 | edbd7971 | ✅ |
| outcome | complete|halt|incomplete | halt | ✅ |
| consistency across nodes | consistente | consistente até o SAFE HALT (1 evento em voo: 1-2) | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
