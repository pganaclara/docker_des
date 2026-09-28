# WSL: latência por passo com percentis, varredura 1–7, 5 repetições

`REPEAT=5 scripts/run-all.sh` no WSL 2 da autora, 27/09/2026: FMS, família
modular local completa, decifração emulada a 69 ms, 1 a 7 containers. É a
primeira varredura com `nodeK.ts.log` (log com carimbo de tempo do Docker),
que permite medir o intervalo da **célula**, e não só o de cada evento.
**35/35 execuções PASS**, nenhuma retransmissão. Tabelas em
[`latencia.md`](latencia.md) (percentis) e [`escala.md`](escala.md) (tempo por
passo); registro completo em `lat-rep5.log`. O `latencia.csv` com todas as
amostras não foi versionado (1,1 MB); `python3 scripts/latency.py
docs/resultados-wsl/20260927-210233-varredura` o recria.

## Reprodutibilidade

A tabela de escala repete a da varredura anterior
([`20260927-170420`](../20260927-170420-varredura/README.md)) dentro de ~1 %:
com 7 containers, 90,3 ± 0,7 e 61,3 ± 0,3 ms/passo (antes 90,1 ± 0,8 e
61,5 ± 0,2). Os invariantes (798 decifrações, 190 no ciclo 1, impressões
digitais) são os mesmos em todas as execuções.

## Latência de decisão e aplicação (ciclos 2–5, ms)

Vem das linhas que o próprio motor imprime (relógio monotônico de cada nó),
então não depende do relógio do host.

| containers | 2PC no dono p50 / p99 | NOTIFY no dono p50 / p99 | local p50 / p99 | apply p50 / p99 |
|---|---|---|---|---|
| 1 | — | — | 70,8 / 490,3 | — |
| 2 | 284,6 / 287,2 | 281,1 / 282,7 | 69,8 / 209,9 | 209,0 / 209,8 |
| 3 | 213,8 / 216,9 | 210,8 / 212,3 | 69,6 / 70,2 | 139,3 / 140,0 |
| 4 | 145,3 / 147,4 | 141,3 / 142,3 | 69,7 / 70,3 | 139,0 / 140,0 |
| 5 | 145,1 / 147,3 | 141,2 / 142,4 | 69,7 / 70,3 | 69,8 / 139,9 |
| 6 | 144,8 / 147,6 | 141,3 / 142,8 | 69,7 / 70,3 | 69,8 / 70,2 |
| 7 | 75,8 / 77,9 | 71,5 / 72,4 | 69,6 / 70,3 | 69,8 / 70,4 |

- **A latência é quantizada em decifrações.** Cada valor é k × 69 ms, onde k
  é o número de supervisores do nó que têm o evento no alfabeto, mais a
  rede. Para o 2PC isso dá 4, 3, 2, 2, 2, 1 decifrações com 2 a 7 containers,
  e a latência cai em degraus de ~69 ms (284,6 → 213,8 → 145,3 → 75,8).
- **A rede custa pouco.** 2PC − local com a mesma quantidade de decifrações:
  ~6 ms com 7 containers (75,8 − 69,6), ~2 ms para o NOTIFY (uma volta a
  menos). Com o ESP32 real esse termo é Wi-Fi, não uma *bridge*.
- **Jitter pequeno.** p99 − p50 ≤ 3,1 ms no 2PC e no NOTIFY,
  de 2 a 7 containers (n = 200 a 240 por célula da tabela). O
  que parece cauda (local com 1 e 2 containers, apply com 5) é bimodal: são
  eventos com mais supervisores no nó, não atrasos.
- Os valores repetem a varredura anterior (2PC p50 283,5 → 214,1 → 144,7 →
  75,8 ms) com diferença ≤ 1,1 ms.

## Intervalo da célula (ciclos 2–5, ms)

Tempo entre a conclusão de um passo, em qualquer nó, e a do seguinte.

| containers | n | média | p50 | p90 | p99 | máx | ms/passo (escala) |
|---|---|---|---|---|---|---|---|
| 1 | 822 | 237,1 | 70,8 | 489,9 | 490,7 | 497,9 | 241,5 |
| 2 | 599 | 151,7 | 70,5 | 285,5 | 288,3 | 289,3 | 149,2 |
| 3 | 741 | 110,7 | 70,0 | 216,9 | 289,1 | 292,8 | 112,3 |
| 4 | 797 | 96,1 | 73,4 | 147,7 | 151,4 | 152,8 | 93,8 |
| 5 | 820 | 83,1 | 70,6 | 147,9 | 151,3 | 152,8 | 82,8 |
| 6 | 727 | 77,2 | 69,7 | 146,3 | 150,9 | 152,9 | 77,2 |
| 7 | 827 | 62,1 | 72,2 | 79,7 | 82,1 | 83,8 | 61,3 |

- A média bate com o tempo por passo da tabela de escala (medido por outro
  caminho, o relógio de execução do motor) com diferença de 0 a 4,4 ms. As
  duas medições se confirmam.
- **O pior caso cai mais que a média.** Com 7 containers nenhum passo levou
  mais de 84 ms, contra 498 ms com 1 container: o máximo cai 5,9×, a média
  3,9×. Para controle, o que limita o período de amostragem é o pior caso,
  não a média, e é aí que a distribuição mais ajuda.
- Com 7 containers a média (62,1) fica abaixo do p50 (72,2): passos de nós
  diferentes terminam quase juntos (intervalos perto de zero), o que é o
  paralelismo aparecendo.
- O ciclo 1 tem cauda maior (p99 de 640 ms com 7 containers): são os
  primeiros passos, enquanto os nós ainda se sincronizam, e o ciclo 1 faz
  mais decifrações. Os valores estão em [`latencia.md`](latencia.md).

## Anomalia: o relógio do WSL salta

Na primeira leitura, o intervalo da célula tinha p99 de 1,7 a 4,9 s e máximo
de 8,6 s, incompatível com ~60 ms por passo. Não era o protocolo:

- O Docker carimba cada linha com o relógio de parede do host no momento em
  que a lê. Em todas as execuções, de tempos em tempos, **todos os nós ao
  mesmo tempo** recebem carimbos ~11,5–12 s no futuro por 1 a 4 linhas, e
  depois o relógio volta. Às vezes o salto fica (o relógio é corrigido para a
  frente e não volta).
- O relógio de execução do motor (monotônico) não vê nada disso: os tempos de
  HE, espera pelos pares e fim de ciclo são normais nessas linhas.
- A causa provável é a sincronização de hora do WSL 2 com o Windows
  (Hyper-V), que ajusta o relógio da VM aos saltos.

O `scripts/latency.py` agora descarta: (1) linhas carimbadas depois de uma que
o mesmo container imprimiu mais tarde, ou antes de uma anterior; (2) ciclos
inteiros cujo início ou fim, pelos carimbos, diverge do relógio do motor em
mais de 200 ms (isso pega os saltos que não voltam). No total, **352
conclusões de passo e 11 ciclos (de 175), ou 719 intervalos**, foram
descartados. Os intervalos que sobram reproduzem o tempo por passo da escala
(tabela acima). A latência de eventos não é afetada, porque não usa os
carimbos.

Para medições futuras no WSL, uma alternativa sem esse problema é o motor
imprimir o relógio de execução em cada linha de passo. Isso exigiria mudar o
`engine/`, que é cópia verbatim do firmware, então não foi feito.
