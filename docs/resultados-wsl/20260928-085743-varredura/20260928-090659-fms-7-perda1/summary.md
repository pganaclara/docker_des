# Execução `20260928-090659-fms-7-perda1`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 19 sondas): média 4.59 ms, mín 2.83, máx 5.91
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 7051.9 | 179/2343 | 16 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7042.4 | 365/2160 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6972.6 | 365/2162 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7184.9 | 359/2146 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7967.2 | 398/2115 | 2 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9028.7 | 442/2084 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10539.5 | 436/2080 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55787.2 | 2544/15090 | 18 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 13141.9, 24769.2, 29803.5, 38779.7, 46748.7

Tempo por passo: ciclo 1 **298.68 ms**; ciclos 2–5 **190.95 ms**

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
