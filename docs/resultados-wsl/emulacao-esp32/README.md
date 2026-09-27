# WSL: emulação do custo de decifração do ESP32

`scripts/run-all.sh fms-1-esp32 fms-2-esp32 fms-7-esp32 fms-1 fms-2 fms-7`
no WSL 2 da autora, 27/09/2026, uma execução de cada: **6/6 PASS**. Tabelas
completas em [`aggregate.md`](aggregate.md).

Invariantes iguais aos da referência e das placas: 798 decifrações (190 no
ciclo 1), `edbd7971` e 405 + 393 no `fms-2`, a mesma divisão por nó no
`fms-7`. A emulação muda o tempo, não a lógica.

| nós | sem emulação, ciclo 1 | **com 69 ms/decifração**, ciclo 1 | ciclos 2–5 | nuvem (emulado), ciclo 1 | limite: nó mais carregado |
|---|---|---|---|---|---|
| 1 | 2,55 ms | **304,7 ms** | 241,5 ms | 299,5 ms | 298,0 ms |
| 2 | 5,25 ms (mais lento) | **193,2 ms** (1,6× mais rápido) | 148,6 ms | 192,7 ms | 164,7 ms |
| 7 | 7,27 ms (mais lento) | **90,5 ms** (3,4× mais rápido) | 61,3 ms | 87,2 ms | 64,3 ms |

1. **A inversão se reproduz numa segunda máquina.** Sem emulação, mais nós
   deixam o passo mais lento (2,55 → 5,25 → 7,27 ms); com a decifração a 69 ms,
   mais rápido (304,7 → 193,2 → 90,5 ms).
2. **Os tempos emulados quase não dependem da máquina:** WSL e nuvem diferem
   em 0,3–4 %, enquanto sem emulação o WSL é ~1,2–1,7× mais lento. Quando a
   decifração domina, a CPU deixa de importar, o que faz da emulação uma
   ferramenta de previsão reproduzível.
3. **O limite do nó mais carregado vale nas duas máquinas.** Com 1 nó o
   medido fica 2 % acima dele; com 2 e 7 nós, 26–28 ms acima, que é o custo
   de coordenação e sincronização entre eventos compartilhados.

Ressalva: n = 1 por cenário. A consistência entre as duas máquinas sugere
baixa variância nos cenários emulados, mas para o artigo vale repetir.
