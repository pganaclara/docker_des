# Latência por passo: percentis

Em ms. Amostras agrupadas por cenário (todos os ciclos da fase e todas as repetições). Percentil pelo posto mais próximo; com n < 100 o p99 é praticamente o máximo.

- **local / 2pc / notify**: latência de *decisão* no nó dono do evento (passo homomórfico + espera pelos pares).
- **apply**: passo homomórfico de um participante ao aplicar um evento compartilhado.
- **célula**: intervalo entre a conclusão de um passo e a do seguinte, em qualquer nó, no relógio comum (exige `nodeK.ts.log`). Linhas com carimbo fora de ordem no próprio nó (relógio do host saltou) são descartadas, junto com os intervalos que as atravessariam.

## `fms-1-nativo` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 220 | 304.0 | 142.9 | 652.4 | 841.2 | 1058.5 | 1094.0 |
| local | ciclos 2+ | 880 | 240.8 | 70.5 | 489.4 | 489.7 | 490.2 | 490.6 |

(sem `nodeK.ts.log`: intervalo da célula não disponível para estas execuções)

## `fms-1-ponte` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 220 | 303.2 | 142.7 | 649.5 | 839.2 | 1072.5 | 1074.9 |
| célula | ciclo 1 | 201 | 309.8 | 210.1 | 651.7 | 840.3 | 1072.3 | 1075.2 |
| local | ciclos 2+ | 880 | 240.8 | 70.8 | 489.4 | 489.6 | 490.2 | 490.7 |
| célula | ciclos 2+ | 757 | 238.6 | 70.9 | 489.6 | 490.0 | 491.0 | 509.1 |

## `fms-2-host` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 140 | 117.3 | 69.9 | 279.2 | 280.2 | 349.5 | 350.3 |
| 2pc | ciclo 1 | 40 | 285.1 | 284.9 | 286.5 | 286.9 | 289.2 | 289.2 |
| notify | ciclo 1 | 40 | 307.6 | 281.3 | 492.3 | 492.8 | 493.1 | 493.1 |
| apply | ciclo 1 | 80 | 338.5 | 279.3 | 578.2 | 581.5 | 583.7 | 583.7 |
| célula | ciclo 1 | 203 | 191.7 | 141.4 | 372.3 | 577.7 | 589.9 | 590.6 |
| local | ciclos 2+ | 560 | 99.6 | 69.8 | 209.3 | 209.5 | 209.9 | 210.1 |
| 2pc | ciclos 2+ | 160 | 284.2 | 284.5 | 286.0 | 286.4 | 286.7 | 287.2 |
| notify | ciclos 2+ | 160 | 280.7 | 281.1 | 281.8 | 282.1 | 282.4 | 283.2 |
| apply | ciclos 2+ | 320 | 208.9 | 209.0 | 209.5 | 209.7 | 210.0 | 210.8 |
| célula | ciclos 2+ | 758 | 149.0 | 70.6 | 285.1 | 285.9 | 287.5 | 289.5 |

## `fms-2-nativo` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 140 | 117.0 | 69.8 | 278.8 | 279.4 | 349.2 | 349.3 |
| 2pc | ciclo 1 | 40 | 284.0 | 284.4 | 286.5 | 287.1 | 287.3 | 287.3 |
| notify | ciclo 1 | 40 | 306.7 | 280.9 | 485.9 | 492.1 | 492.9 | 492.9 |
| apply | ciclo 1 | 80 | 336.3 | 279.2 | 572.8 | 580.1 | 582.7 | 582.7 |
| local | ciclos 2+ | 560 | 99.5 | 69.8 | 209.1 | 209.5 | 210.0 | 210.5 |
| 2pc | ciclos 2+ | 160 | 284.0 | 284.6 | 286.0 | 286.3 | 287.0 | 287.3 |
| notify | ciclos 2+ | 160 | 280.4 | 280.8 | 281.7 | 282.0 | 282.4 | 282.5 |
| apply | ciclos 2+ | 320 | 208.8 | 209.0 | 209.5 | 209.6 | 210.1 | 210.4 |

(sem `nodeK.ts.log`: intervalo da célula não disponível para estas execuções)

## `fms-2-ponte` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 140 | 117.1 | 69.8 | 278.6 | 279.9 | 349.7 | 350.8 |
| 2pc | ciclo 1 | 40 | 284.7 | 284.5 | 286.9 | 288.3 | 288.9 | 288.9 |
| notify | ciclo 1 | 40 | 307.2 | 281.4 | 486.3 | 492.1 | 493.1 | 493.1 |
| apply | ciclo 1 | 80 | 337.7 | 279.3 | 579.5 | 580.6 | 582.9 | 582.9 |
| célula | ciclo 1 | 185 | 202.3 | 277.5 | 372.3 | 581.2 | 591.7 | 593.5 |
| local | ciclos 2+ | 560 | 99.7 | 69.9 | 209.2 | 209.6 | 210.0 | 210.4 |
| 2pc | ciclos 2+ | 160 | 284.9 | 285.1 | 286.3 | 286.7 | 287.2 | 287.2 |
| notify | ciclos 2+ | 160 | 281.1 | 281.1 | 281.9 | 282.0 | 282.5 | 282.6 |
| apply | ciclos 2+ | 320 | 209.0 | 209.0 | 209.4 | 209.5 | 209.8 | 210.0 |
| célula | ciclos 2+ | 717 | 149.4 | 70.6 | 285.8 | 286.5 | 289.2 | 293.5 |

## `fms-4-host` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.0 | 69.7 | 70.1 | 140.4 | 141.4 | 141.4 |
| 2pc | ciclo 1 | 60 | 167.9 | 145.7 | 215.3 | 281.5 | 285.3 | 285.3 |
| notify | ciclo 1 | 50 | 147.8 | 141.3 | 142.1 | 211.3 | 212.0 | 212.0 |
| apply | ciclo 1 | 270 | 152.6 | 139.4 | 223.0 | 350.1 | 357.4 | 358.0 |
| célula | ciclo 1 | 200 | 125.6 | 139.9 | 221.5 | 360.1 | 366.6 | 367.1 |
| local | ciclos 2+ | 440 | 69.6 | 69.6 | 70.0 | 70.0 | 70.1 | 70.2 |
| 2pc | ciclos 2+ | 240 | 144.7 | 145.1 | 146.3 | 146.4 | 147.0 | 147.4 |
| notify | ciclos 2+ | 200 | 140.9 | 141.2 | 141.7 | 141.8 | 142.0 | 142.1 |
| apply | ciclos 2+ | 1080 | 110.9 | 138.4 | 139.6 | 139.8 | 140.0 | 141.6 |
| célula | ciclos 2+ | 793 | 95.1 | 72.6 | 147.3 | 148.3 | 150.3 | 151.6 |

## `fms-4-nativo` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.1 | 69.7 | 70.2 | 141.1 | 141.5 | 142.0 |
| 2pc | ciclo 1 | 60 | 168.0 | 145.8 | 215.8 | 282.4 | 285.5 | 285.5 |
| notify | ciclo 1 | 50 | 147.8 | 141.2 | 142.2 | 210.3 | 211.4 | 211.4 |
| apply | ciclo 1 | 270 | 152.7 | 139.4 | 223.0 | 349.6 | 356.4 | 356.9 |
| local | ciclos 2+ | 440 | 69.6 | 69.6 | 70.0 | 70.1 | 70.4 | 72.7 |
| 2pc | ciclos 2+ | 240 | 144.7 | 145.1 | 146.4 | 146.6 | 147.1 | 147.2 |
| notify | ciclos 2+ | 200 | 141.0 | 141.1 | 141.6 | 141.7 | 142.2 | 156.8 |
| apply | ciclos 2+ | 1080 | 110.8 | 138.4 | 139.6 | 139.7 | 139.9 | 148.3 |

(sem `nodeK.ts.log`: intervalo da célula não disponível para estas execuções)

## `fms-4-ponte` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.1 | 69.6 | 70.2 | 141.5 | 142.1 | 142.2 |
| 2pc | ciclo 1 | 60 | 168.0 | 145.9 | 215.8 | 281.6 | 286.3 | 286.3 |
| notify | ciclo 1 | 50 | 147.9 | 141.3 | 142.4 | 210.5 | 211.3 | 211.3 |
| apply | ciclo 1 | 270 | 152.7 | 139.4 | 222.8 | 350.0 | 356.9 | 358.6 |
| célula | ciclo 1 | 192 | 131.8 | 141.8 | 223.1 | 359.6 | 368.6 | 372.4 |
| local | ciclos 2+ | 440 | 69.6 | 69.6 | 69.9 | 70.0 | 70.2 | 76.0 |
| 2pc | ciclos 2+ | 240 | 144.6 | 144.8 | 146.2 | 146.6 | 147.1 | 151.4 |
| notify | ciclos 2+ | 200 | 140.8 | 141.1 | 141.7 | 141.9 | 142.2 | 142.6 |
| apply | ciclos 2+ | 1080 | 110.8 | 138.4 | 139.6 | 139.7 | 139.9 | 140.4 |
| célula | ciclos 2+ | 821 | 94.0 | 72.2 | 147.2 | 148.3 | 151.1 | 153.6 |

## `fms-7-host` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.1 | 69.6 | 70.3 | 141.1 | 142.0 | 142.1 |
| 2pc | ciclo 1 | 60 | 75.3 | 75.4 | 76.6 | 76.8 | 77.0 | 77.0 |
| notify | ciclo 1 | 50 | 71.3 | 71.3 | 71.9 | 72.2 | 72.3 | 72.3 |
| apply | ciclo 1 | 540 | 94.1 | 69.8 | 145.1 | 212.8 | 229.2 | 282.0 |
| célula | ciclo 1 | 199 | 98.8 | 72.1 | 162.9 | 234.5 | 638.6 | 644.7 |
| local | ciclos 2+ | 440 | 69.7 | 69.7 | 70.0 | 70.1 | 70.4 | 77.4 |
| 2pc | ciclos 2+ | 240 | 75.3 | 75.5 | 76.4 | 76.9 | 77.6 | 83.6 |
| notify | ciclos 2+ | 200 | 71.3 | 71.4 | 71.9 | 72.0 | 72.3 | 72.5 |
| apply | ciclos 2+ | 2160 | 69.7 | 69.8 | 70.1 | 70.1 | 70.4 | 72.7 |
| célula | ciclos 2+ | 819 | 62.0 | 71.8 | 78.8 | 80.4 | 81.6 | 87.9 |

## `fms-7-nativo` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.1 | 69.6 | 70.3 | 141.4 | 142.0 | 142.1 |
| 2pc | ciclo 1 | 60 | 75.4 | 75.7 | 76.5 | 76.9 | 77.2 | 77.2 |
| notify | ciclo 1 | 50 | 71.2 | 71.3 | 71.7 | 71.9 | 72.0 | 72.0 |
| apply | ciclo 1 | 540 | 94.1 | 69.8 | 145.3 | 213.0 | 227.9 | 282.0 |
| local | ciclos 2+ | 440 | 69.6 | 69.7 | 70.0 | 70.1 | 70.3 | 70.6 |
| 2pc | ciclos 2+ | 240 | 75.3 | 75.6 | 76.6 | 76.8 | 77.7 | 82.0 |
| notify | ciclos 2+ | 200 | 71.3 | 71.4 | 71.9 | 72.0 | 72.3 | 72.6 |
| apply | ciclos 2+ | 2160 | 69.7 | 69.7 | 70.0 | 70.1 | 70.3 | 71.1 |

(sem `nodeK.ts.log`: intervalo da célula não disponível para estas execuções)

## `fms-7-ponte` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.0 | 69.6 | 70.3 | 141.4 | 142.6 | 142.7 |
| 2pc | ciclo 1 | 60 | 75.3 | 75.4 | 77.0 | 77.1 | 78.0 | 78.0 |
| notify | ciclo 1 | 50 | 71.2 | 71.4 | 71.8 | 72.1 | 72.3 | 72.3 |
| apply | ciclo 1 | 540 | 93.8 | 69.8 | 145.4 | 210.4 | 233.6 | 282.4 |
| célula | ciclo 1 | 205 | 96.6 | 72.6 | 160.1 | 221.7 | 599.2 | 649.2 |
| local | ciclos 2+ | 440 | 69.5 | 69.6 | 69.9 | 70.0 | 70.2 | 70.4 |
| 2pc | ciclos 2+ | 240 | 75.2 | 75.4 | 76.6 | 77.2 | 77.5 | 77.6 |
| notify | ciclos 2+ | 200 | 71.3 | 71.4 | 72.0 | 72.2 | 72.6 | 72.8 |
| apply | ciclos 2+ | 2160 | 69.6 | 69.7 | 70.0 | 70.1 | 70.4 | 71.4 |
| célula | ciclos 2+ | 738 | 62.2 | 71.9 | 79.3 | 80.5 | 82.2 | 84.7 |

Carimbos inválidos descartados: 356 conclusões de passo, 7 ciclos inteiros cujo início ou fim nos carimbos diverge do relógio do motor em mais de 200 ms, 521 intervalos da célula (em todas as execuções).

