# WSL: S5 isolado × blocos contíguos, 5 repetições

`REPEAT=5 scripts/run-all.sh s5` no WSL 2 da autora, 27/09/2026: FMS, família
modular local completa, decifração emulada a 69 ms, as duas partições para 2
a 6 containers (mais 1 e 7, em que elas coincidem). **60/60 execuções PASS**,
nenhuma anomalia nos logs. Tabela gerada em [`escala.md`](escala.md); registro
completo em `s5-rep5.log`.

## Invariantes

Em cada uma das 12 configurações as 5 repetições deram exatamente o mesmo
resultado lógico: 220/220 passos, 798 decifrações (190 no ciclo 1), a mesma
divisão por nó, a mesma impressão digital, oráculo PASS e nenhuma
retransmissão. A partição muda quem faz cada decifração, não quantas são.

## Diferença S5 isolado − blocos (ms por passo, n = 5 + 5)

Intervalo de confiança de 95 % da diferença das médias (Welch). Negativo =
S5 isolado mais rápido.

| containers | partição S5 isolado | ciclo 1: diferença | IC 95 % | ciclos 2–5: diferença | IC 95 % | limite: blocos → S5 |
|---|---|---|---|---|---|---|
| 2 | S0 S1 S2 S3 S4 S6 · S5 | **+45,4 (+23,2 %)** | [+43,9; +46,9] | **+58,8 (+39,4 %)** | [+58,3; +59,4] | 164,7 → 233,7 |
| 3 | S0 S2 S6 · S1 S3 S4 · S5 | **−5,9 (−3,9 %)** | [−6,3; −5,4] | **+6,6 (+5,8 %)** | [+6,3; +6,8] | 123,9 → 123,9 |
| 4 | S0 S1 · S2 S6 · S3 S4 · S5 | **−15,4 (−11,6 %)** | [−17,1; −13,7] | **−6,4 (−6,8 %)** | [−6,9; −6,0] | 105,1 → 91,0 |
| 5 | S0 S1 · S2 S3 · S4 · S6 · S5 | −0,3 (−0,2 %) | [−1,0; +0,5] | **+1,3 (+1,6 %)** | [+1,2; +1,5] | 76,8 → 67,4 |
| 6 | S0 S2 · S1 · S3 · S4 · S6 · S5 | **−2,4 (−2,4 %)** | [−2,9; −1,8] | +0,1 (+0,2 %) | [−0,0; +0,3] | 65,9 → 64,3 |

Em negrito, as diferenças cujo IC 95 % não contém zero.

## Leitura

1. **A primeira execução (nuvem, n = 1) se confirma**, com os mesmos sinais e
   praticamente as mesmas porcentagens em todas as configurações.
2. **Isolar o S5 só compensa, nas duas fases, com 4 containers:** −11,6 % no
   ciclo 1 e −6,8 % nos ciclos 2–5. É também onde o limite do nó mais
   carregado mais cai (105,1 → 91,0 ms).
3. **Com 2 containers é muito pior** (+23 % e +39 %): os outros 6 supervisores
   ficam juntos.
4. **Com 3 e 6 containers o ciclo 1 melhora e os ciclos 2–5 não.** O S5 é o
   gargalo do ciclo 1 (41 das 190 decifrações), mas depois dele o mais pesado
   é o S6 (28 decifrações por ciclo, contra 22 do S5). Com 3 containers a
   partição S5 isolado deixa os ciclos 2–5 5,8 % mais lentos.
5. **Com 5 containers o limite cai (76,8 → 67,4 ms) e o ciclo 1 não muda**
   (diferença não significativa). O limite só conta o total de trabalho de
   cada nó no ciclo, não *quando* esse trabalho acontece entre dois eventos
   compartilhados. Explicar esse caso exige um modelo pelo caminho crítico ao
   longo do roteiro, que não foi feito.
6. **Conclusão prática:** não existe partição melhor para todo N. Isolar o
   supervisor mais carregado ajuda quando isso reduz o limite *e* não
   concentra os demais num único container, o que neste FMS só acontece
   claramente com 4 containers. A escolha da partição é um parâmetro de
   projeto que vale medir.
