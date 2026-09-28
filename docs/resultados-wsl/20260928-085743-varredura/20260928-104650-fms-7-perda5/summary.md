# Execução `20260928-104650-fms-7-perda5`

- problema `fms`, família `LMOD`, **7 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `04511541`
- RTT de aplicação (nó 1, 11 sondas): média 13.30 ms, mín 2.53, máx 110.23
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 | 0 | 20/40/40 | 0 | 101 (21) | 7066.4 | 247/4667 | 77 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7063.7 | 802/4144 | 0 | PASS | não |
| 3 | S2 | 0 | 20/0/0 | 80 | 100 (20) | 6987.5 | 792/4125 | 0 | PASS | não |
| 4 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7198.0 | 791/4157 | 0 | PASS | não |
| 5 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7997.4 | 795/4153 | 9 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9050.9 | 871/4089 | 0 | PASS | não |
| 7 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10585.5 | 864/4100 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55949.4 | 5162/29435 | 86 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 38306.1, 71533.9, 102453.4, 122412.2, 160302.0

Tempo por passo: ciclo 1 **870.59 ms**; ciclos 2–5 **693.16 ms**

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
