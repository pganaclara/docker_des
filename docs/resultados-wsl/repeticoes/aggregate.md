# Repetições agregadas

Invariantes: têm de ser idênticos em todas as repetições. Medidas: média ± desvio padrão amostral [mín–máx], coeficiente de variação.

## Invariantes

| cenário | n | todas as verificações | impressão digital | decifrações (ciclo 1) | por nó | desfecho |
|---|---|---|---|---|---|---|
| `esf-2-lockstep` | 5 | 5/5 | d42d57d1 (igual em 5/5) | 40 (8) (igual em 5/5) | 20 + 20 (igual em 5/5) | complete (igual em 5/5) |
| `fms-1` | 5 | 5/5 | 3f2beff2 (igual em 5/5) | 798 (190) (igual em 5/5) | 798 (igual em 5/5) | complete (igual em 5/5) |
| `fms-2` | 5 | 5/5 | edbd7971 (igual em 5/5) | 798 (190) (igual em 5/5) | 405 + 393 (igual em 5/5) | complete (igual em 5/5) |
| `fms-2-loss30` | 5 | 5/5 | edbd7971 (igual em 5/5) | varia até o halt | — | halt (igual em 5/5) |
| `fms-7` | 5 | 5/5 | 04511541 (igual em 5/5) | 798 (190) (igual em 5/5) | 101 + 101 + 100 + 103 + 114 + 129 + 150 (igual em 5/5) | complete (igual em 5/5) |
| `fms-7-loss5` | 5 | 5/5 | 04511541 (igual em 5/5) | 798 (190) (igual em 5/5) | 101 + 101 + 100 + 103 + 114 + 129 + 150 (igual em 5/5) | complete (igual em 5/5) |
| `fms-7-loss5-fast` | 5 | 5/5 | 04511541 (igual em 5/5) | 798 (190) (igual em 5/5) | 101 + 101 + 100 + 103 + 114 + 129 + 150 (igual em 5/5) | complete (igual em 5/5) |
| `fms-7-unicast` | 5 | 5/5 | 04511541 (igual em 5/5) | 798 (190) (igual em 5/5) | 101 + 101 + 100 + 103 + 114 + 129 + 150 (igual em 5/5) | complete (igual em 5/5) |
| `fms-7-wifi` | 5 | 5/5 | 04511541 (igual em 5/5) | 798 (190) (igual em 5/5) | 101 + 101 + 100 + 103 + 114 + 129 + 150 (igual em 5/5) | complete (igual em 5/5) |

## Medidas

| cenário | ms/passo, ciclo 1 | ms/passo, ciclos 2–5 | RTT de aplicação, ms | retransmissões | passos até o halt |
|---|---|---|---|---|---|
| `esf-2-lockstep` | 7.91 ± 1.02 [6.73–8.83], CV 13 % | 4.32 ± 0.24 [4.00–4.55], CV 6 % | 3.97 ± 0.16 [3.81–4.22], CV 4 % | 0 ± 0 [0–0] | — |
| `fms-1` | 2.58 ± 0.03 [2.55–2.61], CV 1 % | 1.64 ± 0.01 [1.61–1.65], CV 1 % | — | 0 ± 0 [0–0] | — |
| `fms-2` | 4.99 ± 0.34 [4.43–5.31], CV 7 % | 3.16 ± 0.19 [2.86–3.32], CV 6 % | 3.56 ± 0.53 [2.65–4.03], CV 15 % | 0 ± 0 [0–0] | — |
| `fms-2-loss30` | 852.04 (n=1) | 803.05 (n=1) | 3.76 ± 0.69 [2.87–4.37], CV 18 % | 30 ± 13 [23–53], CV 44 % | 46 ± 31 [32–101], CV 67 % |
| `fms-7` | 5.95 ± 0.40 [5.62–6.47], CV 7 % | 4.40 ± 0.10 [4.30–4.56], CV 2 % | 4.39 ± 0.42 [4.04–4.95], CV 10 % | 0 ± 0 [0–0] | — |
| `fms-7-loss5` | 503.61 ± 55.77 [435.81–569.25], CV 11 % | 679.70 ± 75.55 [555.69–747.93], CV 11 % | 3.95 ± 0.62 [2.93–4.51], CV 16 % | 78 ± 8 [65–86], CV 10 % | — |
| `fms-7-loss5-fast` | 87.75 ± 10.71 [78.28–101.23], CV 12 % | 66.29 ± 6.97 [61.01–76.43], CV 11 % | 4.22 ± 0.32 [3.80–4.64], CV 8 % | 76 ± 4 [70–81], CV 6 % | — |
| `fms-7-unicast` | 5.93 ± 0.70 [5.04–6.70], CV 12 % | 4.19 ± 0.30 [3.91–4.64], CV 7 % | 3.94 ± 0.80 [3.07–4.89], CV 20 % | 0 ± 0 [0–0] | — |
| `fms-7-wifi` | 161.12 ± 107.85 [49.02–299.61], CV 67 % | 162.29 ± 47.63 [112.53–235.19], CV 29 % | 20.25 ± 0.20 [20.01–20.56], CV 1 % | 21 ± 7 [13–26], CV 32 % | — |
