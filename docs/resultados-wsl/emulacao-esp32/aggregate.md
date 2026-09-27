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
| `fms-1` | 2.55 (n=1) | 1.61 (n=1) | — | 0 (n=1) | — |
| `fms-1-esp32` | 304.65 (n=1) | 241.51 (n=1) | — | 0 (n=1) | — |
| `fms-2` | 5.25 (n=1) | 3.32 (n=1) | 4.22 (n=1) | 0 (n=1) | — |
| `fms-2-esp32` | 193.23 (n=1) | 148.56 (n=1) | 2.90 (n=1) | 0 (n=1) | — |
| `fms-7` | 7.27 (n=1) | 4.39 (n=1) | 4.84 (n=1) | 0 (n=1) | — |
| `fms-7-esp32` | 90.50 (n=1) | 61.28 (n=1) | 6.13 (n=1) | 0 (n=1) | — |
