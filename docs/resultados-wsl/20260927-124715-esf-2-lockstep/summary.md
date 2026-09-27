# Execução `20260927-124715-esf-2-lockstep`

- problema `extended_small_factory`, família `LMOD`, **2 containers**, transporte `multicast`
- 5 ciclos × 6 passos = 30 passos; **30 executados**, 0 pulados
- impressão digital da configuração: `d42d57d1`
- RTT de aplicação (nó 1, 20 sondas): média 4.03 ms, mín 2.24, máx 5.77
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 10/5/5 | 0 | 20 (4) | 23.2 | 63/62 | 0 | PASS | não |
| 2 | S1 | 0 | 10/0/0 | 10 | 20 (4) | 23.1 | 63/63 | 0 | PASS | não |
| **total** | | | | | **40 (8)** | 46.3 | 126/125 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 52.5, 81.7, 109.7, 137.7, 170.0

Tempo por passo: ciclo 1 **8.75 ms**; ciclos 2–5 **4.90 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **PASS**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| decryptions, whole cell, cycle 1 | 8 | 8 | ✅ |
| monolithic cross-check | PASS | PASS | ✅ |
| outcome | complete | complete | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
