# Execução `20260927-150422-fms-7-loss5`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 8 sondas): média 3.37 ms, mín 3.33, máx 3.42
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 54.1 | 249/4743 | 81 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 55.9 | 799/4210 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 55.4 | 792/4217 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 55.6 | 801/4196 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 66.2 | 827/4179 | 5 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 77.3 | 889/4132 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 100.3 | 889/4132 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 464.8 | 5246/29809 | 86 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 22480.5, 49560.5, 90575.5, 127773.7, 157619.9

Tempo por passo: ciclo 1 **510.92 ms**; ciclos 2–5 **767.84 ms**

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
