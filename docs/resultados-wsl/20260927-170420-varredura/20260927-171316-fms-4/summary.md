# Execução `20260927-171316-fms-4`

- problema `fms`, família `LMOD`, **4 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `457cc268`
- RTT de aplicação (nó 1, 20 sondas): média 4.51 ms, mín 2.74, máx 5.57
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 | 0 | 40/40/40 | 0 | 202 (42) | 14067.3 | 155/845 | 0 | PASS | não |
| 2 | S2 S3 | 0 | 40/0/0 | 80 | 203 (43) | 14123.8 | 246/754 | 0 | PASS | não |
| 3 | S4 S5 | 0 | 0/20/10 | 80 | 243 (67) | 16952.2 | 284/716 | 0 | PASS | não |
| 4 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10513.3 | 315/685 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55656.6 | 1000/3000 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 5864.3, 9974.3, 14089.4, 18178.3, 22282.1

Tempo por passo: ciclo 1 **133.28 ms**; ciclos 2–5 **93.28 ms**

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
