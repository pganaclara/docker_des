# Execução `20260928-093410-fms-7-perda1`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 19 sondas): média 9.85 ms, mín 2.49, máx 112.45
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 7026.3 | 187/2453 | 20 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7020.9 | 392/2255 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6948.8 | 390/2254 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7164.6 | 383/2245 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7938.2 | 404/2205 | 3 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8980.3 | 454/2131 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10476.5 | 461/2184 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55555.6 | 2671/15727 | 23 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 14772.0, 22473.2, 31231.0, 42721.8, 50130.8

Tempo por passo: ciclo 1 **335.73 ms**; ciclos 2–5 **200.90 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | 04511541 | 04511541 | ✅ |
| decryptions, whole cell | 798 | 798 | ✅ |
| decryptions, whole cell, cycle 1 | 190 | 190 | ✅ |
| outcome | complete|halt|incomplete | complete | ✅ |
| consistency across nodes | consistente | consistente | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
