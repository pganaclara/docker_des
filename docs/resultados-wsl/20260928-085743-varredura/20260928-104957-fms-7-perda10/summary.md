# Execução `20260928-104957-fms-7-perda10`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **134 executados**, 86 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 7 sondas): média 4.38 ms, mín 2.94, máx 5.86
- resultado: **incomplete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 1 | 14/24/24 | 0 | 63 (21) | 4417.3 | 529/12813 | 190 | PASS | não |
| 2 | S1 | 1 | 12/0/0 | 48 | 61 (21) | 4265.6 | 2382/11083 | 0 | PASS | não |
| 3 | S2 | 1 | 12/0/0 | 48 | 60 (20) | 4191.7 | 2376/11076 | 0 | PASS | não |
| 4 | S3 | 1 | 12/0/0 | 48 | 63 (23) | 4402.3 | 2374/11060 | 0 | PASS | não |
| 5 | S4 | 1 | 0/12/6 | 48 | 70 (26) | 4913.7 | 2059/11420 | 31 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 66 | 85 (41) | 5976.8 | 2603/10918 | 0 | PASS | não |
| 7 | S6 | 1 | 18/0/0 | 66 | 94 (38) | 6647.1 | 2413/11078 | 0 | PASS | não |
| **total** | | | | | **496 (190)** | 34814.5 | 14736/79448 | 221 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 66619.0, 259348.6, 349958.0, 512384.4, 647453.5

Tempo por passo: ciclo 1 **1514.07 ms**; ciclos 2–5 **3300.20 ms**

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
