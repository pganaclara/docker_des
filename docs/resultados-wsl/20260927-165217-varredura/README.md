# WSL: varredura de 1 a 7 containers

`scripts/run-all.sh` no WSL 2 da autora, 27/09/2026, família modular local
completa (`LMOD`), decifração emulada a 69 ms (ESP32-S3), uma execução por
configuração. **7/7 PASS, nenhuma anomalia nos logs.**

## Invariantes: iguais à referência

Nas 7 configurações: 220/220 passos, 798 decifrações (190 no ciclo 1),
oráculo PASS em todos os nós, nenhuma retransmissão, todos os containers
saíram com código 0. As 7 impressões digitais coincidem com as da referência
([`../../resultados/escala/`](../../resultados/escala/)), e a de 2 nós
(`edbd7971`) com a das placas ESP32-S3.

## Tempos: WSL × referência

| containers | ciclo 1, WSL | ciclo 1, ref. | diferença | ciclos 2–5, WSL | ciclos 2–5, ref. | aceleração (WSL) | acima do limite (WSL / ref.) |
|---|---|---|---|---|---|---|---|
| 1 | 301,8 | 299,6 | +0,7 % | 240,6 | 239,2 | 1,00× | 3,8 / 1,6 |
| 2 | 195,1 | 192,8 | +1,2 % | 148,6 | 147,5 | 1,55× | 30,4 / 28,1 |
| 3 | 150,4 | 146,8 | +2,5 % | 112,1 | 110,7 | 2,01× | 26,5 / 22,9 |
| 4 | 132,9 | 130,7 | +1,6 % | 93,6 | 92,4 | 2,27× | 27,8 / 25,7 |
| 5 | 109,5 | 106,0 | +3,3 % | 82,9 | 81,2 | 2,76× | 32,7 / 29,2 |
| 6 | 99,7 | 96,3 | +3,6 % | 77,4 | 75,8 | 3,03× | 33,8 / 30,4 |
| 7 | 88,9 | 87,2 | +2,0 % | 61,5 | 59,8 | 3,39× | 24,6 / 22,9 |

(ms por passo.)

1. **A escala se reproduz:** o tempo por passo cai a cada container a mais,
   com aceleração de 1,55× (2) a 3,39× (7) no ciclo 1 e até 3,91× nos ciclos
   2–5.
2. **As duas máquinas diferem em 0,6–3,6 %**, sempre com o WSL um pouco mais
   lento. Com a decifração emulada dominando, a CPU quase não pesa; o
   restante (coordenação, ~25–34 ms acima do limite) é um pouco maior no WSL.
3. **O limite do nó mais carregado explica a forma da curva.** De 6 para 7
   containers o ganho é pequeno (99,7 → 88,9 ms) porque o supervisor S5
   sozinho já concentra 41 das 190 decifrações do ciclo 1; separar o resto
   não o alivia. O ciclo 1 com 7 containers fica 24,6 ms acima do limite de
   64,3 ms.
4. **RTT do `fms-7` (10,75 ms de média):** uma única sonda levou 129,6 ms (as
   demais, a partir de 2,45 ms), um soluço pontual do WSL/Windows durante a
   sondagem inicial, antes do roteiro. Não afeta os tempos por passo.

Ressalva: uma execução por configuração. A concordância com a referência
(≤ 3,6 %) indica pouca variação, mas para o artigo vale `REPEAT=5` ou mais.
