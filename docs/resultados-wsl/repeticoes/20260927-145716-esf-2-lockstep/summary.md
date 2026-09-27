# Execução `20260927-145716-esf-2-lockstep`

- problema `extended_small_factory`, família `LMOD`, **2 containers**, transporte `multicast`
- 5 ciclos × 6 passos = 30 passos; **30 executados**, 0 pulados
- impressão digital da configuração: `d42d57d1`
- RTT de aplicação (nó 1, 20 sondas): média 4.22 ms, mín 2.25, máx 6.41
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 10/5/5 | 0 | 20 (4) | 26.8 | 63/62 | 0 | PASS | não |
| 2 | S1 | 0 | 10/0/0 | 10 | 20 (4) | 24.7 | 63/63 | 0 | PASS | não |
| **total** | | | | | **40 (8)** | 51.5 | 126/125 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 51.4, 81.7, 107.6, 132.4, 160.6

Tempo por passo: ciclo 1 **8.57 ms**; ciclos 2–5 **4.55 ms**

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
