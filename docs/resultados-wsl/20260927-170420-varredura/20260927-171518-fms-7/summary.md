# Execução `20260927-171518-fms-7`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 20 sondas): média 7.62 ms, mín 3.20, máx 65.05
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 7045.3 | 158/1684 | 0 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7038.6 | 251/1593 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6967.1 | 249/1595 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7182.4 | 250/1594 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7969.8 | 290/1553 | 0 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9019.0 | 326/1518 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10552.9 | 320/1524 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55775.1 | 1844/11061 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 3968.0, 6652.3, 9349.7, 12048.6, 14752.0

Tempo por passo: ciclo 1 **90.18 ms**; ciclos 2–5 **61.27 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | 04511541 | 04511541 | ✅ |
| decryptions, whole cell | 798 | 798 | ✅ |
| decryptions, whole cell, cycle 1 | 190 | 190 | ✅ |
| outcome | complete | complete | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
