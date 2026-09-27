# Execução `20260927-145603-fms-7-wifi`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`, netem `delay 7ms 3ms loss 1%`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 19 sondas): média 20.24 ms, mín 16.76, máx 22.71
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 219.9 | 169/2105 | 10 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 321.9 | 329/1983 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 316.9 | 330/1996 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 315.2 | 328/1968 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 348.7 | 366/1967 | 4 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 405.9 | 410/1840 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 503.4 | 415/1919 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2431.9 | 2347/13778 | 14 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 7206.9, 12848.7, 13691.3, 21053.4, 27012.0

Tempo por passo: ciclo 1 **163.79 ms**; ciclos 2–5 **112.53 ms**

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
