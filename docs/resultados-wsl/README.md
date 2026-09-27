# Execuções no WSL 2 (máquina da autora)

Saída de `scripts/run-all.sh` num WSL 2 com Docker Engine 29.8.1 e Compose
5.5.1, em 27/09/2026. A imagem foi compilada na própria máquina (mbedTLS
3.6.5, g++ 15.2.0; ver `BUILD_INFO`). O cenário `fms-7` foi executado duas
vezes (12:45 e 12:55).

## Veredito

**10 execuções, 9 cenários, todos PASS**, incluindo o `fms-7-wifi` (`netem`),
que não pôde rodar no ambiente de referência.

## Comparação com a referência e com o ESP32

Os valores lógicos (impressão digital, decifrações, passos) são **idênticos**
à referência em [`../resultados/`](../resultados/) em todos os cenários que
completam. Os tempos dependem da máquina.

| cenário | decifrações (ciclo 1) | passos | retx | ms/passo ciclo 1 (WSL / ref.) | ciclos 2–5 (WSL / ref.) | RTT ms (WSL / ref.) |
|---|---|---|---|---|---|---|
| `fms-1` | 798 (190) | 220/220 | 0 | 2,54 / 2,36 | 1,63 / 1,60 | — |
| `fms-2` | 405 + 393 (85 + 105) | 220/220 | 0 | 5,29 / 4,05 | 3,33 / 2,84 | 3,8 / 2,3 |
| `fms-7` (1ª) | 798 (190) | 220/220 | 0 | 6,70 / 4,65 | 4,91 / 3,73 | 4,3 / 3,4 |
| `fms-7` (2ª) | 798 (190) | 220/220 | 0 | 6,36 / 4,65 | 4,32 / 3,73 | 3,8 / 3,4 |
| `fms-7-unicast` | 798 (190) | 220/220 | 0 | 6,79 / 4,76 | 4,70 / 3,75 | 4,6 / 3,3 |
| `fms-7-loss5` | 798 (190) | 220/220 | 89 / 86 | 449,7 / 510,9 | 794,3 / 767,8 | — |
| `fms-7-loss5-fast` | 798 (190) | 220/220 | 80 / 57 | 78,4 / 84,5 | 68,9 / 53,7 | — |
| **`fms-7-wifi`** | 798 (190) | 220/220 | 35 | **288,7** / — | **252,3** / — | **20,4** / — |
| `fms-2-loss30` | 135 (parou no ciclo 1) | 32/220, **SAFE HALT** | 25 / 72 | — | — | — |
| `esf-2-lockstep` | 40 (8), monolítico **PASS** | 30/30 | 0 | 8,75 / 7,02 | 4,90 / 3,48 | 4,0 / 2,4 |

Para comparar: as 2 placas ESP32-S3 fizeram **296,9 ms/passo** no ciclo 1 e
**167,2 ms** nos ciclos 2–5, com RTT de 13,9–18,2 ms.

## Leitura

1. **Equivalência confirmada numa segunda máquina.** Mesma impressão digital
   (`edbd7971` no `fms-2`), mesmas 405 + 393 decifrações, mesma divisão por nó
   nos 7 containers, oráculo PASS em todos os nós e monolítico PASS no ESF. O
   resultado lógico não depende de onde roda.
2. **O WSL é ~1,3–1,4× mais lento que a referência** no tempo por passo, e o
   custo homomórfico por decifração variou de ≈ 1,0 a 1,3 ms (contra 0,55 ms
   na referência). As duas execuções do `fms-7` diferem em 5 % (ciclo 1) e
   12 % (ciclos 2–5): é a ordem de grandeza da variância entre execuções nesta
   máquina, o que mostra que tempos precisam de repetições.
3. **`fms-7-wifi` é o primeiro experimento com atraso de rede.** Com 7 ± 3 ms
   por salto e 1 % de perda, o RTT de aplicação ficou em 20,4 ms, na faixa
   medida no Wi-Fi das placas (13,9–18,2 ms). O passo foi a 288,7 ms: com
   rede lenta, o tempo volta à ordem de grandeza do ESP32, mas **por outro
   motivo**. Lá é criptografia (69–100 ms por decifração); aqui é coordenação
   (commit em duas fases com 6 participantes, a ~20 ms por ida e volta, mais
   retransmissões). A igualdade dos números é coincidência de ordem de
   grandeza e não deve ser apresentada como equivalência de desempenho.
4. **`fms-2-loss30` parou mais cedo** (32 passos, contra 116 e 73 nas execuções
   de referência): a perda é aleatória e o ponto de parada varia. O desfecho é
   o mesmo: o COMMIT não confirmado leva o nó 1 a SAFE HALT, e o nó 2 para em
   seguida (`a peer halted`). Ambos saem com código 2 e nada divergente é
   aplicado.
5. **Os *timeouts* ajustados confirmam o achado da referência:** com 5 % de
   perda, 449,7 → 78,4 ms/passo (5,7×) só por trocar 1,5 s por 100 ms.

## Anomalias

Nenhuma: nenhum quadro rejeitado por autenticação, nenhuma divergência do
oráculo, nenhum reinício ou configuração divergente, e a fila de recepção
chegou a no máximo 12 de 64 quadros.
