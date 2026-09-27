# Arquitetura: do ESP32 ao container

> **Nota.** As seções 5–6 descrevem experimentos com cenários que depois foram
> retirados do repositório, que hoje tem só a varredura de 1 a 7 containers.
> Os resultados dessas execuções estão no histórico do git, no commit
> [`b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775/docs).

Este documento explica como o sistema distribuído do
[`esp32_crypto`](https://github.com/pganaclara/esp32_crypto) (supervisores
homomórficos do FMS em duas placas ESP32-S3) virou **um container Docker por
supervisor** conversando por UDP. Também explica por que a linguagem é C++,
como se prova que o container executa *o mesmo sistema* que as placas e o que
os experimentos mostraram. A literatura citada `[n]` está em
[`literatura.md`](literatura.md).

---

## 1. Visão geral

```
                    rede Docker "cell" (bridge)  ─  UDP 239.192.7.1:5077
   ┌───────────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────────┐
   │  node1    │  node2    │  node3    │  node4    │  node5    │  node6    │  node7    │
   │  S0 (E1)  │  S1       │  S2       │  S3       │  S4       │  S5       │  S6       │
   │ 18 estados│           │           │           │           │           │164 estados│
   │ chave EC  │ chave EC  │ chave EC  │ chave EC  │ chave EC  │ chave EC  │ chave EC  │
   │ própria   │ própria   │ própria   │ própria   │ própria   │ própria   │ própria   │
   └───────────┴───────────┴───────────┴───────────┴───────────┴───────────┴───────────┘
        cada container = 1 processo des_nodeK = motor do ESP32 + ponto de entrada POSIX
        quadros de 44 B assinados com HMAC-SHA256 (chave da célula via Docker secret)
```

- Cada container guarda **só o seu supervisor**, cifrado com EC-ElGamal sob
  **o seu próprio par de chaves**, gerado no boot. Nenhum texto cifrado sai do
  container: só bits de habilitação trafegam.
- Os eventos são classificados na inicialização, a partir do cabeçalho gerado
  pelo UltraDES: **locais** (um só nó se importa, sem tráfego),
  **compartilhados controláveis** (commit em duas fases: `REQ → VOTE* →
  COMMIT → ACK*`) e **compartilhados não controláveis** (`NOTIFY → ACK*`).
- O transporte é UDP puro: multicast (padrão) ou unicast (opcional).

---

## 2. O que mudou e o que não mudou

| no ESP32 (`esp32_crypto`) | no Docker (`docker_des`) | mudou? |
|---|---|---|
| `des_generic.h`: motor, criptografia, protocolo | `engine/des_generic.h`, **byte a byte igual** | **não** |
| `des_transport.h`: UDP multicast | `engine/des_transport.h`, **igual** | **não** |
| `supervisor_data_*.h` gerados pelo notebook | `engine/supervisor_data_*.h`, **iguais** | **não** |
| placa gravada com `DES_NODE_ID=k` | imagem com um binário por nó; o container escolhe pelo `command` | forma de implantar |
| Wi-Fi + ponto de acesso | rede Docker *bridge* `cell` | meio físico |
| `secrets.h` compilado (chave no firmware) | chave lida no início de um *Docker secret* | forma de entregar a chave |
| `des_distributed.ino` (entrada Arduino) | `src/des_container_main.cpp` (entrada POSIX) | **novo** |
| — | `src/des_transport_unicast.h` (segundo transporte) | **novo** |
| Serial Monitor | `docker compose logs` + linha `@@RESULT {json}` | saída |
| RESET nas placas | `scripts/run.sh` (sobe, espera, coleta, resume) | operação |

**Por que o motor não é editado.** A afirmação central é "o container
executa o mesmo sistema que as placas". Ela só é verificável se o código for
o mesmo. `engine/SHA256SUMS` guarda os hashes, o `Dockerfile` recusa compilar
se algum arquivo diferir e `scripts/sync-engine.sh` é o único caminho para
atualizá-lo a partir do `esp32_crypto`.

---

## 3. As peças novas

### 3.1 `src/des_container_main.cpp`

É o equivalente do `des_distributed.ino` e do `host_main.cpp`: escolhe a
implantação, sobe o enlace e chama `des_setup()` / `des_loop()`. Ele resolve
quatro coisas que só existem num container:

1. **Chave em tempo de execução.** O motor aplica `sizeof()` a
   `DES_AUTH_KEY`, porque no ESP32 a chave é um literal de string. Aqui ela é
   um vetor de 65 bytes preenchido no início a partir de
   `/run/secrets/des_auth_key`, o que satisfaz o `sizeof` exatamente como o
   literal. Assim o motor não muda e a chave **nunca entra numa camada da
   imagem**. Os 64 caracteres são os mesmos bytes que uma placa compilaria,
   então **um ESP32 e um container com a mesma chave são pares na mesma
   célula**.
2. **Transporte escolhido no início**: `DES_TRANSPORT=multicast` (padrão) ou
   `unicast`. A troca é uma atribuição à estrutura `DES_TRANSPORT_IMPL` do
   motor, antes de `des_setup()`.
3. **Terminar.** Uma placa roda para sempre, um container precisa acabar.
   Depois do roteiro, o nó continua atendendo os pares por `DES_LINGER_MS`
   (padrão 10 s), porque um par pode estar retransmitindo um COMMIT cujo ACK se
   perdeu (até 5 × 1,5 s). Depois imprime `@@RESULT {...}` e sai com um código:
   `0` tudo certo, `1` passos pulados ou oráculo divergente, `2` SAFE HALT,
   `3` erro de configuração, `4` *watchdog*.
4. **Watchdog** (`DES_RUN_TIMEOUT_S`, padrão 900 s). O motor espera todos os
   pares indefinidamente, o que é correto para placas gravadas uma de cada vez
   e errado para um lote de containers em que um deles nem subiu.

### 3.2 `src/des_transport_unicast.h`

Implementa o mesmo contrato de quatro funções (`begin/send/poll/service`) do
`des_transport.h`, enviando o quadro de 44 B por UDP unicast a cada par. Os
pares são **nomes** (`DES_PEERS=node1,...,node7`) resolvidos pelo DNS interno
do Docker, com nova tentativa a cada 500 ms enquanto um par não subiu e
atualização a cada 5 s (um container recriado muda de IP). Existe porque
multicast não atravessa redes *overlay* (Swarm/Kubernetes) [39]. O endereço de
origem nunca é confiável nem precisa ser: todo quadro é autenticado por HMAC
no motor.

É também uma demonstração do argumento fim a fim do motor [33]: como
sequenciamento, confirmação, retransmissão e atomicidade estão no protocolo,
qualquer transporte de melhor esforço serve, e trocá-lo não toca em uma linha
de controle.

### 3.3 `Dockerfile`

- **Estágio de build** (Ubuntu 26.04 LTS): `g++` 15 + `libmbedtls-dev` 3.6.5,
  o mesmo ramo LTS que o ESP-IDF 5.5, e portanto o Arduino-ESP32 3.3, usa nas
  placas (3.6.3) [41]. O Ubuntu 24.04 traz mbedTLS 2.28, que **não lê pontos
  EC comprimidos**, justamente o formato em que o motor guarda os textos
  cifrados. Compila `DES_NUM_NODES` binários em paralelo, cada um com seu
  `DES_NODE_ID`, com `-Wall -Wextra` e zero avisos, e com o mbedTLS ligado
  estaticamente. Grava `BUILD_INFO` com as versões.
- **Estágio final**: só os binários, o `entrypoint` e o `iproute2` (para
  `netem`). O nó roda como usuário sem privilégios, sem capacidades e com
  `no_new_privs`. O root só existe no `entrypoint`, para aplicar o `tc`.

### 3.4 `compose.yaml` e cenários

- Serviços `node1`…`node7`, todos da mesma âncora YAML; o número do nó é o
  `command`. Sobe-se só `node1..nodeN`.
- `cpus: 1.0` por container, como um núcleo por placa no ESP32.
- `cap_add: NET_ADMIN` apenas para o `netem` opcional.
- Cada `scenarios/*.env` é um experimento: problema, número de nós, família,
  transporte, perda, e os **valores esperados** (`EXPECT_*`) que o
  `scripts/summarize.py` confere automaticamente.

---

## 4. Por que C++ (C++17)

**Resposta curta: C++, porque o motor já é C++17, e reaproveitá-lo sem
alteração é o que permite afirmar equivalência com o hardware.**

| critério | C++17 | Rust | Go | Python | C |
|---|---|---|---|---|---|
| reaproveita o motor do ESP32 sem reescrever | **sim** | não | não | não | não (usa `std::vector`) |
| mesma biblioteca criptográfica das placas (mbedTLS 3.6) | **sim** | via FFI | via cgo | via binding | sim |
| tempo previsível (sem coletor de lixo) | **sim** | sim | não (GC) | não (GC, GIL) | sim |
| segurança de memória garantida pelo compilador | não | **sim** | sim | sim | não |
| usada em runtimes industriais | 4diac FORTE (IEC 61499) [38], CODESYS | começando | pouco | não | open62541 (OPC UA) |
| eficiência (energia/tempo) [37] | topo | topo | média | baixa | topo |

- **Reaproveitamento é o argumento decisivo.** Reescrever em Rust, Go ou
  Python criaria uma *segunda implementação*, que precisaria ser validada do
  zero contra a primeira, e o "mesmo sistema" viraria "um sistema parecido".
  Com C++ o mesmo arquivo compila para Xtensa (ESP32) e x86-64/ARM64
  (container), e os hashes provam isso.
- **Criptografia idêntica.** O mbedTLS é a biblioteca do ESP-IDF. Usar o mesmo
  ramo (3.6) no container elimina "a biblioteca é outra" como explicação para
  qualquer diferença.
- **Medição.** Sem coletor de lixo não há pausas espúrias nos tempos por
  passo, o que importa quando a literatura de vPLC cobra latência e *jitter*
  [9]–[11].
- **Quando Rust faria sentido:** num motor novo, escrito do zero, em que a
  segurança de memória pesasse mais que a equivalência com o firmware
  existente. Não é o caso aqui.

---

## 5. Como provar que o container executa o mesmo sistema

Cinco evidências independentes, todas automáticas (`scripts/run-all.sh`):

1. **Mesmo código.** `engine/` é byte a byte igual a
   `esp32_crypto/des_distributed/` no commit `bf0efe6`; o build confere os
   SHA-256.
2. **Mesma configuração.** O motor imprime uma impressão digital (FNV-1a)
   sobre versão do protocolo, número de nós, família, tabela de eventos,
   partição derivada e roteiro. Com FMS, 2 nós e família local modular, as
   placas imprimem **`edbd7971`**. O cenário `fms-2` exige o mesmo valor, e ele
   bate.
3. **Mesmo trabalho criptográfico, na unidade.** O número de decifrações por
   passo é função determinística do supervisor, do roteiro e de quais células
   cifradas são o `Enc(0)` global (o modelo estático do
   `esp32_crypto/docs/code-explained.md` §4.8, que previu o hardware passo a
   passo). O container reproduz:

   | configuração | placas ESP32-S3 | containers |
   |---|---|---|
   | FMS, 1 nó, ciclo 1 | 190 (placa única) | **190** (`fms-1`) |
   | FMS, 2 nós, 5 ciclos | 405 + 393 (85 + 105 no ciclo 1) | **405 + 393 (85 + 105)** (`fms-2`) |
   | FMS, 7 nós, 5 ciclos | — | **798 no total, 190 no ciclo 1** (`fms-7`) |
   | ESF, 2 nós, ciclo 1 | 8 (placa única) | **8** (`esf-2-lockstep`) |

4. **Mesma semântica.** Em todo nó, cada bit homomórfico é comparado com um
   oráculo em texto claro depois de cada passo (**PASS** em todos os cenários
   que completam). No `extended_small_factory`, que tem supervisor monolítico,
   a execução distribuída é conferida evento a evento contra ele (**PASS**).
5. **Criptografia real.** O autoteste EC-ElGamal e HMAC passa em todo nó com
   mbedTLS 3.6.5. A validação em Linux original do `esp32_crypto` usava um
   *test double* no lugar do mbedTLS; aqui a criptografia é a de verdade.

**O que isso *não* prova:** equivalência de **tempo**. Um x86 faz uma
decifração em ≈ 0,5 ms, contra 69–100 ms no ESP32-S3. A rede é uma *bridge*
na memória, não Wi-Fi. Tempos medidos aqui não são tempos de placa (ver §7).

---

## 6. Resultados e achados

Números das execuções de referência em [`docs/resultados/` no commit `b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775/docs/resultados), uma
execução por cenário.

### 6.1 Um supervisor por container maximiza o compartilhamento

| partição | eventos compartilhados | eventos sem tráfego | participantes dos eventos 30–39 |
|---|---|---|---|
| 1 nó (`fms-1`) | 0/31 | 31/31 | — |
| 2 nós (`fms-2`, igual às placas) | 10/31 | 21/31 | 1 |
| 7 nós (`fms-7`, um por supervisor) | 15/31 | 16/31 | **6** |

Os eventos 30–39 aparecem em **todos** os 7 supervisores (todos transitam
neles). Com um supervisor por container, cada um desses eventos controláveis
custa um commit em duas fases com 6 participantes: `2 + 2·6 = 14` quadros. É
o preço de granularidade máxima, e é o dado que justifica estudar a partição
(`DES_SUP_NODE_MAP`) como variável experimental.

### 6.2 Distribuir não aumenta o trabalho criptográfico

798 decifrações no total e 190 no ciclo 1, com 1, 2 ou 7 nós, com multicast ou
unicast, e com ou sem perda (as retransmissões são reconhecidas pelo número de
sequência e não reaplicadas). Distribuir **divide** o trabalho, não o soma.

### 6.3 No container a criptografia fica barata e o protocolo passa a dominar

| | ESP32-S3, 1 placa | ESP32-S3, 2 placas | containers, 1 nó | containers, 2 nós | containers, 7 nós |
|---|---|---|---|---|---|
| tempo por passo, ciclo 1 | 346,0 ms | 296,9 ms | 2,36 ms | 4,05 ms | 4,65 ms |
| tempo por passo, ciclos 2–5 | — | 167,2 ms | 1,60 ms | 2,84 ms | 3,73 ms |
| RTT de aplicação | — | 13,9–18,2 ms | — | 2,3 ms | 3,4 ms |

(ESP32: `esp32_crypto`, família modular local, `DES_WORK_MS 0`. Containers:
[`docs/resultados/` no commit `b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775/docs/resultados).)

No ESP32 o tempo é `decifrações × multiplicação escalar`, e distribuir em 2
placas **acelera** (296,9 contra 346,0 ms), porque divide as decifrações. No
container uma decifração custa ≈ 0,55 ms (427 ms de HE para 798 decifrações
no `fms-7`) e **a espera pelos pares domina**: no nó 1 do `fms-7`, 88 % do
tempo de cada passo é espera de protocolo e rede (53 % no `fms-2`). Por isso,
no container, distribuir **atrasa** (1 nó 2,36 ms → 7 nós 4,65 ms por passo):
não há decifração cara para dividir, e cada nó a mais é mais um participante
por commit. É a mesma arquitetura com o gargalo em outro lugar, e o resultado
vale ser discutido: a vantagem de distribuir depende da razão entre o custo
criptográfico por passo e o custo de coordenação.

### 6.3b Teste da explicação: emulando o custo de decifração do ESP32

Se a explicação acima estiver certa, basta tornar a criptografia tão cara
quanto no ESP32 para distribuir voltar a acelerar. `DES_EMU_SCALARMUL_MS=69`
faz cada **decifração** levar pelo menos 69 ms, o custo medido de uma
multiplicação escalar no ESP32-S3. O motor não é alterado: o ponto de entrada
intercepta a chamada a `mbedtls_ecp_mul` com `-Wl,--wrap` e só dorme o que
falta quando o escalar é a chave privada negada. Cenários `fms-{1,2,7}-esp32`,
resultados em [`docs/resultados/emulacao-esp32/` no commit `b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775/docs/resultados/emulacao-esp32).

| nós | sem emulação, ciclo 1 | **com emulação**, ciclo 1 | com emulação, ciclos 2–5 | limite inferior (nó mais carregado) |
|---|---|---|---|---|
| 1 | 2,08 ms | **299,5 ms** | 239,2 ms | 190 dec × 69 / 44 = 298,0 ms |
| 2 | 3,93 ms | **192,7 ms** (1,6× mais rápido) | 147,5 ms | 105 × 69 / 44 = 164,7 ms |
| 7 | 4,35 ms | **87,2 ms** (3,4× mais rápido) | 59,8 ms | 41 × 69 / 44 = 64,3 ms |

Os invariantes não mudam (798 decifrações, 190 no ciclo 1, `edbd7971`,
405 + 393). A tendência se inverte exatamente como previsto: com
criptografia cara, distribuir paraleliza as decifrações e acelera; com
criptografia barata, só acrescenta coordenação.

O tempo por passo fica no mínimo em *decifrações do nó mais carregado × custo
de uma decifração ÷ passos*, porque os nós só trabalham em paralelo entre dois
eventos compartilhados. A distância até esse limite (1,5 ms, 28 ms e 23 ms
acima) é o custo de coordenação e de serialização. Isso dá uma regra para
escolher a partição: equilibrar as decifrações entre os nós e manter pequeno o
número de eventos compartilhados.

**Ressalvas.** A emulação só reproduz o custo da multiplicação escalar. As
somas de pontos (`muladd`, ≈ 5 ms cada no ESP32), o HMAC, o Wi-Fi e o segundo
núcleo da placa única não são emulados. Por isso os números absolutos não
coincidem com os das placas (2 placas: 296,9 ms/passo; 2 containers
emulados: 192,7), e o ganho de 1 → 2 nós é maior aqui (1,6×) que nas placas
(1,17×, com a placa única usando 2 núcleos). A emulação serve para testar a
**direção** do efeito e prever tendências, não para substituir a medição no
hardware.

### 6.4 Perda: os *timeouts* do protocolo estão calibrados para o ESP32

| cenário | perda | passos | retransmissões | tempo por passo (ciclo 1) |
|---|---|---|---|---|
| `fms-7` | 0 % | 220/220 | 0 | 4,65 ms (3,73 nos ciclos 2–5) |
| `fms-7-loss5` | 5 % | 220/220 | 86 | 510,9 ms (767,8) |
| `fms-7-loss5-fast` | 5 %, *timeouts* de 100 ms | 220/220 | 57 | 84,5 ms (53,7) |

Com 5 % de perda a execução completa, sem divergência e com as mesmas 798
decifrações, mas o passo fica ~100× mais lento. A causa são os *timeouts*
de 1,5 s do motor, dimensionados porque no ESP32 um participante pode passar
3–4 s dentro de um passo homomórfico. Num container o passo leva ~1 ms: com
*timeouts* de 100 ms (`DES_REQ_TIMEOUT_MS`, `DES_ACK_TIMEOUT_MS`) o mesmo
experimento fica 6× (ciclo 1) a 14× (ciclos 2–5) mais rápido. **Regra prática:** o *timeout* deve ser
proporcional ao passo homomórfico mais lento entre os participantes, não ao
RTT da rede.

### 6.5 Perda pesada: segurança preservada, de dois jeitos

- **2 nós, 30 % de perda** (`fms-2-loss30`): depois de 116 dos 220 passos
  (73 numa execução anterior: a perda é aleatória), um COMMIT/NOTIFY esgota as
  retransmissões e o dono entra em **SAFE HALT**; o par também para. Nada
  divergente é aplicado. É o *trade-off* dos Dois Generais: segurança mantida,
  vivacidade sacrificada.
- **7 nós, 40 % de perda** (execução interrompida à mão depois de alguns
  minutos; logs parciais em
  [`observacoes/fms-7-loss40-parcial/` no commit `b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775/docs/resultados/observacoes/fms-7-loss40-parcial)):
  **não há SAFE HALT**. A fase de votação precisa que o
  REQ chegue aos 6 participantes e os 6 votos voltem, com probabilidade
  ≈ 0,6¹² ≈ 0,2 % por tentativa. Ela quase nunca completa, então o dono
  **desiste** do evento (SKIP) *antes* do ponto de commit, e nada é aplicado
  em lugar nenhum. Os eventos não controláveis seguintes são rejeitados pela
  verificação de planta como fisicamente impossíveis. A segurança se mantém,
  mas a execução se arrasta.

A diferença é *onde* a perda acerta o protocolo: antes do ponto de commit ela
vira SKIP (inofensivo), depois dele vira SAFE HALT (a única saída segura).

### 6.6 Multicast × unicast

Mesmos resultados lógicos e criptográficos. O unicast envia `N − 1`
datagramas por quadro (6 com 7 nós). Numa *bridge* isso é cópia de memória,
mas numa rede física a conta muda.

---

## 7. Limitações e ameaças à validade

- **Tempo não é de tempo real.** Kernel genérico, sem PREEMPT_RT, CPUs
  compartilhadas entre 7 containers num mesmo host, uma execução por cenário
  (sem variância). Os tempos servem para comparar cenários *entre si* nesta
  máquina, não para afirmar prazos [6], [9], [11].
- **A rede é uma *bridge* na memória.** Perda e atraso são injetados (motor ou
  `netem`), não medidos num enlace real. O `netem` não existe no kernel do
  ambiente de referência, mas o cenário `fms-7-wifi` rodou e passou num WSL 2
  atual ([`docs/resultados-wsl/` no commit `b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775/docs/resultados-wsl)).
- **Controlabilidade inferida.** Como no `esp32_crypto`, o cabeçalho não diz
  quais eventos são controláveis e o motor infere pelo rótulo (dígito final
  ímpar = controlável). Para um artigo, fixe `DES_CONTROLLABLE_MASK`
  explicitamente (`DES_EXTRA_FLAGS`).
- **O FMS não tem supervisor monolítico** (não coube na flash quando o
  cabeçalho foi gerado), então a verificação cruzada com o monolítico só roda
  no `extended_small_factory`.
- **Canais laterais.** Os canais 2 e 3 do `esp32_crypto` (células inativas
  idênticas a `Enc(0)`; célula ativa copiada sem re-randomização) continuam
  abertos, e num container eles são mais fáceis de explorar: quem tem acesso
  ao host lê a memória de qualquer container. O modelo de ameaça do
  `esp32_crypto/docs/code-explained.md` §7 vale aqui sem mudança.

---

## 8. Como estender

- **Mais de 7 nós:** acrescente serviços `node8`… na `compose.yaml` (mesma
  âncora) e aumente `DES_NUM_NODES`. O motor aceita até 31 nós.
- **Outro problema:** gere o cabeçalho no notebook do `esp32_crypto`, traga-o
  com `scripts/sync-engine.sh` e crie um cenário com `DES_PROBLEM=<nome>`.
- **Célula mista ESP32 + containers:** use uma rede `macvlan` (containers com
  IP na LAN física), a mesma chave de 64 caracteres no `secrets.h` das placas
  e os mesmos parâmetros de build. A impressão digital tem que bater dos dois
  lados.
- **Kubernetes/Swarm:** `DES_TRANSPORT=unicast` e `DES_PEERS` com os nomes DNS
  dos *pods*/serviços.
- **Tempo real:** host com PREEMPT_RT, `cpuset` dedicado por container e
  medição de percentis, como em [6], [11].
