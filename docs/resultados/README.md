# Execuções de referência

Uma execução de cada cenário, feita com `scripts/run-all.sh` sobre o código
deste repositório, em 27/09/2026. Cada pasta é a saída intacta do
`scripts/run.sh`: logs de todos os nós, códigos de saída, cenário, versões da
imagem e o resumo com as verificações (`summary.md` / `summary.json`).

## Veredito

```
esf-2-lockstep         PASS
fms-1                  PASS
fms-2-loss30           PASS   (esperado: SAFE HALT, e parou)
fms-2                  PASS
fms-7-loss5-fast       PASS
fms-7-loss5            PASS
fms-7-unicast          PASS
fms-7-wifi             não executado: o kernel do ambiente não tem sch_netem
fms-7                  PASS
```

## Números

| cenário | nós | impressão digital | resultado | passos | decifrações (ciclo 1) | por nó | retx | ms/passo ciclo 1 | ciclos 2–5 |
|---|---|---|---|---|---|---|---|---|---|
| [`fms-1`](fms-1/summary.md) | 1 | `3f2beff2` | completo | 220/220 | 798 (190) | 798 | 0 | 2,36 | 1,60 |
| [`fms-2`](fms-2/summary.md) | 2 | **`edbd7971`** | completo | 220/220 | 798 (190) | **405 + 393** (85 + 105) | 0 | 4,05 | 2,84 |
| [`fms-7`](fms-7/summary.md) | 7 | `04511541` | completo | 220/220 | 798 (190) | 101 101 100 103 114 129 150 | 0 | 4,65 | 3,73 |
| [`fms-7-unicast`](fms-7-unicast/summary.md) | 7 | `04511541` | completo | 220/220 | 798 (190) | idem | 0 | 4,76 | 3,75 |
| [`fms-7-loss5`](fms-7-loss5/summary.md) | 7 | `04511541` | completo | 220/220 | 798 (190) | idem | 86 | 510,9 | 767,8 |
| [`fms-7-loss5-fast`](fms-7-loss5-fast/summary.md) | 7 | `04511541` | completo | 220/220 | 798 (190) | idem | 57 | 84,5 | 53,7 |
| [`fms-2-loss30`](fms-2-loss30/summary.md) | 2 | `edbd7971` | **SAFE HALT** | 116/220 | 427 (190) | 208 + 219 | 72 | — | — |
| [`esf-2-lockstep`](esf-2-lockstep/summary.md) | 2 | `d42d57d1` | completo, monolítico **PASS** | 30/30 | 40 (8) | 20 + 20 | 0 | 7,02 | 3,48 |

Em negrito, os valores que coincidem com os das placas ESP32-S3 do
`esp32_crypto`. A interpretação está em [`../arquitetura.md`](../arquitetura.md)
§5 e §6.

`observacoes/fms-7-loss40-parcial/` guarda os logs de uma execução com 7 nós e
40 % de perda, interrompida à mão depois de alguns minutos. Ela mostra que,
com muitos participantes, a perda pesada vira passos pulados, e não SAFE HALT
(§6.5 da arquitetura). Não é uma execução completa, e por isso não tem
resumo.

## Ambiente

| | |
|---|---|
| host | VM Linux 6.18 (x86-64), 4 vCPU Intel Xeon @ 2,1 GHz, 15 GiB |
| Docker | Engine 29.3.1, Compose 5.1.1, cgroup v1 |
| imagem base | `ubuntu:26.04` (`mirror.gcr.io/library/ubuntu@sha256:da6fc2be5478…`) |
| compilador | g++ 15.2.0, `-std=c++17 -O2 -Wall -Wextra`, zero avisos |
| criptografia | mbedTLS 3.6.5 (`libmbedtls-dev 3.6.5-0.1ubuntu2`), ligado estaticamente |
| limites | `cpus: 1.0` por container; rede *bridge* única |
| repetições | **uma** execução por cenário; sem variância |

Os tempos dependem desta máquina e **não** são comparáveis aos do ESP32 nem
são tempos de tempo real (ver §7 da arquitetura). As contagens de decifração,
as impressões digitais, os passos e os vereditos não dependem da máquina.
