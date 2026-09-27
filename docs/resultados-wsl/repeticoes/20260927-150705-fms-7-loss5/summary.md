# Execução `20260927-150705-fms-7-loss5`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 11 sondas): média 3.92 ms, mín 2.75, máx 5.32
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 305.2 | 233/4316 | 72 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 342.0 | 735/3859 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 328.0 | 733/3806 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 356.5 | 735/3875 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 379.2 | 742/3824 | 6 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 421.8 | 818/3792 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 513.3 | 816/3795 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2646.0 | 4812/27267 | 78 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 23697.6, 48521.4, 79354.6, 108104.5, 141929.0

Tempo por passo: ciclo 1 **538.58 ms**; ciclos 2–5 **671.77 ms**

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
