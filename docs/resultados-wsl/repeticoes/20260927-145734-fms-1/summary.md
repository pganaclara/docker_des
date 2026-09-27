# Execução `20260927-145734-fms-1`

- problema `fms`, família `LMOD`, **1 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `3f2beff2`
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 S4 S5 S6 | 0 | 220/0/0 | 0 | 798 (190) | 395.4 | 0/0 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 395.4 | 0/0 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 114.1, 185.5, 258.1, 328.9, 402.0

Tempo por passo: ciclo 1 **2.59 ms**; ciclos 2–5 **1.64 ms**

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
