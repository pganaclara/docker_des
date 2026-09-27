# Execução `20260927-145947-fms-7-loss5`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 11 sondas): média 4.51 ms, mín 2.51, máx 5.38
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 256.4 | 225/4306 | 65 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 271.2 | 735/3850 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 263.3 | 733/3811 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 273.6 | 741/3875 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 316.1 | 720/3878 | 19 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 343.8 | 832/3784 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 413.8 | 832/3785 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2138.2 | 4818/27289 | 84 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 22747.6, 40088.8, 75422.8, 106871.3, 144680.1

Tempo por passo: ciclo 1 **516.99 ms**; ciclos 2–5 **692.80 ms**

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
