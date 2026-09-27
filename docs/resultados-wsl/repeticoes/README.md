# WSL: 5 repetições de todos os cenários

`scripts/run-all.sh` executado 5 vezes seguidas no WSL 2 da autora, em
27/09/2026 (14:35–15:11): **45 execuções, 45 PASS.** Registro completo em
`repeticoes.log`; tabelas geradas com

```bash
python3 scripts/aggregate.py docs/resultados-wsl/repeticoes
```

→ [`aggregate.md`](aggregate.md) / `aggregate.json`.

## 1. Invariantes: idênticos em 5/5

Impressão digital, decifrações (total, ciclo 1 e por nó), passos e desfecho
foram iguais nas 5 repetições de todos os cenários. Coincidem também com a
execução avulsa do WSL e com a referência na nuvem, e `fms-2` (`edbd7971`,
405 + 393) coincide com as placas ESP32-S3. Somando as execuções do WSL e da
referência, o `fms-7` rodou **7 vezes em duas máquinas** com o mesmo resultado
lógico.

A única variação é a esperada: no `fms-2-loss30`, o ponto do SAFE HALT
(46 ± 31 passos, de 32 a 101) depende de quais quadros a perda aleatória
derruba. O desfecho foi SAFE HALT nas 5.

## 2. Medidas (média ± desvio padrão amostral, n = 5)

| cenário | ms/passo, ciclo 1 | ms/passo, ciclos 2–5 | RTT, ms | retransmissões |
|---|---|---|---|---|
| `fms-1` (7 supervisores, 1 container) | 2,58 ± 0,03 | 1,64 ± 0,01 | — | 0 |
| `fms-2` | 4,99 ± 0,34 | 3,16 ± 0,19 | 3,56 ± 0,53 | 0 |
| `fms-7` (1 supervisor por container) | 5,95 ± 0,40 | 4,40 ± 0,10 | 4,39 ± 0,42 | 0 |
| `fms-7-unicast` | 5,93 ± 0,70 | 4,19 ± 0,30 | 3,94 ± 0,80 | 0 |
| `esf-2-lockstep` | 7,91 ± 1,02 | 4,32 ± 0,24 | 3,97 ± 0,16 | 0 |
| `fms-7-loss5` (*timeout* 1,5 s) | 503,6 ± 55,8 | 679,7 ± 75,6 | 3,95 ± 0,62 | 78 ± 8 |
| `fms-7-loss5-fast` (*timeout* 100 ms) | 87,8 ± 10,7 | 66,3 ± 7,0 | 4,22 ± 0,32 | 76 ± 4 |
| `fms-7-wifi` (`netem` 7 ± 3 ms, 1 %) | 161 ± 108 | 162 ± 48 | 20,25 ± 0,20 | 21 ± 7 |

## 3. O que as repetições permitem afirmar

1. **Distribuir custa tempo no container, e a diferença é real.**
   1 → 2 → 7 nós: 2,58 → 4,99 → 5,95 ms/passo no ciclo 1 e 1,64 → 3,16 →
   4,40 nos ciclos 2–5. Os desvios (≤ 0,4 ms) são bem menores que as
   diferenças, então a ordenação não é ruído. No ESP32 é o contrário (2 placas
   mais rápidas que 1), porque lá a criptografia domina.
2. **Multicast e unicast não se distinguem** nesta rede: 5,95 ± 0,40 contra
   5,93 ± 0,70 ms. Numa *bridge* local, enviar 6 datagramas em vez de 1 não
   pesa.
3. **Os *timeouts* explicam quase todo o custo da perda.** Com a mesma perda
   (5 %) e praticamente o mesmo número de retransmissões (78 contra 76),
   trocar o *timeout* de 1,5 s por 100 ms reduz o passo de 503,6 para 87,8 ms
   (5,7×) no ciclo 1 e de 679,7 para 66,3 ms (10×) nos ciclos 2–5.
4. **Com atraso de rede, a variância é dominada pelas perdas.** No
   `fms-7-wifi`, o RTT é estável (20,25 ± 0,20 ms), mas o tempo por passo varia
   de 49 a 300 ms. A espera por evento compartilhado é **bimodal**: mediana
   ≈ 36 ms (commit em duas fases normal) e percentil 90 ≈ 1.520 ms, com os
   máximos em múltiplos de 1,5 s. Cada quadro perdido custa um *timeout*
   inteiro, e o número de perdas por execução é aleatório (13 a 35
   retransmissões). Para um artigo, reporte essa distribuição (mediana e
   percentis) em vez da média, ou use *timeouts* ajustados ao RTT.

## 4. Ressalvas

- n = 5 serve para ordenar cenários e mostrar a variância, não para intervalos
  de confiança apertados. Para o artigo, 20–30 repetições dos cenários de
  tempo seriam o mínimo razoável.
- As 5 repetições rodaram em sequência na mesma sessão; efeitos como
  aquecimento de cache ou outros programas abertos no Windows não foram
  controlados.
- Tempo de WSL não é tempo de tempo real (sem PREEMPT_RT, CPU compartilhada
  com o Windows).
