# Execução `20260927-205213-fms-6-s5`

- problema `fms`, família `LMOD`, **6 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `22301a79`
- RTT de aplicação (nó 1, 20 sondas): média 10.58 ms, mín 2.60, máx 135.41
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S2 | 0 | 40/40/40 | 0 | 201 (41) | 14032.3 | 157/1441 | 0 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7044.2 | 251/1347 | 0 | PASS | não |
| 3 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7181.1 | 250/1348 | 0 | PASS | não |
| 4 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7956.3 | 292/1306 | 0 | PASS | não |
| 5 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10485.2 | 318/1280 | 0 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9003.9 | 330/1268 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55703.0 | 1598/7990 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4229.2, 7635.7, 11051.9, 14459.4, 17859.0

Tempo por passo: ciclo 1 **96.12 ms**; ciclos 2–5 **77.44 ms**

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
