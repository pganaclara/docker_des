# Execução `20260927-144524-fms-7-loss5-fast`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 13 sondas): média 4.64 ms, mín 3.04, máx 5.78
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 273.9 | 230/2113 | 68 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 313.5 | 334/2019 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 289.5 | 334/2027 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 300.4 | 336/1955 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 366.0 | 392/1942 | 13 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 410.8 | 416/1898 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 504.8 | 415/1951 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2458.9 | 2457/13905 | 81 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4454.1, 6283.2, 9254.6, 11529.7, 15297.4

Tempo por passo: ciclo 1 **101.23 ms**; ciclos 2–5 **61.61 ms**

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
