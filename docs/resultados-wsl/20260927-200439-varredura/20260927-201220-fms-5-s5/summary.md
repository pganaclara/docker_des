# Execução `20260927-201220-fms-5-s5`

- problema `fms`, família `LMOD`, **5 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `81f89049`
- RTT de aplicação (nó 1, 20 sondas): média 4.47 ms, mín 3.37, máx 9.97
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14079.5 | 154/1180 | 0 | PASS | não |
| 2 | S2 S3 | 0 | 40/0/0 | 80 | 203 (43) | 14126.5 | 245/1089 | 0 | PASS | não |
| 3 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7949.0 | 293/1041 | 0 | PASS | não |
| 4 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10500.6 | 316/1018 | 0 | PASS | não |
| 5 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9004.4 | 326/1008 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55660.0 | 1334/5336 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4764.8, 8456.2, 12151.6, 15830.0, 19522.5

Tempo por passo: ciclo 1 **108.29 ms**; ciclos 2–5 **83.85 ms**

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
