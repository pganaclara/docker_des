# Roteiro de capítulos da dissertação

Proposta de estrutura a partir do que o repositório já tem. Para cada
capítulo: o que ele precisa estabelecer, as seções, de onde vem o material
(documentos e pastas de resultados deste repositório), figuras e tabelas
sugeridas e as referências de [`literatura.md`](literatura.md) (a mesma
numeração). Os números citados são os das execuções no WSL com 5 repetições.

**Título provisório:** *Supervisores modulares locais com estado cifrado em
containers: implantação distribuída, equivalência com o ESP32 e avaliação*

**Pergunta central:** o controle supervisório modular local com estado
cifrado (EC-ElGamal), já executado em placas ESP32, pode ser implantado com
um supervisor por container, sendo comprovadamente o mesmo sistema, e o que
a distribuição custa ou rende em tempo, latência e robustez?

**Contribuições** (vão na introdução e voltam na conclusão):
1. Uma implantação de supervisores da TCS em containers, um por supervisor,
   comunicando só por UDP multicast autenticado. Não foi encontrado trabalho
   publicado que faça isso ([`literatura.md`](literatura.md) §7).
2. Um método para provar a equivalência com o firmware: motor idêntico por
   hash, invariantes de contagem de decifrações e impressão digital da
   configuração, verificados automaticamente em cada execução.
3. A emulação do custo criptográfico do ESP32 no container, que transforma o
   container num modelo de desempenho da placa sem alterar a lógica.
4. Uma avaliação experimental com repetições e intervalos de confiança:
   escala de 1 a 7 nós e seu limite, latência e *jitter*, efeito da
   partição, sobrecarga do container e robustez a perda com verificação de
   consistência entre nós.

---

## 1. Introdução

**Precisa estabelecer:** o problema, a lacuna e o que a dissertação entrega.

- 1.1 Contexto: manufatura flexível, controle supervisório, a tendência de
  levar controle industrial para containers (PLC virtual).
- 1.2 Motivação: estado do supervisor cifrado (privacidade do estado da
  planta) e distribuição (um supervisor por nó). O trabalho anterior nas
  placas ESP32 e seus limites (poucos nós, flash, custo de montar a bancada).
- 1.3 Lacuna: containers já executam lógica IEC 61131/61499, e a TCS
  distribuída roda em CLPs, mas não há supervisores sintetizados com estado
  cifrado em containers.
- 1.4 Objetivos (geral e específicos) e pergunta de pesquisa.
- 1.5 Contribuições (as quatro acima).
- 1.6 Organização do texto.

**Fontes:** [`literatura.md`](literatura.md) "Resumo em uma página", §7 (a
lacuna); [`../README.md`](../README.md) (visão geral).
**Referências:** [1]–[11], [14], [16], [22], [27]–[29].

## 2. Fundamentação teórica

**Precisa estabelecer:** o vocabulário que os capítulos seguintes usam.

- 2.1 Sistemas a eventos discretos e a Teoria de Controle Supervisório
  (Ramadge–Wonham): autômatos, eventos controláveis e não controláveis,
  supervisor. [14], [26]
- 2.2 Controle modular local: supervisores locais, conjunção, a condição de
  não conflito. Por que se usa a família completa, que carrega a planta, e
  não a reduzida: a reduzida pode aceitar um evento fisicamente impossível.
  [16], [17]
- 2.3 Controle distribuído e em rede: localização de supervisores, eventos
  compartilhados, atraso e perda. [15], [18]–[23]
- 2.4 Controle criptografado: cifras homomórficas, EC-ElGamal na curva
  secp192r1, OR homomórfico e teste de zero na decifração. [27]–[29]
- 2.5 Protocolos de acordo distribuído: *two-phase commit*, *wound-wait*,
  argumento fim a fim, multicast IP. [33]–[36]
- 2.6 Containers: namespaces, cgroups, redes *bridge* e host, imagens como
  artefato de reprodutibilidade. [12], [13]
- 2.7 Lei de Amdahl: o limite de aceleração que o capítulo 7 usa. [43]

**Fontes:** [`literatura.md`](literatura.md) §2–§6.

## 3. Trabalhos relacionados

**Precisa estabelecer:** onde este trabalho se encaixa e o que é novo.

- 3.1 Controle industrial em containers (vPLC): o que se mede (latência,
  *jitter*, perdas de prazo), com quais ferramentas e o que concluem. [1]–[11]
- 3.2 Supervisores em controladores reais: CLPs, *hardware-in-the-loop*,
  supervisores distribuídos com atraso. [22], [24], [25]
- 3.3 Controle criptografado em rede. [27]–[29]
- 3.4 Bancadas de rede emuladas. [30]–[32]
- 3.5 Síntese e lacuna: tabela comparativa (containers? supervisores da
  TCS? estado cifrado? distribuído? avaliação com repetições?).

**Fontes:** [`literatura.md`](literatura.md) §1–§7.
**Tabela:** comparação com os trabalhos mais próximos ([22], [9]–[11]).

## 4. O sistema de referência: supervisores cifrados em ESP32

**Precisa estabelecer:** o sistema que será portado e seus números, que são
a referência de equivalência.

- 4.1 O FMS: 7 supervisores modulares locais, 31 eventos, a sequência de 44
  passos por ciclo, 5 ciclos.
- 4.2 O motor genérico (`des_generic.h`): roteamento derivado do cabeçalho,
  passo homomórfico, oráculo em claro.
- 4.3 O protocolo: 2PC para eventos controláveis compartilhados,
  NOTIFY→ACK para não controláveis, *wound-wait*, SAFE HALT, quadros de 44 B
  com HMAC-SHA256/128, desafio de época, impressão digital da configuração.
- 4.4 A bancada com 2 placas: partição S0–S3 · S4–S6, 405 + 393 decifrações,
  impressão digital `edbd7971`, 296,9 ms/passo no ciclo 1.

**Fontes:** repositório `esp32_crypto` (README, `des_distributed/`);
[`../engine/UPSTREAM.md`](../engine/UPSTREAM.md); [`arquitetura.md`](arquitetura.md) §1–§2.
**Figuras:** diagrama da troca de mensagens do 2PC e do NOTIFY, incluindo o
SAFE HALT; tabela de roteamento dos eventos.

## 5. Implantação em containers

**Precisa estabelecer:** o que mudou, o que não mudou e por quê.

- 5.1 Arquitetura: um container por nó, rede *bridge* `cell`, UDP multicast
  239.192.7.1:5077, chave da célula como *Docker secret*, usuário sem
  privilégio.
- 5.2 O que mudou e o que não mudou: motor byte a byte idêntico (hashes
  conferidos no build), só o ponto de entrada é novo.
- 5.3 Um binário por nó: o roteamento é resolvido na compilação, como no
  firmware.
- 5.4 Escolha da linguagem: por que C++ (reaproveitar o motor, a mesma
  mbedTLS 3.6, medição sem coletor de lixo) e quando outra faria sentido.
- 5.5 Emulação do custo do ESP32: `--wrap=mbedtls_ecp_mul`, cada decifração
  leva ≥ 69 ms. Por que a emulação é necessária: sem ela o PC decifra rápido
  demais e o protocolo passa a dominar (o experimento que motivou isso,
  arquitetura §7.3–§7.4).
- 5.6 Reprodutibilidade: Dockerfile, cenários, scripts, BUILD_INFO por
  execução.

**Fontes:** [`arquitetura.md`](arquitetura.md) §1–§4, §7.3–§7.4;
[`../Dockerfile`](../Dockerfile), [`../compose.yaml`](../compose.yaml),
[`../src/des_container_main.cpp`](../src/des_container_main.cpp).
**Figuras:** arquitetura (containers, rede, *secret*); pipeline de build.

## 6. Metodologia experimental

**Precisa estabelecer:** que os resultados são confiáveis e verificáveis.

- 6.1 Ambiente: WSL 2 com Ubuntu, Docker Engine, 1 CPU por container, kernel
  genérico sem PREEMPT_RT (tempos comparativos, não de tempo real).
- 6.2 Métricas: tempo por passo no relógio do motor (ciclo 1 e ciclos 2–5),
  latência de decisão e de aplicação, intervalo da célula, RTT, espera pelos
  pares, retransmissões e desfechos.
- 6.3 Verificações automáticas em toda execução: impressão digital,
  decifrações (798; 190 no ciclo 1), oráculo, autoteste criptográfico,
  consistência entre nós.
- 6.4 Planejamento: 5 repetições por configuração, média ± dp, IC 95 %
  (Welch para diferenças), sementes de perda diferentes por execução.
- 6.5 Tratamento dos dados: o salto do relógio do WSL e como ele é detectado
  e descartado.
- 6.6 Artefatos: onde estão os logs e como reproduzir cada tabela.

**Fontes:** [`arquitetura.md`](arquitetura.md) §5, §6.5;
[`../scripts/`](../scripts/) (`summarize.py`, `scaling.py`, `latency.py`,
`overhead.py`, `loss.py`).
**Tabela:** matriz de experimentos (pergunta → cenários → repetições →
métrica), a partir de [`literatura.md`](literatura.md) §9.

## 7. Resultados

Uma seção por pergunta, sempre com: tabela, IC, leitura e o que isso
permite afirmar.

- **7.1 Equivalência com as placas.** `fms-2` reproduz `edbd7971` e as
  405 + 393 decifrações; 798 decifrações com qualquer número de nós.
  Arquitetura §5 e §6.1.
- **7.2 Escala de 1 a 7 containers.** 303,1 ± 1,3 → 90,1 ± 1,0 ms/passo
  (3,37×; IC 95 %) no ciclo 1; o limite do nó mais carregado e a distância a ele;
  Amdahl. Arquitetura §6.2–§6.3;
  [`resultados-wsl/20260927-170420-varredura`](resultados-wsl/20260927-170420-varredura/README.md).
  *Figura:* ms/passo × nós, com o limite; aceleração × nós.
- **7.3 Efeito da partição.** S5 isolado só compensa com 4 containers
  (−11,6 % e −6,8 %) e piora muito com 2. Arquitetura §6.4;
  [`resultados-wsl/20260927-200439-varredura`](resultados-wsl/20260927-200439-varredura/README.md).
- **7.4 Latência e *jitter*.** Degraus de uma decifração; p99 − p50 ≤ 3,1 ms;
  o pior caso cai 5,9× contra 3,9× na média. Arquitetura §6.5;
  [`resultados-wsl/20260927-210233-varredura`](resultados-wsl/20260927-210233-varredura/README.md).
  *Figura:* distribuição da latência 2PC por número de nós (dados em
  `latencia.csv`, regenerável).
- **7.5 Sobrecarga do container.** Ponte × host × nativo: os 18 IC contêm o
  zero; sobrecarga < 1,6 % nos ciclos 2–5 e < 2,1 % no ciclo 1. Arquitetura
  §6.6;
  [`resultados-wsl/20260928-002448-varredura`](resultados-wsl/20260928-002448-varredura/README.md).
- **7.6 Robustez a perda.** 40/40 sem divergência. 2 nós: SAFE HALT a 30 %;
  7 nós: SKIP antes do commit a 10 %. Acréscimo de tempo ≈ retransmissões ×
  *timeout*; 7 nós são mais sensíveis à perda. Arquitetura §6.7;
  [`resultados-wsl/20260928-085743-varredura`](resultados-wsl/20260928-085743-varredura/README.md).
  *Figura:* desfechos por nível de perda (barras empilhadas); ms/passo ×
  perda para 2 e 7 nós.

## 8. Discussão

**Precisa estabelecer:** o que os resultados significam, juntos.

- 8.1 Distribuição lógica × física: o que o container prova (protocolo,
  equivalência, segurança) e o que só uma rede real mediria.
- 8.2 O gargalo é a criptografia do nó mais carregado, não o container nem a
  rede virtual. Consequência para a escolha da partição.
- 8.3 O *trade-off* da distribuição: acelera sem perda, mas amplifica o custo
  da perda (12 quadros por 2PC com 7 nós contra 2 com 2 nós).
- 8.4 Segurança × vivacidade: os dois modos de falha (SKIP antes do commit,
  SAFE HALT depois) e o paralelo com os Dois Generais.
- 8.5 *Timeouts* do ESP32 como parâmetro de projeto: proporcionais ao passo
  homomórfico mais lento, não ao RTT (arquitetura §7.5).
- 8.6 Comparação com a literatura de vPLC: onde os números se situam e por
  que não são afirmações de tempo real.
- 8.7 Ameaças à validade: interna (emulação só da decifração, relógio do
  WSL), externa (uma máquina, perda sintética independente, sem atraso
  injetado, FMS sem supervisor monolítico), de construto (controlabilidade
  inferida pelo rótulo).

**Fontes:** [`arquitetura.md`](arquitetura.md) §6.3, §7.5–§7.6, §8;
[`literatura.md`](literatura.md) §1 "O que isso significa", §8.

## 9. Conclusão

- 9.1 Resposta à pergunta de pesquisa, em um parágrafo.
- 9.2 Contribuições, retomadas com os números.
- 9.3 Limitações (resumo do 8.7).
- 9.4 Trabalhos futuros: nós em máquinas separadas numa rede real (Wi-Fi ou
  cabo, com o WSL em modo *mirrored*); atraso e perda em rajada; partições
  buscadas automaticamente; PREEMPT_RT para afirmações de tempo real; outros
  problemas com supervisor monolítico disponível; mais de 7 nós.

## Apêndices

- A. Reprodução passo a passo: instalação no WSL, geração da chave, cada
  comando `run-all.sh` e onde sai cada tabela ([`../README.md`](../README.md)).
- B. Formato do quadro de 44 B e do `@@RESULT`.
- C. Tabelas completas por execução (`summary.md` de cada pasta em
  [`resultados-wsl/`](resultados-wsl/)).
- D. Hashes do motor e correspondência com o commit do `esp32_crypto`
  ([`../engine/SHA256SUMS`](../engine/SHA256SUMS), [`../engine/UPSTREAM.md`](../engine/UPSTREAM.md)).

---

## Onde cada afirmação aparece

| afirmação | capítulo | evidência |
|---|---|---|
| O container executa o mesmo sistema que as placas | 5, 7.1 | hashes do motor; `edbd7971`, 405 + 393 |
| Distribuir não aumenta o trabalho criptográfico | 7.1 | 798 decifrações em qualquer N |
| Distribuir acelera, limitado pelo nó mais carregado | 7.2, 8.2 | 3,37×; limite de Amdahl |
| A partição importa e não há uma melhor para todo N | 7.3 | S5 isolado × blocos |
| A latência é previsível e o pior caso melhora | 7.4 | degraus de 69 ms; máximo 498 → 84 ms |
| O container não custa desempenho mensurável | 7.5 | < 1,6 %, 18/18 IC com zero |
| O protocolo é seguro sob perda | 7.6, 8.4 | 40/40 sem divergência |
| Distribuir amplifica o custo da perda | 7.6, 8.3 | 1 % de perda: 61 → 201 ms com 7 nós |
