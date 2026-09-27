# Execução `20260927-210514-fms-4-s5`

- problema `fms`, família `LMOD`, **4 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `10c88d9b`
- RTT de aplicação (nó 1, 20 sondas): média 3.34 ms, mín 2.30, máx 4.38
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 13988.6 | 155/929 | 0 | PASS | não |
| 2 | S2 S6 | 0 | 50/20/10 | 80 | 250 (58) | 17316.6 | 284/800 | 0 | PASS | não |
| 3 | S3 S4 | 0 | 20/0/0 | 110 | 217 (49) | 15019.3 | 320/764 | 0 | PASS | não |
| 4 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8932.1 | 325/759 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55256.6 | 1084/3252 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 5082.5, 8876.7, 12678.0, 16473.4, 20258.5

Tempo por passo: ciclo 1 **115.51 ms**; ciclos 2–5 **86.23 ms**

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
