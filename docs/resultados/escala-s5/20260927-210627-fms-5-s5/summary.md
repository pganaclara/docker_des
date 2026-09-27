# Execução `20260927-210627-fms-5-s5`

- problema `fms`, família `LMOD`, **5 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `81f89049`
- RTT de aplicação (nó 1, 20 sondas): média 3.71 ms, mín 3.29, máx 8.68
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 13985.9 | 154/1173 | 0 | PASS | não |
| 2 | S2 S3 | 0 | 40/0/0 | 80 | 203 (43) | 14048.6 | 242/1085 | 0 | PASS | não |
| 3 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7895.3 | 290/1037 | 0 | PASS | não |
| 4 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10400.5 | 317/1010 | 0 | PASS | não |
| 5 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8933.4 | 324/1003 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55263.7 | 1327/5308 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4667.8, 8309.1, 11951.3, 15590.3, 19238.7

Tempo por passo: ciclo 1 **106.09 ms**; ciclos 2–5 **82.79 ms**

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
