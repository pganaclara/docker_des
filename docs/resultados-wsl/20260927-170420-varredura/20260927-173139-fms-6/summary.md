# Execução `20260927-173139-fms-6`

- problema `fms`, família `LMOD`, **6 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `8d540ec9`
- RTT de aplicação (nó 1, 20 sondas): média 4.63 ms, mín 2.61, máx 6.05
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14100.6 | 156/1446 | 0 | PASS | não |
| 2 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6977.3 | 251/1351 | 0 | PASS | não |
| 3 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7186.4 | 250/1352 | 0 | PASS | não |
| 4 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7975.4 | 296/1306 | 0 | PASS | não |
| 5 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9038.1 | 327/1275 | 0 | PASS | não |
| 6 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10540.6 | 322/1280 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55818.4 | 1602/8010 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4362.6, 7757.9, 11151.7, 14547.0, 17954.3

Tempo por passo: ciclo 1 **99.15 ms**; ciclos 2–5 **77.23 ms**

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
