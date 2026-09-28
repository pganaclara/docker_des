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
scripts/run-all.sh sobrecarga        # sobrecarga do container: ponte × host × nativo
scripts/run-all.sh perda             # robustez a perda de quadros (2 e 7 nós)
python3 scripts/latency.py results/<data>-varredura   # percentis de latência por passo
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

### Latência por passo (percentis)

`scripts/latency.py` (chamado no fim do `run-all.sh`) gera `latencia.md` e
`latencia.csv` com p50/p90/p95/p99/máx de:
- **decisão** no nó dono de cada evento (passo homomórfico + espera pelos
  pares), separada em local, 2PC e NOTIFY;
- **aplicação** nos participantes de cada evento compartilhado;
- **intervalo da célula**: tempo entre a conclusão de um passo e a do
  seguinte, em qualquer nó, no relógio comum. Vem dos logs com carimbo de
  tempo do Docker (`nodeK.ts.log`), que o `run.sh` passou a salvar.

Na varredura de 1 a 7 com 5 repetições e `.ts.log`
([`docs/resultados-wsl/20260927-210233-varredura`](docs/resultados-wsl/20260927-210233-varredura/README.md),
35/35 PASS), ciclos 2–5:

| containers | 2PC no dono p50 / p99 | intervalo da célula média / p99 / máx | ms/passo (escala) |
|---|---|---|---|
| 1 | — | 237,1 / 490,7 / 497,9 | 241,5 |
| 2 | 284,6 / 287,2 | 151,7 / 288,3 / 289,3 | 149,2 |
| 3 | 213,8 / 216,9 | 110,7 / 289,1 / 292,8 | 112,3 |
| 4 | 145,3 / 147,4 | 96,1 / 151,4 / 152,8 | 93,8 |
| 5 | 145,1 / 147,3 | 83,1 / 151,3 / 152,8 | 82,8 |
| 6 | 144,8 / 147,6 | 77,2 / 150,9 / 152,9 | 77,2 |
| 7 | 75,8 / 77,9 | 62,1 / 82,1 / 83,8 | 61,3 |

- A latência de um evento vem em degraus de uma decifração (≈ 69 ms): o 2PC
  no dono custa 4, 3, 2 e 1 decifrações com 2, 3, 4–6 e 7 containers. A rede
  soma ~6 ms. O *jitter* é pequeno: p99 − p50 ≤ 3,1 ms no 2PC e no NOTIFY.
- A média do intervalo da célula confere com o tempo por passo da escala
  (diferença ≤ 4,4 ms), medido por outro caminho. **O pior caso cai mais que a
  média:** o máximo vai de 498 ms (1 container) a 84 ms (7), 5,9×, contra 3,9×
  na média.
- No WSL o relógio do host salta ~12 s de vez em quando (sincronização com o
  Windows), e isso corrompe os carimbos do Docker. O `latency.py` detecta e
  descarta essas amostras conferindo com o relógio do motor. Detalhes no
  README da pasta.

### Partição alternativa: S5 isolado

`scenarios/fms-2-s5.env` a `fms-6-s5.env` põem o supervisor S5 (o mais
carregado no ciclo 1) sozinho num container, e os outros 6 nos demais,
minimizando a carga do container mais carregado (`DES_SUP_NODE_MAP`).
`scripts/run-all.sh s5` roda as duas partições lado a lado e a tabela de
escala ganha uma comparação. Com 5 repetições no WSL (60 execuções, 60/60
PASS): isolar o S5 só compensa nas duas fases com **4 containers** (−11,6 %
no ciclo 1, −6,8 % nos seguintes); com 2 é bem pior (+23 % e +39 %); com 3 e
6 o ciclo 1 melhora pouco e os seguintes não; com 5 não há diferença no
ciclo 1. Não existe partição melhor para todo número de containers.
Detalhes em [`docs/resultados-wsl/20260927-200439-varredura/`](docs/resultados-wsl/20260927-200439-varredura/README.md) (com IC 95 % das diferenças) e na primeira execução, [`docs/resultados/escala-s5/`](docs/resultados/escala-s5/README.md).

### Sobrecarga do container: ponte × host × nativo

A literatura de PLC virtual pergunta quanto o container custa em relação a
rodar direto na máquina (`docs/literatura.md`, [3] e [12]).
`scripts/run-all.sh sobrecarga` roda a mesma célula com 1, 2, 4 e 7 nós em três lugares:

| modo | cenário | onde os nós rodam |
|---|---|---|
| ponte | `fms-N-ponte` | um container por nó na rede *bridge* `cell` (como a varredura principal) |
| host | `fms-N-host` | um container por nó na pilha de rede do host (`compose.host.yaml`): sem veth nem bridge |
| nativo | `fms-N-nativo` | sem Docker na execução: os binários saem da imagem e rodam como processos comuns |

Os três modos usam **os mesmos binários** (uma imagem por N, estáticos para
rodar fora do container, com `-DDES_MCAST_LOOP=1` porque no host e no nativo
todos os nós ficam numa interface só). Portanto, só muda onde eles rodam. O
`scripts/overhead.py` gera `sobrecarga.md` com:
- o tempo por passo em cada modo;
- a diferença para a ponte, com IC 95 % de Welch;
- a parte da rede: RTT de aplicação e espera pelos pares no 2PC e no NOTIFY.

No modo nativo não há `nodeK.ts.log` (não há Docker para carimbar) nem o
limite de 1 CPU por nó (`DES_CPUS`). Como a decifração emulada é espera, e não
cálculo, o limite de CPU pesa pouco.

**Resultado** (WSL, 5 repetições, 55/55 PASS,
[`docs/resultados-wsl/20260928-002448-varredura`](docs/resultados-wsl/20260928-002448-varredura/README.md)):
o container **não tem custo mensurável**. Com 1, 2, 4 e 7 nós, os três modos
dão o mesmo tempo por passo; por exemplo, 7 nós nos ciclos 2–5: ponte
61,1 ± 0,6, host 61,0 ± 0,6, nativo 60,9 ± 0,6 ms. Todos os 18 IC 95 % das
diferenças contêm o zero. Com 95 % de confiança, a sobrecarga fica abaixo de
1,6 % nos ciclos 2–5 e de 2,1 % no ciclo 1. O RTT de aplicação e a espera
pelos pares também são iguais nos três modos: o que custa na rede é o laço
do motor, não a bridge.

### Robustez a perda de quadros

`scripts/run-all.sh perda` roda a célula com perda de quadros injetada pelo
próprio motor (`DES_SIMULATE_LOSS_PCT`). Cada nó descarta P % do que recebe
depois da autenticação, então quem enviou precisa retransmitir de verdade. Os
cenários:
- `fms-2-perda{1,5,10,20,30}`: 2 nós, a partição das placas;
- `fms-7-perda{1,5,10}`: 7 nós.

A decifração continua emulada a 69 ms, e os *timeouts* do motor (1,5 s) são
os do ESP32. O sorteio é novo a cada execução e em cada nó; a semente fica no
log e `DES_LOSS_SEED` a fixa.

Com perda, o desfecho é aleatório. Pode ser:
- **completa**: os 220 passos;
- **SAFE HALT**: um COMMIT esgotou as retransmissões e a célula parou;
- **incompleta**: passos pulados, quando o dono desistiu antes do commit e
  nada foi aplicado.

O que não pode acontecer é **divergência**. O `summarize.py` confere em toda
execução (com ou sem perda) que cada par de nós executou os eventos
compartilhados que tem em comum na mesma ordem e o mesmo número de vezes.
Depois de um SAFE HALT, um dos dois pode estar no máximo um commit à frente,
que é o evento em voo que a parada protege. O `scripts/loss.py` gera
`perda.md` com os desfechos, os passos executados, as retransmissões e essas
verificações.

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
| `DES_MODE` | `bridge` | onde os nós rodam: `bridge`/`ponte` (containers na rede `cell`), `host` (containers na rede do host) ou `nativo` (processos, sem Docker) |
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
├── compose.host.yaml       os mesmos nós na rede do host (teste de sobrecarga)
├── scenarios/*.env         fms-1..7 (blocos), fms-2..6-s5 (S5 isolado),
│                           fms-N-{ponte,host,nativo} (sobrecarga, N = 1, 2, 4, 7),
│                           fms-2-perda1..30 e fms-7-perda1..10 (perda)
├── scripts/
│   ├── install-docker-wsl.sh    instala Docker Engine no WSL 2
│   ├── gen-key.sh               cria a chave da célula (Docker secret)
│   ├── run.sh                   roda um cenário e resume
│   ├── run-all.sh               varredura de 1 a 7 containers (e as séries s5, sobrecarga, perda)
│   ├── scaling.py               tabela de escala da varredura
│   ├── latency.py               percentis de latência por passo
│   ├── overhead.py              tabela ponte × host × nativo (sobrecarga)
│   ├── loss.py                  desfechos e segurança sob perda de quadros
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
