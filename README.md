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
- **Testado: emulando o custo de decifração do ESP32 (69 ms), distribuir
  volta a acelerar.** 1 → 2 → 7 containers: 299,5 → 192,7 → 87,2 ms/passo,
  perto do limite "decifrações do nó mais carregado × 69 ms"
  (`DES_EMU_SCALARMUL_MS`, hoje o padrão).
- **Os *timeouts* do protocolo estão calibrados para o ESP32.** Com 5 % de
  perda, o passo vai a 511 ms com os *timeouts* de 1,5 s e a 85 ms com
  *timeouts* de 100 ms, sem mudar o resultado.
- **Sob perda pesada a segurança se mantém, de dois jeitos:** SAFE HALT quando
  a perda acerta depois do ponto de commit (2 nós, 30 %), passos pulados
  quando acerta antes (7 nós, 40 %).

Os cenários de perda, unicast, `netem` e `extended_small_factory` citados acima foram retirados do repositório para deixar só a varredura de 1 a 7 containers; as execuções deles continuam registradas em [`docs/resultados/`](docs/resultados/) e [`docs/resultados-wsl/`](docs/resultados-wsl/).

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

### Resultado de referência

| containers | ms/passo, ciclo 1 | aceleração | limite (nó mais carregado) |
|---|---|---|---|
| 1 | 299,6 | 1,00× | 298,0 |
| 2 | 192,8 | 1,55× | 164,7 |
| 3 | 146,8 | 2,04× | 123,9 |
| 4 | 130,7 | 2,29× | 105,1 |
| 5 | 106,0 | 2,83× | 76,8 |
| 6 | 96,3 | 3,11× | 65,9 |
| 7 | 87,2 | 3,44× | 64,3 |

Tabela completa em [`docs/resultados/escala/escala.md`](docs/resultados/escala/escala.md).
De 6 para 7 containers o ganho é pequeno porque o supervisor S5 sozinho já é
o nó mais carregado (41 das 190 decifrações do ciclo 1).

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
│   ├── run-all.sh               varredura de 1 a 7 containers
│   ├── scaling.py               tabela de escala da varredura
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
| `[netem] could not shape eth0` | o kernel não tem `sch_netem` (kernels WSL 2 antigos). Atualize com `wsl --update` no PowerShell, ou deixe `DES_NETEM` vazio |
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
