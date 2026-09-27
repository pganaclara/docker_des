# Execução `20260927-201351-fms-6-s5`

- problema `fms`, família `LMOD`, **6 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `22301a79`
- RTT de aplicação (nó 1, 20 sondas): média 11.46 ms, mín 3.18, máx 144.05
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S2 | 0 | 40/40/40 | 0 | 201 (41) | 14017.2 | 156/1445 | 0 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7038.3 | 253/1349 | 0 | PASS | não |
| 3 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7181.1 | 251/1351 | 0 | PASS | não |
| 4 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7955.0 | 295/1307 | 0 | PASS | não |
| 5 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10508.0 | 320/1282 | 0 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9010.6 | 327/1275 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55710.2 | 1602/8009 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4274.7, 7671.4, 11056.3, 14448.8, 17855.8

Tempo por passo: ciclo 1 **97.15 ms**; ciclos 2–5 **77.17 ms**

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
