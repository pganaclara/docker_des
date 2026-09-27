# Execução `20260927-201046-fms-4-s5`

- problema `fms`, família `LMOD`, **4 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `10c88d9b`
- RTT de aplicação (nó 1, 20 sondas): média 4.32 ms, mín 3.07, máx 5.06
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14069.4 | 157/933 | 0 | PASS | não |
| 2 | S2 S6 | 0 | 50/20/10 | 80 | 250 (58) | 17471.1 | 284/806 | 0 | PASS | não |
| 3 | S3 S4 | 0 | 20/0/0 | 110 | 217 (49) | 15110.1 | 321/769 | 0 | PASS | não |
| 4 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9003.6 | 328/762 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55654.2 | 1090/3270 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 5214.8, 9024.6, 12864.6, 16712.5, 20544.0

Tempo por passo: ciclo 1 **118.52 ms**; ciclos 2–5 **87.10 ms**

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
