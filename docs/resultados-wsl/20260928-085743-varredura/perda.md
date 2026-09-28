# Robustez a perda de quadros

Cada nó descarta P % dos quadros que recebe, depois da autenticação (`DES_SIMULATE_LOSS_PCT`), com sorteio novo por execução e por nó. Decifração emulada a 69 ms e *timeouts* do motor (1,5 s) como no ESP32.

## Desfecho

**completa**: os 220 passos; **SAFE HALT**: um COMMIT/NOTIFY esgotou as retransmissões depois do ponto de commit e a célula parou; **incompleta**: terminou com passos pulados (o dono desistiu *antes* do commit, nada foi aplicado).

| nós | perda | execuções | completa | SAFE HALT | incompleta | passos executados | pulados | retransmissões |
|---|---|---|---|---|---|---|---|---|
| 2 | 1 % | 5 | 5 | 0 | 0 | 220.0 ± 0.0 de 220 | 0.0 ± 0.0 | 1.6 ± 1.5 |
| 2 | 5 % | 5 | 5 | 0 | 0 | 220.0 ± 0.0 de 220 | 0.0 ± 0.0 | 15.6 ± 5.1 |
| 2 | 10 % | 5 | 5 | 0 | 0 | 220.0 ± 0.0 de 220 | 0.0 ± 0.0 | 23.8 ± 3.7 |
| 2 | 20 % | 5 | 5 | 0 | 0 | 220.0 ± 0.0 de 220 | 0.0 ± 0.0 | 61.6 ± 10.4 |
| 2 | 30 % | 5 | 0 | 4 | 1 | 62.6 ± 72.2 de 220 | 7.6 ± 17.0 | 36.2 ± 40.9 |
| 7 | 1 % | 5 | 5 | 0 | 0 | 220.0 ± 0.0 de 220 | 0.0 ± 0.0 | 19.0 ± 2.9 |
| 7 | 5 % | 5 | 5 | 0 | 0 | 220.0 ± 0.0 de 220 | 0.0 ± 0.0 | 87.6 ± 4.5 |
| 7 | 10 % | 5 | 0 | 0 | 5 | 148.2 ± 23.1 de 220 | 71.8 ± 23.1 | 218.8 ± 19.0 |

## Segurança (tem de valer em toda execução)

| nós | perda | consistência entre nós | (das quais: 1 evento em voo no SAFE HALT) | oráculo PASS em todo nó | todas as verificações |
|---|---|---|---|---|---|
| 2 | 1 % | 5/5 | 0 | 5/5 | 5/5 |
| 2 | 5 % | 5/5 | 0 | 5/5 | 5/5 |
| 2 | 10 % | 5/5 | 0 | 5/5 | 5/5 |
| 2 | 20 % | 5/5 | 0 | 5/5 | 5/5 |
| 2 | 30 % | 5/5 | 4 | 5/5 | 5/5 |
| 7 | 1 % | 5/5 | 0 | 5/5 | 5/5 |
| 7 | 5 % | 5/5 | 0 | 5/5 | 5/5 |
| 7 | 10 % | 5/5 | 0 | 5/5 | 5/5 |

## Tempo por passo das execuções completas (ms)

Compare com a varredura sem perda: 2 nós ≈ 196 / 149, 7 nós ≈ 90 / 61 ms (ciclo 1 / ciclos 2–5).

| nós | perda | completas | ciclo 1 | ciclos 2–5 |
|---|---|---|---|---|
| 2 | 1 % | 5 | 204.2 ± 13.0 | 162.5 ± 15.5 |
| 2 | 5 % | 5 | 365.0 ± 91.1 | 247.2 ± 34.2 |
| 2 | 10 % | 5 | 334.2 ± 127.2 | 329.0 ± 34.0 |
| 2 | 20 % | 5 | 640.0 ± 147.0 | 605.4 ± 87.4 |
| 2 | 30 % | 0 | — | — |
| 7 | 1 % | 5 | 241.1 ± 83.3 | 201.4 ± 9.9 |
| 7 | 5 % | 5 | 744.1 ± 107.8 | 763.1 ± 62.7 |
| 7 | 10 % | 0 | — | — |

## Motivos de SAFE HALT

- 2 nós, 30 %: COMMIT unacknowledged — a participant may not have applied a shared event
- 2 nós, 30 %: NOTIFY unacknowledged — a participant may have missed an uncontrollable shared event
- 2 nós, 30 %: a peer halted
