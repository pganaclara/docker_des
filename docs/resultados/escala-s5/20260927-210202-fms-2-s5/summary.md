# Execução `20260927-210202-fms-2-s5`

- problema `fms`, família `LMOD`, **2 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `52c9a503`
- RTT de aplicação (nó 1, 20 sondas): média 2.57 ms, mín 2.19, máx 3.42
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 S4 S6 | 0 | 110/60/50 | 0 | 669 (149) | 46332.3 | 198/421 | 0 | PASS | não |
| 2 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8935.5 | 421/198 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55267.8 | 619/619 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 10473.2, 19532.8, 28592.0, 37654.0, 46716.8

Tempo por passo: ciclo 1 **238.03 ms**; ciclos 2–5 **205.93 ms**

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
