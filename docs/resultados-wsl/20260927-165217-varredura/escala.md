# Escala: FMS em 1, 2, 3, 4, 5, 6, 7 containers

Cada decifração leva **69 ms**, como no ESP32-S3 (`DES_EMU_SCALARMUL_MS`).
Repetições por configuração: 1, 1, 1, 1, 1, 1, 1. Tempos em ms por passo (média ± desvio padrão quando repetido).

| containers | ms/passo, ciclo 1 | aceleração | ms/passo, ciclos 2–5 | aceleração | limite (nó mais carregado) | acima do limite | verificações |
|---|---|---|---|---|---|---|---|
| 1 | 301.8 | 1.00× | 240.6 | 1.00× | 298.0 | 3.8 | 1/1 |
| 2 | 195.1 | 1.55× | 148.6 | 1.62× | 164.7 | 30.4 | 1/1 |
| 3 | 150.4 | 2.01× | 112.1 | 2.15× | 123.9 | 26.5 | 1/1 |
| 4 | 132.9 | 2.27× | 93.6 | 2.57× | 105.1 | 27.8 | 1/1 |
| 5 | 109.5 | 2.76× | 82.9 | 2.90× | 76.8 | 32.7 | 1/1 |
| 6 | 99.7 | 3.03× | 77.4 | 3.11× | 65.9 | 33.8 | 1/1 |
| 7 | 88.9 | 3.39× | 61.5 | 3.91× | 64.3 | 24.6 | 1/1 |

Aceleração = tempo com 1 container ÷ tempo com N. Limite = decifrações do nó mais carregado no ciclo 1 × custo de uma decifração ÷ passos do ciclo: os nós só trabalham em paralelo entre dois eventos compartilhados, então a célula nunca é mais rápida que seu nó mais carregado.

## Partição e invariantes

| containers | supervisores por container | decifrações no ciclo 1 do mais carregado | decifrações (total) | impressão digital |
|---|---|---|---|---|
| 1 | S0 S1 S2 S3 S4 S5 S6 | 190 | 798 | `3f2beff2` |
| 2 | S0 S1 S2 S3 · S4 S5 S6 | 105 | 798 | `edbd7971` |
| 3 | S0 S1 S2 · S3 S4 · S5 S6 | 79 | 798 | `04d74714` |
| 4 | S0 S1 · S2 S3 · S4 S5 · S6 | 67 | 798 | `457cc268` |
| 5 | S0 S1 · S2 · S3 S4 · S5 · S6 | 49 | 798 | `6f43d6b9` |
| 6 | S0 S1 · S2 · S3 · S4 · S5 · S6 | 42 | 798 | `8d540ec9` |
| 7 | S0 · S1 · S2 · S3 · S4 · S5 · S6 | 41 | 798 | `04511541` |
