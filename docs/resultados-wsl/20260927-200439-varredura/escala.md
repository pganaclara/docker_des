# Escala: FMS em 1, 2, 3, 4, 5, 6, 7 containers

Cada decifração leva **69 ms**, como no ESP32-S3 (`DES_EMU_SCALARMUL_MS`).
Repetições por configuração: 5, 5, 5, 5, 5, 5, 5. Tempos em ms por passo (média ± desvio padrão quando repetido).

| containers | ms/passo, ciclo 1 | aceleração | ms/passo, ciclos 2–5 | aceleração | limite (nó mais carregado) | acima do limite | verificações |
|---|---|---|---|---|---|---|---|
| 1 | 303.8 ± 1.3 | 1.00× | 241.7 ± 1.5 | 1.00× | 298.0 | 5.9 | 5/5 |
| 2 | 196.0 ± 0.9 | 1.55× | 149.1 ± 0.3 | 1.62× | 164.7 | 31.4 | 5/5 |
| 3 | 150.4 ± 0.3 | 2.02× | 112.5 ± 0.1 | 2.15× | 123.9 | 26.5 | 5/5 |
| 4 | 133.0 ± 1.3 | 2.28× | 93.8 ± 0.3 | 2.58× | 105.1 | 28.0 | 5/5 |
| 5 | 108.6 ± 0.6 | 2.80× | 82.6 ± 0.1 | 2.93× | 76.8 | 31.8 | 5/5 |
| 6 | 99.1 ± 0.2 | 3.06× | 77.2 ± 0.1 | 3.13× | 65.9 | 33.3 | 5/5 |
| 7 | 90.4 ± 0.2 | 3.36× | 61.5 ± 0.2 | 3.93× | 64.3 | 26.1 | 5/5 |

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
| 2 | S0 S1 S2 S3 S4 S6 · S5 | 196.0 ± 0.9 | 241.4 ± 1.2 | +23.2 % | 149.1 ± 0.3 | 207.9 ± 0.4 | +39.4 % | 164.7 | 233.7 | 5/5 |
| 3 | S0 S2 S6 · S1 S3 S4 · S5 | 150.4 ± 0.3 | 144.5 ± 0.3 | -3.9 % | 112.5 ± 0.1 | 119.0 ± 0.2 | +5.8 % | 123.9 | 123.9 | 5/5 |
| 4 | S0 S1 · S2 S6 · S3 S4 · S5 | 133.0 ± 1.3 | 117.7 ± 0.9 | -11.6 % | 93.8 ± 0.3 | 87.4 ± 0.2 | -6.8 % | 105.1 | 91.0 | 5/5 |
| 5 | S0 S1 · S2 S3 · S4 · S6 · S5 | 108.6 ± 0.6 | 108.4 ± 0.4 | -0.2 % | 82.6 ± 0.1 | 83.9 ± 0.1 | +1.6 % | 76.8 | 67.4 | 5/5 |
| 6 | S0 S2 · S1 · S3 · S4 · S6 · S5 | 99.1 ± 0.2 | 96.8 ± 0.5 | -2.4 % | 77.2 ± 0.1 | 77.3 ± 0.1 | +0.2 % | 65.9 | 64.3 | 5/5 |

Com 1 e com 7 containers as duas partições coincidem (1 container: todos juntos; 7: um por container).
