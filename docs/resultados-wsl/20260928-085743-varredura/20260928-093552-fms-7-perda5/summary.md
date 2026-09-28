# Execução `20260928-093552-fms-7-perda5`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 13 sondas): média 4.07 ms, mín 3.49, máx 4.78
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 7028.1 | 247/4644 | 72 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7019.7 | 778/4084 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6949.0 | 791/4115 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7157.8 | 782/4097 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7931.7 | 802/4114 | 9 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8980.2 | 874/4045 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10475.0 | 859/4047 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55541.5 | 5133/29146 | 81 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 27320.9, 66978.0, 102328.4, 131868.9, 163135.7

Tempo por passo: ciclo 1 **620.93 ms**; ciclos 2–5 **771.68 ms**

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
