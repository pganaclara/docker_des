# Sobrecarga do container

Mesma célula, mesmos binários (uma imagem por N, estáticos, `-DDES_MCAST_LOOP=1`), três lugares para rodar:

- **ponte**: um container por nó na rede *bridge* `cell` (veth + bridge), como a varredura principal;
- **host**: um container por nó na pilha de rede do host (`compose.host.yaml`): sem veth nem bridge;
- **nativo**: sem container, processos comuns no host.

Cada decifração leva **69 ms** (`DES_EMU_SCALARMUL_MS`). Tempos em ms, média ± desvio padrão; Δ = modo − ponte com IC 95 % de Welch, em negrito quando o IC não contém zero.

## Tempo por passo

| nós | modo | execuções | ciclo 1 | Δ ciclo 1 | ciclos 2–5 | Δ ciclos 2–5 | verificações |
|---|---|---|---|---|---|---|---|
| 1 | ponte | 5 | 303.4 ± 2.4 | — | 241.0 ± 1.0 | — | 5/5 |
| 1 | nativo | 5 | 304.2 ± 2.8 | +0.7 [-3.1; +4.5] | 241.0 ± 1.0 | -0.1 [-1.5; +1.4] | 5/5 |
| 2 | ponte | 5 | 196.1 ± 1.4 | — | 149.4 ± 0.1 | — | 5/5 |
| 2 | host | 5 | 196.4 ± 0.2 | +0.3 [-1.4; +2.0] | 149.1 ± 0.7 | -0.3 [-1.1; +0.5] | 5/5 |
| 2 | nativo | 5 | 195.4 ± 1.4 | -0.7 [-2.7; +1.4] | 148.9 ± 0.8 | -0.5 [-1.4; +0.5] | 5/5 |
| 4 | ponte | 5 | 132.7 ± 1.2 | — | 93.6 ± 0.6 | — | 5/5 |
| 4 | host | 5 | 132.6 ± 1.1 | -0.1 [-1.8; +1.6] | 93.5 ± 0.6 | -0.0 [-1.0; +0.9] | 5/5 |
| 4 | nativo | 5 | 132.5 ± 1.0 | -0.2 [-1.8; +1.4] | 93.5 ± 0.7 | -0.1 [-1.1; +0.8] | 5/5 |
| 7 | ponte | 5 | 89.4 ± 1.5 | — | 61.1 ± 0.6 | — | 5/5 |
| 7 | host | 5 | 89.7 ± 1.3 | +0.2 [-1.8; +2.2] | 61.0 ± 0.6 | -0.1 [-0.9; +0.8] | 5/5 |
| 7 | nativo | 5 | 89.6 ± 1.3 | +0.2 [-1.9; +2.2] | 60.9 ± 0.6 | -0.1 [-1.0; +0.7] | 5/5 |

## A parte da rede

RTT de aplicação: 20 sondas do nó 1 antes da execução (média por execução, depois média ± dp entre execuções). Espera pelos pares: p50 do tempo que o dono de um evento compartilhado espera pelos outros depois do seu passo homomórfico, ciclos 2–5, todas as execuções.

| nós | modo | RTT (ms) | Δ RTT | espera 2PC p50 (n) | espera NOTIFY p50 (n) |
|---|---|---|---|---|---|
| 2 | ponte | 3.92 ± 0.73 | — | 5.8 (160) | 1.7 (160) |
| 2 | host | 3.93 ± 0.26 | +0.01 [-0.88; +0.90] | 5.0 (160) | 1.6 (160) |
| 2 | nativo | 3.77 ± 0.70 | -0.15 [-1.19; +0.89] | 5.0 (160) | 1.6 (160) |
| 4 | ponte | 4.28 ± 0.81 | — | 5.4 (240) | 1.6 (200) |
| 4 | host | 3.93 ± 0.75 | -0.34 [-1.48; +0.80] | 5.5 (240) | 1.5 (200) |
| 4 | nativo | 3.91 ± 0.56 | -0.36 [-1.41; +0.68] | 5.6 (240) | 1.5 (200) |
| 7 | ponte | 9.55 ± 1.69 | — | 5.6 (240) | 1.7 (200) |
| 7 | host | 10.31 ± 0.32 | +0.76 [-1.33; +2.85] | 5.6 (240) | 1.6 (200) |
| 7 | nativo | 10.37 ± 0.66 | +0.81 [-1.25; +2.88] | 5.7 (240) | 1.6 (200) |

## Invariantes

| nós | modo | impressão digital |
|---|---|---|
| 1 | ponte | `3f2beff2` |
| 1 | nativo | `3f2beff2` |
| 2 | ponte | `edbd7971` |
| 2 | host | `edbd7971` |
| 2 | nativo | `edbd7971` |
| 4 | ponte | `457cc268` |
| 4 | host | `457cc268` |
| 4 | nativo | `457cc268` |
| 7 | ponte | `04511541` |
| 7 | host | `04511541` |
| 7 | nativo | `04511541` |
