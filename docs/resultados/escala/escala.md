# Escala: FMS em 1, 2, 3, 4, 5, 6, 7 containers

Cada decifração leva **69 ms**, como no ESP32-S3 (`DES_EMU_SCALARMUL_MS`).
Repetições por configuração: 1, 1, 1, 1, 1, 1, 1. Tempos em ms por passo (média ± desvio padrão quando repetido).

| containers | ms/passo, ciclo 1 | aceleração | ms/passo, ciclos 2–5 | aceleração | limite (nó mais carregado) | acima do limite | verificações |
|---|---|---|---|---|---|---|---|
| 1 | 299.6 | 1.00× | 239.2 | 1.00× | 298.0 | 1.6 | 1/1 |
| 2 | 192.8 | 1.55× | 147.5 | 1.62× | 164.7 | 28.1 | 1/1 |
| 3 | 146.8 | 2.04× | 110.7 | 2.16× | 123.9 | 22.9 | 1/1 |
| 4 | 130.7 | 2.29× | 92.4 | 2.59× | 105.1 | 25.7 | 1/1 |
| 5 | 106.0 | 2.83× | 81.2 | 2.94× | 76.8 | 29.2 | 1/1 |
| 6 | 96.3 | 3.11× | 75.8 | 3.15× | 65.9 | 30.4 | 1/1 |
| 7 | 87.2 | 3.44× | 59.8 | 4.00× | 64.3 | 22.9 | 1/1 |

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
