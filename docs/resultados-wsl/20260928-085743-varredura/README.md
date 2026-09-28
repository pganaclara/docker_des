# WSL: robustez a perda de quadros, com emulação, 5 repetições

`REPEAT=5 scripts/run-all.sh perda` no WSL 2 da autora, 28/09/2026: FMS,
família modular local completa, decifração emulada a 69 ms, *timeouts* do
motor como no ESP32 (1,5 s; 4 tentativas de REQ, 5 de COMMIT/NOTIFY). Cada
nó descarta P % dos quadros que recebe, depois da autenticação
(`DES_SIMULATE_LOSS_PCT`), com semente nova por nó e por execução (todas
diferentes, registradas no `@@RESULT`). 2 nós (a partição das placas) com 1 a
30 %, 7 nós com 1 a 10 %. **40/40 execuções PASS.** Tabelas em
[`perda.md`](perda.md); registro completo em `perda-rep5.log`.

## Segurança: nenhuma divergência em 40 execuções

Em **todas as 40 execuções**, inclusive as que pararam ou pularam passos:
- **consistência entre nós**: cada par de nós executou os eventos
  compartilhados que tem em comum na mesma ordem e o mesmo número de vezes;
- **oráculo homomórfico PASS** em todo nó: cada bit cifrado bateu com o
  modelo em claro.

Nos 4 SAFE HALT, a única diferença entre os nós é **um** evento, o COMMIT ou
NOTIFY em voo quando a célula parou, que é exatamente o caso que a parada
existe para conter. Nada além disso.

## Desfecho

| nós | perda | completa | SAFE HALT | incompleta | passos executados (de 220) | retransmissões |
|---|---|---|---|---|---|---|
| 2 | 1 % | 5 | 0 | 0 | 220 | 1,6 ± 1,5 |
| 2 | 5 % | 5 | 0 | 0 | 220 | 15,6 ± 5,1 |
| 2 | 10 % | 5 | 0 | 0 | 220 | 23,8 ± 3,7 |
| 2 | 20 % | 5 | 0 | 0 | 220 | 61,6 ± 10,4 |
| 2 | 30 % | 0 | **4** | 1 | 8, 13, 32, 78 (halt); 182 (38 pulados) | 36,2 ± 40,9 |
| 7 | 1 % | 5 | 0 | 0 | 220 | 19,0 ± 2,9 |
| 7 | 5 % | 5 | 0 | 0 | 220 | 87,6 ± 4,5 |
| 7 | 10 % | 0 | 0 | **5** | 148,2 ± 23,1 (36–97 pulados) | 218,8 ± 19,0 |

Os dois modos de falha aparecem, e cada um onde a teoria do protocolo diz:

- **2 nós, 30 %: SAFE HALT.** O dono manda o COMMIT (ou NOTIFY) e precisa do
  ACK do par. Com 30 % de perda de cada lado, uma tentativa falha com
  probabilidade 1 − 0,7² ≈ 0,51, e as 5 falham com ≈ 3,5 %. Em ~80 eventos
  compartilhados por execução, alguma acaba esgotando as tentativas. Como o
  COMMIT já saiu, o dono não sabe se o par aplicou; a única saída segura é
  parar, e o par para junto ("a peer halted"). Motivos registrados: "COMMIT
  unacknowledged" (2 vezes) e "NOTIFY unacknowledged" (2 vezes).
- **7 nós, 10 %: passos pulados, sem SAFE HALT.** No 2PC, o REQ precisa
  chegar aos 6 participantes e os 6 votos precisam voltar: 12 quadros, todos
  entregues com probabilidade 0,9¹² ≈ 0,28 por tentativa. As 4 tentativas
  falham com ≈ 27 %, e o dono **desiste antes do ponto de commit**: nada é
  aplicado em nenhum nó (SKIP). Os eventos que dependiam dele também não
  acontecem, e daí vêm os 36 a 97 passos pulados. A fase de votação funciona
  como filtro: a perda pesada é barrada antes de poder criar inconsistência.
- A execução de 2 nós a 30 % que não parou (182 passos, 38 pulados) mostra
  os dois mecanismos na mesma célula.

Isso reproduz, agora com 5 repetições e a emulação ligada, o que a execução
única anterior sem emulação tinha mostrado (arquitetura §7.6).

## Custo em tempo: cada retransmissão custa um *timeout*

Tempo por passo das execuções completas, ciclos 2–5 (sem perda: 2 nós ≈ 149,
7 nós ≈ 61 ms):

| nós | perda | ms/passo | acréscimo | retransmissões × 1,5 s ÷ 220 passos |
|---|---|---|---|---|
| 2 | 1 % | 162,5 ± 15,5 | +14 | 11 |
| 2 | 5 % | 247,2 ± 34,2 | +98 | 106 |
| 2 | 10 % | 329,0 ± 34,0 | +180 | 162 |
| 2 | 20 % | 605,4 ± 87,4 | +456 | 420 |
| 7 | 1 % | 201,4 ± 9,9 | +140 | 130 |
| 7 | 5 % | 763,1 ± 62,7 | +702 | 597 |

- O acréscimo acompanha **retransmissões × *timeout***: quase todo o custo da
  perda é tempo parado esperando o *timeout* de 1,5 s expirar, não trabalho
  refeito.
- **Com 7 nós a célula é bem mais sensível:** 1 % de perda já triplica o
  tempo por passo (61 → 201 ms), e 5 % multiplica por 12,5. Cada 2PC depende
  de 12 quadros em vez de 2, então a chance de alguma tentativa precisar de
  retransmissão cresce com o número de participantes. Distribuir acelera sem
  perda (varredura principal), mas amplifica o custo da perda. É um
  *trade-off* a declarar.
- O *timeout* de 1,5 s foi mantido de propósito: é o do ESP32, dimensionado
  para um participante que passa até centenas de ms (e, na placa, segundos)
  num passo homomórfico. Reduzi-lo aceleraria a recuperação (arquitetura
  §7.5), mas deixaria de replicar o firmware.

## Limites

- A perda é independente por quadro e por receptor (Bernoulli). Wi-Fi real
  tem perdas em rajada, que tendem a esgotar as tentativas mais cedo.
- Só perda: atraso e reordenação não foram injetados (o `netem` foi retirado
  do repositório).
- 5 repetições por nível: os números de SAFE HALT e de pulos são contagens
  pequenas. O resultado de segurança não depende disso: 40 de 40 execuções,
  nenhuma divergência.
