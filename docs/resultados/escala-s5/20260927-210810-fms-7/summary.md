# Execução `20260927-210810-fms-7`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 20 sondas): média 9.59 ms, mín 2.33, máx 128.86
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 6990.9 | 161/1690 | 0 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 6988.5 | 249/1602 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6918.2 | 250/1601 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7126.6 | 250/1601 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7893.1 | 293/1558 | 0 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8931.0 | 328/1523 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10396.8 | 320/1531 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55245.1 | 1851/11106 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 3848.2, 6482.6, 9110.9, 11743.3, 14381.3

Tempo por passo: ciclo 1 **87.46 ms**; ciclos 2–5 **59.85 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | 04511541 | 04511541 | ✅ |
| decryptions, whole cell | 798 | 798 | ✅ |
| decryptions, whole cell, cycle 1 | 190 | 190 | ✅ |
| outcome | complete | complete | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
