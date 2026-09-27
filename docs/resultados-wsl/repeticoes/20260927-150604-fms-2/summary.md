# Execução `20260927-150604-fms-2`

- problema `fms`, família `LMOD`, **2 containers**, transporte `multicast`
- 5 ciclos × 44 passos = 220 passos; **220 executados**, 0 pulados
- impressão digital da configuração: `edbd7971`
- RTT de aplicação (nó 1, 20 sondas): média 4.03 ms, mín 2.66, máx 5.29
- resultado: **complete**

| nó | supervisores | saída | disparou (local/ctrl/unctrl) | aplicou p/ pares | decifrações (ciclo 1) | HE total ms | quadros tx/rx | retx | oráculo | halt |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S0 S1 S2 S3 | 0 | 80/40/40 | 0 | 405 (85) | 216.3 | 150/229 | 0 | PASS | não |
| 2 | S4 S5 S6 | 0 | 60/0/0 | 80 | 393 (105) | 223.4 | 229/149 | 0 | PASS | não |
| **total** | | | | | **798 (190)** | 439.7 | 379/378 | 0 | | |

Fim de cada ciclo no relógio comum (o **último** nó a terminar), ms: 222.8, 356.2, 503.2, 642.9, 780.2

Tempo por passo: ciclo 1 **5.06 ms**; ciclos 2–5 **3.17 ms**

Verificação cruzada com o supervisor MONOLÍTICO: **off**

## Verificações

| verificação | esperado | obtido | |
|---|---|---|---|
| config fingerprint | edbd7971 | edbd7971 | ✅ |
| decryptions per node | 405 393 | 405 393 | ✅ |
| decryptions per node, cycle 1 | 85 105 | 85 105 | ✅ |
| outcome | complete | complete | ✅ |
| same fingerprint on every node | 1 | 1 | ✅ |
| oracle PASS on every node | True | True | ✅ |
| crypto self-test PASS on every node | True | True | ✅ |

**TODAS AS VERIFICAÇÕES PASSARAM**
