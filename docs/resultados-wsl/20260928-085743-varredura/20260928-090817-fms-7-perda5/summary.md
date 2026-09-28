# Execução `20260928-090817-fms-7-perda5`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 11 sondas): média 4.51 ms, mín 3.34, máx 5.09
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 7020.4 | 255/5053 | 83 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7035.7 | 864/4477 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6947.4 | 863/4482 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7162.4 | 869/4477 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7945.9 | 856/4504 | 10 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 8995.4 | 934/4403 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10509.6 | 933/4431 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55616.8 | 5574/31827 | 93 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 36649.6, 75292.3, 102164.1, 146517.9, 180668.6

Tempo por passo: ciclo 1 **832.95 ms**; ciclos 2–5 **818.29 ms**

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
