# WSL: sobrecarga do container (ponte × host × nativo), 5 repetições

`REPEAT=5 scripts/run-all.sh sobrecarga` no WSL 2 da autora, 28/09/2026: FMS,
família modular local completa, decifração emulada a 69 ms, 1, 2, 4 e 7 nós.
Os nós rodaram em três lugares, sempre com **os mesmos binários** (uma
imagem por N, estáticos, `-DDES_MCAST_LOOP=1`):

- **ponte**: um container por nó na rede *bridge* `cell` (veth + bridge),
  como a varredura principal;
- **host**: um container por nó na pilha de rede do host
  (`compose.host.yaml`), sem veth nem bridge;
- **nativo**: sem Docker na execução, processos comuns no WSL.

**55/55 execuções PASS**, nenhuma retransmissão, e as mesmas impressões
digitais nos três modos (`3f2beff2`, `edbd7971`, `457cc268`, `04511541`).
Tabelas em [`sobrecarga.md`](sobrecarga.md); percentis em
[`latencia.md`](latencia.md); registro completo em `sob-rep5.log`.

## Tempo por passo (ms, média ± dp, n = 5)

Δ = modo − ponte, com IC 95 % de Welch.

| nós | modo | ciclo 1 | Δ ciclo 1 | ciclos 2–5 | Δ ciclos 2–5 |
|---|---|---|---|---|---|
| 1 | ponte | 303,4 ± 2,4 | — | 241,0 ± 1,0 | — |
| 1 | nativo | 304,2 ± 2,8 | +0,7 [−3,1; +4,5] | 241,0 ± 1,0 | −0,1 [−1,5; +1,4] |
| 2 | ponte | 196,1 ± 1,4 | — | 149,4 ± 0,1 | — |
| 2 | host | 196,4 ± 0,2 | +0,3 [−1,4; +2,0] | 149,1 ± 0,7 | −0,3 [−1,1; +0,5] |
| 2 | nativo | 195,4 ± 1,4 | −0,7 [−2,7; +1,4] | 148,9 ± 0,8 | −0,5 [−1,4; +0,5] |
| 4 | ponte | 132,7 ± 1,2 | — | 93,6 ± 0,6 | — |
| 4 | host | 132,6 ± 1,1 | −0,1 [−1,8; +1,6] | 93,5 ± 0,6 | −0,0 [−1,0; +0,9] |
| 4 | nativo | 132,5 ± 1,0 | −0,2 [−1,8; +1,4] | 93,5 ± 0,7 | −0,1 [−1,1; +0,8] |
| 7 | ponte | 89,4 ± 1,5 | — | 61,1 ± 0,6 | — |
| 7 | host | 89,7 ± 1,3 | +0,2 [−1,8; +2,2] | 61,0 ± 0,6 | −0,1 [−0,9; +0,8] |
| 7 | nativo | 89,6 ± 1,3 | +0,2 [−1,9; +2,2] | 60,9 ± 0,6 | −0,1 [−1,0; +0,7] |

**Nenhuma diferença é estatisticamente distinguível de zero**: todos os
18 intervalos contêm o zero, e as médias diferem no máximo 0,7 ms. O que o
experimento permite afirmar é um limite superior. Com 95 % de confiança, o
container (na ponte, contra processos nativos) custa no máximo:
- **1,6 %** do tempo por passo nos ciclos 2–5. É o limite inferior do IC de
  nativo − ponte, com o sinal trocado: 1,5 ms em 241 com 1 nó (0,6 %), 1,4 em
  149 (0,9 %), 1,1 em 93,6 (1,2 %) e 1,0 em 61,1 (1,6 %);
- **2,1 %** no ciclo 1: 3,1 ms em 303 (1,0 %), 2,7 em 196 (1,4 %), 1,8 em
  133 (1,4 %) e 1,9 em 89,4 (2,1 %).

Com n = 5, uma sobrecarga maior que isso teria aparecido como diferença
significativa.

## A parte da rede

É onde o container poderia custar algo: a ponte põe um par veth e uma bridge
no caminho de cada quadro.

| nós | modo | RTT de aplicação (ms) | espera 2PC p50 | espera NOTIFY p50 |
|---|---|---|---|---|
| 2 | ponte / host / nativo | 3,92 / 3,93 / 3,77 | 5,8 / 5,0 / 5,0 | 1,7 / 1,6 / 1,6 |
| 4 | ponte / host / nativo | 4,28 / 3,93 / 3,91 | 5,4 / 5,5 / 5,6 | 1,6 / 1,5 / 1,5 |
| 7 | ponte / host / nativo | 9,55 / 10,31 / 10,37 | 5,6 / 5,6 / 5,7 | 1,7 / 1,6 / 1,6 |

- **O RTT é o mesmo com e sem container**, inclusive nos processos nativos.
  Logo, os ~4 ms (~10 ms com 7 nós) não vêm do caminho de rede do kernel,
  mas do próprio laço do motor (sondagem do socket e processamento do quadro,
  igual nos três modos). Com 7 nós o RTT sobe porque o nó 1 atende mais
  pares durante as sondas. Nenhuma diferença de RTT é significativa (ICs em
  `sobrecarga.md`).
- **A espera pelos pares também não muda**: ~5,5 ms no 2PC e ~1,6 ms no
  NOTIFY em qualquer modo. A resolução aqui é de décimos de ms. Um custo de
  veth + bridge da ordem de microssegundos por quadro não aparece nessa escala.

## Leitura

- Nesta aplicação, **o container não tem custo mensurável**: nem a CPU (a
  decifração emulada e o passo homomórfico duram o mesmo), nem a rede (a
  ponte não se distingue da rede do host nem de processos nativos). Isso
  concorda com a literatura: o isolamento por namespaces não interpõe um
  hipervisor [12], e o custo de rede dos containers em controle virtualizado
  é pequeno para ciclos de ms [3], [9]–[11] (numeração de
  [`docs/literatura.md`](../../literatura.md)).
- Portanto, a escolha "um supervisor = um container" não traz custo de
  desempenho mensurável. O que limita o tempo por passo é a criptografia (o
  nó mais carregado) e o protocolo, não a embalagem.
- **Sem efeito colateral nos binários.** A série ponte, que usa binários
  estáticos com o loop de multicast, repete a varredura principal com
  binários dinâmicos: 7 nós, 89,4 ± 1,5 e 61,1 ± 0,6 contra 90,3 ± 0,7 e
  61,3 ± 0,3 ms/passo.

## Limites

- A decifração emulada (69 ms) é espera, não cálculo. Então a CPU quase não
  é exercida, e o limite de 1 CPU por container (que o modo nativo não tem)
  quase não pesa. Com a emulação desligada (`DES_EMU_SCALARMUL_MS=0`), o
  protocolo e a rede pesariam proporcionalmente mais. Esse teste não foi
  feito, porque a varredura usa só a emulação.
- Tudo roda numa máquina só: a "rede" é memória. Num enlace real (Wi-Fi,
  como nas placas), a rede muda, mas a diferença entre container e processo
  continua sendo só o par veth + bridge.
- Os intervalos da célula em `latencia.md` (só ponte e host, pois o nativo
  não tem carimbos do Docker) também passaram pelo filtro do relógio do WSL:
  356 conclusões e 7 ciclos descartados.
