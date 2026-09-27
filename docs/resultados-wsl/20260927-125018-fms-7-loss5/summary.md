# Execução `20260927-125018-fms-7-loss5`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 9 sondas): média 3.44 ms, mín 2.47, máx 3.93
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 169.0 | 244/4717 | 79 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 202.6 | 804/4195 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 196.4 | 809/4196 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 204.9 | 801/4130 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 218.7 | 798/4156 | 10 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 240.2 | 895/4114 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 286.0 | 884/4109 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 1517.8 | 5235/29617 | 89 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 19787.5, 42464.6, 72161.9, 105391.0, 159584.4

Tempo por passo: ciclo 1 **449.72 ms**; ciclos 2–5 **794.30 ms**

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
