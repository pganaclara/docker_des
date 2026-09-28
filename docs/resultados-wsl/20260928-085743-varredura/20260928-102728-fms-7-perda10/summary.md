# Execução `20260928-102728-fms-7-perda10`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **149 executados**, 71 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 7 sondas): média 4.45 ms, mín 3.28, máx 5.36
- resultado: **incomplete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 1 | 14/27/27 | 0 | 69 (15) | 4821.9 | 501/12394 | 191 | PASS | não |
| 2 | S1 | 1 | 16/0/0 | 54 | 71 (15) | 4962.8 | 2317/10758 | 0 | PASS | não |
| 3 | S2 | 1 | 14/0/0 | 54 | 68 (14) | 4748.8 | 2277/10710 | 0 | PASS | não |
| 4 | S3 | 1 | 14/0/0 | 54 | 71 (15) | 4963.3 | 2287/10768 | 0 | PASS | não |
| 5 | S4 | 1 | 0/13/6 | 54 | 76 (14) | 5329.9 | 2033/10995 | 27 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 73 | 93 (24) | 6537.0 | 2530/10613 | 0 | PASS | não |
| 7 | S6 | 1 | 18/0/0 | 73 | 105 (24) | 7447.2 | 2325/10729 | 0 | PASS | não |
| **total** | | | | | **553 (121)** | 38810.9 | 14270/76967 | 218 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 143708.3, 255457.5, 352496.9, 472915.9, 619707.7

Tempo por passo: ciclo 1 **3266.10 ms**; ciclos 2–5 **2704.54 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | 04511541 | 04511541 | ✅ |
| outcome | complete|halt|incomplete | incomplete | ✅ |
| consistency across nodes | consistente | consistente | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
