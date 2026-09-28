# Revisão de literatura: supervisores SED distribuídos em containers

Este documento reúne a literatura que sustenta o `docker_des`: rodar os
supervisores do FMS (Sistema Flexível de Manufatura), um por container Docker,
conversando por UDP, com o mesmo motor criptográfico das placas ESP32 do
[`esp32_crypto`](https://github.com/pganaclara/esp32_crypto). Ele está
organizado para responder três perguntas:

1. **Como isso costuma ser feito?** (§1–§6)
2. **Onde está a lacuna que este trabalho ocupa?** (§7)
3. **Em que cada afirmação do trabalho pode se apoiar, e que experimentos a
   literatura espera ver?** (§8–§9)

As referências numeradas `[n]` estão no fim.

> **O resultado deste trabalho, em uma frase.** Com o custo de decifração do
> ESP32-S3 emulado (69 ms), distribuir os 7 supervisores modulares locais do
> FMS em 7 containers reduz o tempo por passo de 303,1 ± 1,3 ms para
> 90,1 ± 1,0 ms (3,37×; IC 95 %, n = 5). A aceleração é limitada pelo
> supervisor mais carregado, e cada configuração de 1 a 7 containers repete
> exatamente o resultado lógico das placas. Detalhes em
> [`arquitetura.md`](arquitetura.md) §6; como isso se situa na literatura,
> §8–§9 abaixo.

> **Como as referências foram conferidas.** Busca feita em setembro de 2026.
> No ambiente em que este texto foi escrito, as páginas das editoras (IEEE,
> ACM, Elsevier, Springer) e as bases (arXiv, Crossref, Semantic Scholar)
> estavam bloqueadas. Por isso autores, veículo, ano, páginas e DOI foram
> conferidos cruzando resultados de mecanismos de busca, e não na página da
> editora. Tudo o que não fechou está marcado com ⚠. **Antes de submeter um
> artigo, confira cada DOI na fonte.** As referências [14]–[16], [26], [28],
> [29] e [33]–[36] já estavam verificadas em
> `esp32_crypto/docs/code-explained.md` e foram reaproveitadas de lá.

---

## Resumo em uma página

| linha de pesquisa | o que costuma ser feito | referências-chave |
|---|---|---|
| **Controle industrial em containers** ("PLC virtual") | Lógica de controle de CLP (IEC 61131/61499) empacotada em containers numa plataforma de borda. Mede-se latência, *jitter* e perdas de prazo contra o CLP físico, com Linux PREEMPT_RT e redes *bridge*, *host* ou *macvlan*. A conclusão típica é que funciona para ciclos na faixa de ms (tempo real brando), com sobrecarga pequena. | [1]–[11] |
| **Controle supervisório distribuído e em rede** | Teoria: localização de supervisores, robustez a atraso, condições de controlabilidade e observabilidade em rede com atraso e perda. Implementação: supervisores em CLPs, validados em *hardware-in-the-loop*. | [14]–[25] |
| **Controle criptografado** | Controladores (quase sempre contínuos, lineares) avaliados sobre dados cifrados com cifras homomórficas, ElGamal inclusive, desde 2015. | [26]–[29] |
| **Bancadas de rede emuladas** | Nós como processos ou containers numa máquina, rede emulada com namespaces do Linux e `netem`. | [30]–[32] |
| **Reprodutibilidade** | Imagem Docker como artefato que fixa o ambiente do experimento. | [12], [13] |

**A lacuna (§7):** não foi encontrado trabalho publicado que execute
*supervisores da Teoria de Controle Supervisório (Ramadge–Wonham)* em
containers, e muito menos com o estado do supervisor cifrado. Os vizinhos mais
próximos são Schouten et al. [22] (supervisores distribuídos, com atraso, mas em
CLPs) e a linha de PLC virtual [9]–[11] (containers, mas executando lógica
IEC 61131, não supervisores sintetizados).

---

## 1. Controle industrial em containers: como se faz

**Origem.** A ideia de tirar a lógica de controle do CLP físico e colocá-la em
containers vem da indústria de automação. Goldschmidt e Hauck-Stattelmann
(ABB) [1] propuseram containers de software como unidade de implantação num
controlador multipropósito, com dois objetivos: emular código legado de CLP e
implantar funções novas com flexibilidade. A versão em periódico [2] detalha a
arquitetura, em que cada subsistema fica num container isolado dentro do
controlador. Moga, Sivanthi e Franke [3] fizeram a pergunta de viabilidade
("*are we there yet?*") para Docker com requisitos de tempo real.

**Arquiteturas.** Tasci, Melcher e Verl [4] modularizam aplicações de controle
em tempo real com containers, comunicação por mensagens e uma camada de
abstração de hardware, que é o mesmo padrão deste repositório (motor ↔
transporte ↔ plataforma). Telschig, Schönberger e Knapp [5] tratam
especificamente de aplicações embarcadas **distribuídas** e dependáveis em
containers (LXC), com criticidade de tempo que vai de tempo real rígido a
não-tempo-real.

**Determinismo e nuvem.** Hofer et al. [6] mostram, com testes de latência
dedicados, que executar controle crítico no tempo em containers numa
plataforma IaaS é viável, desde que o sistema seja configurado para isso
(núcleo de tempo real, isolamento de CPU).

**Levantamentos.** Struhár et al. [7] fizeram o levantamento sistemático de
como a comunidade traz propriedades de tempo real para containers. Depois
propuseram orquestração de containers de tempo real (REACT) [8]. Queiroz et
al. [9] (ACM Computing Surveys, 2023) é a revisão sistemática mais recente e
completa sobre virtualização por containers em sistemas industriais de tempo
real. **É a referência a citar para situar o trabalho nessa linha.**

**PLC virtual (vPLC), o estado atual.** Gaffurini et al. [10] avaliam PLCs
virtuais conteinerizados em plataforma de borda trocando dados com máquinas,
controladores e supervisores (M2M). A conclusão é que o vPLC se equipara ao
CLP real em tempo de comutação e resposta para aplicações abaixo de 10 ms, mas
a pilha IP introduz atrasos. Ben Kebaier et al. [11] comparam Docker e Podman
executando CODESYS e OpenPLC com PREEMPT_RT, e o Podman se mostra mais
previsível sem ajuste fino.

**Custo do container.** Felter et al. [12] mostram que containers têm
desempenho igual ou melhor que máquinas virtuais em quase todos os casos: o
isolamento por namespaces não interpõe um hipervisor.

**O que isso significa para este trabalho.**

- A escolha "um controlador = um container" é a prática estabelecida
  [1], [2], [9], [10]. Aqui ela vira "um **supervisor** = um container".
- A métrica que essa literatura cobra é **tempo**: latência, *jitter* e
  perdas de prazo. Os tempos da varredura (de 303,1 ms por passo com 1
  container a 90,1 ms com 7) são tempos com a decifração emulada a 69 ms, num
  kernel genérico. Eles se repetem bem: o coeficiente de variação entre
  execuções fica abaixo de 1 %, e duas máquinas diferentes discordam em só
  1,2–3,3 %. Mas não são tempos de ESP32 nem de CLP. Para afirmar algo de
  tempo real seria preciso PREEMPT_RT, CPU isolada e medição de percentis
  [6], [9], [11]. O que o `docker_des` prova sem ressalvas é outra coisa:
  **equivalência lógica e criptográfica** com o hardware (ver
  [`arquitetura.md`](arquitetura.md) §5), e a **forma** da curva de escala.

---

## 2. Controle supervisório distribuído e em rede: como se faz

**Base.** A Teoria de Controle Supervisório (TCS) de Ramadge e Wonham [14]
sintetiza supervisores corretos por construção, dada uma planta e uma
especificação. O controle **descentralizado** [15] estuda quando agentes com
visão parcial conseguem decidir corretamente (co-observabilidade). O controle
**modular local** de de Queiroz e Cury [16] sintetiza um supervisor pequeno
por especificação em vez de um monolítico, que é exatamente a decomposição
que o FMS usa (7 supervisores) e que este repositório distribui. O manual de
referência é Cassandras e Lafortune [26].

**Localização de supervisores.** Cai e Wonham [18] propõem a abordagem
"de cima para baixo": sintetiza-se o supervisor global e ele é *localizado*
em controladores locais, um por agente, que se comunicam. O motor do
`esp32_crypto` segue o mesmo espírito: parte dos supervisores modulares
sintetizados e deriva a partição, o roteamento de eventos e quem precisa
conversar com quem a partir do cabeçalho gerado.

**Atraso e perda na comunicação.** Esse é o problema que aparece quando os
supervisores saem de um CLP e vão para uma rede:

- Zhang et al. [19] definem **robustez a atraso**: controladores distribuídos
  cujo comportamento com atraso é logicamente equivalente ao sem atraso, com
  um teste computacional para verificá-la.
- Lin [20] estuda sistemas a eventos discretos **em rede** com atrasos e
  perdas na observação e no controle, e dá condições de existência de
  supervisor.
- Zhu et al. [21] fazem o panorama (2023) de controle supervisório em rede com
  canais imperfeitos (atraso, perda, fora de ordem), classificando os arranjos
  em centralizado, descentralizado e distribuído. **É o melhor ponto de
  entrada nessa linha.**
- Hou e Li [23] (pré-print) dão condições necessárias e suficientes para
  controle distribuído não-bloqueante com atrasos e perdas: controlabilidade
  em rede, observabilidade conjunta em rede e fechamento de linguagem.

**Implementação distribuída de verdade.** Schouten et al. [22] é o trabalho
mais próximo do seu: distribuem um supervisor sintetizado (matrizes de
dependência + localização), implementam em controladores reais com atraso de
comunicação e usam **algoritmos de exclusão mútua** para tornar o supervisor
distribuído robusto a atraso, validando em *hardware-in-the-loop*. O protocolo
do `esp32_crypto` resolve o mesmo problema com a ferramenta equivalente de
sistemas distribuídos: *lock* no participante entre o voto e o COMMIT, mais
*wound-wait* [35] entre iniciadores. Vale citar os dois lado a lado.

**O que isso significa para este trabalho.**

- O protocolo não verifica as condições formais de [20], [21], [23]: ele
  **detecta em tempo de execução** quando não pode mais garantir consistência
  e para (SAFE HALT). Formular isso como "garante segurança, não vivacidade,
  sob perda arbitrária" é honesto e defensável.
- Os experimentos de perda feitos durante o desenvolvimento (5 % de perda:
  execução completa sem divergência; 30 %: SAFE HALT) são a contraparte
  empírica dessa literatura. Esses cenários foram depois retirados do
  repositório; ver [`arquitetura.md`](arquitetura.md) §7.5–§7.6 e o
  [commit `b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775).
- A varredura de 1 a 7 containers (§6 da arquitetura) complementa a
  localização [18] e a implementação distribuída [22] com uma medida
  empírica: quanto se ganha, em tempo, distribuindo mais. Distribuir divide o trabalho criptográfico
  (798 decifrações em todas as configurações, repartidas entre os nós), mas
  cada nó a mais é mais um participante a sincronizar nos eventos
  compartilhados. O custo de coordenação medido fica entre 25 e 33 ms por
  passo com 2 a 7 nós, sem tendência clara com o número de nós. A aceleração é limitada pela parte que não se
  divide, como prevê a Lei de Amdahl [43]: aqui, o supervisor mais carregado
  (S5, com 41 das 190 decifrações do ciclo 1).

---

## 3. Supervisores em controladores reais: como se implementa

Há um longo caminho entre o autômato sintetizado e o código que roda.
Fabian e Hellgren [24] apontaram cedo a discrepância entre o supervisor
abstrato e sua implementação física em CLP (sinais, simultaneidade, eventos
"perdidos" entre ciclos de varredura). de Queiroz e Cury [17] implementaram o
controle modular local de uma célula de manufatura em CLP, que é a referência
brasileira direta, de UFSC, para o mesmo tipo de problema. Hoje o ciclo
completo (modelagem → síntese → simulação → geração de código para CLP) é
coberto por ferramentas como o Eclipse ESCET [25].

**Para este trabalho:** o `esp32_crypto` e o `docker_des` pulam o CLP e
executam o supervisor como dados (vetores de habilitação e transição gerados
pelo notebook UltraDES) num motor genérico. Isso evita gerar código por
planta, e é o que permite o **mesmo binário** servir para qualquer problema. É
uma diferença de abordagem em relação a [17], [24], [25] que vale explicitar.

---

## 4. Controle criptografado

Kogiso e Fujita [27] introduziram (CDC 2015) a ideia de **cifrar o
controlador** com cifras homomórficas, RSA e **ElGamal**, para que o
dispositivo de controle só enxergue parâmetros e sinais embaralhados. Schulze
Darup et al. [28] e o levantamento de Schlüter, Binfet e Schulze Darup [29]
organizam a área em gerações: cifras parcialmente homomórficas (Paillier,
ElGamal) e depois cifras em reticulados (BFV, CKKS). Quase toda essa
literatura trata de **controle contínuo linear**. O `esp32_crypto` aplica
ElGamal aditivo em curva elíptica a **supervisores de eventos discretos**, em
que a decisão é booleana e basta um teste de zero, sem logaritmo discreto
(detalhes em `esp32_crypto/docs/code-explained.md` §2).

**Para este trabalho:** a propriedade de que "nenhum texto cifrado sai do
nó, cada nó tem sua própria chave" é o que torna a distribuição em containers
natural. Não há chave homomórfica compartilhada para distribuir entre os
containers, só a chave de autenticação dos quadros (HMAC), entregue como
*Docker secret*.

---

## 5. Bancadas de rede emuladas

Rodar vários nós numa só máquina, cada um no seu *namespace* de rede, é a
técnica do Mininet [31]. O Containernet [32] estendeu o Mininet para usar
containers Docker como hosts. O `netem` do Linux [30] injeta atraso, *jitter*,
perda e reordenamento em interfaces, e é o que se usa para emular um enlace
Wi-Fi ou WAN sobre uma rede virtual.

**Para este trabalho:** a `compose.yaml` é uma bancada no mesmo espírito, com
até 7 containers numa *bridge*. Multicast funciona entre containers na mesma
*bridge*, mas não em redes *overlay* (Swarm/Kubernetes), onde o VXLAN não
replica multicast ([moby/libnetwork#552](https://github.com/moby/libnetwork/issues/552)).
Um transporte UDP *unicast* e cenários com `netem` foram testados durante o
desenvolvimento e depois retirados para manter o repositório enxuto; código e
resultados estão no [commit `b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775). Kernels antigos do WSL 2 não
trazem `sch_netem` ([microsoft/WSL#6065](https://github.com/microsoft/WSL/issues/6065)),
e um kernel WSL 2 atual (setembro de 2026) o traz como módulo.

---

## 6. Reprodutibilidade

Boettiger [13] argumenta que a imagem Docker é o artefato que torna um
experimento computacional reexecutável por terceiros, porque fixa o sistema,
as bibliotecas e as versões. Aqui isso se traduz em: base Ubuntu 26.04 LTS,
mbedTLS 3.6.5 (mesmo ramo LTS 3.6 que o ESP-IDF 5.5 usa nas placas [41]),
`BUILD_INFO` gravado dentro da imagem e cenários como arquivos versionados com
valores esperados (`EXPECT_*`).

Na prática, isso se confirmou. A varredura de 1 a 7 containers rodou na nuvem
(uma vez) e no WSL 2 da autora (5 vezes). Nas 35 execuções do WSL, cada
configuração repetiu exatamente os mesmos invariantes (impressão digital,
decifrações por nó, passos), iguais aos da nuvem. Os tempos variaram menos de
1 % entre repetições e 1,2–3,3 % entre as duas máquinas
([`arquitetura.md`](arquitetura.md) §6).

---

## 7. A lacuna

Cruzando as linhas acima:

| trabalho | supervisor da TCS | distribuído em rede | em container | estado cifrado |
|---|---|---|---|---|
| vPLC [9]–[11] | não (lógica IEC 61131) | às vezes | **sim** | não |
| Schouten et al. [22] | **sim** | **sim** | não (CLP / HIL) | não |
| TCS em rede [19]–[21], [23] | **sim** | **sim** (teoria) | não | não |
| controle criptografado [27]–[29] | não (controle contínuo) | sim | às vezes | **sim** |
| `esp32_crypto` | **sim** | **sim** (2 ESP32) | não | **sim** |
| **`docker_des`** | **sim** | **sim** (1 a 7 nós) | **sim** | **sim** |

Não encontrei trabalho que feche as quatro colunas. A busca foi ampla, mas não
exaustiva: vale repetir no Scopus/IEEE Xplore com termos como
`"supervisory control" AND (container OR Docker OR Kubernetes)`.

---

## 8. Onde cada afirmação do trabalho se apoia

Evidências da varredura atual (§6 da arquitetura, 35 execuções) ou, quando
indicado, de experimentos anteriores (§7 da arquitetura, [commit `b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775)).

| afirmação | evidência | literatura |
|---|---|---|
| Um supervisor por container é uma forma legítima de implantar controle | `compose.yaml`, cenário `fms-7` (5/5 PASS) | [1], [2], [5], [9] |
| O container executa **o mesmo sistema** que as placas | motor byte a byte idêntico (`engine/SHA256SUMS`); `fms-2` reproduz a impressão digital `edbd7971` e as decifrações 405 + 393 das placas nas 5 repetições | [13] (reprodutibilidade) |
| Distribuir não aumenta o trabalho criptográfico | 798 decifrações (190 no ciclo 1) com 1, 2, 3, 4, 5, 6 e 7 containers, em todas as 35 execuções | — (resultado próprio) |
| **Com o custo de decifração do ESP32, distribuir acelera** | 303,1 ± 1,3 → 90,1 ± 1,0 ms/passo de 1 para 7 containers (3,37×; IC 95 %, n = 5); curva estatisticamente distinguível | [18], [22] (distribuir); [43] (limite da aceleração) |
| **A aceleração é limitada pelo supervisor mais carregado** | o tempo medido acompanha o limite "decifrações do nó mais carregado × 69 ms ÷ 44", 25–33 ms acima dele | [43] |
| Sem a emulação, distribuir atrasa | experimento anterior: 2,4 → 4,7 ms/passo de 1 para 7 nós na velocidade de um PC | [43]; [9]–[11] (custo de rede em containers) |
| A decomposição modular local é a partição natural | roteamento derivado do cabeçalho; eventos locais não geram tráfego | [16], [18] |
| O protocolo preserva segurança sob perda | experimento anterior: 5 % de perda completa sem divergência; 30 % para em SAFE HALT | [20], [21], [23], [33] |
| Concorrência entre iniciadores é tratada | *lock* + *wound-wait* | [22] (mutex), [35] |
| A distribuição preserva o comportamento do supervisor monolítico | experimento anterior: `extended_small_factory`, verificação cruzada com o monolítico PASS | [16], [26] |
| UDP basta como transporte | confiabilidade fim a fim no protocolo; multicast nas 35 execuções (e unicast no experimento anterior) | [33], [36] |
| Cifrar supervisores é viável fora do microcontrolador | autoteste EC-ElGamal + oráculo PASS em todos os nós, com mbedTLS real | [27]–[29] |

---

## 9. Experimentos que a literatura espera, e o que já foi feito

| pergunta | linha que a faz | situação | como medir com este repositório |
|---|---|---|---|
| Escalabilidade no número de nós | TCS distribuída [18], [22] | **feito**: 1 a 7 containers, 5 repetições (arquitetura §6) | `REPEAT=5 scripts/run-all.sh` |
| Latência e *jitter* por passo | vPLC [9]–[11] | **feito para eventos**: p50–p99 de decisão e aplicação por classe (varredura 1–7, n = 5); intervalo da célula pronto, falta rodar | `python3 scripts/latency.py <varredura>` (`latencia.md`, `latencia.csv`) |
| Efeito da partição | localização [18] | **parcial**: blocos × S5 isolado, 2 a 6 containers, 5 repetições (arquitetura §6.4) | `scripts/run-all.sh s5`; outras partições com `DES_SUP_NODE_MAP` |
| Robustez a perda | TCS em rede [20], [21] | feito antes (arquitetura §7.5–§7.6), cenários retirados | `DES_EXTRA_FLAGS=-DDES_SIMULATE_LOSS_PCT=<p>` |
| Robustez a atraso | [19], [22] | feito antes com `netem`, retirado | ver [commit `b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775) |
| Equivalência com o monolítico | TCS [16] | feito antes (`extended_small_factory`), retirado; o FMS não tem monolítico | ver [commit `b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775) |
| Sobrecarga do container | [3], [12] | **não feito** | mesmo cenário com `network_mode: host` e sem limite de CPU |

---

## Referências

**Containers em automação e controle**

1. Goldschmidt, T., & Hauck-Stattelmann, S. (2016). Software containers for
   industrial control. *42nd Euromicro Conference on Software Engineering and
   Advanced Applications (SEAA)*, 258–265.
2. Goldschmidt, T., Hauck-Stattelmann, S., Malakuti, S., & Grüner, S. (2018).
   Container-based architecture for flexible industrial control applications.
   *Journal of Systems Architecture*, 84, 28–36.
   doi:10.1016/j.sysarc.2018.03.002
3. Moga, A., Sivanthi, T., & Franke, C. (2016). OS-level virtualization for
   industrial automation systems: are we there yet? *Proc. 31st ACM Symposium
   on Applied Computing (SAC '16)*. doi:10.1145/2851613.2851737
4. Tasci, T., Melcher, J., & Verl, A. (2018). A container-based architecture
   for real-time control applications. *IEEE Int. Conf. on Engineering,
   Technology and Innovation (ICE/ITMC)*.
5. Telschig, K., Schönberger, A., & Knapp, A. (2018). A real-time container
   architecture for dependable distributed embedded applications. *IEEE 14th
   Int. Conf. on Automation Science and Engineering (CASE)*, 1367–1374.
   doi:10.1109/COASE.2018.8560546
6. Hofer, F., Sehr, M. A., Sangiovanni-Vincentelli, A., & Russo, B. (2021).
   Industrial control via application containers: Maintaining determinism in
   IAAS. *Systems Engineering* (Wiley). doi:10.1002/sys.21590 · arXiv:2005.01890.
   ⚠ lista de autores: algumas fontes omitem M. A. Sehr; conferir.
7. Struhár, V., Behnam, M., Ashjaei, M., & Papadopoulos, A. V. (2020).
   Real-time containers: A survey. *2nd Workshop on Fog Computing and the IoT
   (Fog-IoT 2020)*, OASIcs 80, 7:1–7:9. doi:10.4230/OASIcs.Fog-IoT.2020.7
8. Struhár, V., Craciunas, S. S., Ashjaei, M., Behnam, M., & Papadopoulos,
   A. V. (2021). REACT: Enabling real-time container orchestration. *26th IEEE
   Int. Conf. on Emerging Technologies and Factory Automation (ETFA)*.
   doi:10.1109/ETFA45728.2021.9613685
9. Queiroz, R., Cruz, T., Mendes, J., Sousa, P., & Simões, P. (2023).
   Container-based virtualization for real-time industrial systems—A
   systematic review. *ACM Computing Surveys*. doi:10.1145/3617591
10. Gaffurini, M., Bellagente, P., Depari, A., Flammini, A., Sisinni, E., &
    Ferrari, P. (2024). Virtual PLC in industrial edge platform: Performance
    evaluation of supervision and control communication. *IEEE Transactions on
    Instrumentation and Measurement*, 73. (IEEE Xplore 10449455)
11. Ben Kebaier, N., et al. (2025). Real-time performance evaluation of
    containerized virtual PLCs: A comparative study of Docker and Podman for
    industrial automation. *Conferência IEEE, out. 2025* (IEEE Xplore 11229890).
    ⚠ coautores e nome da conferência não confirmados.
12. Felter, W., Ferreira, A., Rajamony, R., & Rubio, J. (2015). An updated
    performance comparison of virtual machines and Linux containers. *IEEE
    Int. Symp. on Performance Analysis of Systems and Software (ISPASS)*,
    171–172.
13. Boettiger, C. (2015). An introduction to Docker for reproducible
    research. *ACM SIGOPS Operating Systems Review*, 49(1), 71–79.
    doi:10.1145/2723872.2723882

**Controle supervisório: base, distribuído, em rede**

14. Ramadge, P. J., & Wonham, W. M. (1987). Supervisory control of a class of
    discrete event processes. *SIAM J. Control and Optimization*, 25(1),
    206–230.
15. Rudie, K., & Wonham, W. M. (1992). Think globally, act locally:
    decentralized supervisory control. *IEEE Trans. Automatic Control*, 37(11),
    1692–1708.
16. de Queiroz, M. H., & Cury, J. E. R. (2000). Modular supervisory control of
    large scale discrete event systems. *WODES 2000*, 103–110.
17. de Queiroz, M. H., & Cury, J. E. R. (2002). Synthesis and implementation
    of local modular supervisory control for a manufacturing cell. *6th Int.
    Workshop on Discrete Event Systems (WODES'02)*, Zaragoza, 377–382.
18. Cai, K., & Wonham, W. M. (2010). Supervisor localization: a top-down
    approach to distributed control of discrete-event systems. *IEEE Trans.
    Automatic Control*, 55(3), 605–618.
19. Zhang, R., Cai, K., Gan, Y., et al. (2016). Distributed supervisory
    control of discrete-event systems with communication delay. *Discrete
    Event Dynamic Systems*, 26, 263–293. arXiv:1207.5072
20. Lin, F. (2014). Control of networked discrete event systems: dealing with
    communication delays and losses. *SIAM J. Control and Optimization*,
    52(2), 1276–1298. doi:10.1137/130914942
21. Zhu, Y., Lin, L., Tai, R., et al. (2023). Overview of networked
    supervisory control with imperfect communication channels. *Discrete Event
    Dynamic Systems*, 33, 25–61. doi:10.1007/s10626-022-00368-2
22. Schouten, R. H. J., Moormann, L., van de Mortel-Fronczak, J. M., & Rooda,
    J. E. Synthesis and implementation of distributed supervisory controllers
    with communication delays. *IEEE CASE 2021*, 1268–1275; versão em
    periódico: *IEEE Trans. Automation Science and Engineering*, 20(3),
    1591–1606 (2023). arXiv:2102.09821
23. Hou, Y., & Li, Q. (2023). Distributed nonblocking supervisory control of
    timed discrete-event systems with communication delays and losses.
    arXiv:2308.16545 (pré-print; publicação em periódico não localizada).
24. Fabian, M., & Hellgren, A. (1998). PLC-based implementation of
    supervisory control for discrete event systems. *37th IEEE Conf. on
    Decision and Control (CDC)*, vol. 3, 3305–3310. doi:10.1109/CDC.1998.758209
25. Fokkink, W., Goorden, M., Hendriks, D., van Beek, D. A., Hofkamp, A.,
    Reijnen, F., et al. (2023). Eclipse ESCET™: The Eclipse Supervisory
    Control Engineering Toolkit. *TACAS 2023*, LNCS, 44–52.
    doi:10.1007/978-3-031-30820-8_6
26. Cassandras, C. G., & Lafortune, S. (2021). *Introduction to Discrete Event
    Systems* (3ª ed.). Springer.

**Controle criptografado**

27. Kogiso, K., & Fujita, T. (2015). Cyber-security enhancement of networked
    control systems using homomorphic encryption. *54th IEEE Conf. on Decision
    and Control (CDC)*, 6836–6843. doi:10.1109/CDC.2015.7403296
28. Schulze Darup, M., Alexandru, A. B., Quevedo, D. E., & Pappas, G. J.
    (2021). Encrypted control for networked systems: An illustrative
    introduction and current challenges. *IEEE Control Systems Magazine*.
    arXiv:2010.00268
29. Schlüter, N., Binfet, P., & Schulze Darup, M. (2023). A brief survey on
    encrypted control: From the first to the second generation and beyond.
    *Annual Reviews in Control*, 56, 100913. doi:10.1016/j.arcontrol.2023.100913

**Emulação de rede**

30. Hemminger, S. (2005). Network emulation with NetEm. *linux.conf.au 2005*,
    Canberra.
31. Lantz, B., Heller, B., & McKeown, N. (2010). A network in a laptop: rapid
    prototyping for software-defined networks. *9th ACM Workshop on Hot Topics
    in Networks (HotNets-IX)*.
32. Peuster, M., Karl, H., & van Rossem, S. (2016). MeDICINE: Rapid
    prototyping of production-ready network services in multi-PoP
    environments. *IEEE NFV-SDN 2016*, 148–153.
    doi:10.1109/NFV-SDN.2016.7919490 (introduz o Containernet)

**Sistemas distribuídos (fundamentos do protocolo)**

33. Saltzer, J. H., Reed, D. P., & Clark, D. D. (1984). End-to-end arguments in
    system design. *ACM Trans. Computer Systems*, 2(4), 277–288.
34. Gray, J. (1978). Notes on data base operating systems. In *Operating
    Systems: An Advanced Course*, LNCS 60. Springer (*two-phase commit*).
35. Rosenkrantz, D. J., Stearns, R. E., & Lewis, P. M. (1978). System level
    concurrency control for distributed database systems. *ACM Trans. Database
    Systems*, 3(2), 178–198 (*wound-wait*).
36. Deering, S. (1989). Host extensions for IP multicasting. RFC 1112.

**Linguagem e ferramentas**

37. Pereira, R., Couto, M., Ribeiro, F., Rua, R., Cunha, J., Fernandes, J. P.,
    & Saraiva, J. (2021). Ranking programming languages by energy efficiency.
    *Science of Computer Programming*, 205, 102609.
38. Eclipse 4diac FORTE, runtime IEC 61499 em C++ para dispositivos de
    controle embarcados. <https://eclipse.dev/4diac/4diac_forte/>
39. moby/libnetwork, *issue* #552: multicast em redes *overlay*.
    <https://github.com/moby/libnetwork/issues/552>
40. Docker, "Install Docker Engine on Ubuntu"
    <https://docs.docker.com/engine/install/ubuntu/>; Microsoft, "systemd
    support in WSL" <https://learn.microsoft.com/windows/wsl/systemd>.
41. Espressif, notas de versão do ESP-IDF v5.5 (mbedTLS atualizado para
    3.6.3). <https://github.com/espressif/esp-idf/releases/tag/v5.5>
42. microsoft/WSL, *issue* #6065: `tc qdisc netem` indisponível no WSL 2.
    <https://github.com/microsoft/WSL/issues/6065>

**Computação paralela**

43. Amdahl, G. M. (1967). Validity of the single processor approach to
    achieving large scale computing capabilities. *AFIPS Spring Joint Computer
    Conference*, 483–485. doi:10.1145/1465482.1465560
