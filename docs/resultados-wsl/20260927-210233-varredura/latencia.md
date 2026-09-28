# Latência por passo: percentis

Em ms. Amostras agrupadas por cenário (todos os ciclos da fase e todas as repetições). Percentil pelo posto mais próximo; com n < 100 o p99 é praticamente o máximo.

- **local / 2pc / notify**: latência de *decisão* no nó dono do evento (passo homomórfico + espera pelos pares).
- **apply**: passo homomórfico de um participante ao aplicar um evento compartilhado.
- **célula**: intervalo entre a conclusão de um passo e a do seguinte, em qualquer nó, no relógio comum (exige `nodeK.ts.log`). Linhas com carimbo fora de ordem no próprio nó (relógio do host saltou) são descartadas, junto com os intervalos que as atravessariam.

## `fms-1` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 220 | 304.0 | 142.8 | 648.5 | 857.6 | 1064.4 | 1071.2 |
| célula | ciclo 1 | 195 | 304.0 | 209.6 | 648.9 | 857.0 | 1062.1 | 1070.5 |
| local | ciclos 2+ | 880 | 241.2 | 70.8 | 489.5 | 489.8 | 490.3 | 491.3 |
| célula | ciclos 2+ | 822 | 237.1 | 70.8 | 489.9 | 490.2 | 490.7 | 497.9 |

## `fms-2` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 140 | 118.0 | 69.9 | 279.5 | 294.7 | 348.7 | 354.7 |
| 2pc | ciclo 1 | 40 | 285.9 | 284.9 | 287.5 | 297.4 | 299.0 | 299.0 |
| notify | ciclo 1 | 40 | 308.7 | 281.3 | 491.2 | 492.6 | 493.3 | 493.3 |
| apply | ciclo 1 | 80 | 340.0 | 279.4 | 578.4 | 581.3 | 604.8 | 604.8 |
| célula | ciclo 1 | 149 | 193.1 | 140.0 | 423.5 | 583.6 | 592.0 | 617.3 |
| local | ciclos 2+ | 560 | 99.6 | 69.8 | 209.2 | 209.4 | 209.9 | 210.3 |
| 2pc | ciclos 2+ | 160 | 284.5 | 284.6 | 286.1 | 286.4 | 287.2 | 287.6 |
| notify | ciclos 2+ | 160 | 280.9 | 281.1 | 281.8 | 282.0 | 282.7 | 282.9 |
| apply | ciclos 2+ | 320 | 208.9 | 209.0 | 209.5 | 209.6 | 209.8 | 210.2 |
| célula | ciclos 2+ | 599 | 151.7 | 70.5 | 285.5 | 286.3 | 288.3 | 289.3 |

## `fms-3` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.2 | 69.7 | 70.2 | 141.0 | 141.6 | 142.2 |
| 2pc | ciclo 1 | 60 | 168.5 | 214.4 | 216.2 | 216.4 | 216.8 | 216.8 |
| notify | ciclo 1 | 50 | 183.0 | 210.7 | 211.7 | 211.8 | 212.5 | 212.5 |
| apply | ciclo 1 | 190 | 208.2 | 144.3 | 417.8 | 432.2 | 437.6 | 438.2 |
| célula | ciclo 1 | 160 | 138.0 | 70.3 | 353.4 | 427.7 | 447.6 | 449.4 |
| local | ciclos 2+ | 440 | 69.6 | 69.6 | 69.9 | 70.0 | 70.2 | 70.3 |
| 2pc | ciclos 2+ | 240 | 168.1 | 213.8 | 215.9 | 216.3 | 216.9 | 217.3 |
| notify | ciclos 2+ | 200 | 182.9 | 210.8 | 211.8 | 212.0 | 212.3 | 213.0 |
| apply | ciclos 2+ | 760 | 139.2 | 139.3 | 139.7 | 139.8 | 140.0 | 140.5 |
| célula | ciclos 2+ | 741 | 110.7 | 70.0 | 216.9 | 238.1 | 289.1 | 292.8 |

## `fms-4` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.2 | 69.7 | 70.4 | 141.0 | 141.7 | 142.3 |
| 2pc | ciclo 1 | 60 | 168.7 | 145.8 | 216.0 | 285.8 | 286.2 | 286.2 |
| notify | ciclo 1 | 50 | 148.4 | 141.4 | 142.3 | 211.5 | 211.7 | 211.7 |
| apply | ciclo 1 | 270 | 152.9 | 139.5 | 223.3 | 353.3 | 356.3 | 357.0 |
| célula | ciclo 1 | 198 | 127.6 | 141.5 | 220.9 | 362.2 | 365.2 | 367.2 |
| local | ciclos 2+ | 440 | 69.7 | 69.7 | 70.0 | 70.1 | 70.3 | 76.8 |
| 2pc | ciclos 2+ | 240 | 145.2 | 145.3 | 146.3 | 146.6 | 147.4 | 147.7 |
| notify | ciclos 2+ | 200 | 141.2 | 141.3 | 141.8 | 142.0 | 142.3 | 142.3 |
| apply | ciclos 2+ | 1080 | 111.0 | 139.0 | 139.6 | 139.8 | 140.0 | 144.6 |
| célula | ciclos 2+ | 797 | 96.1 | 73.4 | 147.7 | 148.7 | 151.4 | 152.8 |

## `fms-5` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.7 | 69.8 | 75.1 | 141.7 | 144.8 | 150.1 |
| 2pc | ciclo 1 | 60 | 122.3 | 145.1 | 146.2 | 146.9 | 149.0 | 149.0 |
| notify | ciclo 1 | 50 | 127.6 | 141.1 | 142.0 | 145.0 | 147.1 | 147.1 |
| apply | ciclo 1 | 380 | 119.3 | 73.9 | 212.1 | 220.0 | 421.2 | 435.5 |
| célula | ciclo 1 | 183 | 108.4 | 75.4 | 224.5 | 248.1 | 362.6 | 369.9 |
| local | ciclos 2+ | 440 | 69.7 | 69.7 | 70.0 | 70.1 | 70.3 | 70.5 |
| 2pc | ciclos 2+ | 240 | 122.2 | 145.1 | 146.3 | 146.5 | 147.3 | 148.1 |
| notify | ciclos 2+ | 200 | 127.3 | 141.2 | 141.8 | 142.2 | 142.4 | 142.9 |
| apply | ciclos 2+ | 1520 | 84.4 | 69.8 | 139.5 | 139.6 | 139.9 | 141.7 |
| célula | ciclos 2+ | 820 | 83.1 | 70.6 | 147.9 | 149.8 | 151.3 | 152.8 |

## `fms-6` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.2 | 69.7 | 70.2 | 141.2 | 141.7 | 141.8 |
| 2pc | ciclo 1 | 60 | 122.4 | 145.5 | 146.7 | 147.0 | 147.4 | 147.4 |
| notify | ciclo 1 | 50 | 127.4 | 141.3 | 142.0 | 142.1 | 142.2 | 142.2 |
| apply | ciclo 1 | 460 | 98.5 | 69.9 | 153.5 | 215.3 | 279.4 | 282.5 |
| célula | ciclo 1 | 189 | 98.6 | 70.5 | 219.7 | 234.8 | 291.4 | 291.5 |
| local | ciclos 2+ | 440 | 69.7 | 69.7 | 70.0 | 70.1 | 70.3 | 70.5 |
| 2pc | ciclos 2+ | 240 | 122.1 | 144.8 | 146.6 | 146.9 | 147.6 | 148.0 |
| notify | ciclos 2+ | 200 | 127.4 | 141.3 | 142.1 | 142.3 | 142.8 | 142.9 |
| apply | ciclos 2+ | 1840 | 69.7 | 69.8 | 70.0 | 70.1 | 70.2 | 73.2 |
| célula | ciclos 2+ | 727 | 77.2 | 69.7 | 146.3 | 147.8 | 150.9 | 152.9 |

## `fms-7` (5 execuções)

| classe | fase | n | média | p50 | p90 | p95 | p99 | máx |
|---|---|---|---|---|---|---|---|---|
| local | ciclo 1 | 110 | 76.1 | 69.7 | 70.2 | 141.1 | 141.5 | 141.6 |
| 2pc | ciclo 1 | 60 | 76.0 | 76.1 | 77.2 | 77.5 | 77.8 | 77.8 |
| notify | ciclo 1 | 50 | 71.5 | 71.6 | 72.0 | 72.1 | 72.2 | 72.2 |
| apply | ciclo 1 | 540 | 94.3 | 69.9 | 145.8 | 214.2 | 229.4 | 282.7 |
| célula | ciclo 1 | 187 | 102.0 | 73.4 | 162.3 | 236.4 | 639.6 | 657.0 |
| local | ciclos 2+ | 440 | 69.6 | 69.6 | 70.0 | 70.1 | 70.3 | 70.4 |
| 2pc | ciclos 2+ | 240 | 75.6 | 75.8 | 76.9 | 77.2 | 77.9 | 78.0 |
| notify | ciclos 2+ | 200 | 71.5 | 71.5 | 72.0 | 72.1 | 72.4 | 73.1 |
| apply | ciclos 2+ | 2160 | 69.7 | 69.8 | 70.0 | 70.1 | 70.4 | 71.2 |
| célula | ciclos 2+ | 827 | 62.1 | 72.2 | 79.7 | 80.8 | 82.1 | 83.8 |

Carimbos inválidos descartados: 352 conclusões de passo, 11 ciclos inteiros cujo início ou fim nos carimbos diverge do relógio do motor em mais de 200 ms, 719 intervalos da célula (em todas as execuções).

