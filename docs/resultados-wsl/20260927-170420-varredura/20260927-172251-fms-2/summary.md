# Execução `20260927-172251-fms-2`

- problema `fms`, família `LMOD`, **2 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 20 sondas): média 3.76 ms, mín 2.54, máx 5.30
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 0 | 80/40/40 | 0 | 405 (85) | 28221.5 | 148/230 | 0 | PASS | não |
| 2 | S4 S5 S6 | 0 | 60/0/0 | 80 | 393 (105) | 27429.4 | 230/148 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55650.9 | 378/378 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 8585.3, 15130.6, 21667.1, 28216.8, 34780.0

Tempo por passo: ciclo 1 **195.12 ms**; ciclos 2–5 **148.83 ms**

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
