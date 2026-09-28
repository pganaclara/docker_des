# Latência por passo: percentis

Em ms. Amostras agrupadas por cenário (todos os ciclos da fase e todas as repetições). Percentil pelo posto mais próximo; com n < 100 o p99 é praticamente o máximo.

- **local / 2pc / notify**: latência de *decisão* no nó dono do evento (passo homomórfico + espera pelos pares).
- **apply**: passo homomórfico de um participante ao aplicar um evento compartilhado.
- **célula**: intervalo entre a conclusão de um passo e a do seguinte, em qualquer nó, no relógio comum (exige `nodeK.ts.log`).

## `fms-1` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 220 | 302.9 | 141.8 | 646.2 | 849.6 | 1061.2 | 1073.0 |
| local | ciclos 2+ | 880 | 240.6 | 70.4 | 488.5 | 488.8 | 489.4 | 498.2 |

(sem `nodeK.ts.log`: intervalo da célula não disponível para estas execuções)

## `fms-2` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 140 | 116.8 | 69.6 | 277.9 | 278.7 | 348.0 | 348.3 |
| 2pc | ciclo 1 | 40 | 283.8 | 283.7 | 285.2 | 286.9 | 287.4 | 287.4 |
| notify | ciclo 1 | 40 | 306.6 | 280.4 | 487.4 | 490.7 | 492.4 | 492.4 |
| apply | ciclo 1 | 80 | 335.5 | 278.8 | 571.9 | 576.4 | 580.0 | 580.0 |
| local | ciclos 2+ | 560 | 99.5 | 69.7 | 208.7 | 209.1 | 209.8 | 220.7 |
| 2pc | ciclos 2+ | 160 | 283.7 | 283.5 | 285.1 | 285.4 | 290.5 | 296.1 |
| notify | ciclos 2+ | 160 | 280.4 | 280.3 | 281.3 | 281.6 | 288.5 | 294.1 |
| apply | ciclos 2+ | 320 | 208.8 | 208.7 | 209.3 | 209.5 | 217.0 | 220.2 |

(sem `nodeK.ts.log`: intervalo da célula não disponível para estas execuções)

## `fms-3` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.0 | 69.6 | 70.1 | 139.4 | 141.3 | 141.6 |
| 2pc | ciclo 1 | 60 | 167.8 | 213.5 | 215.3 | 215.8 | 216.3 | 216.3 |
| notify | ciclo 1 | 50 | 182.6 | 210.2 | 211.0 | 211.6 | 212.0 | 212.0 |
| apply | ciclo 1 | 190 | 207.0 | 142.0 | 417.8 | 426.6 | 435.9 | 438.2 |
| local | ciclos 2+ | 440 | 69.6 | 69.6 | 69.9 | 70.1 | 70.3 | 70.5 |
| 2pc | ciclos 2+ | 240 | 168.3 | 214.1 | 216.0 | 216.3 | 216.9 | 217.4 |
| notify | ciclos 2+ | 200 | 183.0 | 210.7 | 211.7 | 212.0 | 212.5 | 212.8 |
| apply | ciclos 2+ | 760 | 139.3 | 139.3 | 139.7 | 139.8 | 140.0 | 140.5 |

(sem `nodeK.ts.log`: intervalo da célula não disponível para estas execuções)

## `fms-4` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.2 | 69.7 | 70.1 | 141.8 | 142.1 | 142.5 |
| 2pc | ciclo 1 | 60 | 168.6 | 145.9 | 215.3 | 283.6 | 284.8 | 284.8 |
| notify | ciclo 1 | 50 | 148.1 | 141.2 | 142.2 | 210.7 | 211.4 | 211.4 |
| apply | ciclo 1 | 270 | 153.3 | 139.6 | 226.8 | 352.9 | 357.2 | 358.3 |
| local | ciclos 2+ | 440 | 69.6 | 69.6 | 69.9 | 70.0 | 70.3 | 70.4 |
| 2pc | ciclos 2+ | 240 | 144.8 | 144.7 | 146.1 | 146.4 | 147.0 | 149.9 |
| notify | ciclos 2+ | 200 | 140.9 | 140.9 | 141.6 | 141.8 | 142.0 | 142.3 |
| apply | ciclos 2+ | 1080 | 110.9 | 138.8 | 139.6 | 139.8 | 140.1 | 143.2 |

(sem `nodeK.ts.log`: intervalo da célula não disponível para estas execuções)

## `fms-5` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 75.9 | 69.5 | 70.1 | 139.5 | 141.5 | 141.5 |
| 2pc | ciclo 1 | 60 | 121.7 | 144.3 | 146.2 | 146.4 | 147.5 | 147.5 |
| notify | ciclo 1 | 50 | 126.9 | 140.6 | 141.5 | 141.8 | 143.1 | 143.1 |
| apply | ciclo 1 | 380 | 118.5 | 70.9 | 209.9 | 214.2 | 418.2 | 424.0 |
| local | ciclos 2+ | 440 | 69.7 | 69.6 | 69.9 | 70.0 | 70.3 | 71.0 |
| 2pc | ciclos 2+ | 240 | 122.0 | 144.6 | 146.2 | 146.6 | 147.1 | 147.6 |
| notify | ciclos 2+ | 200 | 127.2 | 141.0 | 141.8 | 142.0 | 142.3 | 142.3 |
| apply | ciclos 2+ | 1520 | 84.4 | 69.8 | 139.5 | 139.7 | 140.0 | 147.2 |

(sem `nodeK.ts.log`: intervalo da célula não disponível para estas execuções)

## `fms-6` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.1 | 69.6 | 70.3 | 141.2 | 141.9 | 142.0 |
| 2pc | ciclo 1 | 60 | 121.8 | 143.9 | 146.2 | 146.9 | 147.6 | 147.6 |
| notify | ciclo 1 | 50 | 127.1 | 140.8 | 141.8 | 141.8 | 142.3 | 142.3 |
| apply | ciclo 1 | 460 | 98.2 | 69.8 | 150.9 | 213.4 | 279.9 | 281.8 |
| local | ciclos 2+ | 440 | 69.6 | 69.6 | 70.0 | 70.1 | 70.3 | 70.5 |
| 2pc | ciclos 2+ | 240 | 122.2 | 144.8 | 146.5 | 146.9 | 148.0 | 148.3 |
| notify | ciclos 2+ | 200 | 127.4 | 141.3 | 142.0 | 142.2 | 142.6 | 144.1 |
| apply | ciclos 2+ | 1840 | 69.8 | 69.8 | 70.0 | 70.2 | 70.5 | 71.7 |

(sem `nodeK.ts.log`: intervalo da célula não disponível para estas execuções)

## `fms-7` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.0 | 69.6 | 70.3 | 140.6 | 141.7 | 141.7 |
| 2pc | ciclo 1 | 60 | 75.5 | 75.5 | 76.9 | 77.7 | 78.1 | 78.1 |
| notify | ciclo 1 | 50 | 71.4 | 71.4 | 71.9 | 72.1 | 72.3 | 72.3 |
| apply | ciclo 1 | 540 | 94.2 | 69.8 | 146.0 | 213.2 | 229.7 | 281.9 |
| local | ciclos 2+ | 440 | 69.6 | 69.6 | 70.0 | 70.0 | 70.1 | 70.3 |
| 2pc | ciclos 2+ | 240 | 75.8 | 75.8 | 77.0 | 77.5 | 78.1 | 78.3 |
| notify | ciclos 2+ | 200 | 71.5 | 71.4 | 72.1 | 72.3 | 72.6 | 72.9 |
| apply | ciclos 2+ | 2160 | 69.8 | 69.8 | 70.1 | 70.2 | 70.7 | 76.1 |

(sem `nodeK.ts.log`: intervalo da célula não disponível para estas execuções)

