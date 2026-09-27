# Execução `20260927-151028-fms-7-wifi`

- problema `fms`, família `LMOD`, **7 containers**, transporte `multicast`, netem `delay 7ms 3ms loss 1%`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 20 sondas): média 20.30 ms, mín 17.21, máx 24.44
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 218.1 | 172/2111 | 12 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 291.5 | 323/1953 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 291.4 | 325/1979 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 306.1 | 322/1929 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 330.0 | 369/1927 | 1 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 379.2 | 401/1822 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 458.3 | 405/1898 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 2274.6 | 2317/13619 | 13 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 2722.7, 6543.4, 16654.8, 21029.4, 25149.2

Tempo por passo: ciclo 1 **61.88 ms**; ciclos 2–5 **127.42 ms**

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
