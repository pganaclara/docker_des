# Execução `20260928-100752-fms-7-perda10`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **184 executados**, 36 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 3 sondas): média 4.39 ms, mín 4.16, máx 4.72
- resultado: **incomplete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 1 | 18/33/33 | 0 | 85 (21) | 5942.1 | 420/9689 | 162 | PASS | não |
| 2 | S1 | 1 | 18/0/0 | 66 | 85 (21) | 5938.0 | 1824/8463 | 0 | PASS | não |
| 3 | S2 | 1 | 18/0/0 | 66 | 84 (20) | 5866.8 | 1817/8465 | 0 | PASS | não |
| 4 | S3 | 1 | 16/0/0 | 66 | 85 (23) | 5943.0 | 1784/8502 | 0 | PASS | não |
| 5 | S4 | 1 | 0/16/8 | 66 | 94 (26) | 6591.7 | 1577/8707 | 32 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 90 | 109 (41) | 7647.9 | 1942/8336 | 0 | PASS | não |
| 7 | S6 | 1 | 24/0/0 | 90 | 124 (38) | 8754.5 | 1832/8383 | 0 | PASS | não |
| **total** | | | | | **666 (190)** | 46684.0 | 11196/60545 | 194 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 80206.4, 140041.8, 205150.5, 314068.5, 457826.3

Tempo por passo: ciclo 1 **1822.87 ms**; ciclos 2–5 **2145.57 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | 04511541 | 04511541 | ✅ |
| outcome | complete|halt|incomplete | incomplete | ✅ |
| consistency across nodes | consistente | consistente | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
