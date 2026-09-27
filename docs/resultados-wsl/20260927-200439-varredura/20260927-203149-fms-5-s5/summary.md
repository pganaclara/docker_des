# Execução `20260927-203149-fms-5-s5`

- problema `fms`, família `LMOD`, **5 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `81f89049`
- RTT de aplicação (nó 1, 20 sondas): média 4.83 ms, mín 4.21, máx 5.95
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14090.0 | 154/1177 | 0 | PASS | não |
| 2 | S2 S3 | 0 | 40/0/0 | 80 | 203 (43) | 14139.1 | 244/1087 | 0 | PASS | não |
| 3 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7954.0 | 290/1041 | 0 | PASS | não |
| 4 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10494.9 | 317/1014 | 0 | PASS | não |
| 5 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9003.6 | 326/1005 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55681.6 | 1331/5324 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4744.8, 8440.1, 12137.1, 15835.0, 19521.9

Tempo por passo: ciclo 1 **107.84 ms**; ciclos 2–5 **83.96 ms**

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
