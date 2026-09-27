# Execução `20260927-210702-fms-6`

- problema `fms`, família `LMOD`, **6 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `8d540ec9`
- RTT de aplicação (nó 1, 20 sondas): média 2.91 ms, mín 2.18, máx 3.51
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14017.4 | 156/1431 | 0 | PASS | não |
| 2 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6920.5 | 248/1339 | 0 | PASS | não |
| 3 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7128.7 | 247/1340 | 0 | PASS | não |
| 4 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7892.6 | 291/1296 | 0 | PASS | não |
| 5 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8932.1 | 326/1261 | 0 | PASS | não |
| 6 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10430.4 | 319/1268 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55321.7 | 1587/7935 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4241.5, 7573.7, 10913.2, 14261.0, 17609.3

Tempo por passo: ciclo 1 **96.40 ms**; ciclos 2–5 **75.95 ms**

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
