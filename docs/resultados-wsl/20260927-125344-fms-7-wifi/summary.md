# Execução `20260927-125344-fms-7-wifi`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`, netem `delay 7ms 3ms loss 1%`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 15 sondas): média 20.41 ms, mín 16.86, máx 24.08
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 170.6 | 190/2839 | 29 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 224.2 | 448/2515 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 199.4 | 449/2558 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 233.2 | 452/2589 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 237.3 | 473/2558 | 6 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 261.4 | 532/2514 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 347.3 | 529/2479 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 1673.4 | 3073/18052 | 35 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 12702.4, 18279.2, 30150.8, 45875.2, 57110.6

Tempo por passo: ciclo 1 **288.69 ms**; ciclos 2–5 **252.32 ms**

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
