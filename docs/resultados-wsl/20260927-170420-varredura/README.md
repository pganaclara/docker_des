# WSL: varredura de 1 a 7 containers, 5 repetições

`REPEAT=5 scripts/run-all.sh` no WSL 2 da autora, 27/09/2026: família modular
local completa (`LMOD`), decifração emulada a 69 ms (ESP32-S3), 5 execuções de
cada configuração. **35/35 PASS, nenhuma anomalia nos logs.** Tabela gerada
pelo `scaling.py` em [`escala.md`](escala.md); registro completo em
`varredura-rep5.log`.

## Invariantes: idênticos nas 35 execuções

Em cada configuração, as 5 repetições deram exatamente o mesmo resultado
lógico: 220/220 passos, 798 decifrações (190 no ciclo 1), a mesma divisão por
nó, a mesma impressão digital (as mesmas da referência e, com 2 nós,
`edbd7971`, a das placas ESP32-S3), oráculo PASS em todos os nós e nenhuma
retransmissão.

## Tempos (ms por passo, média ± intervalo de confiança de 95 %, n = 5)

| containers | ciclo 1 | aceleração | ciclos 2–5 | aceleração | limite (nó mais carregado) | acima do limite |
|---|---|---|---|---|---|---|
| 1 | 303,1 ± 1,3 | 1,00× | 240,8 ± 0,2 | 1,00× | 298,0 | 5,2 |
| 2 | 195,2 ± 0,6 | 1,55× | 148,9 ± 0,2 | 1,62× | 164,7 | 30,5 |
| 3 | 149,2 ± 0,6 | 2,03× | 112,4 ± 0,2 | 2,14× | 123,9 | 25,3 |
| 4 | 133,2 ± 0,3 | 2,28× | 93,6 ± 0,3 | 2,57× | 105,1 | 28,1 |
| 5 | 108,2 ± 1,3 | 2,80× | 82,7 ± 0,3 | 2,91× | 76,8 | 31,3 |
| 6 | 98,8 ± 1,1 | 3,07× | 77,2 ± 0,2 | 3,12× | 65,9 | 32,9 |
| 7 | 90,1 ± 1,0 | 3,37× | 61,5 ± 0,3 | 3,92× | 64,3 | 25,8 |

Intervalo de 95 % = t(0,975; 4) × desvio padrão ÷ √5, com t = 2,776.

1. **A variação entre repetições é mínima:** coeficiente de variação de
   0,2–1,0 % no ciclo 1 e ≤ 0,3 % nos ciclos 2–5. Os intervalos de confiança
   (≤ 1,3 ms) são muito menores que as diferenças entre configurações vizinhas
   (≥ 8,7 ms), então **toda a curva é estatisticamente distinguível**: cada
   container a mais reduz o tempo por passo.
2. **A aceleração é sublinear e segue o nó mais carregado.** 7 containers dão
   3,37× (ciclo 1) e 3,92× (ciclos 2–5), longe do ideal de 7×. O limite
   "decifrações do nó mais carregado × 69 ms ÷ 44" explica a forma da curva:
   ele cai de 298,0 para 64,3 ms, e o medido acompanha 25–33 ms acima dele (o
   custo de coordenação). De 6 para 7 o limite quase não muda (65,9 → 64,3),
   porque S5 sozinho concentra 41 das 190 decifrações do ciclo 1.
3. **Reprodutível entre máquinas:** a média do WSL difere da referência na
   nuvem em 0,4–2,1 % no ciclo 1.
4. **RTT de aplicação:** algumas sondas iniciais passaram de 130 ms (máximo
   141,8 ms), com médias até 11 ms. São soluços do WSL/Windows durante a
   sondagem, antes do roteiro: não aparecem nos tempos por passo, cuja
   variação é < 1 %.
