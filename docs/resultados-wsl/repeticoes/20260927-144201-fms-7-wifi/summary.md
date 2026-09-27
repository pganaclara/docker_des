# Execução `20260927-144201-fms-7-wifi`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`, netem `delay 7ms 3ms loss 1%`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 19 sondas): média 20.01 ms, mín 14.40, máx 23.21
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 201.5 | 183/2452 | 22 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 271.3 | 396/2300 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 266.8 | 394/2297 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 276.0 | 392/2288 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 302.1 | 421/2246 | 4 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 349.3 | 473/2222 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 426.5 | 465/2143 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2093.5 | 2724/15948 | 26 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 13182.7, 21794.0, 27319.8, 35447.1, 42762.3

Tempo por passo: ciclo 1 **299.61 ms**; ciclos 2–5 **168.07 ms**

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
