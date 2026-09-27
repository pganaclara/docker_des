# Repetições agregadas

Invariantes: têm de ser idênticos em todas as repetições. Medidas: média ± desvio padrão amostral [mín–máx], coeficiente de variação.

## Invariantes

| cenário | n | todas as verificações | impressão digital | decifrações (ciclo 1) | por nó | desfecho |
|---|---|---|---|---|---|---|
| `fms-1` | 1 | 1/1 | 3f2beff2 (igual em 1/1) | 798 (190) (igual em 1/1) | 798 (igual em 1/1) | complete (igual em 1/1) |
| `fms-1-esp32` | 1 | 1/1 | 3f2beff2 (igual em 1/1) | 798 (190) (igual em 1/1) | 798 (igual em 1/1) | complete (igual em 1/1) |
| `fms-2` | 1 | 1/1 | edbd7971 (igual em 1/1) | 798 (190) (igual em 1/1) | 405 + 393 (igual em 1/1) | complete (igual em 1/1) |
| `fms-2-esp32` | 1 | 1/1 | edbd7971 (igual em 1/1) | 798 (190) (igual em 1/1) | 405 + 393 (igual em 1/1) | complete (igual em 1/1) |
| `fms-7` | 1 | 1/1 | 04511541 (igual em 1/1) | 798 (190) (igual em 1/1) | 101 + 101 + 100 + 103 + 114 + 129 + 150 (igual em 1/1) | complete (igual em 1/1) |
| `fms-7-esp32` | 1 | 1/1 | 04511541 (igual em 1/1) | 798 (190) (igual em 1/1) | 101 + 101 + 100 + 103 + 114 + 129 + 150 (igual em 1/1) | complete (igual em 1/1) |

## Medidas

| cenário | ms/passo, ciclo 1 | ms/passo, ciclos 2–5 | RTT de aplicação, ms | retransmissões | passos até o halt |
|---|---|---|---|---|---|
| `fms-1` | 2.08 (n=1) | 1.38 (n=1) | — | 0 (n=1) | — |
| `fms-1-esp32` | 299.54 (n=1) | 239.16 (n=1) | — | 0 (n=1) | — |
| `fms-2` | 3.93 (n=1) | 2.73 (n=1) | 2.48 (n=1) | 0 (n=1) | — |
| `fms-2-esp32` | 192.73 (n=1) | 147.48 (n=1) | 2.59 (n=1) | 0 (n=1) | — |
| `fms-7` | 4.35 (n=1) | 3.76 (n=1) | 3.32 (n=1) | 0 (n=1) | — |
| `fms-7-esp32` | 87.19 (n=1) | 59.81 (n=1) | 2.99 (n=1) | 0 (n=1) | — |
