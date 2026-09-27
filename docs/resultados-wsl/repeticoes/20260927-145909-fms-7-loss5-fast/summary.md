# Execução `20260927-145909-fms-7-loss5-fast`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 12 sondas): média 4.41 ms, mín 3.29, máx 5.05
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 311.8 | 226/2099 | 64 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 358.1 | 334/2040 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 338.0 | 335/2006 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 360.9 | 337/2020 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 409.7 | 393/1977 | 12 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 456.5 | 421/1887 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 566.4 | 424/1955 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2801.4 | 2470/13984 | 76 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4276.7, 5699.9, 8985.6, 11429.3, 15122.9

Tempo por passo: ciclo 1 **97.20 ms**; ciclos 2–5 **61.63 ms**

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
