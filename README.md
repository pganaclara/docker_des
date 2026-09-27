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
por SHA-256). Só o ponto de entrada e um transporte opcional são novos
(`src/`). Por isso dá para afirmar, e verificar, que o container executa **o
mesmo sistema** que o hardware.

---

## O resultado principal

Todos os cenários foram executados com o código deste repositório. Detalhes em
[`docs/resultados/`](docs/resultados/).

| o que se verifica | hardware (ESP32-S3) | containers | |
|---|---|---|---|
| impressão digital da configuração, FMS em 2 nós | `edbd7971` | `edbd7971` | ✅ |
| decifrações, FMS em 2 nós, 5 ciclos | 405 + 393 | 405 + 393 | ✅ |
| decifrações no ciclo 1, por nó | 85 + 105 | 85 + 105 | ✅ |
| decifrações no ciclo 1, FMS em 1 nó (placa única) | 190 | 190 | ✅ |
| FMS com **7 containers, um por supervisor**: passos executados | — | 220/220, 0 pulados | ✅ |
| decifrações com 7 containers | — | 798 (= 405 + 393), 190 no ciclo 1 | ✅ |
| bits homomórficos × oráculo em texto claro, em todo nó | PASS | PASS | ✅ |
| execução distribuída × supervisor monolítico (ESF) | — ¹ | PASS | ✅ |
| 5 % de perda: completa sem divergência | — | 220/220, mesmas 798 decifrações | ✅ |
| 30 % de perda: para com segurança (SAFE HALT) | — ¹ | SAFE HALT nos 2 nós | ✅ |

¹ O `esp32_crypto` documenta esses dois casos só no teste em Linux (com um
*test double* no lugar da criptografia), não nas placas.

A mesma impressão digital e as mesmas contagens de decifração, na unidade,
são a evidência de que se trata do mesmo sistema. A contagem é função
determinística do supervisor, do roteiro e do padrão de textos cifrados, e o
modelo estático do `esp32_crypto` previu o hardware passo a passo com ela.
O argumento completo está em [`docs/arquitetura.md`](docs/arquitetura.md) §5.

### O que os experimentos mostraram

- **Um supervisor por container maximiza a coordenação.** Os eventos 30–39
  aparecem nos 7 supervisores, então cada um vira um commit em duas fases com
  6 participantes (14 quadros). Com 2 nós são 10 eventos compartilhados; com 7,
  são 15.
- **Distribuir não soma trabalho criptográfico:** são 798 decifrações com 1, 2
  ou 7 nós, com ou sem perda.
- **O gargalo muda de lugar.** No ESP32 a decifração custa 69–100 ms e
  distribuir acelera (2 placas: 296,9 ms/passo contra 346,0 numa só). No
  container ela custa ≈ 0,55 ms, a coordenação domina (88 % do passo) e
  distribuir atrasa (1 nó: 2,4 ms/passo; 7 nós: 4,7).
- **Os *timeouts* do protocolo estão calibrados para o ESP32.** Com 5 % de
  perda, o passo vai a 511 ms com os *timeouts* de 1,5 s e a 85 ms com
  *timeouts* de 100 ms, sem mudar o resultado.
- **Sob perda pesada a segurança se mantém, de dois jeitos:** SAFE HALT quando
  a perda acerta depois do ponto de commit (2 nós, 30 %), passos pulados
  quando acerta antes (7 nós, 40 %).

Detalhes e ressalvas em [`docs/arquitetura.md`](docs/arquitetura.md) §6–§7.
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

**3. Rode o FMS com um container por supervisor:**

```bash
scripts/run.sh scenarios/fms-7.env
```

O script cria a chave da célula se ela não existir (`secrets/des_auth_key`),
compila a imagem, sobe `node1`…`node7`, mostra os logs intercalados, espera
todos terminarem e imprime o resumo com as verificações. Tudo fica em
`results/<data>-fms-7/`.

**4. Rode todos os cenários e veja o veredito:**

```bash
scripts/run-all.sh
```

---

## Cenários

Cada arquivo em `scenarios/` é um experimento, com os valores esperados
(`EXPECT_*`) que o resumo confere sozinho.

| cenário | containers | o que mostra |
|---|---|---|
| `fms-7` | 7 | **um supervisor por container**, UDP multicast |
| `fms-7-unicast` | 7 | o mesmo sobre UDP unicast (para redes sem multicast) |
| `fms-2` | 2 | a mesma partição das 2 placas ESP32: deve reproduzir `edbd7971` e 405 + 393 |
| `fms-1` | 1 | os 7 supervisores num container só, o equivalente da placa única: 190 no ciclo 1 |
| `esf-2-lockstep` | 2 | `extended_small_factory` conferida evento a evento contra o supervisor monolítico |
| `fms-7-loss5` | 7 | 5 % de perda de quadros: retransmissão, sem divergência |
| `fms-7-loss5-fast` | 7 | idem, com *timeouts* ajustados para container (100 ms em vez de 1,5 s) |
| `fms-2-loss30` | 2 | teste negativo: 30 % de perda leva ao **SAFE HALT** propagado |
| `fms-7-wifi` | 7 | atraso de 7 ± 3 ms e 1 % de perda via `netem` (exige `sch_netem` no kernel; kernels WSL 2 recentes trazem como módulo, os antigos não) |

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
| `DES_PROBLEM` | `fms` | `fms`, `extended_small_factory` ou `small_factory` |
| `DES_NUM_NODES` | `7` | número de containers (1–7 com a `compose.yaml` atual) |
| `DES_FAMILY` | `LMOD` | `LMOD` (modular local), `LMOD_RED` (reduzida) ou `MONO` |
| `DES_ROUNDS` | `5` | ciclos de produção |
| `DES_WORK_MS` | `0` | tempo de máquina simulado antes de cada evento não controlável |
| `DES_TRANSPORT` | `multicast` | `multicast` ou `unicast` |
| `DES_NETEM` | vazio | argumentos do `netem`, ex. `"delay 7ms 3ms loss 1%"` |
| `DES_EXTRA_FLAGS` | vazio | qualquer macro do motor, ex. `-DDES_SIMULATE_LOSS_PCT=5`, `"-DDES_SUP_NODE_MAP={1,1,2,2,3,3,4}"`, `-DDES_CONTROLLABLE_MASK=...` |
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
│   ├── des_container_main.cpp   ponto de entrada do container
│   └── des_transport_unicast.h  transporte UDP unicast (alternativa ao multicast)
├── docker/entrypoint.sh    escolhe o binário do nó, aplica netem, larga o root
├── Dockerfile              build (um binário por nó) + imagem final
├── compose.yaml            node1..node7 numa rede bridge "cell"
├── scenarios/*.env         experimentos com valores esperados
├── scripts/
│   ├── install-docker-wsl.sh    instala Docker Engine no WSL 2
│   ├── gen-key.sh               cria a chave da célula (Docker secret)
│   ├── run.sh                   roda um cenário e resume
│   ├── run-all.sh               roda todos
│   ├── summarize.py             tabela + verificações a partir dos logs
│   └── sync-engine.sh           atualiza engine/ a partir do esp32_crypto
└── docs/
    ├── arquitetura.md      ESP32 → container, por que C++, prova de equivalência, achados
    ├── literatura.md       revisão de literatura com referências conferidas
    └── resultados/         execuções de referência
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
| `[netem] could not shape eth0` | o kernel não tem `sch_netem` (kernels WSL 2 antigos). Atualize com `wsl --update` no PowerShell, ou use `fms-7-loss5` (perda injetada no próprio motor) |
| nós esperando para sempre `waiting for N peer(s)` | multicast bloqueado na sua rede Docker. Use `DES_TRANSPORT=unicast` |
| `this image has no binary for node K` | a imagem foi compilada para menos nós; confira `DES_NUM_NODES` no cenário |
| `[key] cannot open /run/secrets/des_auth_key` | rode `scripts/gen-key.sh` |
| lentidão ou permissões estranhas | o repositório está em `/mnt/c/...`; clone em `~/` dentro do WSL |

---

## Relação com o `esp32_crypto`

| | `esp32_crypto` | `docker_des` |
|---|---|---|
| motor (`des_generic.h`, `des_transport.h`) | original | cópia fiel, commit `bf0efe6` |
| supervisores (`supervisor_data_*.h`) | gerados pelo notebook UltraDES | cópia fiel |
| plataforma | ESP32-S3, Wi-Fi | containers Linux, rede Docker |
| nós | 2 placas | 1 a 7 containers (7 = um por supervisor do FMS) |
| criptografia validada em Linux | com *test double* | com **mbedTLS 3.6.5 real** |

Os dois podem até formar uma célula mista: um ESP32 e containers com a mesma
chave e a mesma configuração são pares no mesmo grupo multicast (rede
`macvlan`; ver [`docs/arquitetura.md`](docs/arquitetura.md) §8).
