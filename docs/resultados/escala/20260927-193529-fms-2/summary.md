# Execução `20260927-193529-fms-2`

- problema `fms`, família `LMOD`, **2 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 20 sondas): média 2.34 ms, mín 2.19, máx 3.36
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 0 | 80/40/40 | 0 | 405 (85) | 28030.6 | 149/230 | 0 | PASS | não |
| 2 | S4 S5 S6 | 0 | 60/0/0 | 80 | 393 (105) | 27223.5 | 230/149 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55254.1 | 379/379 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 8481.0, 14971.7, 21461.3, 27952.0, 34445.9

Tempo por passo: ciclo 1 **192.75 ms**; ciclos 2–5 **147.53 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | edbd7971 | edbd7971 | ✅ |
| decryptions per node | 405 393 | 405 393 | ✅ |
| decryptions per node, cycle 1 | 85 105 | 85 105 | ✅ |
| decryptions, whole cell | 798 | 798 | ✅ |
| decryptions, whole cell, cycle 1 | 190 | 190 | ✅ |
| outcome | complete | complete | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
