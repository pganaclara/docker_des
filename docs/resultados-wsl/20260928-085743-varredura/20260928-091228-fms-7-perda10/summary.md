# Execução `20260928-091228-fms-7-perda10`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **123 executados**, 97 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 5 sondas): média 4.79 ms, mín 4.12, máx 6.22
- resultado: **incomplete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 1 | 14/23/23 | 0 | 61 (19) | 4241.7 | 557/13775 | 210 | PASS | não |
| 2 | S1 | 1 | 12/0/0 | 46 | 59 (19) | 4098.3 | 2618/12083 | 0 | PASS | não |
| 3 | S2 | 1 | 14/0/0 | 46 | 60 (18) | 4175.0 | 2672/12025 | 0 | PASS | não |
| 4 | S3 | 1 | 10/0/0 | 46 | 59 (21) | 4100.3 | 2592/12115 | 0 | PASS | não |
| 5 | S4 | 1 | 0/10/5 | 46 | 65 (22) | 4525.1 | 2213/12489 | 37 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 61 | 82 (37) | 5715.2 | 2865/11868 | 0 | PASS | não |
| 7 | S6 | 1 | 12/0/0 | 61 | 83 (34) | 5815.7 | 2583/12150 | 0 | PASS | não |
| **total** | | | | | **469 (170)** | 32671.3 | 16100/86505 | 247 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 86489.1, 263100.2, 452186.7, 553520.4, 715268.0

Tempo por passo: ciclo 1 **1965.66 ms**; ciclos 2–5 **3572.61 ms**

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
