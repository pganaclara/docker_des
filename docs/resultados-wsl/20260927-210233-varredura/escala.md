# Escala: FMS em 1, 2, 3, 4, 5, 6, 7 containers

Cada decifração leva **69 ms**, como no ESP32-S3 (`DES_EMU_SCALARMUL_MS`).
Repetições por configuração: 5, 5, 5, 5, 5, 5, 5. Tempos em ms por passo (média ± desvio padrão quando repetido).

| containers | ms/passo, ciclo 1 | aceleração | ms/passo, ciclos 2–5 | aceleração | limite (nó mais carregado) | acima do limite | verificações |
|---|---|---|---|---|---|---|---|
| 1 | 304.3 ± 0.9 | 1.00× | 241.5 ± 0.1 | 1.00× | 298.0 | 6.3 | 5/5 |
| 2 | 197.4 ± 2.2 | 1.54× | 149.2 ± 0.2 | 1.62× | 164.7 | 32.7 | 5/5 |
| 3 | 150.3 ± 0.3 | 2.02× | 112.3 ± 0.5 | 2.15× | 123.9 | 26.5 | 5/5 |
| 4 | 133.1 ± 0.3 | 2.29× | 93.8 ± 0.2 | 2.57× | 105.1 | 28.1 | 5/5 |
| 5 | 109.2 ± 1.3 | 2.79× | 82.8 ± 0.1 | 2.92× | 76.8 | 32.4 | 5/5 |
| 6 | 99.3 ± 0.6 | 3.06× | 77.2 ± 0.3 | 3.13× | 65.9 | 33.4 | 5/5 |
| 7 | 90.3 ± 0.7 | 3.37× | 61.3 ± 0.3 | 3.94× | 64.3 | 26.0 | 5/5 |

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
