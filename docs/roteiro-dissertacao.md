# Roteiro da dissertação

A dissertação (abnTeX2, PPGEE/UFMG, em inglês) se chama *Secure Supervisory
Control of Discrete Event Systems using Homomorphic Encryption*. O trabalho
com containers deste repositório é uma parte dela: §4.8 (metodologia) e §5.8
(resultados), além de trechos da introdução, da discussão e da conclusão.
Este roteiro mostra a estrutura atual (versão v4 do projeto Overleaf), onde
entra cada resultado do `docker_des` e o que ainda falta.

## Estrutura atual

| cap. | título | conteúdo | origem |
|---|---|---|---|
| 1 | Introduction | motivação (CPS, ataques passivos, EC-ElGamal), objetivos, organização | — |
| 2 | Preliminary Concepts | linguagens, autômatos, TCS monolítica e modular local, redução, curvas elípticas, EC-ElGamal e homomorfismo | — |
| 3 | State of the Art | cibersegurança de SED, HE em controle, representação matricial, TCS distribuída/em rede, **controle em containers** (§3.5), posicionamento | [`literatura.md`](literatura.md) |
| 4 | Proposed Methodology | codificação e EC-ElGamal (1ª implementação), evolução, síntese, avaliação homomórfica (vetor indicador, teste de zero), otimizações, arquitetura distribuída (2PC, NOTIFY, *wound-wait*, SAFE HALT, HMAC), **implantação em containers** (§4.8) | `esp32_crypto`; [`arquitetura.md`](arquitetura.md) §1–§5 |
| 5 | Results | pequena fábrica no ESP32, fábrica estendida e FMS, benchmark no ESP32-S3, 2 placas, **containers** (§5.8), discussão | resultados abaixo |
| 6 | Conclusions | síntese, compromissos, trabalhos futuros | — |

## §5.8 Execution in Containers: o que cada subseção usa

| subseção | resultado | pasta de resultados | na v3? |
|---|---|---|---|
| 5.8.1 Equivalence with the Boards | `edbd7971`, 405 + 393, 798 decifrações | [`20260927-170420-varredura`](resultados-wsl/20260927-170420-varredura/README.md) | sim |
| 5.8.2 Scaling from One to Seven Containers | 303,1 → 90,1 ms/passo (3,37×; IC 95 %), limite do nó mais carregado | [`20260927-170420-varredura`](resultados-wsl/20260927-170420-varredura/README.md), [`resultados/escala`](resultados/escala/README.md) | sim |
| 5.8.3 Choice of the Partition | S5 isolado só compensa com 4 containers | [`20260927-200439-varredura`](resultados-wsl/20260927-200439-varredura/README.md) | **novo na v4** |
| 5.8.4 Latency and Jitter per Step | degraus de 69 ms, *jitter* ≤ 3,1 ms, pior caso 498 → 84 ms | [`20260927-210233-varredura`](resultados-wsl/20260927-210233-varredura/README.md) | **novo na v4** |
| 5.8.5 Overhead of the Container | ponte × host × nativo: 14/14 IC com zero, < 1,6 % | [`20260928-002448-varredura`](resultados-wsl/20260928-002448-varredura/README.md) | **novo na v4** |
| 5.8.6 Robustness to Frame Loss | 40/40 sem divergência; SAFE HALT (2 nós, 30 %) e SKIP (7 nós, 10 %) | [`20260928-085743-varredura`](resultados-wsl/20260928-085743-varredura/README.md) | **novo na v4** |
| 5.8.7 Preliminary Experiments | sem emulação, *timeouts*, perda pesada (1ª versão), `netem` | commit [`b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775) | sim (agora remete a 5.8.6) |

## O que mudou da v3 para a v4

- **§3.5:** Felter et al. (2015) sobre o custo de containers; nova entrada
  `felter2015updated` no `references.bib`.
- **§4.8:** a verificação de consistência entre nós, os modos host e nativo
  e a semente de perda por nó e por execução.
- **§5.8:** a introdução cita as 190 execuções extras; entram as quatro
  subseções novas (tabelas 15 a 18); as "Preliminary Experiments" remetem ao
  teste de perda com emulação.
- **§5.9 Discussion:** dois parágrafos novos ("o container não é o gargalo,
  mas a rede pode ser"; "segurança preservada, vivacidade não") e três
  limitações: distribuição lógica × física, perda sintética sem atraso e o
  relógio do WSL.
- **Cap. 6:** um parágrafo com os resultados novos; a limitação de uma
  máquina só; trabalhos futuros com núcleo de tempo real e nós em máquinas
  separadas numa rede real.
- **Resumo e Abstract:** uma frase sobre a sobrecarga e a perda.
- `compile-cache/` regenerado (a primeira compilação no Overleaf continua
  rápida). Compilado do zero com TeX Live 2023: 79 páginas, nenhuma
  referência indefinida; os únicos avisos já existiam na v3.

## Ainda falta (fora do trabalho com containers)

- Elementos pré-textuais de modelo: dedicatória (`xxx`), agradecimentos
  (*lorem ipsum*), epígrafe (`aaaaa`, citando `sinek2018comece`), ficha
  catalográfica e folha de aprovação (comentadas até haver as oficiais).
- Apêndice A "Large Table" com o texto `Test`: preencher ou remover.
- `back-matter/attachments.tex` ("Looney Tunes") não é incluído no
  `main.tex`: pode ser apagado.
- O `references.bib` ainda tem entradas do modelo (`saaty1986ahp`,
  `paradox_of_choice_book`, `ThomasL.Saaty1980`, `ho2008integrated`) e a
  figura `iteracao_dm_ahp.png`, que não são usadas no texto.
- Resultados de hardware com uma execução por configuração (limitação já
  declarada no texto).

## Onde cada afirmação do trabalho com containers aparece

| afirmação | seção | evidência |
|---|---|---|
| Os containers executam o mesmo sistema que as placas | 4.8, 5.8.1 | hashes do motor; `edbd7971`, 405 + 393 |
| Distribuir não aumenta o trabalho criptográfico | 5.8.1 | 798 decifrações em qualquer N |
| Distribuir acelera, limitado pelo nó mais carregado | 5.8.2 | 3,37×; limite de 298,0 → 64,3 ms |
| Balancear decifrações é necessário, mas não suficiente | 5.8.3 | S5 isolado × blocos |
| A latência é previsível e o pior caso melhora mais que a média | 5.8.4 | degraus de 69 ms; máximo 498 → 84 ms |
| O container não custa desempenho mensurável | 5.8.5 | < 1,6 %, 14/14 IC com zero |
| O protocolo é seguro sob perda | 5.8.6, 5.9 | 40/40 sem divergência |
| Distribuir amplifica o custo da perda | 5.8.6, 5.9 | 1 % de perda: 61 → 201 ms com 7 nós |
