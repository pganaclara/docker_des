# Execução `20260927-144851-fms-7-wifi`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`, netem `delay 7ms 3ms loss 1%`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 20 sondas): média 20.16 ms, mín 17.76, máx 24.66
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 234.2 | 174/2330 | 16 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 327.4 | 370/2164 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 321.2 | 373/2190 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 343.6 | 371/2183 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 345.9 | 388/2159 | 8 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 418.3 | 455/2109 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 482.1 | 452/2057 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2472.7 | 2583/15192 | 24 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 10177.9, 16045.8, 20179.9, 33010.2, 39790.4

Tempo por passo: ciclo 1 **231.32 ms**; ciclos 2–5 **168.25 ms**

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
