# S5 isolado × blocos contíguos (referência na nuvem, n = 1)

`scripts/run-all.sh s5`, 27/09/2026: a mesma varredura de 1 a 7 containers,
agora com duas partições para cada N de 2 a 6. **12/12 PASS**; em todas, 798
decifrações (190 no ciclo 1), 220/220 passos e oráculo PASS. A partição muda
quem faz cada decifração, não quantas são.

- **blocos** (`fms-N`): a partição que o motor deriva, em blocos contíguos.
- **S5 isolado** (`fms-N-s5`): o supervisor S5 sozinho num container; os
  outros 6 distribuídos para minimizar as decifrações do container mais
  carregado no ciclo 1 (`DES_SUP_NODE_MAP`, ver os cenários).

Tabela completa em [`escala.md`](escala.md). Tempo por passo em ms:

| containers | partição S5 isolado | ciclo 1: blocos | ciclo 1: S5 | Δ | ciclos 2–5: Δ | limite: blocos → S5 |
|---|---|---|---|---|---|---|
| 2 | S0 S1 S2 S3 S4 S6 · S5 | 192,7 | 238,0 | +23,5 % | +39,6 % | 164,7 → 233,7 |
| 3 | S0 S2 S6 · S1 S3 S4 · S5 | 146,9 | 141,6 | −3,6 % | +6,0 % | 123,9 → 123,9 |
| 4 | S0 S1 · S2 S6 · S3 S4 · S5 | 130,7 | 115,5 | −11,6 % | −6,6 % | 105,1 → 91,0 |
| 5 | S0 S1 · S2 S3 · S4 · S6 · S5 | 106,1 | 106,1 | 0,0 % | +1,8 % | 76,8 → 67,4 |
| 6 | S0 S2 · S1 · S3 · S4 · S6 · S5 | 96,4 | 94,8 | −1,7 % | +0,3 % | 65,9 → 64,3 |

## Leitura (preliminar: uma execução por configuração)

1. **Isolar o S5 só compensa com 4 containers.** Com 4, o ciclo 1 fica 11,6 %
   mais rápido e os ciclos 2–5, 6,6 %, acompanhando a queda do limite
   (105,1 → 91,0 ms). É o único N em que as duas fases melhoram.
2. **Com 2 containers é muito pior (+23,5 %).** Isolar o S5 deixa os outros
   6 supervisores juntos, com 149 decifrações no ciclo 1 contra 105 na
   partição em blocos. Foi o previsto.
3. **Os ciclos 2–5 quase não ganham.** Depois do ciclo 1 o supervisor mais
   pesado é o S6 (28 decifrações por ciclo, contra 22 do S5), então isolar o
   S5 ataca o gargalo do ciclo 1, não o dos seguintes.
4. **Baixar o limite não basta.** Com 5 containers o limite cai de 76,8 para
   67,4 ms, mas o tempo medido não muda (106,1 ms nas duas partições) e fica
   38,7 ms acima do limite, contra 25–33 ms nas outras configurações. O limite
   só conta o nó mais carregado no ciclo inteiro; ele não vê *quando* cada nó
   trabalha. Se o trabalho de nós diferentes cai nos mesmos trechos entre
   eventos compartilhados, eles se esperam. Um modelo pelo caminho crítico ao
   longo do roteiro explicaria isso melhor, e não foi feito.
5. **Diferenças pequenas precisam de repetição.** Com 5 repetições, o IC 95 %
   dos tempos foi ≤ 1,3 ms. Diferenças de 5 ms ou mais (N = 2, 3, 4) devem se
   manter; as de N = 5 e 6 (≤ 1,6 ms) não se distinguem com uma execução.
   Para confirmar: `REPEAT=5 scripts/run-all.sh s5`.
