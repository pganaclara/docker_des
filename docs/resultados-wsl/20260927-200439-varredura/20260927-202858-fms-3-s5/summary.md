# Execução `20260927-202858-fms-3-s5`

- problema `fms`, família `LMOD`, **3 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `6d9dd456`
- RTT de aplicação (nó 1, 20 sondas): média 10.69 ms, mín 2.67, máx 135.02
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S2 S6 | 0 | 70/60/50 | 0 | 351 (79) | 24554.1 | 200/652 | 0 | PASS | não |
| 2 | S1 S3 S4 | 0 | 40/0/0 | 110 | 318 (70) | 22154.9 | 321/531 | 0 | PASS | não |
| 3 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9005.2 | 331/521 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55714.2 | 852/1704 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 6363.7, 11582.3, 16821.6, 22054.6, 27268.2

Tempo por passo: ciclo 1 **144.63 ms**; ciclos 2–5 **118.78 ms**

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
