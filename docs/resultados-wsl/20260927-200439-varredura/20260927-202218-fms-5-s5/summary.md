# Execução `20260927-202218-fms-5-s5`

- problema `fms`, família `LMOD`, **5 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `81f89049`
- RTT de aplicação (nó 1, 20 sondas): média 4.82 ms, mín 4.20, máx 6.41
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14102.9 | 157/1181 | 0 | PASS | não |
| 2 | S2 S3 | 0 | 40/0/0 | 80 | 203 (43) | 14151.7 | 242/1096 | 0 | PASS | não |
| 3 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7966.3 | 293/1045 | 0 | PASS | não |
| 4 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10525.3 | 318/1020 | 0 | PASS | não |
| 5 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9018.1 | 328/1010 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55764.3 | 1338/5352 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4781.9, 8484.3, 12186.8, 15891.4, 19582.4

Tempo por passo: ciclo 1 **108.68 ms**; ciclos 2–5 **84.09 ms**

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
