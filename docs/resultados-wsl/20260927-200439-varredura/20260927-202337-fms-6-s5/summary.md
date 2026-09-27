# Execução `20260927-202337-fms-6-s5`

- problema `fms`, família `LMOD`, **6 containers**, UDP multicast
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `22301a79`
- RTT de aplicação (nó 1, 20 sondas): média 10.96 ms, mín 3.32, máx 130.28
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S2 | 0 | 40/40/40 | 0 | 201 (41) | 14032.5 | 156/1423 | 0 | PASS | não |
| 2 | S1 | 0 | 20/0/0 | 80 | 101 (21) | 7052.1 | 245/1334 | 0 | PASS | não |
| 3 | S3 | 0 | 20/0/0 | 80 | 103 (23) | 7189.1 | 246/1333 | 0 | PASS | não |
| 4 | S4 | 0 | 0/20/10 | 80 | 114 (26) | 7965.5 | 288/1291 | 0 | PASS | não |
| 5 | S6 | 0 | 30/0/0 | 110 | 150 (38) | 10524.9 | 319/1260 | 0 | PASS | não |
| 6 | S5 | 0 | 0/0/0 | 110 | 129 (41) | 9017.2 | 325/1254 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 55781.3 | 1579/7895 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 4247.2, 7649.7, 11062.0, 14470.4, 17873.8

Tempo por passo: ciclo 1 **96.53 ms**; ciclos 2–5 **77.42 ms**

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
