# Execução `20260927-170855-fms-6`

- problema `fms`, família `LMOD`, **6 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `8d540ec9`
- RTT de aplicação (nó 1, 20 sondas): média 4.12 ms, mín 2.42, máx 6.22
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14073.8 | 156/1440 | 0 | PASS | não |
| 2 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6958.5 | 252/1344 | 0 | PASS | não |
| 3 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7177.0 | 250/1346 | 0 | PASS | não |
| 4 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7949.8 | 294/1302 | 0 | PASS | não |
| 5 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9003.2 | 325/1270 | 0 | PASS | não |
| 6 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10508.0 | 319/1277 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55670.3 | 1596/7979 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4327.2, 7697.8, 11068.2, 14464.9, 17865.7

Tempo por passo: ciclo 1 **98.35 ms**; ciclos 2–5 **76.92 ms**

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
