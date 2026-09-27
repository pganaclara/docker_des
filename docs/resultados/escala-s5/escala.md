# Escala: FMS em 1, 2, 3, 4, 5, 6, 7 containers

Cada decifração leva **69 ms**, como no ESP32-S3 (`DES_EMU_SCALARMUL_MS`).
Repetições por configuração: 1, 1, 1, 1, 1, 1, 1. Tempos em ms por passo (média ± desvio padrão quando repetido).

| containers | ms/passo, ciclo 1 | aceleração | ms/passo, ciclos 2–5 | aceleração | limite (nó mais carregado) | acima do limite | verificações |
|---|---|---|---|---|---|---|---|
| 1 | 299.6 | 1.00× | 239.2 | 1.00× | 298.0 | 1.7 | 1/1 |
| 2 | 192.7 | 1.56× | 147.5 | 1.62× | 164.7 | 28.0 | 1/1 |
| 3 | 146.9 | 2.04× | 110.9 | 2.16× | 123.9 | 23.0 | 1/1 |
| 4 | 130.7 | 2.29× | 92.3 | 2.59× | 105.1 | 25.6 | 1/1 |
| 5 | 106.1 | 2.82× | 81.4 | 2.94× | 76.8 | 29.2 | 1/1 |
| 6 | 96.4 | 3.11× | 76.0 | 3.15× | 65.9 | 30.5 | 1/1 |
| 7 | 87.5 | 3.43× | 59.8 | 4.00× | 64.3 | 23.2 | 1/1 |

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

## Comparação: partição `s5` × blocos contíguos

Mesmo número de containers, outra distribuição dos supervisores. Δ = variação do tempo por passo em relação aos blocos (negativo = mais rápido).

| containers | partição `s5` | ciclo 1: blocos | ciclo 1: `s5` | Δ | ciclos 2–5: blocos | ciclos 2–5: `s5` | Δ | limite: blocos | limite: `s5` | verificações |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | S0 S1 S2 S3 S4 S6 · S5 | 192.7 | 238.0 | +23.5 % | 147.5 | 205.9 | +39.6 % | 164.7 | 233.7 | 1/1 |
| 3 | S0 S2 S6 · S1 S3 S4 · S5 | 146.9 | 141.6 | -3.6 % | 110.9 | 117.5 | +6.0 % | 123.9 | 123.9 | 1/1 |
| 4 | S0 S1 · S2 S6 · S3 S4 · S5 | 130.7 | 115.5 | -11.6 % | 92.3 | 86.2 | -6.6 % | 105.1 | 91.0 | 1/1 |
| 5 | S0 S1 · S2 S3 · S4 · S6 · S5 | 106.1 | 106.1 | +0.0 % | 81.4 | 82.8 | +1.8 % | 76.8 | 67.4 | 1/1 |
| 6 | S0 S2 · S1 · S3 · S4 · S6 · S5 | 96.4 | 94.8 | -1.7 % | 76.0 | 76.2 | +0.3 % | 65.9 | 64.3 | 1/1 |

Com 1 e com 7 containers as duas partições coincidem (1 container: todos juntos; 7: um por container).
