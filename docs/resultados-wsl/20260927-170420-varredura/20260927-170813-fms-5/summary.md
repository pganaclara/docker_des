# Execução `20260927-170813-fms-5`

- problema `fms`, família `LMOD`, **5 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `6f43d6b9`
- RTT de aplicação (nó 1, 20 sondas): média 3.36 ms, mín 2.38, máx 4.87
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14082.0 | 154/1180 | 0 | PASS | não |
| 2 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6963.7 | 250/1084 | 0 | PASS | não |
| 3 | S3 S4 | 0 | 20/20/10 | 80 | 217 (49) | 15119.5 | 287/1047 | 0 | PASS | não |
| 4 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9002.6 | 325/1009 | 0 | PASS | não |
| 5 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10502.1 | 318/1016 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55669.9 | 1334/5336 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4755.5, 8379.3, 12015.0, 15637.5, 19264.0

Tempo por passo: ciclo 1 **108.08 ms**; ciclos 2–5 **82.43 ms**

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
