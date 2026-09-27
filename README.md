# docker_des: supervisores SED homomórficos distribuídos, um container por supervisor

O SFM (Sistema Flexível de Manufatura, *FMS* de Queiroz & Cury) que roda em
duas placas ESP32 no [`esp32_crypto`](https://github.com/pganaclara/esp32_crypto),
agora em **Docker**: **um container por supervisor**, com os 7 supervisores
modulares locais do FMS em 7 containers que conversam **só por UDP**.

Cada container guarda apenas o estado do seu supervisor, cifrado com
EC-ElGamal sob a sua própria chave. Os containers coordenam os eventos
compartilhados com o mesmo protocolo das placas: commit em duas fases para
eventos controláveis e notificação confiável para os não controláveis, com
quadros assinados por HMAC-SHA256.

**O motor é o mesmo arquivo das placas, byte a byte** (`engine/`, conferido
por SHA-256). Só o ponto de entrada é novo (`src/`). Por isso dá para afirmar,
e verificar, que o container executa **o mesmo sistema** que o hardware.

Os supervisores são os **modulares locais completos** do FMS (família
`LMOD`), que carregam a planta local e por isso rejeitam eventos não
controláveis fisicamente impossíveis. Cada decifração leva **69 ms**, como no
ESP32-S3 (emulado; `DES_EMU_SCALARMUL_MS`).

---

## O resultado principal

### 1. Escala: de 1 a 7 containers

`REPEAT=5 scripts/run-all.sh` no WSL 2, 35 execuções, **35/35 PASS**. Tempo
por passo em ms, média ± intervalo de confiança de 95 % (n = 5):

| containers | supervisores por container | ciclo 1 | aceleração | ciclos 2–5 | aceleração | limite (nó mais carregado) |
|---|---|---|---|---|---|---|
| 1 | S0–S6 | 303,1 ± 1,3 | 1,00× | 240,8 ± 0,2 | 1,00× | 298,0 |
| 2 | S0–S3 · S4–S6 | 195,2 ± 0,6 | 1,55× | 148,9 ± 0,2 | 1,62× | 164,7 |
| 3 | S0–S2 · S3–S4 · S5–S6 | 149,2 ± 0,6 | 2,03× | 112,4 ± 0,2 | 2,14× | 123,9 |
| 4 | S0–S1 · S2–S3 · S4–S5 · S6 | 133,2 ± 0,3 | 2,28× | 93,6 ± 0,3 | 2,57× | 105,1 |
| 5 | S0–S1 · S2 · S3–S4 · S5 · S6 | 108,2 ± 1,3 | 2,80× | 82,7 ± 0,3 | 2,91× | 76,8 |
| 6 | S0–S1 · S2 · S3 · S4 · S5 · S6 | 98,8 ± 1,1 | 3,07× | 77,2 ± 0,2 | 3,12× | 65,9 |
| 7 | um por container | 90,1 ± 1,0 | 3,37× | 61,5 ± 0,3 | 3,92× | 64,3 |

- **Cada container a mais reduz o tempo por passo**, e toda a curva é
  estatisticamente distinguível: os intervalos (≤ 1,3 ms) são bem menores que
  as diferenças entre configurações vizinhas (≥ 8,7 ms). A variação entre
  repetições fica abaixo de 1 %.
- **A aceleração é limitada pelo nó mais carregado.** Os nós só trabalham em
  paralelo entre dois eventos compartilhados, então a célula nunca é mais
  rápida que *decifrações do nó mais carregado × 69 ms ÷ 44 passos*. O tempo
  medido fica 25–33 ms acima desse limite, e essa diferença é o custo de
  coordenação. De 6 para 7 containers o ganho é pequeno porque o supervisor
  S5 sozinho concentra 41 das 190 decifrações do ciclo 1.
- **Reprodutível entre máquinas:** a mesma varredura na nuvem
  ([`docs/resultados/escala/`](docs/resultados/escala/escala.md)) deu tempos
  1,2–3,3 % menores e exatamente os mesmos invariantes.

Análise completa em [`docs/resultados-wsl/20260927-170420-varredura/README.md`](docs/resultados-wsl/20260927-170420-varredura/README.md).

### 2. Equivalência com as placas ESP32

Em todas as 35 execuções, cada configuração repetiu exatamente o mesmo
resultado lógico, e com 2 containers ele coincide com o das placas:

| o que se verifica | ESP32-S3 | containers | |
|---|---|---|---|
| impressão digital da configuração, FMS em 2 nós | `edbd7971` | `edbd7971` | ✅ |
| decifrações por nó, 2 nós, 5 ciclos | 405 + 393 | 405 + 393 | ✅ |
| decifrações por nó, 2 nós, ciclo 1 | 85 + 105 | 85 + 105 | ✅ |
| decifrações no ciclo 1, 1 nó (placa única) | 190 | 190 | ✅ |
| decifrações da célula, qualquer número de nós | — | 798 (190 no ciclo 1) | ✅ |
| passos executados | 220/220 | 220/220 em todas as configurações | ✅ |
| bits homomórficos × oráculo em texto claro, em todo nó | PASS | PASS | ✅ |

A mesma impressão digital e as mesmas contagens de decifração, na unidade,
são a evidência de que se trata do mesmo sistema: a contagem é função
determinística do supervisor, do roteiro e do padrão de textos cifrados, e o
modelo estático do `esp32_crypto` previu o hardware passo a passo com ela.
Argumento completo em [`docs/arquitetura.md`](docs/arquitetura.md) §5.

**Para citar:** *com o custo de decifração do ESP32-S3 emulado, distribuir os
7 supervisores modulares locais do FMS em 7 containers reduz o tempo por passo
de 303,1 ± 1,3 ms para 90,1 ± 1,0 ms (3,37×; IC 95 %, n = 5), com aceleração
limitada pelo supervisor mais carregado.*

### 3. Experimentos anteriores

Antes de fixar a varredura, outros cenários foram testados e depois retirados
do repositório; código e resultados estão no
[commit `b7f013b`](https://github.com/pganaclara/docker_des/tree/b7f013bcc9bb1502148459f825c7523ec3ce0775/docs). O que eles mostraram:

- **Sem a emulação, distribuir atrasa.** Na velocidade de um PC a decifração
  custa ≈ 0,55 ms, a coordenação domina (88 % do passo) e 1 → 7 nós vai de
  2,4 para 4,7 ms/passo. No ESP32, onde a decifração custa 69–100 ms,
  distribuir acelera. Foi isso que motivou tornar a emulação o padrão.
- **Distribuir não soma trabalho criptográfico:** 798 decifrações com 1, 2 ou 7
  nós, com ou sem perda de quadros.
- **Os *timeouts* do protocolo estão calibrados para o ESP32:** com 5 % de
  perda, 511 ms/passo com *timeouts* de 1,5 s e 85 ms com 100 ms, sem mudar o
  resultado.
- **Sob perda pesada a segurança se mantém:** SAFE HALT quando a perda acerta
  depois do ponto de commit (2 nós, 30 %), passos pulados quando acerta antes
  (7 nós, 40 %).
- **Transporte unicast e rede com `netem`** (atraso de Wi-Fi) deram os mesmos
  resultados lógicos.
- **Verificação contra o supervisor monolítico** (`extended_small_factory`):
  PASS.

Detalhes e ressalvas em [`docs/arquitetura.md`](docs/arquitetura.md) §6–§8.
A revisão de literatura, com como isso costuma ser feito, a lacuna e onde cada
afirmação se apoia, está em [`docs/literatura.md`](docs/literatura.md).

---

## Início rápido (Windows + WSL 2)

**1. Clone dentro do WSL**, no sistema de arquivos Linux (`~/`), não em `/mnt/c`:

```bash
cd ~
git clone https://github.com/pganaclara/docker_des.git
cd docker_des
```

**2. Instale o Docker Engine no WSL** (Ubuntu). O script segue o procedimento
oficial da Docker, liga o systemd no WSL se precisar e confere tudo no fim:

```bash
bash scripts/install-docker-wsl.sh
```

Se ele ligar o systemd, vai pedir para reiniciar o WSL uma vez (no PowerShell:
`wsl --shutdown`) e rodar o script de novo. No fim, abra um terminal novo
(para o grupo `docker` valer) e teste com `docker run --rm hello-world`.

> Prefere o Docker Desktop? Também funciona: instale-o no Windows com a
> integração WSL 2 ligada e **não** rode o script acima. Não instale os dois.

**3. Rode a varredura de 1 a 7 containers:**

```bash
scripts/run-all.sh
```

O script cria a chave da célula se ela não existir (`secrets/des_auth_key`),
compila uma imagem para cada número de containers e roda o FMS com 1, 2, 3,
4, 5, 6 e 7 containers, um cenário depois do outro. **Cada decifração leva
69 ms, como no ESP32-S3.** No fim imprime o veredito de cada configuração e a
tabela de escala (tempo por passo, aceleração sobre 1 container e o limite
imposto pelo nó mais carregado). Leva uns 8 minutos. Tudo fica em
`results/<data>-varredura/`, incluindo `escala.md`.

Variações:

```bash
REPEAT=5 scripts/run-all.sh          # 5 vezes cada configuração (média ± desvio)
scripts/run-all.sh 1 2 7             # só algumas configurações
scripts/run-all.sh s5                # partição com S5 isolado × blocos, de 1 a 7
scripts/run.sh scenarios/fms-7.env   # uma configuração, com os logs ao vivo
```

---

## Cenários

Um por número de containers, `scenarios/fms-1.env` a `scenarios/fms-7.env`. O
motor distribui os 7 supervisores do FMS em blocos contíguos:

| cenário | supervisores por container | observação |
|---|---|---|
| `fms-1` | S0–S6 | equivalente da placa única |
| `fms-2` | S0–S3 · S4–S6 | mesma partição das 2 placas ESP32: tem de reproduzir `edbd7971` e 405 + 393 decifrações |
| `fms-3` | S0–S2 · S3–S4 · S5–S6 | |
| `fms-4` | S0–S1 · S2–S3 · S4–S5 · S6 | |
| `fms-5` | S0–S1 · S2 · S3–S4 · S5 · S6 | |
| `fms-6` | S0–S1 · S2 · S3 · S4 · S5 · S6 | |
| `fms-7` | um supervisor por container | |

Em todos, o resumo confere sozinho os invariantes (`EXPECT_*`): 798
decifrações (190 no ciclo 1), oráculo PASS em todo nó e nenhum passo pulado.

### Partição alternativa: S5 isolado

`scenarios/fms-2-s5.env` a `fms-6-s5.env` põem o supervisor S5 (o mais
carregado no ciclo 1) sozinho num container, e os outros 6 nos demais,
minimizando a carga do container mais carregado (`DES_SUP_NODE_MAP`).
`scripts/run-all.sh s5` roda as duas partições lado a lado e a tabela de
escala ganha uma comparação. Primeira execução (nuvem, n = 1): isolar o S5
só compensa com **4 containers** (−11,6 % no ciclo 1, −6,6 % nos seguintes);
com 2 é bem pior (+23,5 %), e com 3, 5 e 6 a diferença é pequena ou nula.
Detalhes em [`docs/resultados/escala-s5/`](docs/resultados/escala-s5/README.md).

O resultado da varredura está na seção "O resultado principal", acima.

---

## O que sai de uma execução

```
results/20260927-150102-fms-7/
├── node1.log … node7.log   log completo de cada container
├── node1.exit …            código de saída (0 ok, 1 pulos/oráculo, 2 SAFE HALT, 3 config, 4 watchdog)
├── scenario.env            o cenário usado
├── BUILD_INFO, image.id    versões dentro da imagem (mbedTLS, g++, parâmetros)
├── summary.md              tabela por nó + verificações
└── summary.json            o mesmo, para análise
```

Cada nó imprime por último uma linha `@@RESULT {json}` com seus contadores:
quadros, retransmissões, pulos, oráculo, fim de cada ciclo etc.

---

## Parâmetros

No arquivo de cenário (ou no ambiente):

| variável | padrão | o que faz |
|---|---|---|
| `DES_PROBLEM` | `fms` | o problema (só o cabeçalho do FMS está em `engine/`) |
| `DES_NUM_NODES` | `7` | número de containers (1–7 com a `compose.yaml` atual) |
| `DES_FAMILY` | `LMOD` | `LMOD`, modular local completo (carrega a planta). O motor também aceita `LMOD_RED` (reduzida), que **não** é usada aqui porque não carrega a planta e pode aceitar um evento impossível |
| `DES_ROUNDS` | `5` | ciclos de produção |
| `DES_WORK_MS` | `0` | tempo de máquina simulado antes de cada evento não controlável |
| `DES_EXTRA_FLAGS` | vazio | qualquer macro do motor, ex. `-DDES_SIMULATE_LOSS_PCT=5`, `"-DDES_SUP_NODE_MAP={1,1,2,2,3,3,4}"`, `-DDES_CONTROLLABLE_MASK=...` |
| `DES_EMU_SCALARMUL_MS` | `69` | custo emulado de uma decifração, em ms (ESP32-S3). `0` desliga e roda na velocidade do PC; só muda o tempo, não a lógica |
| `DES_SKIP_BUILD` | `0` | `1` reaproveita a imagem já compilada (sem internet) |
| `DES_CPUS` | `1.0` | CPUs por container |
| `DES_LINGER_MS` | `10000` | quanto o nó ainda atende os pares depois de terminar |
| `DES_RUN_TIMEOUT_S` | `900` | *watchdog* da execução |
| `UBUNTU_IMAGE` | `ubuntu:26.04` | imagem base (ver "Problemas comuns") |
| `DES_BUILD_NETWORK` | `default` | `host` se o `apt` do build precisa de um proxy em `127.0.0.1` |

---

## Estrutura

```
docker_des/
├── engine/                 motor do ESP32, cópia fiel (SHA256SUMS, UPSTREAM.md)
├── src/
│   └── des_container_main.cpp   ponto de entrada do container
├── docker/entrypoint.sh    escolhe o binário do nó
├── Dockerfile              build (um binário por nó) + imagem final
├── compose.yaml            node1..node7 numa rede bridge "cell"
├── scenarios/*.env         fms-1..7 (blocos) e fms-2..6-s5 (S5 isolado)
├── scripts/
│   ├── install-docker-wsl.sh    instala Docker Engine no WSL 2
│   ├── gen-key.sh               cria a chave da célula (Docker secret)
│   ├── run.sh                   roda um cenário e resume
│   ├── run-all.sh               varredura de 1 a 7 containers (e a série s5)
│   ├── scaling.py               tabela de escala da varredura
│   ├── summarize.py             tabela + verificações a partir dos logs
│   └── sync-engine.sh           atualiza engine/ a partir do esp32_crypto
└── docs/
    ├── arquitetura.md      ESP32 → container, por que C++, prova de equivalência, achados
    ├── literatura.md       revisão de literatura com referências conferidas
    ├── resultados/escala/  varredura de referência na nuvem (1 a 7 containers)
    ├── resultados/escala-s5/  S5 isolado × blocos (nuvem, n = 1)
    └── resultados-wsl/     varreduras no WSL (a com 5 repetições é o resultado principal)
```

---

## Por que C++?

Porque o motor já é C++17 e roda sem alteração nos dois lados. Reescrever em
outra linguagem criaria uma segunda implementação a ser validada do zero, e o
"mesmo sistema" viraria "um sistema parecido". O container também usa a mesma
biblioteca criptográfica das placas (mbedTLS, ramo LTS 3.6). A comparação com
Rust, Go, Python e C está em [`docs/arquitetura.md`](docs/arquitetura.md) §4.

---

## Problemas comuns

| sintoma | causa e solução |
|---|---|
| `429 Too Many Requests` ao baixar `ubuntu:26.04` | limite de pulls anônimos do Docker Hub. Faça `docker login` ou use um espelho: `UBUNTU_IMAGE=mirror.gcr.io/library/ubuntu:26.04 scripts/run.sh ...` |
| `apt-get` falha no build atrás de proxy corporativo | `DES_BUILD_NETWORK=host` e configure o proxy do Docker (`~/.docker/config.json`, seção `proxies`) |
| nós esperando para sempre `waiting for N peer(s)` | multicast bloqueado na rede Docker (acontece em redes *overlay*/Kubernetes; na *bridge* local funciona) |
| `this image has no binary for node K` | a imagem foi compilada para menos nós; confira `DES_NUM_NODES` no cenário |
| `[key] cannot open /run/secrets/des_auth_key` | rode `scripts/gen-key.sh` |
| lentidão ou permissões estranhas | o repositório está em `/mnt/c/...`; clone em `~/` dentro do WSL |

---

## Relação com o `esp32_crypto`

| | `esp32_crypto` | `docker_des` |
|---|---|---|
| motor (`des_generic.h`, `des_transport.h`) | original | cópia fiel, commit `bf0efe6` |
| supervisores | `supervisor_data_*.h`, gerados pelo notebook UltraDES | `supervisor_data_fms.h`, cópia fiel |
| plataforma | ESP32-S3, Wi-Fi | containers Linux, rede Docker |
| nós | 2 placas | 1 a 7 containers (7 = um por supervisor do FMS) |
| custo de uma decifração | 69 ms (medido) | 69 ms (emulado) |
| criptografia validada em Linux | com *test double* | com **mbedTLS 3.6.5 real** |

Os dois podem até formar uma célula mista: um ESP32 e containers com a mesma
chave e a mesma configuração são pares no mesmo grupo multicast (rede
`macvlan`; ver [`docs/arquitetura.md`](docs/arquitetura.md) §9).
