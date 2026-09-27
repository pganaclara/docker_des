# Execução `20260927-205054-fms-5-s5`

- problema `fms`, família `LMOD`, **5 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `81f89049`
- RTT de aplicação (nó 1, 20 sondas): média 3.42 ms, mín 2.45, máx 5.39
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14071.0 | 157/1180 | 0 | PASS | não |
| 2 | S2 S3 | 0 | 40/0/0 | 80 | 203 (43) | 14122.2 | 242/1095 | 0 | PASS | não |
| 3 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7949.2 | 292/1045 | 0 | PASS | não |
| 4 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10497.8 | 318/1019 | 0 | PASS | não |
| 5 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9002.2 | 328/1009 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55642.4 | 1337/5348 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4756.2, 8417.9, 12116.3, 15814.1, 19511.0

Tempo por passo: ciclo 1 **108.10 ms**; ciclos 2–5 **83.83 ms**

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
